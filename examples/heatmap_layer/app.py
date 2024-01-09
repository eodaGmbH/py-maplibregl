from maplibre import Layer, LayerType, Map, output_maplibregl, render_maplibregl
from maplibre.basemaps import Carto
from shiny import App, ui

# bounds = [{"lat": 51.069, "lng": -128.584}, {"lat": 21.657, "lng": -59.590}]
bounds = [[-128.584, 51.069], [-59.590, 21.657]]


population = {
    "type": "geojson",
    "data": "https://www.geoapify.com/data-share/assets/us-population-data.json",
}

heatmap_layer = Layer(
    LayerType.HEATMAP,
    source=population,
    maxzoom=9,
    layout=None,
    paint={
        "heatmap-weight": [
            "interpolate",
            ["linear"],
            ["get", "population"],
            0,
            0,
            1000,
            0.1,
            10000,
            0.2,
            100000,
            0.3,
            1000000,
            0.5,
            10000000,
            1,
        ],
        "heatmap-intensity": ["interpolate", ["linear"], ["zoom"], 0, 1, 9, 3],
        "heatmap-color": [
            "interpolate",
            ["linear"],
            ["heatmap-density"],
            0,
            "rgba(50, 50, 255, 0)",
            0.2,
            "rgb(0, 204, 255)",
            0.4,
            "rgb(128, 255, 128)",
            0.6,
            "rgb(255, 255, 102)",
            0.8,
            "rgb(255, 128, 0)",
            1,
            "rgb(204, 0, 0)",
        ],
        "heatmap-radius": [
            "interpolate",
            ["linear"],
            ["get", "population"],
            1000,
            1,
            1000000,
            20,
            10000000,
            30,
        ],
        "heatmap-opacity": ["interpolate", ["linear"], ["zoom"], 7, 1, 9, 0],
    },
)


app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("maplibre", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(style=Carto.VOYAGER, bounds=bounds)
        m.add_layer(heatmap_layer)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
