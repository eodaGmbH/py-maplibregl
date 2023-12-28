from __future__ import annotations

from enum import Enum


class SourceType(Enum):
    RASTER = "raster"
    VECTOR = "vector"
    RASTER_DEM = "raster-dem"
    GEOJSON = "geojson"
    IMAGE = "image"
    VIDEO = "video"
