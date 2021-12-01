import os
import requests
from datetime import datetime
from chris.errors import PaginationNotImplementedException
from typing import Optional, Union, Iterator
from collections.abc import Iterable
from pathlib import Path
import logging






class UploadedFile(ConnectedResource):
    """
    Represents a file resource in CUBE.

    TODO: rename to RegisteredFile
    """
    def __init__(self, creation_date: str, file_resource: str, fname: str, fsize: int, id: int,
                 url: str, session: requests.Session,
                 owner: Optional[str] = None,
                 feed_id: Optional[int] = None, plugin_inst: Optional[str] = None,
                 plugin_inst_id: Optional[int] = None,

                 PatientID: Optional[str] = None,
                 PatientName: Optional[str] = None,
                 PatientBirthDate: Optional[str] = None,
                 PatientAge: Optional[float] = None,  # float or int?
                 PatientSex: Optional[str] = None,
                 StudyDate: Optional[str] = None,
                 Modality: Optional[str] = None,
                 ProtocolName: Optional[str] = None,
                 StudyInstanceUID: Optional[str] = None,
                 StudyDescription: Optional[str] = None,
                 SeriesInstanceUID: Optional[str] = None,
                 SeriesDescription: Optional[str] = None,
                 pacs_identifier: Optional[str] = None):
        super().__init__(url, session)
        self.creation_date = datetime.fromisoformat(creation_date)
        self.file_resource = file_resource
        self.fname = fname
        self.fsize = fsize
        self.id = id
        self.ownder = owner
        self.feed_id = feed_id
        self.plugin_inst = plugin_inst
        self.plugin_inst_id = plugin_inst_id

        self.PatientID = PatientID
        self.PatientName = PatientName
        self.PatientBirthDate = PatientBirthDate
        self.PatientAge: Optional[float] = PatientAge
        self.PatientSex = PatientSex
        self.StudyDate = StudyDate
        self.Modality = Modality
        self.ProtocolName = ProtocolName
        self.StudyInstanceUID = StudyInstanceUID
        self.StudyDescription = StudyDescription
        self.SeriesInstanceUID = SeriesInstanceUID
        self.SeriesDescription = SeriesDescription
        self.pacs_identifier = pacs_identifier

    def download(self, destination: Union[Path, str], chunk_size=8192):
        with self._s.get(self.file_resource, stream=True, headers={'Accept': None}) as r:
            r.raise_for_status()
            with open(destination, 'wb') as f:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)


class InvalidFilesResourceUrlException(Exception):
    pass


class UploadedFiles(ConnectedResource, Iterable):
    """
    Lazy iterable over paginated response.
    """
    __logger = logging.getLogger('UploadedFiles')

    def __init__(self, url: str, session: requests.Session):
        super().__init__(url, session)
        if 'limit=' not in self.url:
            self.url += f"{'&' if '?' in self.url else '?'}limit={PAGINATION_LIMIT}"

        try:
            self._initial_data = self._do_get(self.url)
        except requests.exceptions.HTTPError as e:
            raise InvalidFilesResourceUrlException(f'{e.response.status_code} error getting {self.url}')
        # check given URL is a files collection resource
        if 'count' not in self._initial_data:
            raise InvalidFilesResourceUrlException(f'{self.url} does not look like a files collection resource.')
        if self._initial_data['count'] > 0:
            try:
                UploadedFile(session=self._s, **self._initial_data['results'][0])
            except KeyError:
                raise InvalidFilesResourceUrlException(f'{self.url} is not a files collection resource.')

    def __iter__(self) -> Iterator[UploadedFile]:
        data = self._initial_data  # first page
        if data['previous'] is not None:
            self.__logger.warning('%s is not the first page.', self.url)

        while data['next']:
            for fdata in data['results']:
                yield UploadedFile(**fdata, session=self._s)
            self.__logger.debug('next page: %s', data['next'])
            data = self._do_get(data['next'])  # next page
        for fdata in data['results']:  # last page
            yield UploadedFile(**fdata, session=self._s)

    def __len__(self):
        return self._initial_data['count']

    def _do_get(self, url):
        self.__logger.info('getting %s', url)
        res = self._s.get(url)
        res.raise_for_status()
        return res.json()
