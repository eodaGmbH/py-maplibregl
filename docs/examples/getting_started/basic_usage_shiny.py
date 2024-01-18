from maplibre import Map, MapContext, output_maplibregl, render_maplibregl
from maplibre.controls import Marker
from shiny import App, reactive, ui

app_ui = ui.page_fluid(
    output_maplibregl("maplibre", height=600),
    ui.div("Click on map to set a marker"),
)


def server(input, output, session):
    @render_maplibregl
    def maplibre():
        m = Map()
        return m

    @reactive.Effect
    @reactive.event(input.maplibre)
    async def coords():
        async with MapContext("maplibre") as m:
            print(input.maplibre())
            lng_lat = tuple(input.maplibre()["coords"].values())
            marker = Marker(lng_lat=lng_lat)
            m.add_marker(marker)
            m.add_call("flyTo", {"center": lng_lat})


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
