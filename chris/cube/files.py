from pathlib import Path
from dataclasses import dataclass
from typing import Iterable, Generator
import requests

from chris.cube.resource import CUBEResource
from chris.cube.pagination import fetch_paginated_objects
from chris.types import FileResourceUrl, FileResourceName


# TODO add all the fields of the various kinds of files
# UploadedFile, FeedFile, PACSFile


@dataclass(frozen=True)
class DownloadableFile(CUBEResource):
    file_resource: FileResourceUrl
    fname: FileResourceName

    def download(self, destination: Path, chunk_size=8192):
        with self.s.get(self.file_resource, stream=True, headers={'Accept': None}) as r:
            r.raise_for_status()
            with destination.open('wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)


@dataclass(frozen=True)
class ListOfDownloadableFiles(Iterable[DownloadableFile], CUBEResource):
    def __iter__(self) -> Generator[DownloadableFile, None, None]:
        return fetch_paginated_objects(s=self.s, url=self.url, constructor=self._construct_downloadable_file)

    @staticmethod
    def _construct_downloadable_file(s: requests.Session, **kwargs):
        return DownloadableFile(s=s, url=kwargs['url'],
                                fname=kwargs['fname'],
                                file_resource=kwargs['file_resource'])
