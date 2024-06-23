# Shiny Express App

import json

from maplibre import Map, MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.controls import ControlPosition, NavigationControl
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

draw_options = {
    "displayControlsDefault": False,
    "controls": {
        "polygon": True,
        "line_string": True,
        "trash": True,
    },
}
m.add_call("addMapboxDraw", draw_options, ControlPosition.TOP_LEFT.value)

# Shiny Express
use_mapboxgl_draw()


@render_maplibregl
def maplibre():
    return m


@render.code
def selected_features():
    obj = input.maplibre_draw_selected_features()
    print(obj)
    return json.dumps(obj["features"], indent=2) if obj else "Pick some features!"


if __name__ == "__main__":
    with open("docs/examples/mapbox_draw_plugin/app.html", "w") as f:
        f.write(m.to_html())
