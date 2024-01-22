from maplibre import Map, MapOptions, output_maplibregl, render_maplibregl
from maplibre.controls import ControlPosition, FullscreenControl
from maplibre.layer import Layer, LayerType
from maplibre.sources import GeoJSONSource
from shiny import App, ui

CENTER = (-123.0753056, 49.2686511)
LAYER_ID = "vancouver-blocks"
SOURCE_ID = "vancouver-blocks"


vancouver_blocks_source = GeoJSONSource(
    data="https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json",
)


vancouver_blocks_layer = Layer(
    type=LayerType.LINE,
    id=LAYER_ID,
    source=SOURCE_ID,
    paint={"line-color": "yellow"},
    min_zoom=12,
)


app_ui = ui.page_fluid(
    ui.panel_title(LAYER_ID),
    output_maplibregl("ml_map", height=600),
)


def server(input, output, session):
    @render_maplibregl
    async def ml_map():
        m = Map(MapOptions(center=CENTER, zoom=12, pitch=35))
        m.add_control(FullscreenControl(), position=ControlPosition.BOTTOM_LEFT)
        m.add_source(SOURCE_ID, vancouver_blocks_source)
        m.add_layer(vancouver_blocks_layer)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
