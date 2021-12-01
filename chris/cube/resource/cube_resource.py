import abc
from dataclasses import dataclass
from chris.types import CUBEUrl
from chris.cube.resource.connected_resource import ConnectedResource


@dataclass(frozen=True)
class CUBEResource(ConnectedResource, abc.ABC):
    """
    A ``CUBEResource`` represents data returned from an endpoint of the CUBE API.

    Responses from the CUBE API always return a ``url`` which indicated the requested URI.
    """
    url: CUBEUrl
