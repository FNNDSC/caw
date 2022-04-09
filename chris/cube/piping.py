from dataclasses import dataclass
from typing import Optional

from chris.types import (
    PluginUrl,
    PipelineId,
    ParameterName,
    ParameterType,
    ParameterTypeName,
    PipingId,
    PipelineParameterId,
    PluginParameterId,
    PluginName,
    PluginVersion,
    PluginId,
    PipingUrl,
    PluginParametersUrl,
    PipelineParameterUrl,
    PipelineUrl,
)
from chris.helpers.connected_resource import ConnectedResource
from serde import deserialize


@deserialize()
@dataclass(frozen=True)
class PipelineParameter(ConnectedResource):
    url: PipelineParameterUrl
    id: PipelineParameterId
    value: ParameterType
    type: ParameterTypeName
    plugin_piping_id: PipingId
    previous_plugin_piping_id: None
    param_name: ParameterName
    param_id: PluginParameterId
    plugin_piping: PipingUrl
    plugin_name: PluginName
    plugin_version: PluginVersion
    plugin_id: PluginId
    plugin_param: PluginParametersUrl


@deserialize()
@dataclass(frozen=True)
class Piping(ConnectedResource):
    url: PipingUrl
    id: PipingId
    plugin_id: PluginId
    pipeline_id: PipelineId
    previous: Optional[PipingUrl]
    plugin: PluginUrl
    pipeline: PipelineUrl
    previous_id: Optional[PipingId] = None
