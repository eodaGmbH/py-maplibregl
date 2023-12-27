from pymaplibregl import Layer, Map, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import Carto
from shiny import App, reactive, render, ui

SOURCE_ID = "vancouver-blocks"

vancouver_blocks = {
    "type": "geojson",
    "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json",
}

fill_layer = Layer(
    "fill",
    id_="vancouver-blocks-fill",
    source=SOURCE_ID,
    # paint={"fill-color": "lightgreen", "fill-opacity": 0.6},
    paint={
        "fill-color": [
            "step",
            ["get", "valuePerSqm"],
            "darkred",
            500,
            "red",
            1500,
            "yellow",
        ],
        "fill-opacity": 0.7,
    },
    filter=["<", ["get", "valuePerSqm"], 2300],
)

line_layer = Layer(
    "line",
    id_="vancouver-blocks-line",
    source=SOURCE_ID,
    paint={"line-color": "white", "line-opacity": 1.0},
)

center = [-123.0753056, 49.2686511]

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("maplibre", height=600),
    ui.output_text_verbatim("props", placeholder=True),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(style=Carto.DARK_MATTER, center=center, zoom=12, pitch=35)
        m.add_source(SOURCE_ID, vancouver_blocks)
        m.add_layer(fill_layer)
        m.add_popup("vancouver-blocks-fill", "valuePerSqm")
        m.add_layer(line_layer)
        return m

    @reactive.Effect
    @reactive.event(input.maplibre_layer_vancouver_blocks_fill)
    async def feature():
        print(f"result: {input.maplibre_layer_vancouver_blocks_fill()}")

    @reactive.Effect
    @reactive.event(input.maplibre)
    async def result():
        print(f"result: {input.maplibre()}")

    @render.text
    def props():
        return str(input.maplibre_layer_vancouver_blocks_fill())


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
