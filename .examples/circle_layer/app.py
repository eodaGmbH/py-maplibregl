from maplibre import Layer, Map, output_maplibregl, render_maplibregl
from maplibre.basemaps import Carto
from shiny import App, reactive, render, ui

circle_layer = Layer(
    "circle",
    id_="counties",
    source={
        "type": "geojson",
        "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/arc/counties.json",
    },
    paint={"circle-color": "black", "circle-radius": 7},
)

center = [-118.0931, 33.78615]

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("map", height=500),
    #
    ui.div("Click on map to show coords."),
    ui.output_text_verbatim("coords", placeholder=True),
    #
    ui.div("Click on feature to show name."),
    ui.output_text_verbatim("feature", placeholder=True),
)


def server(input, output, session):
    @render_maplibregl
    async def map():
        map_ = Map(style=Carto.POSITRON, center=center, zoom=7)
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


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
