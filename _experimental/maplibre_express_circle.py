from maplibre import express as mx
from maplibre.__future__ import datasets
from maplibre.settings import settings

settings.fallback_color = "steelblue"

data = datasets.DataSets.earthquakes.url
# data = "/home/stefan/tmp/vancouver-blocks.json"

# l = mx.fill(data)
# print(l)

# layer = mx.circle(data).color_quantile("mag", cmap="YlOrRd").opacity(0.7)
# layer = mx.circle(data).interpolate_color("mag").opacity(0.7)
layer = mx.circle(data).color_bin("mag", [0, 1, 2, 3])
# print(layer.to_dict())
m = layer.to_map()
# m = mx.fill(data).interpolate_color("growth", (0, 1)).to_map()
# m = mx.fill(data).color("green").opacity(0.5).to_map()
print(m.map_options)
m.save("/tmp/py-maplibre-express.html")
