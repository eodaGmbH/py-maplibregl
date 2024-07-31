# from __future__ import annotations

from typing import Union

from geopandas import GeoDataFrame, read_file
from maplibre.layer import Layer
from maplibre.sources import GeoJSONSource
from maplibre.utils import geopandas_to_geojson

# from pandas import DataFrame
from pydantic import ConfigDict, field_validator


class BaseLayer(Layer):
    data: Union[GeoDataFrame, str]
    color: str = None
    cmap: str = "viridis"
    n: int = None
    q: int = None
    breaks: list = None

    @field_validator("data")
    def validate_data(cls, v):
        if isinstance(v, str):
            return read_file(v)

        return v

    @property
    def bounds(self):
        return self.data.total_bounds

    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True, exclude={"data"}) | {
            "source": GeoJSONSource(data=geopandas_to_geojson(self.data))
        }
