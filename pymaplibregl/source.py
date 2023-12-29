from __future__ import annotations

from enum import Enum
from typing import Union

from pydantic import BaseModel, ConfigDict, Field, computed_field


class SourceType(Enum):
    RASTER = "raster"
    VECTOR = "vector"
    RASTER_DEM = "raster-dem"
    GEOJSON = "geojson"
    IMAGE = "image"
    VIDEO = "video"


class SourceModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra="allow")

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)


class GeoJSONSource(SourceModel):
    data: Union[str, dict]
    cluster_radius: int = Field(None, serialization_alias="clusterRadius")
    cluster_min_points: int = Field(None, serialization_alias="clusterMinPoints")

    @computed_field
    @property
    def type(self) -> str:
        return SourceType.GEOJSON.value
