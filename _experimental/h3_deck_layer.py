from maplibre import MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.controls import NavigationControl
from maplibre.ipywidget import MapWidget as Map
from maplibre.ui import use_deckgl, use_h3
from shiny.express import app, ui

m = Map(
    MapOptions(
        style=Carto.POSITRON,
        center=(-122.4, 37.74),
        zoom=12,
        hash=True,
        pitch=40,
    )
)
m.add_control(NavigationControl())

h3_hexagon_layer = {
    "@@type": "H3HexagonLayer",
    "id": "HexagonLayer",
    "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf.h3cells.json",
    "getHexagon": "@@=hex",
    "getFillColor": "@@=[255, (1 - count / 500) * 255, 0]",
    "getElevation": "@@=count",
    "elevationScale": 20,
    "extruded": True,
    "pickable": True,
}

m.add_deck_layers([h3_hexagon_layer], tooltip="{{ hex }} count: {{ count }}")

use_h3()
use_deckgl()


@render_maplibregl
def render_map():
    return m


if __name__ == "__main__":
    m.save("/tmp/py-maplibre-express.html", preview=True)
