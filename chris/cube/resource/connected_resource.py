import abc
from dataclasses import dataclass
import requests


@dataclass(frozen=True)
class ConnectedResource(abc.ABC):
    """
    A ``ConnectedResource`` has a :class:`requests.Session` for
    communicating with a *ChRIS* backend.

    CONSTRAINT: ``s`` must have HTTP headers for authentication
                with CUBE and also the header ``Accept: application/json``
    """
    s: requests.Session
