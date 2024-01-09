from __future__ import annotations

from enum import Enum
from typing import Union

from pydantic import ConfigDict, Field, computed_field

from ._utils import BaseModel


class SourceType(Enum):
    """Source types"""

    RASTER = "raster"
    VECTOR = "vector"
    RASTER_DEM = "raster-dem"
    GEOJSON = "geojson"
    IMAGE = "image"
    VIDEO = "video"


class Source(BaseModel):
    pass
    # model_config = ConfigDict(validate_assignment=True, extra="forbid")

    """
    def model_dump(self):
        return super().model_dump(exclude_none=True, by_alias=True)
    """


class GeoJSONSource(Source):
    """GeoJSON Source

    Examples:
        >>> from maplibre.sources import GeoJSONSource

        >>> source = GeoJSONSource(data="https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson")
    """

    data: Union[str, dict]
    attribution: str = None
    buffer: int = None
    cluster: bool = None
    cluster_max_zoom: int = Field(None, serialization_alias="clusterMaxZoom")
    cluster_min_points: int = Field(None, serialization_alias="clusterMinPoints")
    cluster_properties: dict = Field(None, serialization_alias="clusterProperties")
    cluster_radius: int = Field(None, serialization_alias="clusterRadius")
    filter: list = None
    generate_id: bool = Field(None, serialization_alias="generateId")
    line_metrics: bool = Field(None, serialization_alias="lineMetrics")
    maxzoom: int = None
    promote_id: Union[str, dict] = Field(None, serialization_alias="promoteId")
    tolerance: float = None

    @computed_field
    @property
    def type(self) -> str:
        return SourceType.GEOJSON.value


class RasterTileSource(Source):
    """Raster tile source

    Examples:
        >>> from maplibre.sources import RasterTileSource
        >>> raster_source = RasterTileSource(
        ...     tiles=["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
        ...     tile_size=256,
        ...     min_zoom=0,
        ...     max_zoom=19,
        ... )
    """

    attribution: str = None
    bounds: tuple = None
    max_zoom: int = Field(None, serialization_alias="maxzoom")
    min_zoom: int = Field(None, serialization_alias="minzoom")
    scheme: str = None
    tile_size: int = Field(None, serialization_alias="tileSize")
    tiles: Union[tuple, list] = None
    url: str = None
    volatile: bool = None

    @computed_field
    @property
    def type(self) -> str:
        return SourceType.RASTER.value
