import geopandas as gpd

# from maplibre import Map
from maplibre.__future__ import datasets, pandas_ext
from maplibre.__future__.pandas_ext import MapLibreAccessor

data = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

print(data.maplibre.to_source())

l = data.maplibre.fill().color("green")
print(l)
