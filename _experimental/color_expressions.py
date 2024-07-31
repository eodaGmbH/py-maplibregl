from _deprecated.color_utils import create_categorical_color_expression
from geopandas import read_file
from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.basemaps import Carto
from maplibre.sources import GeoJSONSource
from maplibre.utils import geopandas_to_geojson

path = "https://github.com/Toblerity/Fiona/files/11151652/coutwildrnp.zip"
data = read_file(path)

fill_color = create_categorical_color_expression(data.NAME, "NAME")
# fill_color, _, _ = create_numeric_color_expression(
#    data.AREA, n=4, column_name="AREA", cmap="YlOrRd"
# )

print(fill_color)

layer = Layer(
    id="wilderness",
    type=LayerType.FILL,
    paint={"fill-color": fill_color},
    source=GeoJSONSource(data=geopandas_to_geojson(data)),
)

filename = "/tmp/py-maplibre-express.html"

m = Map(MapOptions(bounds=data.total_bounds, style=Carto.POSITRON))
m.add_layer(layer)
m.add_tooltip("wilderness")
m.save(filename, preview=True)
