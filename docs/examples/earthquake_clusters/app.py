from pymaplibregl import (
    Layer,
    LayerType,
    Map,
    MapOptions,
    output_maplibregl,
    render_maplibregl,
)
from pymaplibregl.basemaps import Carto
from pymaplibregl.sources import GeoJSONSource
from shiny import App, reactive, ui

EARTHQUAKE_SOURCE = "earthquakes"
EARTHQUAKE_CIRCLES = "earthquake-circles"
EARTHQUAKE_CLUSTERS = "earthquake-clusters"
EARTHQUAKE_LABELS = "earthquake-labels"

CENTER = (-118.0931, 33.78615)

earthquakes_source = GeoJSONSource(
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

earthquake_circles = Layer(
    type=LayerType.CIRCLE,
    id=EARTHQUAKE_CIRCLES,
    source=EARTHQUAKE_SOURCE,
    paint={"circle-color": "darkblue"},
    filter=["!", ["has", "point_count"]],
)

earthquake_clusters = Layer(
    type=LayerType.CIRCLE,
    id=EARTHQUAKE_CLUSTERS,
    source=EARTHQUAKE_SOURCE,
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

earthquake_labels = Layer(
    type=LayerType.SYMBOL,
    id="text",
    source=EARTHQUAKE_SOURCE,
    filter=["has", "point_count"],
    layout={
        "text-field": ["get", "point_count_abbreviated"],
        "text-size": 12,
    },
)

map_options = MapOptions(style=Carto.POSITRON, center=CENTER, zoom=3, hash=True)

app_ui = ui.page_fluid(
    ui.panel_title("Earthquakes Cluster"),
    output_maplibregl("maplibre", height=500),
)


def server(input, output, session):
    @render_maplibregl
    def maplibre():
        m = Map(map_options)
        m.add_source(EARTHQUAKE_SOURCE, earthquakes_source)
        m.add_layer(earthquake_clusters)
        m.add_layer(earthquake_circles)
        m.add_tooltip(EARTHQUAKE_CLUSTERS, "maxMag")
        m.add_layer(earthquake_labels)
        return m

    @reactive.Effect
    @reactive.event(input.maplibre)
    async def result():
        print(f"result: {input.maplibre()}")


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
