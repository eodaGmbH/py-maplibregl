from maplibre import Layer, Map, MapOptions, output_maplibregl, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.sources import GeoJSONSource
from shiny import App, reactive, ui

SOURCE_ID = "earthquakes"
LAYER_ID = "earthquakes"

earthquakes_source = GeoJSONSource(
    # data="https://raw.githubusercontent.com/crazycapivara/mapboxer/master/data-raw/earthquakes.geojson",
    data="https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson",
    cluster=True,
    cluster_radius=50,
    cluster_min_points=2,
    cluster_max_zoom=14,
    cluster_properties={
        "maxMag": ["max", ["get", "mag"]],
        "minMag": ["min", ["get", "mag"]],
    },
)

earthquakes_layer = Layer(
    type="circle",
    source=SOURCE_ID,
    paint={"circle-color": "darkblue"},
    filter=["!", ["has", "point_count"]],
)


earthquakes_cluster_layer = Layer(
    type="circle",
    id=LAYER_ID,
    source=SOURCE_ID,
    filter=["has", "point_count"],
    paint={
        "circle-color": [
            "step",
            ["get", "point_count"],
            "#51bbd6",
            100,
            "#f1f075",
            750,
            "#f28cb1",
        ],
        "circle-radius": ["step", ["get", "point_count"], 20, 100, 30, 750, 40],
    },
)


center = [-118.0931, 33.78615]

app_ui = ui.page_fluid(
    ui.panel_title("Earthquakes Cluster"),
    output_maplibregl("maplibre", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(MapOptions(style=Carto.POSITRON, center=([-103.5917, 40.6699]), zoom=3))
        m.add_source(SOURCE_ID, earthquakes_source)
        m.add_layer(earthquakes_cluster_layer)
        m.add_popup(LAYER_ID, "maxMag")
        m.add_layer(earthquakes_layer)
        m.add_layer(
            Layer(
                type="symbol",
                id="text",
                source=SOURCE_ID,
                filter=["has", "point_count"],
                layout={
                    "text-field": ["get", "point_count_abbreviated"],
                    "text-size": 12,
                },
            )
        )
        return m

    @reactive.Effect
    @reactive.event(input.maplibre)
    async def result():
        print(f"result: {input.maplibre()}")


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
