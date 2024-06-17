import webbrowser

from maplibre import Layer, LayerType, Map, MapOptions, render_maplibregl
from maplibre.basemaps import construct_basemap_style
from maplibre.controls import NavigationControl
from maplibre.sources import GeoJSONSource
from shiny.express import input, render, ui

# see example: https://maplibre.org/maplibre-gl-js/docs/examples/pmtiles/
PMTILES_URL = "https://pmtiles.io/protomaps(vector)ODbL_firenze.pmtiles"

pmtiles_source = {
    "type": "vector",
    "url": f"pmtiles://{PMTILES_URL}",
    "attribution": '© <a href="https://openstreetmap.org">OpenStreetMap</a>',
}

bg_layer = Layer(
    type=LayerType.BACKGROUND,
    id="background",
    source=None,
    paint={"background-color": "pink", "background-opacity": 0.8},
)

custom_basemap = construct_basemap_style(
    sources={"pmtiles": pmtiles_source},
    layers=[
        # bg_layer,
        {
            "id": "buildings",
            "source": "pmtiles",
            "source-layer": "landuse",
            "type": "fill",
            "paint": {"fill-color": "steelblue"},
        },
        {
            "id": "roads",
            "source": "pmtiles",
            "source-layer": "roads",
            "type": "line",
            "paint": {"line-color": "black"},
        },
        Layer(
            id="mask",
            source="pmtiles",
            source_layer="mask",
            type=LayerType.FILL,
            paint={"fill-color": "white"},
        ),
    ],
)


map_options = MapOptions(
    style=custom_basemap,
    bounds=(11.154026, 43.7270125, 11.3289395, 43.8325455),
)


def create_map():
    m = Map(map_options)
    m.add_control(NavigationControl())
    m.add_layer(
        Layer(
            type=LayerType.CIRCLE,
            id="earthquakes",
            source=GeoJSONSource(
                data="https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson"
            ),
            paint={"circle-color": "yellow", "circle-radius": 5},
        )
    )
    m.add_popup("earthquakes", "mag")
    return m


@render_maplibregl
def render_map():
    return create_map()


if __name__ == "__main__":
    file_name = "docs/examples/custom_basemap/app.html"

    m = create_map()
    with open(file_name, "w") as f:
        f.write(m.to_html())

    webbrowser.open(file_name)
