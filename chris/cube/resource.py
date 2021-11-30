import abc
from dataclasses import dataclass
import requests
from typing import Union
from chris.types import CUBEUrl


@dataclass(frozen=True)
class AbstractResource(abc.ABC):
    """
    A representation of data returned from the CUBE API, which provides methods
    for making further requests to the CUBE API.
    """
    url: Union[CUBEUrl, str]
    s: requests.Session
