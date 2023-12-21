from pymaplibregl import Map, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import carto_positron
from shiny import App, ui

center_kassel = (9.5, 51.31667)

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("map", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def map():
        m = Map(style=carto_positron(), center=center_kassel, zoom=8)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
