import webbrowser

import geopandas as gpd
from maplibre.basemaps import Carto
from maplibre.express import create_map


# data = gpd.read_file(
#    "zip+https://github.com/Toblerity/Fiona/files/11151652/coutwildrnp.zip"
# )

data = gpd.read_file(gpd.datasets.get_path("nybb"))


m = create_map(data, style=Carto.POSITRON)

filename = "/tmp/py-maplibre-express.html"
with open(filename, "w") as f:
    f.write(m.to_html())

webbrowser.open(filename)
