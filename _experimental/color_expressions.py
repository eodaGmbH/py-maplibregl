import webbrowser

from geopandas import read_file
from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.sources import GeoJSONSource
from maplibre.utils import geopandas_to_geojson

from _experimental.color_utils import create_color_expression

path = "https://github.com/Toblerity/Fiona/files/11151652/coutwildrnp.zip"
data = read_file(path)

fill_color = create_color_expression(data.NAME, "NAME")

print(fill_color)
m = Map(MapOptions(bounds=data.total_bounds))
m.add_layer(
    Layer(
        id="wilderness",
        type=LayerType.FILL,
        paint={"fill-color": fill_color},
        source=GeoJSONSource(data=geopandas_to_geojson(data)),
    )
)
m.add_tooltip("wilderness")
filename = "/tmp/py-maplibre-express.html"
with open(filename, "w") as f:
    f.write(m.to_html())

webbrowser.open(filename)
