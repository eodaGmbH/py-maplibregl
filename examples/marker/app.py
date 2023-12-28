from pymaplibregl import Map, Marker, Popup, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import Carto
from shiny import App, ui

center_kassel = [9.5, 51.31667]

marker = Marker(
    [9.54, 51.31667],
    popup=Popup("Hello <strong>PyMapLibreGL</strong>!", options={"closeButton": False}),
    options={"color": "darkred"},
)

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("maplibre", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(style=Carto.VOYAGER, center=center_kassel, zoom=9)
        m.add_marker(Marker(center_kassel, color="green"))
        m.add_marker(marker)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
