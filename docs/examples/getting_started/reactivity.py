from pymaplibregl import (Layer, LayerType, Map, MapContext, output_maplibregl,
                          render_maplibregl)
from pymaplibregl.sources import GeoJSONSource
from shiny import App, reactive, render, ui

LAYER_ID = "earthquakes"
CIRCLE_RADIUS = 5

app_ui = ui.page_fluid(
    #
    # Render map
    #
    ui.panel_title("MapLibre"),
    output_maplibregl("maplibre", height=600),
    #
    # Show coords
    #
    ui.div("Click on the map to print the coords.", style="padding: 10px;"),
    ui.output_text_verbatim("coords", placeholder=True),
    #
    # Show props of a feature
    #
    ui.div("Click on a feature to print its props.", style="padding: 10px;"),
    ui.output_text_verbatim("props", placeholder=True),
    #
    # Change radius
    #
    ui.input_slider("radius", "Radius", value=CIRCLE_RADIUS, min=1, max=10),
)


def server(input, output, session):
    @render_maplibregl
    def maplibre():
        m = Map(zoom=3)
        m.add_layer(
            Layer(
                type=LayerType.CIRCLE,
                id=LAYER_ID,
                source=GeoJSONSource(
                    data="https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson"
                ),
                paint={"circle-color": "yellow"},
            )
        )
        return m

    @render.text
    def coords():
        return str(input.maplibre())

    @render.text
    def props():
        return str(input.maplibre_layer_earthquakes())

    @reactive.Effect
    @reactive.event(input.radius)
    async def radius():
        async with MapContext("maplibre") as m:
            m.set_paint_property(LAYER_ID, "circle-radius", input.radius())


app = App(app_ui, server)
