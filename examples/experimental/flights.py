import json

import pandas as pd
import shapely
from maplibre import (Layer, LayerType, Map, MapContext, output_maplibregl,
                      render_maplibregl)
from maplibre.basemaps import Carto
from maplibre.utils import GeometryType, df_to_geojson
from shiny import App, reactive, ui

"""
LAYER_ID_FLIGHTS = "flights"

flights_data = pd.read_json(
    "https://github.com/visgl/deck.gl-data/raw/master/examples/line/heathrow-flights.json"
)

flights_source = {
    "type": "geojson",
    "data": df_to_geojson(
        flights_data, ["start", "end"], GeometryType.LINE_STRING, properties=["name"]
    ),
}
"""

airports_data = pd.read_json(
    "https://github.com/visgl/deck.gl-data/raw/master/examples/line/airports.json"
)
airports_source = {
    "type": "geojson",
    "data": df_to_geojson(
        airports_data,
        "coordinates",
        GeometryType.POINT,
        properties=["type", "name", "abbrev"],
    ),
}


bbox = shapely.bounds(shapely.from_geojson(json.dumps(airports_source["data"])))
print(bbox)

"""
flights_layer = Layer(
    LayerType.LINE,
    id_=LAYER_ID_FLIGHTS,
    source=flights_source,
    paint={
        "line-color": "darkred",
    },
)
"""

airport_layer = Layer(
    LayerType.CIRCLE,
    source=airports_source,
    paint={
        "circle-color": [
            "match",
            ["get", "type"],
            "mid",
            "darkred",
            "major",
            "darkgreen",
            "darkblue",
        ]
    },
)

app_ui = ui.page_fluid(
    ui.panel_title("Flights"),
    output_maplibregl("maplibre", height=600),
    # ui.input_slider("radius", "Radius", value=CIRCLE_RADIUS, min=1, max=5),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(
            style=Carto.POSITRON,
            # center=[-73.987157, 40.729906],
            # zoom=12,
            bounds=list(bbox),
            fitBoundsOptions={"padding": 20},
        )
        # m.add_layer(flights_layer)
        m.add_layer(airport_layer)
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
