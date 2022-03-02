from dataclasses import dataclass
from typing import Optional
from chris.cube.resource import CUBEResource

from chris.types import (
    PluginUrl, CUBEUrl, PipelineId, CUBEUsername, ISOFormatDateString,
    ParameterName, ParameterType, ParameterTypeName, PipingId,
    PipelineParameterId, PluginParameterId,
    PluginName, PluginVersion, PluginId, PipingUrl
)


@dataclass(frozen=True)
class PipingParameter(CUBEResource):
    id: PipelineParameterId
    value: ParameterType
    type: ParameterTypeName
    plugin_piping_id: PipingId
    previous_plugin_piping_id: None
    param_name: ParameterName
    param_id: PluginParameterId
    plugin_piping: CUBEUrl
    plugin_name: PluginName
    plugin_version: PluginVersion
    plugin_id: PluginId
    plugin_param: CUBEUrl


@dataclass(frozen=True)
class Piping(CUBEResource):
    id: PipingId
    plugin_id: PluginId
    pipeline_id: PipelineId
    previous: Optional[PipingUrl]
    plugin: PluginUrl
    pipeline: CUBEUrl
    previous_id: Optional[PipingId] = None
