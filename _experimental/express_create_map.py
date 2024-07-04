import webbrowser

import geodatasets
import geopandas as gpd

# from maplibre.express import ColorPalette, MapOptions, create_map
import maplibre.express as mx
import maplibre.settings
import pandas as pd
from colour import Color
from maplibre import colors as ml_colors
from maplibre.basemaps import Carto

# maplibre.settings.default_layer_types["polygon"] = "line"
# maplibre.settings.default_layer_types["multipolygon"] = "line"

# data = gpd.read_file(
#    "zip+https://github.com/Toblerity/Fiona/files/11151652/coutwildrnp.zip"
# )

# data = gpd.read_file(geodatasets.get_path("ny.bb"))
# print("reading data")
# data = gpd.read_file(geodatasets.get_path("geoda.airbnb"))
# print("ready")
# data = "https://github.com/Toblerity/Fiona/files/11151652/coutwildrnp.zip"

n = 10
# colors = random_colors(n)
# colors = [str(color) for color in list(Color("yellow").range_to("red", n))]

# colors = ml_colors.color_palette("yellow", "red", n)
# data["color"] = pd.cut(data["population"], n, labels=False).apply(lambda i: colors[i])
# data["color"] = "green"


# m = create_map(data, style=Carto.POSITRON, color_column="color")
"""
def create_map_():
    m = create_map(
        data,
        # color="population",
        # color="community",
        color="STATE",
        n=4,
        # set_centroid=True,
        # map_options=MapOptions(zoom=10),
        tooltip_props=["NAME", "STATE"],
        # pal=ColorPalette("yellow", "darkred"),
        # pal=ColorPalette("green", "yellow"),
    )
"""
path = "https://github.com/Toblerity/Fiona/files/11151652/coutwildrnp.zip"
path = geodatasets.get_path("geoda.airbnb")
# airbnb = mx.read_file(geodatasets.get_path("geoda.airbnb"))
gdf = mx.read_file(path)

"""
m = mx.Map(mx.MapOptions(bounds=gdf.total_bounds))
m.add_layer(
    gdf.to_maplibre_layer(
        color_column="population",
        layer_options=mx.LayerOptions(id="test", bins=6, cmap="viridis"),
    )
)
m.add_tooltip("test")
"""

path = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"

m, layer_id = mx.create_map(
    path,
    # color_column="community",
    color_column="region",
    ret_layer_id=True,
    layer_options=mx.LayerOptions(
        bins=4,
        type="fill-extrusion",
        paint={"fill-extrusion-height": ["*", 10000, ["get", "adm0_sr"]]},
    ),
    pitch=35,
)
print(layer_id)
print(m.map_options)

filename = "/tmp/py-maplibre-express.html"
with open(filename, "w") as f:
    f.write(m.to_html())

webbrowser.open(filename)
