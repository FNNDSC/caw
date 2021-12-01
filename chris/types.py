from typing import NewType, Literal, Union

CUBEToken = NewType('CUBEToken', str)
CUBEAddress = NewType('CUBEAddress', str)
CUBEUsername = NewType('CUBEUsername', str)
CUBEPassword = NewType('CUBEPassword', str)

CUBEUrl = NewType('CUBEUrl', str)

PluginId = NewType('PluginId', int)
PluginName = NewType('PluginName', str)
PluginVersion = NewType('PluginVersion', str)
PluginType = Literal['ds', 'fs', 'ts']

SwiftPath = NewType('SwiftPath', str)

ISOFormatDateString = NewType('ISOFormatDateString', str)

# TODO: PluginInstanceStatus should be an enum
PluginInstanceStatus = Literal[
    'created', 'waiting', 'scheduled', 'started', 'registeringFiles',
    'finishedSuccessfully', 'finishedWithError', 'cancelled'
]

CUBEErrorCode = NewType('CUBEErrorCode', str)

ContainerImageTag = NewType('ContainerImageTag', str)

FeedId = NewType('FeedId', int)
PipingId = NewType('PipingId', int)
PipelineId = NewType('PipelineId', int)

FilesUrl = NewType('FilesUrl', CUBEUrl)

ParameterName = NewType('ParameterName', str)
ParameterType = Union[str, int, float, bool]
ParameterTypeName = Literal['string', 'integer', 'float', 'boolean']
PipelineParameterId = NewType('ParameterLocalId', int)
PluginParameterId = NewType('ParameterGlobalId', int)
PluginInstanceId = NewType('PluginInstanceId', int)

ComputeResourceName = NewType('ComputeResourceName', str)

FileResourceName = NewType('FileResourceName', str)
FileResourceUrl = NewType('FileResourceUrl', str)
FileId = NewType('FileId', int)