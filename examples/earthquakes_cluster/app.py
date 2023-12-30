from pymaplibregl import Layer, Map, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import Carto
from pymaplibregl.sources import GeoJSONSource
from shiny import App, reactive, ui

SOURCE_ID = "earthquakes"
LAYER_ID = "earthquakes"

earthquakes_source = GeoJSONSource(
    data="https://raw.githubusercontent.com/crazycapivara/mapboxer/master/data-raw/earthquakes.geojson",
    cluster=True,
    cluster_radius=50,
    cluster_min_points=2,
    cluster_max_zoom=14,
)

circle_layer = Layer(
    "circle",
    id_=LAYER_ID,
    source=SOURCE_ID,
    filter=["has", "point_count"],
    paint={
        "circle-color": "darkred",
        "circle-radius": [
            "step",
            ["get", "point_count"],
            10,
            50,
            15,
            100,
            20,
            200,
            25,
            300,
            30,
            400,
            40,
        ],
    },
)

circle_layer_ = Layer(
    "circle",
    source=SOURCE_ID,
    paint={"circle-color": "darkblue"},
    filter=["!", ["has", "point_count"]],
)

center = [-118.0931, 33.78615]

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("maplibre", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(style=Carto.POSITRON, center=center, zoom=5)
        m.add_source(SOURCE_ID, earthquakes_source)
        m.add_layer(circle_layer)
        m.add_popup(LAYER_ID, "point_count")
        m.add_layer(circle_layer_)
        return m

    @reactive.Effect
    @reactive.event(input.maplibre)
    async def result():
        print(f"result: {input.maplibre()}")


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
