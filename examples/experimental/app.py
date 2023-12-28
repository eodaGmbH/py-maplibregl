import requests as req
from pymaplibregl import Layer, LayerType, Map, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import Carto
from pymaplibregl.mapcontext import MapContext
from shiny import App, reactive, render, ui

LAYER_ID = "counties"

circle_layer = Layer(
    LayerType.CIRCLE,
    id_=LAYER_ID,
    source={
        "type": "geojson",
        "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/arc/counties.json",
    },
    paint={"circle-color": "black", "circle-radius": 7},
)

center = [-118.0931, 33.78615]

us_states = {
    "type": "geojson",
    "data": req.get(
        "https://raw.githubusercontent.com/maplibre/maplibre-gl-js/main/docs/assets/us_states.geojson"
    ).json(),
}

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("map", height=500),
    #
    ui.div("Click on map to show coords."),
    ui.output_text_verbatim("coords", placeholder=True),
    #
    ui.div("Click on feature to show name."),
    ui.output_text_verbatim("feature", placeholder=True),
    #
    ui.input_select("color", "color", ["green", "red", "blue"]),
)


def server(input, output, session):
    @render_maplibregl
    async def map():
        map_ = Map(style=Carto.POSITRON, center=center, zoom=7)
        map_.add_source("us-states", us_states)
        map_.add_layer(
            Layer(
                LayerType.FILL,
                source="us-states",
                paint={"fill-color": "green", "fill-opacity": 0.5},
            )
        )
        map_.add_layer(
            Layer(LayerType.LINE, source="us-states", paint={"line-color": "white"})
        )
        map_.add_layer(circle_layer)
        return map_

    @reactive.Effect
    @reactive.event(input.map)
    async def result():
        print(f"result: {input.map()}")

    @render.text
    def coords():
        data = input.map()["coords"]
        return f'lng: {data["lng"]}, lat: {data["lat"]}'

    @render.text
    def feature():
        feature_ = input.map_layer_counties()
        print(feature_)
        return feature_["props"]["name"]

    @reactive.Effect
    @reactive.event(input.color, ignore_init=True)
    async def color():
        print(input.color())
        map = MapContext("map")
        # map.add_call("setPaintProperty", [LAYER_ID, "circle-color", input.color()])
        map.set_paint_property(LAYER_ID, "circle-color", input.color())
        # map.add_call("setFilter", [LAYER_ID, ["==", "Imperial, CA", ["get", "name"]]])
        # map.set_filter(LAYER_ID, ["==", "Imperial, CA", ["get", "name"]])
        await map.render()


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
