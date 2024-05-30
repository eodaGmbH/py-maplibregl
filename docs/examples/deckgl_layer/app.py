# Shiny Express App

from maplibre import Map, MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.ui import use_deckgl
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
    "id": "GridLayer",
    "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf-bike-parking.json",
    "extruded": True,
    "getPosition": "@@=COORDINATES",
    "getColorWeight": "@@=SPACES",
    "getElevationWeight": "@@=SPACES",
    "elevationScale": 4,
    "cellSize": 200,
    "pickable": True,
}

m.add_deck_layers([deck_grid_layer])

# Shiny Express
use_deckgl()


@render_maplibregl
def render_map():
    return m


if __name__ == "__main__":
    with open("docs/examples/deckgl_layer/app.html", "w") as f:
        f.write(m.to_html())
