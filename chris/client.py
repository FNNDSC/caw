from pathlib import Path
from dataclasses import dataclass, field
import requests
from typing import Optional, Union, Generator, Dict

from chris.types import (
    CUBEAddress, CUBEToken, CUBEUsername, CUBEPassword, CUBEUrl, PluginInstanceId, PluginName, PluginVersion
)
from chris.cube.plugin import Plugin
from chris.cube.plugin_instance import PluginInstance
from chris.cube.files import ListOfDownloadableFiles
from chris.cube.registered_pipeline import RegisteredPipeline
from chris.cube.pagination import fetch_paginated_objects
from chris.cube.resource import ConnectedResource
from chris.errors import (
    ChrisClientError, ChrisIncorrectLoginError, PluginNotFoundError, PipelineNotFoundError
)
from chris.helpers.peek import peek

import logging

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ChrisClient(ConnectedResource):

    address: CUBEAddress
    token: CUBEToken

    collection_links: Dict[str, CUBEUrl] = field(init=False)
    s: requests.Session = field(init=False)
    url: CUBEUrl = field(init=False)
    """
    An alias for ``address``
    """

    def __post_init__(self):
        if not self.address.endswith('/api/v1/'):
            raise ValueError('Address of CUBE must end with "/api/v1/"')
        object.__setattr__(self, 'url', self.address)
        object.__setattr__(self, 's', self.__start_session(self.token))
        object.__setattr__(self, 'collection_links', self.__get_collection_links())

    @classmethod
    def from_login(cls,
                   address: Union[CUBEAddress, str],
                   username: Union[CUBEUsername, str],
                   password: Union[CUBEPassword, str]) -> 'ChrisClient':
        login = requests.post(address + 'auth-token/', json={
            'username': username,
            'password': password
        })
        if login.status_code == 400:
            res = login.json()
            raise ChrisIncorrectLoginError(
                res['non_field_errors'][0] if 'non_field_errors' in res else login.text
            )
        login.raise_for_status()
        return cls(address=address, token=login.json()['token'])

    @staticmethod
    def __start_session(token) -> requests.Session:
        s = requests.Session()
        s.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/vnd.collection+json',
            'Authorization': 'Token ' + token
        })
        return s

    def __get_collection_links(self) -> Dict[str, CUBEUrl]:
        """
        Make a request to the CUBE address. Calling this method verifies
        that the login token is correct.
        """
        res = self.s.get(self.address)
        if res.status_code == 401:
            data = res.json()
            raise ChrisIncorrectLoginError(data['detail'] if 'detail' in data else res.text)
        if res.status_code != 200:
            raise ChrisClientError(f'CUBE response status code was {res.status_code}.')
        res.raise_for_status()
        data = res.json()
        if 'collection_links' not in data or 'uploadedfiles' not in data['collection_links']:
            raise ChrisClientError(f'Unexpected CUBE response: {res.text}')
        return data['collection_links']

    @property
    def search_addr_plugins(self) -> CUBEUrl:
        return CUBEUrl(self.address + 'plugins/search/')

    @property
    def search_addr_plugins_instances(self) -> CUBEUrl:
        return CUBEUrl(self.address + 'plugins/instances/search/')

    @property
    def search_addr_pipelines(self) -> CUBEUrl:
        return CUBEUrl(self.address + 'pipelines/search/')

    def upload(self, file_path: Path, upload_folder: Path) -> dict:
        """
        Upload a local file into ChRIS backend Swift storage.

        :param file_path: local file path
        :param upload_folder: path in Swift where to upload to
        :return: response
        """
        upload_path = upload_folder / file_path.name

        with open(file_path, 'rb') as file_object:
            files = {
                'upload_path': (None, str(upload_path)),
                'fname': (file_path.name, file_object)
            }
            res = self.s.post(
                self.collection_links['uploadedfiles'],
                files=files,
                headers={
                    'Accept': 'application/vnd.collection+json',
                    'Content-Type': None
                }
            )
        res.raise_for_status()
        return res.json()

    def get_plugin(self, name_exact='', version='', url='') -> Plugin:
        """
        Get a single plugin, either searching for it by its exact name, or by URL.

        :param name_exact: name of plugin
        :param version: (optional) version of plugin
        :param url: (alternative to name_exact) url of plugin
        """
        if url:
            return self.get_plugin_by_url(url)
        return self.get_plugin_by_name(name_exact, version)

    def get_plugin_by_url(self, url: Union[CUBEUrl, str]):
        res = self.s.get(url)
        res.raise_for_status()
        return Plugin(**res.json(), s=self.s)

    def get_plugin_by_name(self, name_exact: Union[PluginName, str],
                           version: Optional[Union[PluginVersion, str]] = None):
        search = self.search_plugin(name_exact, version)
        return peek(search, mt=PluginNotFoundError)

    def search_plugin(self, name_exact: str, version: Optional[str] = None
                      ) -> Generator[Plugin, None, None]:
        qs = self._join_qs(name_exact=name_exact, version=version)
        url = CUBEUrl(f'{self.search_addr_plugins}?{qs}')
        return fetch_paginated_objects(s=self.s, url=url, constructor=Plugin)

    def get_plugin_instance(self, plugin: Union[CUBEUrl, PluginInstanceId]):
        """
        Get a plugin instance.
        :param plugin: Either a plugin instance ID or URL
        :return: plugin instance
        """
        url = plugin if '/' in plugin else f'{self.address}plugins/instances/{plugin}/'
        res = self.s.get(url)
        res.raise_for_status()
        return PluginInstance(**res.json(), s=self.s)

    def run(self, plugin_name='', plugin_url='', plugin: Optional[PluginInstance] = None,
            params: Optional[dict] = None) -> PluginInstance:
        """
        Create a plugin instance. Either provide a plugin object,
        or search for a plugin by name or URL.
        :param plugin: plugin to run
        :param plugin_name: name of plugin to run
        :param plugin_url: alternatively specify plugin URL
        :param params: plugin parameters as key-value pairs (not collection+json)
        :return:
        """
        if not plugin:
            plugin = self.get_plugin(name_exact=plugin_name, url=plugin_url)
        return plugin.create_instance(params)

    def search_uploadedfiles(self, fname='', fname_exact='') -> ListOfDownloadableFiles:
        qs = self._join_qs(fname=fname, fname_exact=fname_exact)
        url = CUBEUrl(f"{self.collection_links['uploadedfiles']}search/?{qs}")
        return self.get_files(url)

    def get_files(self, url: CUBEUrl) -> ListOfDownloadableFiles:
        return ListOfDownloadableFiles(url=url, s=self.s)

    def search_pipelines(self, name='') -> Generator[RegisteredPipeline, None, None]:
        return fetch_paginated_objects(
            s=self.s,
            url=CUBEUrl(f"{self.collection_links['pipelines']}search/?name={name}"),
            constructor=RegisteredPipeline
        )

    def get_pipeline(self, name: str) -> RegisteredPipeline:
        return peek(self.search_pipelines(name), mt=PipelineNotFoundError)

    def get_username(self) -> CUBEUsername:
        res = self.s.get(url=self.collection_links['user'])
        res.raise_for_status()
        data = res.json()
        return CUBEUsername(data['username'])

    @staticmethod
    def _join_qs(**kwargs) -> str:
        return '&'.join([f'{k}={v}' for k, v in kwargs.items() if v])
