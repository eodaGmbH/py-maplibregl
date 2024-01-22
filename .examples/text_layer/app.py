from maplibre import Layer, LayerType, Map, output_maplibregl, render_maplibregl
from maplibre.basemaps import Carto
from shiny import App, reactive, render, ui

urban_areas = {
    "type": "geojson",
    "data": "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson",
}

fill_layer = Layer(
    LayerType.FILL,
    source=urban_areas,
    paint={"fill-color": "#f08", "fill-opacity": 0.4},
)

text_layer = Layer(
    LayerType.SYMBOL,
    source=urban_areas,
    layout={
        "text-field": ["concat", "area: ", ["get", "area_sqkm"], " sqkm"],
        "text-size": 12,
    },
    paint={"text-color": "white"},
)

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("maplibre", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(
            style=Carto.DARK_MATTER,
            center=[-88.13734351262877, 35.137451890638886],
            zoom=6,
        )
        m.add_layer(fill_layer)
        m.add_layer(text_layer)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
