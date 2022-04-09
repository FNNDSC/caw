from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from chris.helpers.connected_resource import ConnectedResource
from chris.cube.feed import Feed
from chris.types import (
    Username,
    PluginName,
    PluginVersion,
    PluginType,
    PluginInstanceId,
    FeedId,
    PluginId,
    ComputeResourceName,
    SwiftPath,
    PluginInstanceStatus,
    CUBEErrorCode,
    PluginInstanceUrl,
    FeedUrl,
    PluginUrl,
    FilesUrl,
    SplitsUrl,
    ComputeResourceUrl,
    PluginInstanceParamtersUrl,
    DescendantsUrl,
)

import serde


# TODO It'd be better to use inheritance instead of optionals
@serde.deserialize()
@dataclass(frozen=True)
class PluginInstance(ConnectedResource):
    """
    A *plugin instance* in _ChRIS_ is a computing job, i.e. an attempt to run
    a computation (a non-interactive command-line app) to produce data.
    """

    url: PluginInstanceUrl
    id: Optional[PluginInstanceId]  # why is this optional again?
    title: str
    compute_resource_name: ComputeResourceName
    plugin_id: PluginId
    plugin_name: PluginName
    plugin_version: PluginVersion
    plugin_type: PluginType

    pipeline_inst: Optional[int]
    feed_id: FeedId
    start_date: datetime
    end_date: datetime
    output_path: SwiftPath

    status: PluginInstanceStatus

    summary: str
    raw: str
    owner_username: Username
    cpu_limit: int
    memory_limit: int
    number_of_workers: int
    gpu_limit: int
    error_code: CUBEErrorCode

    previous: Optional[PluginInstanceUrl]
    feed: FeedUrl
    plugin: Optional[PluginUrl]
    descendants: DescendantsUrl
    files: FilesUrl
    parameters: PluginInstanceParamtersUrl
    compute_resource: ComputeResourceUrl
    splits: SplitsUrl

    previous_id: Optional[int] = None
    """
    FS plugins will not produce a `previous_id` value
    (even though they will return `"previous": null`)
    """

    size: Optional[int] = None
    """
    IDK what it is the size of.
    
    This field shows up when the plugin instance is maybe done,
    but not when the plugin instance is created.
    """
    template: Optional[dict] = None
    """
    Present only when getting a plugin instance.
    """

    def get_feed(self) -> Feed:
        res = self.session.get(self.feed)
        return Feed.deserialize(res, self.session)
