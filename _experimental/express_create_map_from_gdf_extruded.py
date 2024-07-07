import maplibre.express as mx

# import pandas as pd
import numpy as np

# path = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"
path = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"

data = mx.read_file(path)

"""
color_column = {
    "property": "valuePerSqm",
    "stops": [
        [0, "grey"],
        [1000, "yellow"],
        [5000, "orange"],
        [10000, "darkred"],
        [50000, "lightblue"],
    ],
}
"""

m, layer_id = data.maplibre.to_map(
    "valuePerSqm",
    # color_column,
    bins=[-1, 1000, 5000, 10000, 50000, 100000, np.inf],
    cmap="viridis",
    # extrusion_column="valuePerSqm",
    extrusion_column=["*", 10, ["sqrt", ["get", "valuePerSqm"]]],
    controls=[
        mx.NavigationControl(),
        mx.ScaleControl(),
    ],
    map_options=mx.MapOptions(pitch=45),
    ret_layer_id=True,
)
print(layer_id)
m.add_layer(
    mx.Layer(
        id="line",
        type=mx.LayerType.LINE,
        source=layer_id,
        paint={"line-color": "yellow", "line-width": 2},
    ),
    before_id=layer_id,
)
m.add_control(mx.LayerSwitcherControl(layer_ids=[layer_id, "line"]))
filename = m.save("/tmp/py-maplibre-gl-express.html", preview=True)
print(filename)
