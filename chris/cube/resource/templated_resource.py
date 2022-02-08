import abc
from typing import TypedDict, List
from dataclasses import dataclass, InitVar
from chris.cube.resource.cube_resource import CUBEResource


class CollectionEntry(TypedDict):
    name: str
    value: str


class Template(TypedDict):
    data: List[CollectionEntry]


@dataclass(frozen=True)
class ResourceWithTemplate(CUBEResource, abc.ABC):
    template: InitVar[Template]

    def __post_init__(self, template: Template):
        pass
