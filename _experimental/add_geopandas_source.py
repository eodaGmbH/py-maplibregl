# from maplibre.sources import SimpleFeatures
from geopandas import read_file
from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.basemaps import Carto

path = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"

data = read_file(path)

m = Map(MapOptions(style=Carto.POSITRON, bounds=data.total_bounds))
# m.add_source("states", data)
# m.add_layer(Layer(type=LayerType.LINE, source="states"))
m.add_layer(Layer(type=LayerType.LINE, source=data))
m.save("/tmp/py-maplibre-express.html")
