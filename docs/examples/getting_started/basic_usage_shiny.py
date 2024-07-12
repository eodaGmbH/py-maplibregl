from maplibre import Map, MapContext, output_maplibregl, render_maplibregl
from maplibre.controls import Marker
from shiny import App, reactive, ui

app_ui = ui.page_fluid(
    output_maplibregl("maplibre_map", height=600),
    ui.div("Click on map to set a marker"),
)


def server(input, output, session):
    @render_maplibregl
    def maplibre_map():
        return Map()

    @reactive.Effect
    @reactive.event(input.maplibre_map_clicked)
    async def coords():
        async with MapContext("maplibre_map") as m:
            input_value = input.maplibre_map_clicked()
            print(input_value)
            lng_lat = tuple(input_value["coords"].values())
            marker = Marker(lng_lat=lng_lat)
            m.add_marker(marker)
            m.add_call("flyTo", {"center": lng_lat})


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
