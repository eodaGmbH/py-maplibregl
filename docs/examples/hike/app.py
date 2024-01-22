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
# print(data.get_coordinates().to_numpy()[0])


feature_collection = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "geometry": {"type": "LineString", "coordinates": []}}
    ],
}
print(feature_collection)

hike = GeoJSONSource(data="https://docs.mapbox.com/mapbox-gl-js/assets/hike.geojson")
layer = Layer(
    type=LayerType.LINE,
    id=LAYER_ID,
    source="hike",
    paint={"line-color": "orange", "line-width": 3},
    layout={"visibility": "visible"},
)

app_ui = ui.page_fluid(
    output_maplibregl("mapylibre", height=600),
    ui.input_action_button("run", "Run"),
)


def server(input, output, session):
    @render_maplibregl
    def mapylibre():
        m = Map(
            # MapOptions(center=data.get_coordinates().to_numpy()[0], zoom=16, pitch=30)
            MapOptions(bounds=data.total_bounds, fit_bounds_options={"padding": 10})
        )
        m.add_source(SOURCE_ID, hike)
        m.add_layer(layer)
        m.add_source("hike-animation", GeoJSONSource(data=feature_collection))
        m.add_layer(
            Layer(
                type=LayerType.LINE,
                id="hike-animation",
                source="hike-animation",
                paint={"line-color": "yellow", "line-width": 5},
            )
        )
        return m

    @reactive.Effect
    @reactive.event(input.run)
    async def run():
        for lng_lat in data.get_coordinates().to_numpy():
            # print(lng_lat)
            feature_collection["features"][0]["geometry"]["coordinates"].append(
                tuple(lng_lat)
            )
            async with MapContext("mapylibre") as m:
                m.set_data("hike-animation", feature_collection)
                m.add_call("panTo", tuple(lng_lat))
            # await asyncio.sleep(0.005)

        feature_collection["features"][0]["geometry"]["coordinates"] = []


app = App(app_ui, server)
