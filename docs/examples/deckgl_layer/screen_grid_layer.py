# Shiny Express App

import json

from maplibre import Map, MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.ui import use_deckgl

# from shiny import reactive
from shiny.express import input, render, ui

m = Map(
    MapOptions(
        style=Carto.POSITRON,
        center=(-122.4, 37.74),
        zoom=11,
        hash=True,
        pitch=40,
    )
)


deck_screen_grid_layer = {
    "@@type": "ScreenGridLayer",
    "id": "MyAwesomeScreenGridLayer",
    "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf-bike-parking.json",
    "cellSizePixels": 50,
    "colorRange": [
        [0, 25, 0, 25],
        [0, 85, 0, 85],
        [0, 127, 0, 127],
        [0, 170, 0, 170],
        [0, 190, 0, 190],
        [0, 255, 0, 255],
    ],
    "getPosition": "@@=COORDINATES",
    "getWeight": "@@=SPACES",
    "opacity": 0.8,
    "pickable": True,
    # "gpuAggregation": False,
}
tooltip = "{{ weight }}"
m.add_deck_layers([deck_screen_grid_layer], tooltip=tooltip)

# Shiny Express
use_deckgl()


@render_maplibregl
def render_map():
    return m


@render.code
def picking_object():
    obj = input.render_map_layer_MyAwesomeScreenGridLayer()
    print(obj)
    return json.dumps(obj["points"], indent=2) if obj else "Pick a feature!"


if __name__ == "__main__":
    with open("docs/examples/deckgl_layer/app.html", "w") as f:
        f.write(m.to_html())
