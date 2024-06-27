# Shiny Express App

import json
import webbrowser

from maplibre import Map, MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.controls import ControlPosition, NavigationControl, ScaleControl
from maplibre.plugins import MapboxDrawControls, MapboxDrawOptions
from maplibre.ui import use_mapboxgl_draw

# from shiny import reactive
from shiny.express import input, render, ui

m = Map(
    MapOptions(
        style=Carto.POSITRON,
        center=(-122.4, 37.74),
        zoom=12,
        hash=True,
        pitch=40,
    )
)
m.add_control(NavigationControl())
m.add_control(ScaleControl(), ControlPosition.BOTTOM_LEFT)

# m.add_call(
#    "addControl",
#    "InfoBoxControl",
#    {
#        "cssText": "padding: 20px; font-size: 20px;font-family: monospace;",
#        "content": "<h1>Awesome control.</h1><p>And some text.</p>",
#    },
#    ControlPosition.TOP_LEFT.value,
# )

m.add_call(
    "addControl",
    "LayerSwitcherControl",
    {"layerIds": ["landcover", "water", "landuse"]},
    ControlPosition.TOP_LEFT.value,
)


@render_maplibregl
def maplibre():
    return m


@render.code
def selected_features():
    obj = input.maplibre_draw_features_selected()
    print(obj)
    return json.dumps(obj["features"], indent=2) if obj else "Pick some features!"


if __name__ == "__main__":
    filename = "docs/examples/mapbox_draw_plugin/app.html"
    with open(filename, "w") as f:
        f.write(m.to_html())

    webbrowser.open(filename)
