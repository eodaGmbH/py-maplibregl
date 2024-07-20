from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.sources import SimpleFeatures

path = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"

simple_features = SimpleFeatures(path, source_id="states")
# sources = {"states": simple_features.to_source()}
sources = simple_features.to_sources_dict()
layers = [
    Layer(
        type=LayerType.FILL,
        paint={"fill-color": "green"},
        source=simple_features.source_id,
    ),
    Layer(
        type=LayerType.LINE,
        paint={"line-color": "blue"},
        source=simple_features.source_id,
    ),
]

m = Map(MapOptions(bounds=simple_features.bounds))
m.add_layers(layers, sources)
m.save("/tmp/py-maplibre-express.html")
