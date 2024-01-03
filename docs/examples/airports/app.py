import pandas as pd
from pymaplibregl import (
    Layer,
    LayerType,
    Map,
    MapOptions,
    output_maplibregl,
    render_maplibregl,
)
from pymaplibregl.basemaps import Carto
from pymaplibregl.controls import Marker, MarkerOptions, Popup, PopupOptions
from pymaplibregl.sources import GeoJSONSource
from pymaplibregl.utils import GeometryType, df_to_geojson
from shiny import App, ui

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

airport_circles = Layer(
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

map_options = MapOptions(
    style=Carto.POSITRON,
    bounds=BOUNDS,
    fit_bounds_options={"padding": 20},
    hash=True,
)

popup_options = PopupOptions(close_button=False)

app_ui = ui.page_fluid(
    ui.panel_title("Airports"),
    output_maplibregl("maplibre", height=600),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(map_options)
        for _, r in airports_data.iterrows():
            marker = Marker(
                lng_lat=r["coordinates"],
                options=MarkerOptions(color=get_color(r["type"])),
                popup=Popup(
                    text=r["name"],
                    options=popup_options,
                ),
            )
            m.add_marker(marker)
        m.add_layer(airport_circles)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
