from maplibre import MapOptions
from maplibre.basemaps import Carto
from maplibre.controls import NavigationControl
from maplibre.ipywidget import MapWidget as Map

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
m.save("/tmp/py-maplibre-express.html")
