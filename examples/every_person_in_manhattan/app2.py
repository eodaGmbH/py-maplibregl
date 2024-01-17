import geopandas as gpd
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
from maplibre.basemaps import Carto
from maplibre.controls import ScaleControl
from maplibre.sources import GeoJSONSource
from maplibre.utils import geopandas_to_geojson
from shiny import App, reactive, ui

MALE_COLOR = "rgb(0, 128, 255)"
FEMALE_COLOR = "rgb(255, 0, 128)"
LAYER_ID = "every-person-in-manhattan-circles"
CIRCLE_RADIUS = 2

point_data = pd.read_json(
    "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/scatterplot/manhattan.json"
)

point_data.columns = ["lng", "lat", "sex"]

point_data = gpd.GeoDataFrame(
    point_data["sex"], geometry=gpd.points_from_xy(point_data.lng, point_data.lat)
)

every_person_in_manhattan_source = GeoJSONSource(data=geopandas_to_geojson(point_data))


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
    bounds=point_data.total_bounds,
    fit_bounds_options={"padding": 20},
)

app_ui = ui.page_fluid(
    ui.panel_title("Every Person in Manhattan"),
    output_maplibregl("maplibre", height=600),
    ui.input_slider("radius", "Radius", value=CIRCLE_RADIUS, min=1, max=5),
)


def server(input, output, session):
    @render_maplibregl
    def maplibre():
        m = Map(map_options)
        m.add_control(ScaleControl(), position="bottom-left")
        m.add_layer(every_person_in_manhattan_circles)
        return m

    @reactive.Effect
    @reactive.event(input.radius, ignore_init=True)
    async def radius():
        async with MapContext("maplibre") as m:
            m.set_paint_property(LAYER_ID, "circle-radius", input.radius())


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
