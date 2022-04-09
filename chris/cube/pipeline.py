from dataclasses import dataclass
from typing import Sequence

from chris.helpers.pagination import Paginated
from chris.cube.piping import Piping, PipelineParameter
from chris.types import (
    PipelineId,
    Username,
    PipelineUrl,
    PipelinePluginsUrl,
    PipingsUrl,
    PipelineDefaultParametersUrl,
)
from chris.helpers.connected_resource import ConnectedResource
from datetime import datetime


@dataclass(frozen=True)
class Pipeline(ConnectedResource):
    url: PipelineUrl
    id: PipelineId

    name: str
    authors: str
    description: str
    category: str
    locked: bool

    owner_username: Username
    creation_date: datetime
    modification_date: datetime
    plugins: PipelinePluginsUrl
    plugin_pipings: PipingsUrl
    default_parameters: PipelineDefaultParametersUrl
    instances: str

    def get_default_parameters(self) -> Sequence[PipelineParameter]:
        return tuple(
            Paginated(
                item=PipelineParameter,
                url=self.default_parameters,
                session=self.session,
            )
        )

    def get_pipings(self) -> Paginated[Piping]:
        return Paginated(item=Piping, url=self.plugin_pipings, session=self.session)
