from dataclasses import dataclass
from serde import deserialize

from chris.types import UserUrl, FilesUrl, TagsUrl


@deserialize()
@dataclass(frozen=True)
class BaseCollectionLinks:
    chrisinstance: str
    admin: str
    files: FilesUrl
    compute_resources: str
    plugin_metas: str
    plugins: str
    plugin_instances: str
    pipelines: str
    pipeline_instances: str
    tags: TagsUrl
    uploadedfiles: FilesUrl
    pacsfiles: FilesUrl
    servicefiles: FilesUrl
    filebrowser: str
    user: UserUrl


@deserialize()
@dataclass(frozen=True)
class BaseResponse:
    collection_links: BaseCollectionLinks
