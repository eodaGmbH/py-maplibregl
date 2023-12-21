from pymaplibregl import Map, output_maplibregl, render_maplibregl
from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("map", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def map():
        m = Map(zoom=4)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
