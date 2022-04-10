from os import PathLike
from dataclasses import dataclass
from contextlib import contextmanager
from typing import Iterable, Sized, Iterator, Union, ContextManager
from requests import Response

from chris.types import FileResourceUrl, FileResourceName
import serde
from chris.helpers.connected_resource import ConnectedResource


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


@serde.deserialize()
@dataclass(frozen=True)
class File(ConnectedResource):
    """
    A file in _ChRIS_.
    """

    url: str
    fname: FileResourceName
    fsize: int
    file_resource: FileResourceUrl

    def download(self, destination: Union[PathLike, str], chunk_size=8192):
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
