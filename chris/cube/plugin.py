from dataclasses import dataclass
from chris.types import (
    PluginId,
    PluginName,
    PluginType,
    PluginVersion,
    ContainerImageTag,
    PluginUrl,
    PluginInstancesUrl,
    ComputeResourceName,
)
from typing import Union, Optional
from chris.cube.plugin_instance import PluginInstance
from chris.helpers.connected_resource import ConnectedResource
import serde
from datetime import datetime


@serde.deserialize()
@dataclass(frozen=True)
class Plugin(ConnectedResource):
    """
    A *plugin* in *ChRIS* describes a unit of compute.
    To run something on *ChRIS*, a user creates a :class:`PluginInstance`
    of a *plugin*.
    """

    url: PluginUrl
    id: PluginId
    creation_date: datetime
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

    meta: str
    parameters: str
    instances: PluginInstancesUrl
    compute_resources: str

    def create_instance(
        self,
        params: Optional[dict] = None,
        compute_resource: Optional[Union[ComputeResourceName, str]] = None,
    ) -> PluginInstance:
        """
        Create a plugin instance, i.e. run this plugin.

        Parameters
        ----------
        params : dict
            Parameters to run the plugin with.
        compute_resource : str
            Name of compute resource where to run the plugin instance.
        """
        if compute_resource:
            if not params:
                params = {}
            params["compute_resource"] = compute_resource
        res = self.session.post(self.instances, json=params)
        return PluginInstance.deserialize(res, self.session)
