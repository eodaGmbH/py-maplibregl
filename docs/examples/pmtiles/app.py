# Example taken from here: https://maplibre.org/maplibre-gl-js/docs/examples/pmtiles/

import webbrowser

from maplibre import Layer, LayerType, Map, MapOptions, render_maplibregl
from maplibre.basemaps import construct_basemap_style
from maplibre.controls import NavigationControl
from shiny.express import input, render, ui

PMTILES_URL = "https://pmtiles.io/protomaps(vector)ODbL_firenze.pmtiles"

pmtiles_source = {
    "type": "vector",
    "url": f"pmtiles://{PMTILES_URL}",
    "attribution": '© <a href="https://openstreetmap.org">OpenStreetMap</a>',
}

custom_basemap = construct_basemap_style(
    sources={"pmtiles": pmtiles_source},
    layers=[
        Layer(
            id="buildings",
            source="pmtiles",
            source_layer="landuse",
            type=LayerType.FILL,
            paint={"fill-color": "steelblue"},
        ),
        Layer(
            id="roads",
            source="pmtiles",
            source_layer="roads",
            type=LayerType.LINE,
            paint={"line-color": "black"},
        ),
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
    return m


@render_maplibregl
def render_map():
    return create_map()


if __name__ == "__main__":
    file_name = "docs/examples/pmtiles/app.html"

    m = create_map()
    with open(file_name, "w") as f:
        f.write(m.to_html())

    webbrowser.open(file_name)
