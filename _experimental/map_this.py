import geopandas as gpd
from maplibre import MapOptions
from maplibre import express as mx
from maplibre.basemaps import Carto

data = gpd.read_file("~/BART-Districts.json")

# m = mx.map_this(data)
m = (
    mx.fill(data)
    .color("darkred")
    # .color_category("Name", cmap="YlOrRd")
    .opacity(0.5)
    .set_paint_props(fill_outline_color="white")
    .to_map(MapOptions(style=Carto.POSITRON))
)
m.save("/tmp/py-maplibre-express.html")
