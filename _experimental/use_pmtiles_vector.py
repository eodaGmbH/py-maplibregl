from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.pmtiles_utils import DemoPMTiles, PMTiles

tiles = PMTiles(DemoPMTiles.pmtiles_io_vector_firenze_base_layer)
map_options = MapOptions(bounds=tiles.header.bounds)
source = tiles.to_source()
print(source)

layer = Layer(
    id="roads",
    source="pmtiles",
    source_layer="roads",
    type=LayerType.LINE,
    paint={"line-color": "pink"},
)

m = Map(map_options)
m.add_source("pmtiles", source)
m.add_layer(layer)
m.save("/tmp/py-maplibre-express.html", preview=True)
