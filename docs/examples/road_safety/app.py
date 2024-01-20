import webbrowser

import h3
import pandas as pd
from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.sources import GeoJSONSource
from maplibre.utils import df_to_geojson, get_bounds

RESOLUTION = 7

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

df["color"] = pd.cut(
    df["count"],
    bins=6,
    labels=("lightblue", "darkblue", "lightgreen", "yellow", "orange", "darkred"),
)

source = GeoJSONSource(
    data=df_to_geojson(
        df, "hexagon", geometry_type="Polygon", properties=["count", "color"]
    )
)
bounds = get_bounds(source.data)


def create_map() -> Map:
    m = Map(MapOptions(bounds=bounds))
    m.add_layer(
        Layer(
            id="road-safety",
            type=LayerType.FILL,
            source=source,
            paint={"fill-color": ["get", "color"], "fill-opacity": 0.5},
        )
    )
    m.add_tooltip("road-safety", "count")
    return m


filename = "/tmp/road_safety.html"
with open(filename, "w") as f:
    m = create_map()
    f.write(m.to_html())


webbrowser.open(filename)
