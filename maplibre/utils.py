from __future__ import annotations

import json
import webbrowser
from enum import Enum

from ._utils import get_temp_filename
from .map import Map

try:
    from pandas import DataFrame
except ImportError:
    DataFrame = None


try:
    from geopandas import GeoDataFrame
except ImportError:
    GeoDataFrame = None


class GeometryType(str, Enum):
    POINT = "Point"
    LINE_STRING = "LineString"
    POLYGON = "Polygon"


def geopandas_to_geojson(df: GeoDataFrame) -> dict:
    return json.loads(df.to_json())


def df_to_geojson(
    df: DataFrame,
    coordinates: str | list = ["lng", "lat"],
    geometry_type: str | GeometryType = GeometryType.POINT,
    properties: list = [],
) -> dict:
    geojson = {"type": "FeatureCollection", "features": []}
    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": GeometryType(geometry_type).value, "coordinates": []},
        }
        feature["geometry"]["coordinates"] = list(row[coordinates])
        for prop in properties:
            feature["properties"][prop] = row[prop]

        geojson["features"].append(feature)

    return geojson


def get_bounds(geojson: dict) -> list:
    try:
        import shapely
    except ImportError:
        print("shapely is not installed")
        return

    return list(shapely.bounds(shapely.from_geojson(json.dumps(geojson))))


def save_map(map: Map, filename: str = None, preview=True, **kwargs) -> str:
    if not filename:
        filename = get_temp_filename()

    with open(filename, "w") as f:
        f.write(map.to_html(**kwargs))

    if preview:
        webbrowser.open(filename)

    return filename
