from typing import NewType, Union
from enum import Enum

# pyserde doesn't support typing.Literal

CUBEToken = NewType("CUBEToken", str)
CUBEAddress = NewType("CUBEAddress", str)
Username = NewType("Username", str)

PluginUrl = NewType("PluginUrl", str)
PluginId = NewType("PluginId", int)
PluginName = NewType("PluginName", str)
PluginVersion = NewType("PluginVersion", str)


SwiftPath = NewType("SwiftPath", str)


CUBEErrorCode = NewType("CUBEErrorCode", str)

ContainerImageTag = NewType("ContainerImageTag", str)

FeedId = NewType("FeedId", int)
PipingId = NewType("PipingId", int)
PipelineId = NewType("PipelineId", int)


ParameterName = NewType("ParameterName", str)
ParameterType = Union[str, int, float, bool]

PipelineParameterId = NewType("ParameterLocalId", int)
PluginParameterId = NewType("ParameterGlobalId", int)
PluginInstanceId = NewType("PluginInstanceId", int)

ComputeResourceName = NewType("ComputeResourceName", str)
FileResourceName = NewType("FileResourceName", str)
FileId = NewType("FileId", int)

UserUrl = NewType("UserUrl", str)
FilesUrl = NewType("FilesUrl", str)
FileResourceUrl = NewType("FileResourceUrl", str)
PipelineUrl = NewType("PipelineUrl", str)
PipingsUrl = NewType("PipingsUrl", str)
PipelinePluginsUrl = NewType("PipelinePluginsUrl", str)
PipelineDefaultParametersUrl = NewType("PipelineDefaultParametersUrl", str)
PipingUrl = NewType("PipingUrl", str)

PipelineParameterUrl = NewType("PipingParameterUrl", str)
PluginInstanceUrl = NewType("PluginInstanceUrl", str)
PluginInstancesUrl = NewType("PluginInstancesUrl", str)
DescendantsUrl = NewType("DescendantsUrl", str)
PipelineInstancesUrl = NewType("PipelineInstancesUrl", str)
PluginInstanceParamtersUrl = NewType("PluginInstanceParametersUrl", str)
ComputeResourceUrl = NewType("ComputeResourceUrl", str)
SplitsUrl = NewType("SplitsUrl", str)
FeedUrl = NewType("FeedUrl", str)
NoteUrl = NewType("NoteUrl", str)
"""A feed's note."""
PluginParametersUrl = NewType("PluginParametersUrl", str)
TagsUrl = NewType("TagsUrl", str)
TaggingsUrl = NewType("TaggingsUrl", str)
CommentsUrl = NewType("CommentsUrl", str)


class PluginType(Enum):
    ds = "ds"
    fs = "fs"
    ts = "ts"


class PluginInstanceStatus(Enum):
    created = "created"
    waiting = "waiting"
    scheduled = "scheduled"
    started = "started"
    registeringFiles = "registeringFiles"
    finishedSuccessfully = "finishedSuccessfully"
    finishedWithError = "finishedWithError"
    cancelled = "cancelled"


class ParameterTypeName(Enum):
    string = "string"
    integer = "integer"
    float = "float"
    boolean = "boolean"
