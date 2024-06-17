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


deck_column_layer = {
    "@@type": "ColumnLayer",
    "id": "ColumnLayer",
    "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/hexagons.json",
    "diskResolution": 12,
    "extruded": True,
    "radius": 250,
    "elevationScale": 5000,
    "getElevation": "@@=value",
    "getFillColor": "@@=[48, 128, value * 255, 255]",
    "getPosition": "@@=centroid",
    "pickable": True,
}
tooltip = "Centroid: {{ centroid }}\nValue: {{ value }}"
m.add_deck_layers([deck_column_layer], tooltip=tooltip)

# Shiny Express
use_deckgl()


@render_maplibregl
def render_map():
    return m


@render.code
def picking_object():
    obj = input.render_map_layer_ColumnLayer()
    print(obj)
    return obj.keys()
    # return json.dumps(obj["points"], indent=2) if obj else "Pick a feature!"


if __name__ == "__main__":
    with open("docs/examples/deckgl_layer/column_layer.html", "w") as f:
        f.write(m.to_html())
