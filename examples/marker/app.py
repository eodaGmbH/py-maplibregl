from pymaplibregl import Map, Marker, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import carto_positron
from shiny import App, ui

center_kassel = [9.5, 51.31667]

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("map", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def map():
        m = Map(style=carto_positron(), center=center_kassel, zoom=9)
        m.add_marker(Marker(center_kassel, color="green"))
        marker = {
            "lngLat": [9.54, 51.31667],
            "popup": "Hello PyMapLibreGL!",
            "options": {"color": "darkred"},
        }
        m.add_marker(marker)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
