from __future__ import annotations

from enum import Enum
from typing import Union
from uuid import uuid4

from pydantic import Field, field_validator

from ._utils import BaseModel, fix_keys
from .sources import Source


class LayerType(str, Enum):
    CIRCLE = "circle"
    FILL = "fill"
    FILL_EXTRUSION = "fill-extrusion"
    LINE = "line"
    SYMBOL = "symbol"
    RASTER = "raster"
    HEATMAP = "heatmap"
    HILLSHADE = "hillshade"
    BACKGROUND = "background"


class Layer(object):
    def __init__(
        self,
        type_: [str | LayerType],
        source: [str | Source | dict],
        id_: str = None,
        paint: dict = {},
        layout: dict = {},
        **kwargs,
    ):
        if isinstance(source, Source):
            source = source.to_dict()
        self._data = {
            "id": id_ or str(uuid4()),
            "type": type_,
            "source": source,
            "paint": paint,
            "layout": layout,
        }
        # kwargs = fix_keys(kwargs)
        self._data.update(kwargs)
        self._data["type"] = LayerType(self._data["type"]).value
        self._data = fix_keys(self._data)
        for k in self._data.keys():
            if k in ["paint", "layout"]:
                self.data[k] = fix_keys(self._data[k])

    @property
    def data(self) -> dict:
        return self._data

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def id(self) -> str:
        return self._data["id"]


class LayerModel(BaseModel):
    id: str = str(uuid4())
    type: LayerType
    filter: list = None
    layout: dict = None
    max_zoom: int = Field(None, serialization_alias="maxzoom")
    metadata: dict = None
    min_zoom: int = Field(None, serialization_alias="minzoom")
    paint: dict = None
    source: Union[str, Source, dict] = None
    source_layer: str = Field(None, serialization_alias="source-layer")

    @field_validator("paint", "layout")
    # @classmethod
    def fix_paint(cls, v):
        if isinstance(v, dict):
            v = fix_keys(v)

        return v
