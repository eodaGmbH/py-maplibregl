# Example taken from here:
# https://maplibre.org/maplibre-gl-js/docs/API/classes/VectorTileSource/
# https://maplibre.org/maplibre-style-spec/sources/

import webbrowser

from shiny.express import input, render, ui

from maplibre import Layer, LayerType, Map, MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.controls import NavigationControl
from maplibre.sources import VectorTileSource

# get layer ids and pbf url from here
VECTORTILES_URL = "https://demotiles.maplibre.org/tiles/tiles.json"

vectortiles_source = VectorTileSource(
    tiles=["https://demotiles.maplibre.org/tiles/{z}/{x}/{y}.pbf"],
    min_zoom=0,
    max_zoom=6,
)

vector_layer = Layer(
    type=LayerType.FILL,
    id="countries",
    source=vectortiles_source,
    paint={"fill-color": "lightgreen", "fill-outline-color": "black"},
    source_layer="countries",
)

CENTER = (11, 42)


def create_map():
    m = Map(
        map_options=MapOptions(style=Carto.POSITRON, center=CENTER, zoom=3, hash=True)
    )
    m.add_control(NavigationControl())
    m.add_layer(vector_layer)
    return m


@render_maplibregl
def render_map():
    return create_map()


if __name__ == "__main__":
    file_name = "docs/examples/vectortiles/app.html"

    m = create_map()
    with open(file_name, "w") as f:
        f.write(m.to_html())

    webbrowser.open(file_name)
