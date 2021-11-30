import abc
from typing import TypedDict
from dataclasses import dataclass, InitVar
from chris.cube.resource import AbstractResource


class CollectionEntry(TypedDict):
    name: str
    value: str


class Template(TypedDict):
    data: list[CollectionEntry]


@dataclass(frozen=True)
class ResourceWithTemplate(AbstractResource, abc.ABC):
    template: InitVar[Template]

    def __post_init__(self, template: Template):
        pass
