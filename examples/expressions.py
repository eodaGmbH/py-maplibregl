# https://docs.mapbox.com/help/tutorials/mapbox-gl-js-expressions/

from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.controls import NavigationControl
from maplibre.expressions import interpolate
from maplibre.sources import GeoJSONSource

path = ""

map_options = MapOptions(center=(-118.0931, 33.78615), zoom=3, hash=True)
layer = Layer(
    type=LayerType.CIRCLE,
    id="earthquakes",
    paint={
        "circle-color": interpolate("mag", [0, 6], ["yellow", "red"]),
        "circle-radius": interpolate(["zoom"], [6, 20], [3, 20]),
    },
    source=GeoJSONSource(
        data="https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson"
    ),
)
m = Map(map_options, layers=[layer], controls=[NavigationControl()])
m.add_tooltip("earthquakes")
m.save("/tmp/py-maplibre-express.html")
