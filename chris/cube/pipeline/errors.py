class PipelineAssemblyException(Exception):
    """
    Pipeline JSON representation cannot be reassembled as a Piping DAG.
    """
    pass


class PipelineHasMultipleRootsException(PipelineAssemblyException):
    """
    Multiple *pipings* with 'previous': null were found in the pipeline JSON representation.
    """
    pass


class PipelineRootNotFoundException(PipelineAssemblyException):
    """
    No piping found in the pipelines JSON representation with 'previous': null.
    """
    pass
