from maplibre.__future__ import datasets
from maplibre.__future__ import express as mx
from maplibre.settings import settings
from maplibre.sources import SimpleFeatures

settings.fallback_color = "steelblue"

# data = datasets.DataSets.vancouver_blocks.url
data = "/home/stefan/tmp/vancouver-blocks.json"

# l = mx.fill(data)
# print(l)

m = mx.fill(data).color_quantile("growth", cmap="YlOrRd").to_map()
# .interpolate_color("growth", (0, 1)).to_map()
print(m.map_options)
m.save("/tmp/py-maplibre-express.html")
