import json

from maplibre import (
    Layer,
    LayerType,
    Map,
    MapContext,
    output_maplibregl,
    render_maplibregl,
)
from maplibre.controls import NavigationControl
from maplibre.sources import GeoJSONSource
from shiny import App, reactive, render, ui

LAYER_ID = "earthquakes"
CIRCLE_RADIUS = 5

app_ui = ui.page_fluid(
    ui.panel_title("MapLibre for Python"),
    output_maplibregl("mapgl", height=600),
    ui.div("Click on the map to print the coords.", style="padding: 10px;"),
    ui.output_text_verbatim("coords", placeholder=True),
    ui.div("Click on a feature to print its props.", style="padding: 10px;"),
    ui.output_text_verbatim("props", placeholder=True),
    ui.div("View state.", style="padding: 10px;"),
    ui.output_text_verbatim("view_state", placeholder=True),
    ui.input_slider("radius", "Radius", value=CIRCLE_RADIUS, min=1, max=10),
)

circle_layer = Layer(
    type=LayerType.CIRCLE,
    id=LAYER_ID,
    source=GeoJSONSource(
        data="https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson"
    ),
    paint={"circle-color": "yellow"},
)


def server(input, output, session):
    @render_maplibregl
    def mapgl():
        m = Map(zoom=3, pitch=40)
        m.add_control(NavigationControl())
        m.add_layer(circle_layer)
        return m

    @render.text
    def coords():
        return str(input.mapgl_clicked())

    @render.text
    def view_state():
        return json.dumps(input.mapgl_view_state(), indent=2)

    @render.text
    def props():
        return str(input.mapgl_layer_earthquakes())

    @reactive.Effect
    @reactive.event(input.radius)
    async def radius():
        async with MapContext("mapgl") as m:
            m.set_paint_property(LAYER_ID, "circle-radius", input.radius())


app = App(app_ui, server)
