from maplibre import express as mx
from maplibre.expressions import interpolate
from maplibre.settings import settings

data = "https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson"

mx.circle(data).interpolate_color("mag").set_paint_props(
    circle_radius=interpolate(["zoom"], [3, 20], [2, 10])
).to_map(hash=True).save("/tmp/py-maplibre-express.html")
