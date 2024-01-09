from maplibre import Map, output_maplibregl, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.controls import Marker, MarkerOptions, Popup, PopupOptions
from shiny import App, ui

center_kassel = (9.5, 51.31667)

marker = Marker(
    lng_lat=(9.54, 51.31667),
    popup=Popup(
        text="Hello <strong>PyMapLibreGL</strong>!",
        options=PopupOptions(close_button=False),
    ),
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
        m.add_marker(
            Marker(
                lng_lat=center_kassel,
                options=MarkerOptions(color="green"),
                popup=Popup(**{"text": "Hi", "options": {"closeButton": False}}),
            )
        )
        m.add_marker(marker)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
