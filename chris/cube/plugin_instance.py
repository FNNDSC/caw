from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from chris.cube.resource.cube_resource import CUBEResource
from chris.cube.feed import Feed
from chris.types import (
    CUBEUsername, CUBEUrl, PluginName, PluginVersion, PluginType,
    PluginInstanceId, FeedId, PluginId, ComputeResourceName,
    SwiftPath, ISOFormatDateString, PluginInstanceStatus, CUBEErrorCode
)


# It'd be better to use inheritance instead of optionals
@dataclass(frozen=True)
class PluginInstance(CUBEResource):
    """
    A *plugin instance* in _ChRIS_ is a computing job, i.e. an attempt to run
    a computation (a non-interactive command-line app) to produce data.
    """
    id: Optional[PluginInstanceId]
    title: str
    compute_resource_name: ComputeResourceName
    plugin_id: PluginId
    plugin_name: PluginName
    plugin_version: PluginVersion
    plugin_type: PluginType

    pipeline_inst: Optional[int]
    feed_id: FeedId
    start_date: ISOFormatDateString
    end_date: ISOFormatDateString
    output_path: SwiftPath

    status: PluginInstanceStatus

    summary: str
    raw: str
    owner_username: CUBEUsername
    cpu_limit: int
    memory_limit: int
    number_of_workers: int
    gpu_limit: int
    error_code: CUBEErrorCode

    previous: CUBEUrl
    feed: CUBEUrl
    plugin: CUBEUrl
    descendants: CUBEUrl
    files: CUBEUrl
    parameters: CUBEUrl
    compute_resource: CUBEUrl
    splits: CUBEUrl

    previous_id: Optional[int] = None
    """
    FS plugins will not produce a ``previous_id`` value
    (even though they will return ``"previous": null``)
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
        inst_res = self.s.get(self.url).json()
        feed_url = inst_res['feed']
        feed_res = self.s.get(feed_url).json()
        return Feed(s=self.s, **feed_res)

    def get_start_date(self) -> datetime:
        return datetime.fromisoformat(self.start_date)

    def get_end_date(self) -> datetime:
        return datetime.fromisoformat(self.end_date)
