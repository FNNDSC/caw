from dataclasses import dataclass
from typing import Generator, Sequence, Dict

from chris.cube.pagination import fetch_paginated_objects
from chris.cube.pipeline import Pipeline
from chris.cube.piping import PipingParameter, Piping
from chris.cube.resource import CUBEResource
from chris.types import (
    CUBEUrl,
    PipelineId,
    CUBEUsername,
    ISOFormatDateString,
    ParameterName,
    ParameterType,
    PipingId,
)


@dataclass(frozen=True)
class RegisteredPipeline(CUBEResource, Pipeline):
    id: PipelineId
    owner_username: CUBEUsername
    creation_date: ISOFormatDateString
    modification_date: ISOFormatDateString
    plugins: CUBEUrl
    plugin_pipings: CUBEUrl
    default_parameters: CUBEUrl
    instances: CUBEUrl

    def get_default_parameters(self) -> Sequence[PipingParameter]:
        return list(
            fetch_paginated_objects(
                session=self.s, url=self.default_parameters, constructor=PipingParameter
            )
        )

    @staticmethod
    def map_parameters(
        params: Sequence[PipingParameter],
    ) -> Dict[PipingId, Dict[ParameterName, ParameterType]]:
        assembled_params: Dict[PipingId, Dict[ParameterName, ParameterType]] = {
            p.plugin_piping_id: {} for p in params
        }
        for p in params:
            assembled_params[p.plugin_piping_id][ParameterName(p.param_name)] = p.value
        return assembled_params

    def get_pipings(self) -> Generator[Piping, None, None]:
        yield from fetch_paginated_objects(
            session=self.s, url=self.plugin_pipings, constructor=Piping
        )
