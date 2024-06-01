# Shiny Express App

import json

from maplibre import Map, MapContext, MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.ui import use_deckgl
from shiny import reactive
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

layer_id = "GridLayer"

CELL_SIZES = [100, 200, 300]
DEFAULT_CELL_SIZE = CELL_SIZES[1]


def deck_grid_layer(cell_size: int = DEFAULT_CELL_SIZE):
    return {
        "@@type": layer_id,
        "id": "GridLayer",
        "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf-bike-parking.json",
        "extruded": True,
        "getPosition": "@@=COORDINATES",
        "getColorWeight": "@@=SPACES",
        "getElevationWeight": "@@=SPACES",
        "elevationScale": 4,
        "cellSize": cell_size,
        "pickable": True,
    }


m.add_deck_layers([deck_grid_layer()], tooltip="Number of points: {{ count }}")

# Shiny Express
use_deckgl()

ui.input_select(
    "cell_size", "Cell size", choices=CELL_SIZES, selected=DEFAULT_CELL_SIZE
)
ui.input_action_button("update_layer", "Update layer")


@render_maplibregl
def render_map():
    return m


@render.code
def picking_object():
    obj = input.render_map_layer_GridLayer()
    print(obj)
    # return json.dumps(obj, indent=2) if obj else "Pick a feature!"
    # return f"{obj['count']}" if obj else "Pick a feature!"
    return json.dumps(obj["points"], indent=2) if obj else "Pick a feature!"


@reactive.Effect
@reactive.event(input.update_layer)
async def update_layer():
    print(input.update_layer())
    async with MapContext("render_map") as m:
        m.set_deck_layers([deck_grid_layer(input.cell_size())])


if __name__ == "__main__":
    with open("docs/examples/deckgl_layer/app.html", "w") as f:
        f.write(m.to_html())
