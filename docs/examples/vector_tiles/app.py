# Example taken from here:
# https://maplibre.org/maplibre-gl-js/docs/API/classes/VectorTileSource/
# https://maplibre.org/maplibre-style-spec/sources/

import webbrowser

from maplibre import Layer, LayerType, Map, MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.controls import NavigationControl
from maplibre.sources import VectorTileSource
from shiny.express import input, render, ui

# Get layer ids and pbf url from here
VECTOR_TILES_URL = "https://demotiles.maplibre.org/tiles/tiles.json"
LAYER_ID = "countries"

vector_source = VectorTileSource(
    url=VECTOR_TILES_URL,
    # tiles=["https://demotiles.maplibre.org/tiles/{z}/{x}/{y}.pbf"],
    min_zoom=0,
    max_zoom=6,
)

vector_layer = Layer(
    type=LayerType.FILL,
    id=LAYER_ID,
    source=vector_source,
    paint={"fill-color": "lightgreen", "fill-outline-color": "black"},
    source_layer="countries",
)


def create_map():
    m = Map(MapOptions(style=Carto.POSITRON, center=(11, 42), zoom=3, hash=True))
    m.add_control(NavigationControl())
    m.add_layer(vector_layer)
    m.add_tooltip(LAYER_ID)
    return m


@render_maplibregl
def render_map():
    return create_map()


if __name__ == "__main__":
    file_name = "docs/examples/vector_tiles/app.html"

    m = create_map()
    with open(file_name, "w") as f:
        f.write(m.to_html())

    webbrowser.open(file_name)
