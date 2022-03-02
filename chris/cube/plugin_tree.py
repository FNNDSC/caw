import json
from functools import cached_property
from dataclasses import dataclass, field
from typing import Generator, Collection, Dict, Tuple, Optional
from collections import deque
from chris.types import ParameterType, PluginInstanceId, PipingId
from chris.cube.plugin import Plugin
from chris.cube.plugin_instance import PluginInstance
from chris.cube.resource import ConnectedResource
from chris.cube.piping import Piping


@dataclass(frozen=True)
class PluginTree(ConnectedResource, Collection['PluginTree']):
    """
    A ``PluginTree`` is an immutable node of a directed acyclic graph
    of plugins and default parameters for each plugin.
    It usually represents a piping, its associated plugin, and
    default parameters of a runnable *ChRIS* pipeline.

    CONSTRAINT: all plugins must be associated with the same CUBE.
    """

    piping: Piping
    default_parameters: Dict[str, ParameterType]
    children: Tuple['PluginTree', ...] = field(default_factory=tuple)
    # tuple instead of frozenset because PluginTree.default_parameters
    # is a dict, which is not hashable

    def get_plugin(self) -> Plugin:
        res = self.s.get(self.piping.plugin)
        res.raise_for_status()
        return Plugin(s=self.s, **res.json())

    def run(self, plugin_instance_id: PluginInstanceId
            ) -> Generator[Tuple[PluginInstance, 'PluginTree'], None, None]:
        """
        Create plugin instances in DFS-order.
        The returned iterator must be iterated through to
        schedule this entire plugin tree.
        It produces 2-tuples of the created ``PluginInstance``
        and the ``PluginTree`` from which the instance was created.

        :param plugin_instance_id: parent plugin instance
        """
        params = {
            'previous_id': plugin_instance_id
        }
        params.update(self.default_parameters)
        created_instance = self.get_plugin().create_instance(params)
        yield created_instance, self
        for child in self.children:
            yield from child.run(created_instance.id)

    # the two traversal methods below are not currently used

    def dfs(self) -> Generator['PluginTree', None, None]:
        """
        Depth-first graph traversal.
        """
        yield self
        yield from self.children

    def bfs(self) -> Generator['PluginTree', None, None]:
        """
        Breadth-first graph traversal.

        BFS is insignificantly better than DFS because sibling
        plugin instances can be scheduled insignificantly sooner.
        A stupidly optimal solution would schedule branches by
        doing the HTTP POST requests in parallel.
        """
        queue: deque['PluginTree'] = deque()
        queue.append(self)
        while queue:
            current = queue.popleft()
            yield current
            queue.extend(current.children)

    def __iter__(self):
        return self.dfs()

    def __len__(self):
        return self.length

    @cached_property
    def length(self) -> int:
        count = 0
        for _ in self:
            count += 1
        return count

    def __contains__(self, __x: object) -> bool:
        return any(__x == e for e in self)

    def deserialize(self) -> str:
        """
        Produce this Plugin Tree as JSON according to the ``plugin_tree`` schema
        of the *ChRIS* pipeline spec.
        """
        return json.dumps(self.deserialize_tree())

    def deserialize_tree(self) -> list:
        data = []
        index_map: dict[Optional[PipingId], Optional[int]] = {
            None: None
        }

        for node in self.bfs():
            index_map[node.piping.id] = len(data)
            previous_index = index_map[node.piping.previous_id]
            data.append(node.deserialize_node(previous_index))

        return data

    def deserialize_node(self, previous_index: Optional[int]) -> dict:
        """
        Deserialize just this ``PluginTree`` (and not its children).
        """
        plugin = self.get_plugin()
        data = {
            'plugin_name': plugin.name,
            'plugin_version': plugin.version,
            'previous_index': previous_index
        }

        if self.default_parameters:
            data['plugin_parameter_defaults'] = [
                {
                    'name': name,
                    'default': value
                }
                for name, value in self.default_parameters.items()
            ]

        return data
