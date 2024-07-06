import maplibre.express as mx
# import pandas as pd
import numpy as np

# path = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"
path = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"

data = mx.read_file(path)

m = data.maplibre.to_map(
    "valuePerSqm",
    bins=[-1, 1000, 5000, 10000, 50000, 100000, np.inf],
    cmap="YlOrRd",
    controls=[
        mx.NavigationControl(),
        mx.ScaleControl(),
    ],
    map_options=mx.MapOptions(pitch=45),
)
filename = m.save("/tmp/py-maplibre-gl-express.html", preview=True)
print(filename)
