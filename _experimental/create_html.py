from maplibre import Map, MapOptions
from maplibre.basemaps import Carto
from maplibre.map import save_map

m = Map(MapOptions(style=Carto.VOYAGER))
filename = save_map(m, preview=True)
print(filename)
