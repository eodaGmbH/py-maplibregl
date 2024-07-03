import webbrowser

import geodatasets
import geopandas as gpd
import maplibre.settings
import pandas as pd
from colour import Color
from maplibre import colors as ml_colors
from maplibre.basemaps import Carto
from maplibre.express import ColorPalette, create_map

# maplibre.settings.default_layer_types["polygon"] = "line"
# maplibre.settings.default_layer_types["multipolygon"] = "line"

# data = gpd.read_file(
#    "zip+https://github.com/Toblerity/Fiona/files/11151652/coutwildrnp.zip"
# )

# data = gpd.read_file(geodatasets.get_path("ny.bb"))
data = gpd.read_file(geodatasets.get_path("geoda.airbnb"))

n = 10
# colors = random_colors(n)
# colors = [str(color) for color in list(Color("yellow").range_to("red", n))]

# colors = ml_colors.color_palette("yellow", "red", n)
# data["color"] = pd.cut(data["population"], n, labels=False).apply(lambda i: colors[i])
# data["color"] = "green"

# m = create_map(data, style=Carto.POSITRON, color_column="color")
m = create_map(
    data,
    # color="population",
    color="community",
    n=4,
    pal=ColorPalette("yellow", "darkred"),
    # pal=ColorPalette("green", "yellow"),
)

filename = "/tmp/py-maplibre-express.html"
with open(filename, "w") as f:
    f.write(m.to_html())

webbrowser.open(filename)
