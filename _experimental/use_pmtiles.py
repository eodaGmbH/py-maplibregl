from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.pmtiles_utils import DemoPMTiles, PMTiles

tiles = PMTiles(DemoPMTiles.pmtiles_io_ugs_mt_whitney)
# tiles = PMTiles(DemoPMTiles.pmtiles_io_stamen)
raster_source = tiles.to_source()

m = Map(MapOptions(bounds=tiles.header.bounds))
m.add_layer(Layer(type=LayerType.RASTER, source=raster_source))
m.save("/tmp/py-maplibre-express.html", preview=True)
