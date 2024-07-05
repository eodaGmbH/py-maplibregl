import maplibre.express as mx
from maplibre.utils import save_map

path = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"

data = mx.gpd.read_file(path)

layer_options = mx.LayerOptions(cmap="viridis")
m = data.loc[:, ["name", "region", "geometry"]].maplibre.to_map(
    "region",
    layer_options=layer_options,
    # tooltip_props=["name", "region"],
)
filename = save_map(m, "/tmp/py-maplibre-gl-express.html", preview=True)
print(filename)
