from pathlib import Path
from dataclasses import dataclass, field
import requests
from requests import Session
from typing import Optional, Union
import functools

from chris.types import (
    CUBEAddress,
    CUBEToken,
    Username,
    PluginInstanceId,
    PluginUrl,
    PluginName,
    PluginVersion,
    PluginInstanceUrl,
)
from chris.cube.plugin import Plugin
from chris.cube.plugin_instance import PluginInstance
from chris.cube.files import File
from chris.cube.pipeline import Pipeline
from chris.helpers.pagination import Paginated
from chris.errors import (
    ChrisIncorrectLoginError,
    PipelineNotFoundError,
    PluginNotFoundError,
)
from chris.helpers.peek import peek
from chris.cube.base_collection_links import BaseResponse, BaseCollectionLinks
from chris.helpers.deserialize import deserialize


@dataclass(frozen=True)
class ChrisClient:

    url: CUBEAddress
    token: CUBEToken

    collection_links: BaseCollectionLinks = field(init=False)
    _s: Session = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "_s", self.__authenticated_session(self.token))
        object.__setattr__(self, "collection_links", self.__get_collection_links())

    @classmethod
    def from_login(
        cls,
        address: Union[CUBEAddress, str],
        username: Union[Username, str],
        password: str,
    ) -> "ChrisClient":
        if not address.endswith("/api/v1/"):
            raise ValueError('Address of CUBE must end with "/api/v1/"')
        login = requests.post(
            address + "auth-token/", json={"username": username, "password": password}
        )
        if login.status_code == 400:
            res = login.json()
            raise ChrisIncorrectLoginError(
                res["non_field_errors"][0] if "non_field_errors" in res else login.text
            )
        login.raise_for_status()
        return cls(url=address, token=login.json()["token"])

    @staticmethod
    def __authenticated_session(token: CUBEToken) -> requests.Session:
        s = requests.Session()
        s.headers.update(
            {
                "Accept": "application/json",
                "Authorization": "Token " + token,
            }
        )
        return s

    def __get_collection_links(self) -> BaseCollectionLinks:
        """
        Make a request to the CUBE address. Calling this method verifies
        that the login token is correct.
        """
        res = self._s.get(self.url)
        if res.status_code == 401:
            raise ChrisIncorrectLoginError(res.json()["detail"])
        return deserialize(BaseResponse, res).collection_links

    def upload(self, local_file: Path, upload_path: str) -> File:
        """
        Upload a local file into *ChRIS*.

        Paramters
        ---------
        local_file: Path
            file to upload
        upload_path: str
            name of upload destination in *ChRIS* `uploadedfiles` resource
        """
        if not upload_path.startswith(f"{self.username}/uploads/"):
            upload_path = f"{self.username}/uploads/{upload_path}"

        with local_file.open("rb") as file_object:
            files = {
                "upload_path": (None, upload_path),
                "fname": (local_file.name, file_object),
            }
            res = self._s.post(
                self.collection_links.uploadedfiles,
                files=files,
            )

        return File.deserialize(res, self._s)

    def get_plugin_by_url(self, url: Union[PluginUrl, str]) -> Plugin:
        return Plugin.deserialize(self._s.get(url), self._s)

    def get_plugin_by_name(
        self,
        name_exact: Union[PluginName, str],
        version: Optional[Union[PluginVersion, str]] = None,
    ) -> Plugin:
        search = self.search_plugin(name_exact, version)
        return peek(search, mt=PluginNotFoundError)

    def search_plugin(
        self, name_exact: str, version: Optional[str] = None
    ) -> Paginated[Plugin]:
        qs = self._join_qs(name_exact=name_exact, version=version)
        return Paginated(
            item=Plugin,
            url=f"{self.collection_links.plugins}search/?{qs}",
            session=self._s,
        )

    def get_plugin_instance(
        self, plugin: Union[PluginInstanceUrl, PluginInstanceId, int, str]
    ) -> PluginInstance:
        """
        Get a plugin instance.
        :param plugin: Either a plugin instance ID or URL
        :return: plugin instance
        """
        if isinstance(plugin, str) and "/" in plugin:
            url = plugin
        else:
            url = f"{self.url}plugins/instances/{plugin}/"
        res = self._s.get(url)
        return PluginInstance.deserialize(res, self._s)

    def search_files(self, fname="", fname_exact="") -> Paginated[File]:
        return self._search_files(self.collection_links.files, fname, fname_exact)

    def search_uploadedfiles(self, fname="", fname_exact="") -> Paginated[File]:
        return self._search_files(
            self.collection_links.uploadedfiles, fname, fname_exact
        )

    def _search_files(
        self, base_url: str, fname: str, fname_exact: str
    ) -> Paginated[File]:
        qs = self._join_qs(fname=fname, fname_exact=fname_exact)
        url = f"{base_url}search/?{qs}"
        return self.get_files(url)

    def get_files(self, url: str) -> Paginated[File]:
        return Paginated(item=File, session=self._s, url=url)

    def search_pipelines(self, name="") -> Paginated[Pipeline]:
        return Paginated(
            item=Pipeline,
            url=f"{self.collection_links.pipelines}search/?name={name}",
            session=self._s,
        )

    def get_pipeline(self, name: str) -> Pipeline:
        return peek(self.search_pipelines(name), mt=PipelineNotFoundError)

    @property
    def username(self) -> Username:
        return Username(self.__user["username"])

    @functools.cached_property
    def __user(self) -> dict:
        res = self._s.get(url=self.collection_links.user)
        res.raise_for_status()
        return res.json()

    @staticmethod
    def _join_qs(**kwargs) -> str:
        return "&".join([f"{k}={v}" for k, v in kwargs.items() if v])
