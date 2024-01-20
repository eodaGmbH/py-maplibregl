import webbrowser

import h3
import pandas as pd
from maplibre import (
    Layer,
    LayerType,
    Map,
    MapContext,
    MapOptions,
    output_maplibregl,
    render_maplibregl,
)
from maplibre.sources import GeoJSONSource
from maplibre.utils import df_to_geojson
from shiny import App, reactive, ui

RESOLUTION = 6
COLORS = (
    "lightblue",
    "turquoise",
    "lightgreen",
    "yellow",
    "orange",
    "darkred",
)

road_safety = pd.read_csv(
    "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv"
).dropna()


def create_h3_grid(res=RESOLUTION) -> dict:
    road_safety["h3"] = road_safety.apply(
        lambda x: h3.geo_to_h3(x["lat"], x["lng"], resolution=res), axis=1
    )
    df = road_safety.groupby("h3").h3.agg("count").to_frame("count").reset_index()
    df["hexagon"] = df.apply(
        lambda x: [h3.h3_to_geo_boundary(x["h3"], geo_json=True)], axis=1
    )
    df["color"] = pd.cut(
        df["count"],
        bins=len(COLORS),
        labels=COLORS,
    )
    return df_to_geojson(
        df, "hexagon", geometry_type="Polygon", properties=["count", "color"]
    )


geojson = create_h3_grid()
source = GeoJSONSource(data=geojson)


def create_map() -> Map:
    m = Map(MapOptions(center=(-1.415727, 52.232395), zoom=7, pitch=40, bearing=-27))
    m.add_layer(
        Layer(
            id="road-safety",
            type=LayerType.FILL_EXTRUSION,
            source=source,
            paint={
                "fill-extrusion-color": ["get", "color"],
                "fill-extrusion-opacity": 0.7,
                "fill-extrusion-height": ["*", 100, ["get", "count"]],
            },
        )
    )
    m.add_tooltip("road-safety", "count")
    return m


app_ui = ui.page_fluid(
    ui.panel_title("Road safety in UK"),
    output_maplibregl("mapylibre", height=700),
    ui.input_slider("res", "Resolution", min=4, max=8, step=1, value=RESOLUTION),
)


def server(input, output, session):
    @render_maplibregl
    def mapylibre():
        return create_map()

    @reactive.Effect
    @reactive.event(input.res, ignore_init=True)
    async def resolution():
        async with MapContext("mapylibre", session=session) as m:
            with ui.Progress() as p:
                p.set(message="H3 calculation in progress")
                geojson = create_h3_grid(input.res())
                m.set_data("road-safety", geojson)
                p.set(1, message="Calculation finished")


app = App(app_ui, server)

if __name__ == "__main__":
    filename = "/tmp/road_safety.html"
    with open(filename, "w") as f:
        m = create_map()
        f.write(m.to_html())

    webbrowser.open(filename)
