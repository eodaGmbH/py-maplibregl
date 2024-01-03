from pymaplibregl import Layer, LayerType, Map, MapOptions
from pymaplibregl.sources import GeoJSONSource

m = Map(MapOptions())

with open("tmp/index.html", "w") as f:
    f.write(m.to_html())
