from dataclasses import dataclass
from chris.cube.resource import CUBEResource
from chris.types import (
    PluginId, PluginName, PluginType, PluginVersion, ISOFormatDateString, ContainerImageTag, CUBEUrl
)
from chris.cube.plugin_instance import PluginInstance
from chris.helpers.collection import collection_helper

import logging

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Plugin(CUBEResource):
    """
    A *plugin* in *ChRIS* describes a unit of compute.
    To run something on *ChRIS*, a user creates a :class:`PluginInstance`
    of a *plugin*.
    """
    id: PluginId
    creation_date: ISOFormatDateString
    name: PluginName

    version: PluginVersion
    dock_image: ContainerImageTag
    public_repo: str
    icon: str
    type: PluginType
    stars: int

    authors: str
    title: str
    category: str
    description: str
    documentation: str
    license: str

    execshell: str
    selfpath: str
    selfexec: str
    min_number_of_workers: int
    max_number_of_workers: int
    min_cpu_limit: int
    max_cpu_limit: int
    min_gpu_limit: int
    max_gpu_limit: int
    min_memory_limit: int
    max_memory_limit: int

    meta: CUBEUrl
    parameters: CUBEUrl
    instances: CUBEUrl
    compute_resources: CUBEUrl

    def create_instance(self, params: dict = None) -> PluginInstance:
        logging.debug('%s: %s', self.name, params)
        payload = collection_helper(params)
        res = self.s.post(self.instances, json=payload)
        res.raise_for_status()
        return PluginInstance(**res.json(), s=self.s)
