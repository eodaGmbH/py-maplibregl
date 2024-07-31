from __future__ import annotations

from typing import Literal

from geopandas import GeoDataFrame
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    field_validator,
    model_serializer,
)

from maplibre import Layer, LayerType
from maplibre.utils import geopandas_to_geojson


class LineLayer(Layer):
    def __init__(self, source: [dict | str], id_: str = None, *args, **kwargs):
        super().__init__(LayerType.LINE, source=source, id_=id_, *args, **kwargs)


class PydanticSer(BaseModel):
    a: int = Field(..., serialization_alias="aa")
    b: int

    # @model_serializer
    def to_dict(self):
        return self.model_dump() | {"type": self.__class__.__name__}

    # @model_serializer
    def model_dump(self):
        return super().model_dump(by_alias=True) | {"type": self.__class__.__name__}


class LayoutProperties(BaseModel):
    visibility: Literal["visible", "none"] = None
    #
    fill_sort_key: list = None  # Example: ["get", "priority"]
    #
    line_cap: Literal["butt", "round", "square"] = None
    line_join: Literal["bevel", "round", "miter"] = None
    line_miter_limit: int = None
    line_round_limit: float = None
    line_sort_key: int = None


class PaintProperties(BaseModel):
    background_color: str = None
    background_emissive_strength: int = None
    background_opacity: int = None
    background_pattern: str = None


class GeoJSONifyable(object):
    def color(self, column: str):
        pass

    def color_quantile(self, column: str, q: list):
        pass

    def color_bins(self, column: str, n: int):
        pass

    def color_steps(self, column: str, steps: list):
        pass


class FeaturesCollection(object):
    def __init__(self, data):
        self._data = data

    def color(
        self,
        column: str,
        n: int = None,
        q: list = None,
        steps: list = None,
        cmap: str = None,
    ):
        return self

    def to_source(self):
        pass

    def fill(self, **kwargs):
        pass

    def line(self):
        pass


# FeaturesCollection("data").color("STATE").fill()

from typing import TypeVar, Union

from geopandas import GeoDataFrame

PandasGeoDataFrame = TypeVar("geopandas.GeoDataFrame")


class LineLayer(Layer):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: Union[dict, GeoDataFrame]

    @field_validator("data")
    def data_validator(cls, v):
        if isinstance(v, GeoDataFrame):
            return geopandas_to_geojson(v)

        return v


def _create_layer_props(layer_type: str, props: dict) -> dict:
    return {f"{layer_type}-{k}": v for k, v in props.items() if v is not None}
