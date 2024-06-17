import sys

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
from maplibre.controls import NavigationControl, ScaleControl
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
                [10000, "darkred"],
                [50000, "lightblue"],
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


def create_map() -> Map:
    m = Map(map_options)
    m.add_control(NavigationControl())
    m.add_control(ScaleControl(), position="bottom-left")
    m.add_source(SOURCE_ID, vancouver_blocks_source)
    m.add_layer(vancouver_blocks_lines)
    m.add_layer(vancouver_blocks_fill)
    m.add_tooltip(LAYER_ID_FILL, "valuePerSqm")
    return m


app_ui = ui.page_fluid(
    ui.panel_title("Vancouver Property Value"),
    ui.div(
        "Height of polygons - average property value per square meter of lot",
        style="padding: 10px;",
    ),
    output_maplibregl("maplibre", height=600),
    ui.input_select(
        "filter",
        "max property value per square meter",
        choices=[0, 1000, 5000, 10000, 50000, 100000, MAX_FILTER_VALUE],
        selected=MAX_FILTER_VALUE,
    ),
    ui.input_checkbox_group(
        "layers",
        "Layers",
        choices=[LAYER_ID_FILL, LAYER_ID_LINES],
        selected=[LAYER_ID_FILL, LAYER_ID_LINES],
    ),
)


def server(input, output, session):
    @render_maplibregl
    def maplibre():
        m = create_map()
        return m

    @reactive.Effect
    @reactive.event(input.filter)
    async def filter():
        async with MapContext("maplibre") as m:
            filter_ = ["<=", ["get", "valuePerSqm"], int(input.filter())]
            m.set_filter(LAYER_ID_FILL, filter_)

    @reactive.Effect
    @reactive.event(input.layers)
    async def layers():
        visible_layers = input.layers()
        async with MapContext("maplibre") as m:
            for layer in [LAYER_ID_FILL, LAYER_ID_LINES]:
                m.set_visibility(layer, layer in visible_layers)


app = App(app_ui, server)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        m = create_map()
        with open(file_name, "w") as f:
            f.write(m.to_html())
    else:
        app.run()
