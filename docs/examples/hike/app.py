import asyncio

import geopandas as gpd
from maplibre import (
    Layer,
    LayerType,
    Map,
    MapContext,
    MapOptions,
    output_maplibregl,
    render_maplibregl,
)
from maplibre.controls import Marker
from maplibre.sources import GeoJSONSource
from shiny import App, reactive, ui

SOURCE_ID = "hike"
LAYER_ID = "hike"
data = gpd.read_file("https://docs.mapbox.com/mapbox-gl-js/assets/hike.geojson")
# print(data)
print(data.get_coordinates().to_numpy()[0])

hike = GeoJSONSource(data="https://docs.mapbox.com/mapbox-gl-js/assets/hike.geojson")
layer = Layer(
    type=LayerType.LINE,
    id=LAYER_ID,
    source="hike",
    paint={"line-color": "yellow", "line-width": 3},
)

app_ui = ui.page_fluid(
    output_maplibregl("mapylibre", height=600),
    ui.input_action_button("run", "Run"),
)


def server(input, output, session):
    @render_maplibregl
    def mapylibre():
        m = Map(
            MapOptions(bounds=data.total_bounds, fit_bounds_options={"padding": 20})
        )
        m.add_source(SOURCE_ID, hike)
        m.add_layer(layer)
        # m.add_marker(Marker(lng_lat=data.get_coordinates().to_numpy()[0]))
        return m

    @reactive.Effect
    @reactive.event(input.run)
    async def run():
        print("run")
        for lng_lat in data.get_coordinates().to_numpy():
            async with MapContext("mapylibre") as m:
                m.add_marker(Marker(lng_lat=lng_lat))
                m.add_call("setCenter", tuple(lng_lat))
            # await asyncio.sleep(2)


app = App(app_ui, server)
