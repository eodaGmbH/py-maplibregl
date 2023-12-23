from pymaplibregl import Layer, Map, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import Carto
from shiny import App, ui

circle_layer = Layer(
    "circle",
    source={
        "type": "geojson",
        "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/arc/counties.json",
    },
    paint={"circle-color": "black"},
)

center = [-118.0931, 33.78615]

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("map", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def map():
        m = Map(style=Carto.POSITRON, center=center, zoom=7)
        m.add_layer(circle_layer)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
