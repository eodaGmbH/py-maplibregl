from pymaplibregl import Layer, Map, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import Carto
from shiny import App, ui

fill_extrusion_layer = Layer(
    id_="vancouver-blocks",
    type_="fill-extrusion",
    source={
        "type": "geojson",
        "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json",
        "filter": ["<", ["get", "valuePerSqm"], 3000],
    },
    paint={
        # "fill-extrusion-color": "lightgreen",
        "fill-extrusion-color": {
            "property": "valuePerSqm",
            "stops": [[0, "lightgreen"], [1500, "darkred"]],
        },
        "fill-extrusion-opacity": 0.8,
        "fill-extrusion-height": ["*", ["to-number", ["get", "valuePerSqm"]], 0.5],
    },
)


center = [-123.0753056, 49.2686511]

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("maplibre", height=600),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(
            style=Carto.DARK_MATTER,
            center=center,
            zoom=11,
            pitch=35,
        )
        # Change properties of basemap
        m.set_paint_property("water", "fill-color", "yellow")
        m.set_paint_property("water", "fill-opacity", 0.5)
        m.add_layer(fill_extrusion_layer)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
