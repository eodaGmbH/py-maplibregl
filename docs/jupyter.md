Use `MapWidget` in your [Juyper](https://jupyter.org/) Notebook:

```python
import ipywidgets as widgets

from maplibre import Layer, LayerType
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
_ = widgets.interact(
    lambda radius: m.set_paint_property(layer_id, "circle-radius", radius),
    radius=(1, 8, 1)
)

# Change color
_ = widgets.interact(
    lambda color: m.set_paint_property(layer_id, "circle-color", color),
    color=["green", "yellow", "orange", "red"]
)

# Set filter on magnitude
_ = widgets.interact(
    lambda mag_min: m.set_filter(layer_id, [">=", ["get", "mag"], mag_min]),
    mag_min=(1, 8, 1)
)
```
