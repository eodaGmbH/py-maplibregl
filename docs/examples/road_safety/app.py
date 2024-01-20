import webbrowser

import h3
import pandas as pd
from maplibre import Layer, Map, MapOptions
from maplibre.sources import GeoJSONSource
from maplibre.utils import df_to_geojson, get_bounds

RESOLUTION = 5

road_safety = pd.read_csv(
    "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv"
).dropna()

road_safety["h3"] = road_safety.apply(
    lambda x: h3.geo_to_h3(x["lat"], x["lng"], resolution=RESOLUTION), axis=1
)

df = road_safety.groupby("h3").h3.agg("count").to_frame("count").reset_index()

df["hexagon"] = df.apply(
    lambda x: [h3.h3_to_geo_boundary(x["h3"], geo_json=True)], axis=1
)

source = GeoJSONSource(
    data=df_to_geojson(df, "hexagon", geometry_type="Polygon", properties=["count"])
)
bounds = get_bounds(source.data)

m = Map(MapOptions(bounds=bounds))
m.add_layer(
    Layer(id="road-safety", type="line", source=source, paint={"line-color": "yellow"})
)
m.add_tooltip("road-safety", "count")

filename = "/tmp/road_safety.html"
with open(filename, "w") as f:
    f.write(m.to_html())


webbrowser.open(filename)
