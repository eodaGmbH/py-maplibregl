"""
RTL Text Plugin Test - Shiny

Run with: shiny run examples/rtl_test_shiny.py
"""

from shiny import App, ui

from maplibre import MapOptions, render_maplibregl
from maplibre.shiny import output_maplibregl

app_ui = ui.page_fluid(
    ui.h2("RTL Text Plugin Test - Shiny"),
    ui.p("Arabic street names should render correctly (right-to-left, connected characters)"),
    output_maplibregl("map", height="600px"),
)


def server(input, output, session):
    @render_maplibregl
    def map():
        from maplibre import Map

        return Map(
            MapOptions(
                style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
                center=(31.2243, 30.0626),  # Zamalek, Cairo, Egypt
                zoom=14,
            )
        )


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
