from __future__ import annotations

from enum import Enum
from typing import Optional, Union
from uuid import uuid4

from pydantic import Field, computed_field, field_validator

from ._core import MapLibreBaseModel
from .utils import geopandas_to_geojson

try:
    from geopandas import GeoDataFrame, read_file
except ImportError:
    GeoDataFrame, read_file = None, None

CRS = "EPSG:4326"


class SourceType(Enum):
    """Source types"""

    RASTER = "raster"
    VECTOR = "vector"
    RASTER_DEM = "raster-dem"
    GEOJSON = "geojson"
    IMAGE = "image"
    VIDEO = "video"


class Source(MapLibreBaseModel):
    pass


class GeoJSONSource(Source):
    """GeoJSON Source

    Examples:
        >>> from maplibre.sources import GeoJSONSource

        >>> geojson = "https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson"
        >>> source = GeoJSONSource(data=geojson)
    """

    data: Union[str, dict]
    attribution: Optional[str] = None
    buffer: Optional[int] = None
    cluster: Optional[bool] = None
    cluster_max_zoom: Optional[int] = Field(None, serialization_alias="clusterMaxZoom")
    cluster_min_points: Optional[int] = Field(
        None, serialization_alias="clusterMinPoints"
    )
    cluster_properties: Optional[dict] = Field(
        None, serialization_alias="clusterProperties"
    )
    cluster_radius: Optional[int] = Field(None, serialization_alias="clusterRadius")
    filter: Optional[list] = None
    generate_id: Optional[bool] = Field(None, serialization_alias="generateId")
    line_metrics: Optional[bool] = Field(None, serialization_alias="lineMetrics")
    min_zoom: Optional[int] = Field(None, serialization_alias="minzoom")
    max_zoom: Optional[int] = Field(None, serialization_alias="maxzoom")
    promote_id: Union[str, dict, None] = Field(None, serialization_alias="promoteId")
    tolerance: Optional[float] = None

    @computed_field
    @property
    def type(self) -> str:
        return SourceType.GEOJSON.value


class RasterTileSource(Source):
    """Raster tile source

    Examples:
        >>> from maplibre.sources import RasterTileSource

        >>> raster_tile_source = RasterTileSource(
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


class VectorTileSource(Source):
    """Vector tile source

    Examples:
        >>> from maplibre.sources import VectorTileSource
        >>> from maplibre import LayerType, Layer

        >>> vector_tile_source = VectorTileSource(
        ...     tiles=["https://demotiles.maplibre.org/tiles/{z}/{x}/{y}.pbf"],
        ...     min_zoom=0,
        ...     max_zoom=6,
        ... )

        >>> layer = Layer(
        ...     type=LayerType.LINE,
        ...     id="countries",
        ...     source=vector_tile_source,
        ...     source_layer="countries",
        ...     paint={"fill-color": "lightgreen", "fill-outline-color": "black"},
        ... )
    """

    attribution: str = None
    bounds: tuple = None
    max_zoom: int = Field(None, serialization_alias="maxzoom")
    min_zoom: int = Field(None, serialization_alias="minzoom")
    scheme: str = None
    tiles: Union[tuple, list] = None
    url: str = None
    volatile: bool = None

    @computed_field
    @property
    def type(self) -> str:
        return SourceType.VECTOR.value


class SimpleFeatures(object):
    def __init__(self, data: GeoDataFrame | str, source_id: str = None):
        self._path = data if isinstance(data, str) else None
        if self._path is not None:
            data = read_file(self._path)

        if str(data.crs) != CRS:
            data = data.to_crs(CRS)

        self._data = data
        self._source_id = source_id or str(uuid4())

    @property
    def path(self):
        return self._path

    @property
    def crs(self):
        return self._data.crs

    @property
    def bounds(self) -> tuple:
        return self._data.total_bounds

    @property
    def source_id(self) -> str:
        return self._source_id

    @property
    def data(self) -> GeoDataFrame:
        return self._data

    def to_source(self, **kwargs) -> GeoJSONSource:
        kwargs["data"] = geopandas_to_geojson(self._data)
        return GeoJSONSource(**kwargs)

    def to_sources_dict(self, **kwargs) -> dict:
        return {self.source_id: self.to_source(**kwargs)}
