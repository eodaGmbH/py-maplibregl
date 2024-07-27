from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.__future__ import DataSets
from maplibre.controls import NavigationControl
from maplibre.expressions import color_quantile_step_expr, interpolate

data = DataSets.vancouver_blocks

map_options = MapOptions(bounds=data.bounds, hash=True)
layer = Layer(
    type=LayerType.FILL,
    id=data.name,
    paint={"fill-color": interpolate("growth", [0, 1], ["yellow", "red"])},
    source=data.source,
    filter=["all", [">=", ["get", "growth"], 0.2], ["<=", ["get", "growth"], 0.5]],
)
m = Map(map_options, layers=[layer], controls=[NavigationControl()])
m.add_tooltip(data.name)
m.save("/tmp/py-maplibre-express.html")
