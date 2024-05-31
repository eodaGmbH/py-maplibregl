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
        zoom=12,
        hash=True,
        pitch=40,
    )
)


deck_grid_layer = {
    "@@type": "GridLayer",
    "id": "MyAwesomeGridLayer",
    "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf-bike-parking.json",
    "extruded": True,
    "getPosition": "@@=COORDINATES",
    "getColorWeight": "@@=SPACES",
    "getElevationWeight": "@@=SPACES",
    "elevationScale": 4,
    "cellSize": 200,
    "pickable": True,
}

m.add_deck_layers([deck_grid_layer], tooltip_template="Number of points: {{ count }}")

# Shiny Express
use_deckgl()


@render_maplibregl
def render_map():
    return m


@render.code
def picking_object():
    obj = input.render_map_layer_GridLayer()
    print(obj)
    return json.dumps(obj["points"], indent=2) if obj else "Pick a feature!"


if __name__ == "__main__":
    with open("docs/examples/deckgl_layer/app.html", "w") as f:
        f.write(m.to_html())
