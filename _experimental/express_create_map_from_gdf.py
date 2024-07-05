import maplibre.express as mx
from maplibre.utils import save_map

path = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"

data = mx.read_file(path)[["name", "region", "geometry"]]

m = data.maplibre.to_map("region", tooltip_props=["name", "region"], cmap="YlOrRd")
filename = save_map(m, "/tmp/py-maplibre-gl-express.html", preview=True)
print(filename)
