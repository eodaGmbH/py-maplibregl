from __future__ import annotations

from enum import Enum
from typing import Optional, Union
from uuid import uuid4

from pydantic import Field, field_validator

from ._utils import BaseModel, fix_keys
from .sources import Source


class LayerType(Enum):
    """Rendering type of layer

    Attributes:
        CIRCLE: A filled circle.
        FILL: A filled polygon with an optional stroked border.
        FILL_EXTRUSION: An extruded polygon.
        LINE: A stroked line.
        SYMBOL: An icon or a text label.
        RASTER: Raster map textures such as satellite imagery.
        HEATMAP: A heatmap.
        HILLSHADE: A Client-side hillshading visualization based on DEM data.
        BACKGROUND: A background color or pattern.
    """

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
    """Layer properties

    Notes:
        See [layers](https://maplibre.org/maplibre-style-spec/layers/) for more details on the
        `paint` and `layout` properties of the layers.

    Attributes:
        id (str): **Required.** The unique ID of the layer. Defaults to `str(uuid4())`.
        type (str | LayerType): **Required.** The type of the layer.
        filter (list): The filter expression that is applied to the source of the layer.
        layout (dict): The layout properties of the layer.
        max_zoom (int): The maximum zoom level for the layer.
        min_zoom (int): The minimum zoom level for the layer.
        paint (dict): The paint properties of the layer.
        source (str | Source): The name (unique ID) of a source or a source object to be used for the layer.
        source_layer (str): The layer to use from a vector tile source.

    Examples:
        >>> from maplibre.layer import Layer, LayerType

        >>> layer = Layer(id="test-layer", type=LayerType.CIRCLE, source="test-source")
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    type: LayerType
    filter: list = None
    layout: dict = None
    max_zoom: int = Field(None, serialization_alias="maxzoom")
    metadata: dict = None
    min_zoom: int = Field(None, serialization_alias="minzoom")
    paint: dict = None
    source: Union[str, Source, dict, None] = None
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
