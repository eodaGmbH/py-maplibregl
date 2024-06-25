# Shiny Express App

import json
import webbrowser

from maplibre import Map, MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.controls import ControlPosition, NavigationControl
from maplibre.ui import use_mapboxgl_draw

# from shiny import reactive
from shiny.express import input, render, ui

geojson_feature = {
    "id": "xyz",
    "type": "Feature",
    "properties": {},
    "geometry": {
        "coordinates": [
            [
                [-122.4523683552298, 37.775540942000546],
                [-122.41910082339776, 37.75932501909665],
                [-122.43487191413453, 37.72543546737114],
                [-122.46053073611722, 37.729612763886834],
                [-122.4523683552298, 37.775540942000546],
            ]
        ],
        "type": "Polygon",
    },
}

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
m.add_call(
    "addMapboxDraw", draw_options, ControlPosition.TOP_LEFT.value, geojson_feature
)

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
    filename = "docs/examples/mapbox_draw_plugin/app.html"
    with open(filename, "w") as f:
        f.write(m.to_html())

    webbrowser.open(filename)
