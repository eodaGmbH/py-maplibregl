import json
import sys

import pandas as pd
import shapely
from maplibre import (
    Layer,
    LayerType,
    Map,
    MapContext,
    MapOptions,
    output_maplibregl,
    render_maplibregl,
)
from maplibre.basemaps import Carto
from maplibre.controls import ScaleControl
from maplibre.sources import GeoJSONSource
from maplibre.ui import use_deckgl
from maplibre.utils import df_to_geojson
from shiny import App, reactive, ui

MALE_COLOR = "rgb(0, 128, 255)"
FEMALE_COLOR = "rgb(255, 0, 128)"
LAYER_ID = "every-person-in-manhattan-circles"
CIRCLE_RADIUS = 2

point_data = pd.read_json(
    "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/scatterplot/manhattan.json"
)

point_data.columns = ["lng", "lat", "sex"]

every_person_in_manhattan_source = GeoJSONSource(
    data=df_to_geojson(point_data, properties=["sex"]),
)

bbox = shapely.bounds(
    shapely.from_geojson(json.dumps(every_person_in_manhattan_source.data))
)

every_person_in_manhattan_circles = Layer(
    type=LayerType.CIRCLE,
    id=LAYER_ID,
    source=every_person_in_manhattan_source,
    paint={
        "circle-color": ["match", ["get", "sex"], 1, MALE_COLOR, FEMALE_COLOR],
        "circle-radius": CIRCLE_RADIUS,
    },
)

map_options = MapOptions(
    style=Carto.POSITRON,
    bounds=tuple(bbox),
    fit_bounds_options={"padding": 20},
    hash=True,
)


def create_map() -> Map:
    m = Map(map_options)
    m.add_control(ScaleControl(), position="bottom-left")
    m.add_layer(every_person_in_manhattan_circles)
    return m


app_ui = ui.page_fluid(
    use_deckgl(),
    ui.panel_title("Every Person in Manhattan"),
    output_maplibregl("maplibre", height=600),
    ui.input_slider("radius", "Radius", value=CIRCLE_RADIUS, min=1, max=5),
)


def server(input, output, session):
    @render_maplibregl
    def maplibre():
        return create_map()

    @reactive.Effect
    @reactive.event(input.radius, ignore_init=True)
    async def radius():
        async with MapContext("maplibre") as m:
            m.set_paint_property(LAYER_ID, "circle-radius", input.radius())


app = App(app_ui, server)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        with open(file_name, "w") as f:
            f.write(create_map().to_html())
    else:
        app.run()
