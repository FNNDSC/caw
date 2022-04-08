from os import PathLike
from dataclasses import dataclass, InitVar, field
from contextlib import contextmanager
from typing import Iterable, Generator, Sized, Iterator, Union, ContextManager
from requests import Session, Response

from chris.cube.resource import CUBEResource
from chris.cube.pagination import fetch_paginated_objects
from chris.types import FileResourceUrl, FileResourceName
from serde import deserialize
from serde.json import from_dict


@dataclass(frozen=True)
class Stream(Iterable[bytes], Sized):
    """
    Byte-stream.
    """

    fsize: int
    chunk_size: int
    res: Response

    def __iter__(self) -> Iterator[bytes]:
        return self.res.iter_content(chunk_size=self.chunk_size)

    def __len__(self) -> int:
        return self.fsize


@deserialize
@dataclass(frozen=True)
class File:
    """
    A file in _ChRIS_.
    """

    url: str
    fname: FileResourceName
    fsize: int
    file_resource: FileResourceUrl


@dataclass(frozen=True)
class DownloadableFile(File):
    """
    A file in _ChRIS_ which can be downloaded.
    """

    session: Session

    def download(self, destination: Union[str | PathLike], chunk_size=8192):
        """
        Download this file to a path.
        """
        with self.stream(chunk_size) as stream:
            with open(destination, "wb") as f:
                for data in stream:
                    f.write(data)

    @contextmanager
    def stream(self, chunk_size: int) -> ContextManager[Stream]:
        """
        Download the file as a bytes-stream, useful for adding a progress bar to large files.

        # Example

        ```python
        from tqdm import tqdm

        with open("file.dat", "wb") as f:
            with file.stream(8196) as stream:
                for chunk in tqdm(stream):
                    f.write(chunk)
        ```
        """
        with self.session.get(
            self.file_resource, stream=True, headers={"Accept": None}
        ) as r:
            r.raise_for_status()
            yield Stream(self.fsize, chunk_size, r)

    @classmethod
    def deserialize(cls, data: dict, session: Session) -> "DownloadableFile":
        f: File = from_dict(File, data)
        return cls(f.url, f.fname, f.fsize, f.file_resource, session)


@dataclass(frozen=True)
class DownloadableFilesGenerator(Iterable[DownloadableFile], Sized):
    url: str
    session: Session

    def __len__(self) -> int:
        self.session.get(self.url, params={"limit": 0})

    def __iter__(self) -> Generator[DownloadableFile, None, None]:
        return fetch_paginated_objects(
            session=self.session, url=self.url, constructor=DownloadableFile.deserialize
        )
