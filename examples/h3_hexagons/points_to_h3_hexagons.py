import json

import h3
import shapely
from pandas import read_csv
from pymaplibregl.utils import df_to_geojson

df = read_csv(
    "https://github.com/crazycapivara/mapboxer/raw/master/data-raw/motor_vehicle_collisions.csv",
    sep=";",
)

df["h3_index"] = df.apply(
    lambda x: h3.geo_to_h3(x["lat"], x["lng"], resolution=7), axis=1
)

df_aggr = (
    df[["h3_index", "injured", "killed"]].groupby("h3_index", as_index=False).sum()
)
df_aggr["hexagon"] = df_aggr.apply(
    lambda x: [list(h3.h3_to_geo_boundary(x["h3_index"], geo_json=True))], axis=1
)
# df_aggr.apply(lambda x: h3.h3_to_geo_boundary(x["h3_index"]), axis=1)

print(df_aggr.head())
geojson = df_to_geojson(df_aggr.head(), "hexagon", "Polygon")
print(geojson)
print(json.dumps(geojson))
shapely.from_geojson(json.dumps(geojson))

import requests

d = requests.get(
    "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
).json()
# print(d)
