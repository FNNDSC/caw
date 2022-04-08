import abc
from dataclasses import dataclass


@dataclass(frozen=True)
class Pipeline(abc.ABC):
    name: str
    authors: str
    description: str
    category: str
    locked: bool
