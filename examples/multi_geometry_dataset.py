from maplibre import Layer, LayerType, Map
from maplibre import expressions as expr
from maplibre.__future__.datasets import DataSets
from maplibre.controls import NavigationControl
from maplibre.sources import SimpleFeatures

data = DataSets.bart.read_data()
feature_types = set(data.geom_type)
print(feature_types)

polygon_data = data[data.geom_type == "Polygon"]

source_id = "bart"
sf = SimpleFeatures(DataSets.bart.url, source_id=source_id)

polygons = Layer(
    type=LayerType.FILL,
    source=source_id,
    filter=["==", ["geometry-type"], "Polygon"],
).set_paint_props(fill_color="green")
print(polygons)

points = Layer(
    type=LayerType.CIRCLE, source=source_id, filter=expr.geometry_type_filter("Point")
).set_paint_props(circle_color="yellow", circle_radius=5)
print(points)

lines = Layer(
    type=LayerType.LINE,
    source=source_id,
    filter=expr.geometry_type_filter(expr.GeometryType.LINE_STRING),
).set_paint_props(line_color="steelblue", line_width=4)
print(lines)

m = Map(
    sources=sf.to_sources_dict(),
    layers=[polygons],
    controls=[NavigationControl()],
)
m.fit_bounds(data=sf.data)

# m = mx.fill(polygon_data).color("yellow").to_map()
m.save("/tmp/py-maplibre-express.html")
