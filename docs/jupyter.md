Use `MapWidget` in your [Juyper](https://jupyter.org/) Notebook:

```python
import ipywidgets as widgets

from maplibre import MapOptions, Layer, LayerType
from maplibre.sources import GeoJSONSource
from maplibre.controls import ScaleControl, Marker
from maplibre.ipywidget import MapWidget as Map

# Create a source
earthquakes = GeoJSONSource(
    data="https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson"
)

# Create a layer
layer_id = "earthquakes"

earthquake_circles = Layer(
    type=LayerType.CIRCLE,
    id=layer_id,
    source=earthquakes,
    paint={"circle-color": "yellow"}
)

# Render map
m = Map()
m.add_control(ScaleControl(), position="bottom-left")
m.add_layer(earthquake_circles)
m.add_tooltip(layer_id, "mag")
m.add_marker(Marker(lng_lat=(100.507, 13.745)))
m

# Change radius
widgets.interact(
    lambda radius: m.set_paint_property(layer_id, "circle-radius", radius),
    radius=5
)

# Change color
widgets.interact(
    lambda color: m.set_paint_property(layer_id, "circle-color", color),
    color=["green", "yellow", "orange", "red"]
)

# Set filter on magnitude
widgets.interact(
    lambda mag_min: m.set_filter(layer_id, [">=", ["get", "mag"], mag_min]),
    mag_min=3
)

# Observe map-on-click event
from IPython.display import clear_output

output = widgets.Output()


def log_lng_lat(lng_lat):
    with output:
        clear_output()
        print(lng_lat.new)


m.observe(log_lng_lat, names="lng_lat")
output
```
