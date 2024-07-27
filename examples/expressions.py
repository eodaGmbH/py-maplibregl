# https://docs.mapbox.com/help/tutorials/mapbox-gl-js-expressions/

from geopandas import read_file
from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.controls import NavigationControl
from maplibre.expressions import color_quantile_step_expr, interpolate
from maplibre.sources import GeoJSONSource

path = "https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson"
data = read_file(path)

map_options = MapOptions(center=(-118.0931, 33.78615), zoom=3, hash=True)
layer = Layer(
    type=LayerType.CIRCLE,
    id="earthquakes",
    paint={
        # "circle-color": interpolate("mag", [0, 6], ["yellow", "red"]),
        "circle-color": color_quantile_step_expr(
            "mag", [0.1, 0.5, 0.9], values=data.mag
        ),
        "circle-radius": interpolate(["zoom"], [3, 20], [5, 100], type=["linear"]),
    },
    source=data,
    # source=GeoJSONSource(
    #    data="https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson"
    # ),
)
m = Map(map_options, layers=[layer], controls=[NavigationControl()])
m.add_tooltip("earthquakes")
m.save("/tmp/py-maplibre-express.html")
