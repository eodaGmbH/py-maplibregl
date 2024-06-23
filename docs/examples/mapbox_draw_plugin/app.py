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
        "trash": True,
    },
}
m.add_call("addMapboxDraw", draw_options, ControlPosition.TOP_LEFT.value)

# Shiny Express
use_mapboxgl_draw()


@render_maplibregl
def render_map():
    return m


if __name__ == "__main__":
    with open("docs/examples/mapbox_draw_plugin/app.html", "w") as f:
        f.write(m.to_html())
