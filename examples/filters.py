from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.__future__.datasets import DataSets
from maplibre.controls import NavigationControl
from maplibre.expressions import filter_expr, interpolate, range_filter

data = DataSets.vancouver_blocks

map_options = MapOptions(bounds=data.bounds, hash=True)
layer = Layer(
    type=LayerType.FILL,
    id=data.name,
    paint={"fill-color": interpolate("growth", [0.2, 0.4], ["yellow", "red"])},
    source=data.source,
    # filter=range_filter("growth", (0.2, 0.4)),
    filter=filter_expr("growth", ">=", 0.7),
    # filter=["all", [">=", ["get", "growth"], 0.2], ["<=", ["get", "growth"], 0.5]],
)
m = Map(map_options, layers=[layer], controls=[NavigationControl()])
m.add_tooltip(data.name)
m.save("/tmp/py-maplibre-express.html")
