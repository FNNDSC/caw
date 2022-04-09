from dataclasses import dataclass

import serde

from chris.types import (
    FeedId,
    Username,
    FilesUrl,
    FeedUrl,
    PluginInstancesUrl,
    NoteUrl,
    UserUrl,
    TagsUrl,
    TaggingsUrl,
    CommentsUrl,
)

from chris.helpers.connected_resource import ConnectedResource
from typing import List
from datetime import datetime


@serde.deserialize()
@dataclass(frozen=True)
class Feed(ConnectedResource):
    """
    A *feed* in *ChRIS* is a DAG of *plugin instances*.
    """

    url: FeedUrl
    id: FeedId
    creation_date: datetime
    modification_date: datetime
    name: str
    creator_username: Username
    created_jobs: int
    waiting_jobs: int
    scheduled_jobs: int
    started_jobs: int
    registering_jobs: int
    finished_jobs: int
    errored_jobs: int
    cancelled_jobs: int
    owner: List[UserUrl]
    note: NoteUrl
    tags: TagsUrl
    taggings: TaggingsUrl
    comments: CommentsUrl
    files: FilesUrl
    plugin_instances: PluginInstancesUrl

    def set_name(self, name: str) -> "Feed":
        self.__put(url=self.url, data={"name": name})
        return self.__refresh()

    def set_description(self, description: str) -> "Feed":
        self.__put(url=self.note, data={"title": "Description", "content": description})
        return self.__refresh()

    def __put(self, url: str, data: dict) -> dict:
        res = self.session.put(url, json=data)
        res.raise_for_status()
        return res.json()

    def __refresh(self) -> "Feed":
        res = self.session.get(self.url)
        return self.deserialize(res, self.session)
