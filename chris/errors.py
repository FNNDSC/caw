
class ChrisClientError(Exception):
    pass


class ChrisIncorrectLoginError(ChrisClientError):
    pass


class ChrisResourceNotFoundError(ChrisClientError):
    pass


class PluginNotFoundError(ChrisResourceNotFoundError):
    pass


class PipelineNotFoundError(ChrisResourceNotFoundError):
    pass


class PaginationNotImplementedException(Exception):
    pass
