from dataclasses import dataclass, field
from typing import Generator, Sequence, Optional, List, Dict
import requests
from chris.cube.resource import CUBEResource
from chris.cube.pagination import fetch_paginated_objects
from chris.cube.pipeline import Pipeline
from chris.cube.plugin_tree import PluginTree

from chris.types import (
    CUBEUrl, PipelineId, CUBEUsername, ISOFormatDateString,
    ParameterName, ParameterType, ParameterTypeName, PipingId,
    PipelineParameterId, PluginParameterId,
    PluginName, PluginVersion, PluginId
)


class PipelineAssemblyException(Exception):
    """
    Pipeline JSON representation cannot be reassembled as a Piping DAG.
    """
    pass


class PipelineHasMultipleRootsException(PipelineAssemblyException):
    """
    Multiple *pipings* with 'previous': null were found in the pipeline JSON representation.
    """
    pass


class PipelineRootNotFoundException(PipelineAssemblyException):
    """
    No piping found in the pipelines JSON representation with 'previous': null.
    """
    pass


@dataclass(frozen=True)
class PipingParameter(CUBEResource):
    id: PipelineParameterId
    value: ParameterType
    type: ParameterTypeName
    plugin_piping_id: PipingId
    previous_plugin_piping_id: None
    param_name: ParameterName
    param_id: PluginParameterId
    plugin_piping: CUBEUrl
    plugin_name: PluginName
    plugin_version: PluginVersion
    plugin_id: PluginId
    plugin_param: CUBEUrl


@dataclass(frozen=True)
class Piping(CUBEResource):
    id: PipingId
    plugin_id: PluginId
    pipeline_id: PipelineId
    previous: CUBEUrl
    plugin: CUBEUrl
    pipeline: CUBEUrl
    previous_id: Optional[PipingId] = None


@dataclass
class MutablePluginTreeNode:
    """
    A mutable predecessor to :class:`PluginTree`.
    """
    s: requests.Session
    piping: Piping
    params: Dict[ParameterName, ParameterType] = field(default_factory=dict)
    children: List['MutablePluginTreeNode'] = field(default_factory=list)

    def freeze(self) -> PluginTree:
        """
        Convert to an immutable :class:`PluginTree`.
        """
        return PluginTree(
            s=self.s,
            plugin=self.piping.plugin,
            default_parameters=self.params,
            children=tuple(n.freeze() for n in self.children)
        )


@dataclass(frozen=True)
class RegisteredPipeline(CUBEResource, Pipeline):
    id: PipelineId
    locked: bool
    owner_username: CUBEUsername
    creation_date: ISOFormatDateString
    modification_date: ISOFormatDateString
    plugins: CUBEUrl
    plugin_pipings: CUBEUrl
    default_parameters: CUBEUrl
    instances: CUBEUrl

    def get_default_parameters(self) -> Sequence[PipingParameter]:
        return list(fetch_paginated_objects(s=self.s, url=self.default_parameters, constructor=PipingParameter))

    @staticmethod
    def map_parameters(params: Sequence[PipingParameter]) -> Dict[PipingId, Dict[ParameterName, ParameterType]]:
        assembled_params: Dict[PipingId, Dict[ParameterName, ParameterType]] = {
            p.plugin_piping_id: {} for p in params
        }
        for p in params:
            assembled_params[p.plugin_piping_id][ParameterName(p.param_name)] = p.value
        return assembled_params

    def get_pipings(self) -> Generator[Piping, None, None]:
        yield from fetch_paginated_objects(s=self.s, url=self.plugin_pipings, constructor=Piping)

    def get_root(self) -> PluginTree:
        """
        Assemble a tree of plugins by making requests to CUBE.
        """
        # collect all default parameters
        assembled_params = self.map_parameters(self.get_default_parameters())
        pipings_map: Dict[PipingId, MutablePluginTreeNode] = {}
        root: Optional[MutablePluginTreeNode] = None

        # create DAG nodes
        for piping in self.get_pipings():
            params = assembled_params[piping.id] if piping.id in assembled_params else {}

            node = MutablePluginTreeNode(piping=piping, params=params, s=self.s)
            pipings_map[piping.id] = node

            if piping.previous:
                pipings_map[piping.previous_id].children.append(node)
            else:
                if root is not None:
                    raise PipelineHasMultipleRootsException()
                root = node
        if not root:
            raise PipelineRootNotFoundException()
        return root.freeze()
