from pymaplibregl import Map, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import carto_dark_matter, carto_positron
from shiny import App, ui

fill_extrusion_layer = {
    "id": "vancouver-blocks-fill-extrusion",
    "type": "fill-extrusion",
    "source": {
        "type": "geojson",
        "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json",
    },
    "paint": {
        "fill-extrusion-color": "lightgreen",
        "fill-extrusion-opacity": 0.8,
        "fill-extrusion-height": ["*", ["to-number", ["get", "valuePerSqm"]], 0.5],
    },
}


center = [-123.0753056, 49.2686511]

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("map", height=600),
)


def server(input, output, session):
    @render_maplibregl
    async def map():
        m = Map(style=carto_dark_matter(), center=center, zoom=11, pitch=35)
        m.add_layer(fill_extrusion_layer)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
