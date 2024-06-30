from maplibre import Map, MapOptions
from maplibre.basemaps import Carto
from maplibre.utils import save_map

m = Map(MapOptions(style=Carto.VOYAGER))
filename = save_map(m, preview=True)
print(filename)
