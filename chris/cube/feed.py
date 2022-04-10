from dataclasses import dataclass

from serde import deserialize
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


from requests import Response


@deserialize
@dataclass(frozen=True)
class Note(ConnectedResource):
    url: NoteUrl
    id: int
    title: str
    content: str
    feed: FeedUrl


@deserialize
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
        res = self.session.put(self.url, data={"name": name})
        res.raise_for_status()
        return self.__refresh()

    def set_description(self, description: str) -> Note:
        res = self.session.put(
            self.note, data={"title": "Description", "content": description}
        )
        return Note.deserialize(res, self.session)

    def get_note(self) -> Note:
        return Note.deserialize(self.session.get(self.note), self.session)

    def __refresh(self) -> "Feed":
        res = self.session.get(self.url)
        return self.deserialize(res, self.session)
