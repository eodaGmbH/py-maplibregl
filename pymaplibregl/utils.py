from pandas import DataFrame

"""
def _get_feature_type(lng: str = None, lat: str = None) -> str:
    if lng and lat:
        return "Point"
"""


def df_to_geojson(
    df: DataFrame, lng: str = None, lat: str = None, properties: list = None
) -> dict:
    geojson = {"type": "FeatureCollection", "features": []}
    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Point", "coordinates": []},
        }
        feature["geometry"]["coordinates"] = [row[lng], row[lat]]
        for prop in properties:
            feature["properties"][prop] = row[prop]

        geojson["features"].append(feature)

    return geojson
