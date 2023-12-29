import pandas as pd
from pymaplibregl import Layer, LayerType, Map, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import Carto
from pymaplibregl.utils import df_to_geojson
from shiny import App, ui

MALE_COLOR = "rgb(0, 128, 255)"
FEMALE_COLOR = "rgb(255, 0, 128)"

point_data = pd.read_json(
    "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/scatterplot/manhattan.json"
)
point_data.columns = ["lng", "lat", "sex"]
every_person_in_manhattan_source = {
    "type": "geojson",
    "data": df_to_geojson(point_data, lng="lng", lat="lat", properties=["sex"]),
}

every_person_in_manhattan_layer = Layer(
    LayerType.CIRCLE,
    id_="every-person-in-manhattan",
    source=every_person_in_manhattan_source,
    paint={
        "circle-color": ["match", ["get", "sex"], 1, MALE_COLOR, FEMALE_COLOR],
        "circle-radius": 2,
    },
)

center = [-118.0931, 33.78615]

app_ui = ui.page_fluid(
    ui.panel_title("Every Person in Manhattan"),
    output_maplibregl("maplibre", height=600),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(style=Carto.POSITRON, center=[-73.987157, 40.729906], zoom=12)
        m.add_layer(every_person_in_manhattan_layer)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
