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
from shiny import App, reactive, ui

SOURCE_ID = "vancouver-blocks"
LAYER_ID_LINES = "vancouver-blocks-lines"
LAYER_ID_FILL = "vancouver-blocks-fill-extrusion"
MAX_FILTER_VALUE = 1000000

vancouver_blocks_source = GeoJSONSource(
    data="https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
)

vancouver_blocks_lines = Layer(
    type=LayerType.LINE,
    id=LAYER_ID_LINES,
    source=SOURCE_ID,
    paint={
        "line-color": "white",
        "line-width": 2,
    },
)

vancouver_blocks_fill = Layer(
    type=LayerType.FILL_EXTRUSION,
    id=LAYER_ID_FILL,
    source=SOURCE_ID,
    paint={
        "fill-extrusion-color": {
            "property": "valuePerSqm",
            "stops": [
                [0, "grey"],
                [1000, "yellow"],
                [5000, "orange"],
                [10000, "red"],
                [50000, "darkred"],
            ],
        },
        "fill-extrusion-height": ["*", 10, ["sqrt", ["get", "valuePerSqm"]]],
        "fill-extrusion-opacity": 0.9,
    },
)

map_options = MapOptions(
    style=Carto.DARK_MATTER,
    center=(-123.13, 49.254),
    zoom=11,
    pitch=45,
    bearing=0,
)

app_ui = ui.page_fluid(
    ui.panel_title("Vancouver Property Value"),
    ui.div(
        "Height of polygons - average property value per square meter of lot",
        style="padding: 10px;",
    ),
    output_maplibregl("maplibre", height=700),
    ui.input_select(
        "filter",
        "max property value per square meter",
        choices=[0, 1000, 5000, 10000, 50000, 100000, MAX_FILTER_VALUE],
        selected=MAX_FILTER_VALUE,
    ),
)


def server(input, output, session):
    @render_maplibregl
    def maplibre():
        m = Map(map_options)
        m.add_control(ScaleControl(), position="bottom-left")
        m.add_source(SOURCE_ID, vancouver_blocks_source)
        m.add_layer(vancouver_blocks_lines)
        m.add_layer(vancouver_blocks_fill)
        m.add_tooltip(LAYER_ID_FILL, "valuePerSqm")
        return m

    @reactive.Effect
    @reactive.event(input.filter)
    async def filter():
        async with MapContext("maplibre") as m:
            filter_ = ["<=", ["get", "valuePerSqm"], int(input.filter())]
            m.set_filter(LAYER_ID_FILL, filter_)


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
