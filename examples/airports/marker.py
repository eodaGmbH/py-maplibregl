import json

import pandas as pd
from pymaplibregl import (
    Layer,
    LayerType,
    Map,
    MapContext,
    MapOptions,
    output_maplibregl,
    render_maplibregl,
)
from pymaplibregl.basemaps import Carto
from pymaplibregl.controls import Marker, MarkerOptions, Popup, PopupOptions
from pymaplibregl.sources import GeoJSONSource
from pymaplibregl.utils import GeometryType, df_to_geojson
from shiny import App, reactive, ui

BOUNDS = (-8.92242886, 43.30508298, 13.76496714, 59.87668996)

airports_data = pd.read_json(
    "https://github.com/visgl/deck.gl-data/raw/master/examples/line/airports.json"
)


def get_color(airport_type: str) -> str:
    color = "darkblue"
    if airport_type == "mid":
        color = "darkred"
    elif airport_type == "major":
        color = "darkgreen"

    return color


geojson = df_to_geojson(
    airports_data,
    "coordinates",
    GeometryType.POINT,
    properties=["type", "name", "abbrev"],
)

airports_layer = Layer(
    type=LayerType.CIRCLE,
    source=GeoJSONSource(data=geojson),
    paint={
        "circle-color": [
            "match",
            ["get", "type"],
            "mid",
            "darkred",
            "major",
            "darkgreen",
            "darkblue",
        ],
        "circle_radius": 10,
        "circle-opacity": 0.3,
    },
)

app_ui = ui.page_fluid(
    ui.panel_title("Airports"),
    output_maplibregl("maplibre", height=600),
    # ui.input_slider("radius", "Radius", value=CIRCLE_RADIUS, min=1, max=5),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(
            MapOptions(style=Carto.POSITRON),
            bounds=BOUNDS,
            fitBoundsOptions={"padding": 20},
        )
        for _, r in airports_data.iterrows():
            # print(r["coordinates"], r["name"])
            marker = Marker(
                lng_lat=r["coordinates"],
                options=MarkerOptions(color=get_color(r["type"]), draggable=True),
                popup=Popup(
                    text=r["name"],
                    options=PopupOptions(close_button=False),
                ),
            )
            m.add_marker(marker)
        m.add_layer(airports_layer)
        return m

    """
    @reactive.Effect
    @reactive.event(input.radius, ignore_init=True)
    async def radius():
        async with MapContext("maplibre") as m:
            m.set_paint_property(LAYER_ID, "circle-radius", input.radius())
    """


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
