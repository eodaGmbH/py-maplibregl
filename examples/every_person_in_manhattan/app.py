import json

import pandas as pd
import shapely
from pymaplibregl import (
    Layer,
    LayerType,
    Map,
    MapContext,
    output_maplibregl,
    render_maplibregl,
)
from pymaplibregl.basemaps import Carto
from pymaplibregl.utils import df_to_geojson
from shiny import App, reactive, ui

MALE_COLOR = "rgb(0, 128, 255)"
FEMALE_COLOR = "rgb(255, 0, 128)"
LAYER_ID = "every-person-in-manhattan"
CIRCLE_RADIUS = 2

point_data = pd.read_json(
    "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/scatterplot/manhattan.json"
)
point_data.columns = ["lng", "lat", "sex"]

every_person_in_manhattan_source = {
    "type": "geojson",
    "data": df_to_geojson(point_data, lng="lng", lat="lat", properties=["sex"]),
}

bbox = shapely.bounds(
    shapely.from_geojson(json.dumps(every_person_in_manhattan_source["data"]))
)
print(bbox)

every_person_in_manhattan_layer = Layer(
    LayerType.CIRCLE,
    id_=LAYER_ID,
    source=every_person_in_manhattan_source,
    paint={
        "circle-color": ["match", ["get", "sex"], 1, MALE_COLOR, FEMALE_COLOR],
        "circle-radius": CIRCLE_RADIUS,
    },
)

app_ui = ui.page_fluid(
    ui.panel_title("Every Person in Manhattan"),
    output_maplibregl("maplibre", height=600),
    ui.input_slider("radius", "Radius", value=CIRCLE_RADIUS, min=1, max=5),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(
            style=Carto.POSITRON,
            # center=[-73.987157, 40.729906], zoom=12
            bounds=list(bbox),
            fitBoundsOptions={"padding": 20},
        )
        m.add_layer(every_person_in_manhattan_layer)
        return m

    @reactive.Effect
    @reactive.event(input.radius, ignore_init=True)
    async def radius():
        async with MapContext("maplibre") as m:
            m.set_paint_property(LAYER_ID, "circle-radius", input.radius())


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
