import json
import abc
from dataclasses import dataclass
from chris.cube.plugin_tree import PluginTree


@dataclass(frozen=True)
class Pipeline(abc.ABC):
    name: str
    authors: str
    description: str
    category: str
    locked: bool

    @abc.abstractmethod
    def get_root(self) -> PluginTree:
        ...

    def deserialize(self) -> str:
        """
        Produce a JSON representation which can be uploaded to a CUBE instance.
        """
        data = [
            {
                'name': 'name',
                'value': self.name
            },
            {
                'name': 'authors',
                'value': self.authors,
            },
            {
                'name': 'category',
                'value': self.category,
            },
            {
                'name': 'description',
                'value': self.description,
            },
            {
                'name': 'locked',
                'value': self.locked,
            },
            {
                'name': 'plugin_tree',
                'value': self.get_root().deserialize()
            }
        ]
        template = {
            'template': {
                'data': data
            }
        }
        return json.dumps(template)
