from pymaplibregl import Map, Marker, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import Carto
from shiny import App, ui

center_kassel = [9.5, 51.31667]

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("map", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def map():
        map_ = Map(style=Carto.VOYAGER, center=center_kassel, zoom=9)
        map_.add_marker(Marker(center_kassel, color="green"))
        marker = {
            "lngLat": [9.54, 51.31667],
            "popup": "Hello PyMapLibreGL!",
            "options": {"color": "darkred"},
        }
        map_.add_marker(marker)
        return map_


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
