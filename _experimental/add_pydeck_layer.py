import json

import pandas as pd
from maplibre import Map, MapOptions
from maplibre.controls import NavigationControl
from pydeck import Layer as PyDeckLayer

UK_ACCIDENTS_DATA = (
    "https://raw.githubusercontent.com/uber-common/"
    "deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv"
)

print("loading")
df = pd.read_csv(UK_ACCIDENTS_DATA)
print("loaded")

layer = PyDeckLayer(
    "HexagonLayer",
    df,
    # UK_ACCIDENTS_DATA,
    get_position=["lng", "lat"],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1,
)

m = Map(MapOptions(center=(1.415, 52.2323), zoom=6), controls=[NavigationControl()])
# m.add_deck_layers([json.loads(layer.to_json())])
m.add_deck_layers([layer])
m.save("/tmp/py-maplibre-express.html")
