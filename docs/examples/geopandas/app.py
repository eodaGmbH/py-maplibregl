import sys
import webbrowser

from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.sources import GeoJSONSource
from maplibre.utils import geopandas_to_geojson

import geopandas as gpd

file_name = "/tmp/pymaplibregl_temp.html"
LAYER_ID = "wilderness"

df_geo = gpd.read_file(
    "zip+https://github.com/Toblerity/Fiona/files/11151652/coutwildrnp.zip"
)

wilderness_source = GeoJSONSource(data=geopandas_to_geojson(df_geo))

wilderness_layer = Layer(
    type=LayerType.FILL,
    id=LAYER_ID,
    source=wilderness_source,
    paint={"fill-color": "darkred", "fill-opacity": 0.5},
)

map_options = MapOptions(bounds=df_geo.total_bounds)


def create_map():
    m = Map(map_options)
    m.add_layer(wilderness_layer)
    m.add_tooltip(LAYER_ID, "NAME")
    # m.add_tooltip(LAYER_ID)
    # m.add_popup(LAYER_ID, "NAME")
    return m


if __name__ == "__main__":
    m = create_map()
    if len(sys.argv) == 2:
        file_name = sys.argv[1]

    with open(file_name, "w") as f:
        f.write(m.to_html())

    webbrowser.open(file_name)
