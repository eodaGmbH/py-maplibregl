import webbrowser

import geodatasets
import geopandas as gpd
import maplibre.settings
from maplibre.basemaps import Carto
from maplibre.express import create_map

# maplibre.settings.default_layer_types["polygon"] = "line"
# maplibre.settings.default_layer_types["multipolygon"] = "line"

# data = gpd.read_file(
#    "zip+https://github.com/Toblerity/Fiona/files/11151652/coutwildrnp.zip"
# )

# data = gpd.read_file(geodatasets.get_path("ny.bb"))
data = gpd.read_file(geodatasets.get_path("geoda.airbnb"))

m = create_map(data, style=Carto.POSITRON)

filename = "/tmp/py-maplibre-express.html"
with open(filename, "w") as f:
    f.write(m.to_html())

webbrowser.open(filename)
