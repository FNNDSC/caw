import abc
from dataclasses import dataclass
from chris.cube.plugin_tree import PluginTree


@dataclass(frozen=True)
class Pipeline(abc.ABC):
    name: str
    authors: str
    description: str
    category: str

    @abc.abstractmethod
    def get_root(self) -> PluginTree:
        ...
