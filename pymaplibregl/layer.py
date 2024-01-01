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


class Layer(BaseModel):
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

    @field_validator("source")
    def validate_source(cls, v):
        if isinstance(v, Source):
            return v.to_dict()
        return v

    @field_validator("paint", "layout")
    def fix_paint(cls, v):
        if isinstance(v, dict):
            return fix_keys(v)

        return v
