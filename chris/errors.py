from dataclasses import dataclass


class ChrisError(Exception):
    """
    Base class for exceptions produced by the `chris` module.
    """

    pass


@dataclass(frozen=True)
class StatusError(ChrisError):
    """
    Unexpected HTTP status from CUBE.
    """

    status: int
    body: str


@dataclass(frozen=True)
class ResponseError(ChrisError):
    """
    Unexpected response from CUBE.
    """

    msg: str
    body: str


class ChrisIncorrectLoginError(ChrisError):
    pass


class ChrisResourceNotFoundError(ChrisError):
    pass


class PluginNotFoundError(ChrisResourceNotFoundError):
    pass


class PipelineNotFoundError(ChrisResourceNotFoundError):
    pass


class WaitTimeoutException(Exception):
    pass
