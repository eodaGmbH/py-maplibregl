from __future__ import annotations

from enum import Enum

try:
    from pandas import DataFrame
except:
    print("pandas is not installed")


class GeometryType(str, Enum):
    POINT = "Point"
    LINE_STRING = "LineString"
    POLYGON = "Polygon"


def df_to_geojson(
    df: DataFrame,
    coordinates: str | list = ["lng", "lat"],
    geometry_type: str | GeometryType = GeometryType.POINT,
    properties: list = None,
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
