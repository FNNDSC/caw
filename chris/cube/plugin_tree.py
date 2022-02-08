from dataclasses import dataclass, field
from typing import Generator, Collection, Dict, Tuple
from collections import deque
from chris.types import CUBEUrl, ParameterType, PluginInstanceId
from chris.cube.plugin import Plugin
from chris.cube.plugin_instance import PluginInstance
from chris.cube.resource import ConnectedResource


@dataclass(frozen=True)
class PluginTree(ConnectedResource, Collection['PluginTree']):
    """
    A ``PluginTree`` is an immutable node of a directed acyclic graph
    of plugins and default parameters for each plugin.
    It usually represents a runnable pipeline.

    CONSTRAINT: all plugins must be associated with the same CUBE.
    """

    plugin: CUBEUrl
    default_parameters: Dict[str, ParameterType]
    children: Tuple['PluginTree', ...] = field(default_factory=tuple)
    # tuple instead of frozenset because PluginTree.default_parameters
    # is a dict, which is not hashable

    def get_plugin(self) -> Plugin:
        res = self.s.get(self.plugin)
        res.raise_for_status()
        return Plugin(s=self.s, **res.json())

    def run(self, plugin_instance_id: PluginInstanceId
            ) -> Generator[PluginInstance, None, None]:
        """
        Create plugin instances in DFS-order.
        The returned iterator must be iterated through to
        schedule this entire plugin tree.

        :param plugin_instance_id: parent plugin instance
        """
        params = {
            'previous_id': plugin_instance_id
        }
        params.update(self.default_parameters)
        created_instance = self.get_plugin().create_instance(params)
        yield created_instance
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
        count = 0
        for _ in self:
            count += 1
        return count

    def __contains__(self, __x: object) -> bool:
        return any(__x == e for e in self)
