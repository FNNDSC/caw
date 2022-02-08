from dataclasses import dataclass

from chris.types import CUBEUrl, FeedId, ISOFormatDateString, CUBEUsername, FilesUrl

from chris.helpers.collection import collection_helper
from chris.cube.resource.templated_resource import ResourceWithTemplate

from typing import List


@dataclass(frozen=True)
class Feed(ResourceWithTemplate):
    """
    A *feed* in *ChRIS* is a DAG of *plugin instances*.
    """
    id: FeedId
    creation_date: ISOFormatDateString
    modification_date: ISOFormatDateString
    name: str
    creator_username: CUBEUsername
    created_jobs: int
    waiting_jobs: int
    scheduled_jobs: int
    started_jobs: int
    registering_jobs: int
    finished_jobs: int
    errored_jobs: int
    cancelled_jobs: int
    owner: List[CUBEUrl]
    note: CUBEUrl
    tags: CUBEUrl
    taggings: CUBEUrl
    comments: CUBEUrl
    files: FilesUrl
    plugin_instances: CUBEUrl

    def set_name(self, name: str) -> dict:
        return self.__put(
            url=self.url,
            data={'name': name}
        )

    def set_description(self, description: str) -> dict:
        return self.__put(
            url=self.note,
            data={
                'title': 'Description',
                'content': description
            }
        )

    def __put(self, url: CUBEUrl, data: dict) -> dict:
        payload = collection_helper(data)
        res = self.s.put(url, json=payload)
        res.raise_for_status()
        return res.json()
