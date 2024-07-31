from __future__ import annotations

from enum import Enum
from typing import Optional, Union
from uuid import uuid4

from pydantic import Field, field_validator

from ._core import MapLibreBaseModel
from ._utils import fix_keys
from .sources import SimpleFeatures, Source
from .utils import get_bounds

try:
    from geopandas import GeoDataFrame
except ImportError:
    GeoDataFrame = None


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


class Layer(MapLibreBaseModel):
    """Layer properties

    Notes:
        See [layers](https://maplibre.org/maplibre-style-spec/layers/) for more details on the
        `paint` and `layout` properties of the layers.

    Attributes:
        id (str): **Required.** The unique ID of the layer. Defaults to `str(uuid4())`.
        type (str | LayerType): **Required.** The type of the layer.
        filter (list): A filter expression that is applied to the source of the layer.
        layout (dict): The layout properties for the layer.
        max_zoom (int): The maximum zoom level for the layer.
        min_zoom (int): The minimum zoom level for the layer.
        paint (dict): The paint properties for the layer.
        source (str | Source | GeoDataFrame): The name (unique ID) of a source, a source object or a GeoDataFrame
            to be used for the layer.
        source_layer (str): The layer to use from a vector tile source.

    Examples:
        >>> from maplibre.layer import Layer, LayerType

        >>> layer = Layer(id="test-layer", type=LayerType.CIRCLE, source="test-source")
    """

    id: Optional[str] = Field(default_factory=lambda: str(uuid4()))
    type: LayerType
    filter: Optional[list] = None
    layout: Optional[dict] = None
    max_zoom: Optional[int] = Field(None, serialization_alias="maxzoom")
    metadata: Optional[dict] = None
    min_zoom: Optional[int] = Field(None, serialization_alias="minzoom")
    paint: Optional[dict] = None
    source: Union[str, Source, dict, GeoDataFrame, None] = None
    source_layer: Optional[str] = Field(None, serialization_alias="source-layer")

    @field_validator("source")
    def validate_source(cls, v):
        if GeoDataFrame is not None and isinstance(v, GeoDataFrame):
            return SimpleFeatures(v).to_source().to_dict()

        if isinstance(v, Source):
            return v.to_dict()

        return v

    @field_validator("paint", "layout")
    def fix_paint(cls, v):
        if isinstance(v, dict):
            return fix_keys(v)

        return v

    @property
    def bounds(self) -> tuple | None:
        try:
            bounds = get_bounds(self.source["data"])
        except Exception as e:
            # print(e)
            bounds = None

        return bounds

    def set_paint_props(self, **props) -> Layer:
        if self.paint is None:
            self.paint = dict()

        self.paint = self.paint | fix_keys(props)
        return self

    def set_layout_props(self, **props) -> Layer:
        if self.layout is None:
            self.layout = dict()

        self.paint = self.paint | fix_keys(props)
        return self
