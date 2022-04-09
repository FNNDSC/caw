from typing import NewType, Literal, Union

CUBEToken = NewType("CUBEToken", str)
CUBEAddress = NewType("CUBEAddress", str)
Username = NewType("Username", str)

PluginUrl = NewType("PluginUrl", str)
PluginId = NewType("PluginId", int)
PluginName = NewType("PluginName", str)
PluginVersion = NewType("PluginVersion", str)
PluginType = Literal["ds", "fs", "ts"]

SwiftPath = NewType("SwiftPath", str)

# TODO: PluginInstanceStatus should be an enum
PluginInstanceStatus = Literal[
    "created",
    "waiting",
    "scheduled",
    "started",
    "registeringFiles",
    "finishedSuccessfully",
    "finishedWithError",
    "cancelled",
]

CUBEErrorCode = NewType("CUBEErrorCode", str)

ContainerImageTag = NewType("ContainerImageTag", str)

FeedId = NewType("FeedId", int)
PipingId = NewType("PipingId", int)
PipelineId = NewType("PipelineId", int)


ParameterName = NewType("ParameterName", str)
ParameterType = Union[str, int, float, bool]
ParameterTypeName = Literal["string", "integer", "float", "boolean"]
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
