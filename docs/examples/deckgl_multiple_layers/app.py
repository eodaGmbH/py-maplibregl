# Shiny Express App

import requests as req
from maplibre import Map, MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.controls import NavigationControl
from maplibre.ui import use_deckgl
from shiny.express import input, render, ui

data = req.get(
    "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_airports.geojson"
).json()

m = Map(
    MapOptions(
        style=Carto.POSITRON,
        center=(0.45, 51.47),
        zoom=4,
        hash=True,
        pitch=30,
    )
)
m.add_control(NavigationControl())

deck_geojson_layer = {
    "@@type": "GeoJsonLayer",
    "id": "airports",
    "data": data,
    "filled": True,
    "pointRadiusMinPixels": 2,
    "pointRadiusScale": 2000,
    "getPointRadius": "@@=11 - properties.scalerank",
    "getFillColor": [200, 0, 80, 180],
    "autoHighlight": True,
    "pickable": True,
}

deck_arc_layer = {
    "@@type": "ArcLayer",
    "id": "arcs",
    "data": [
        feature
        for feature in data["features"]
        if feature["properties"]["scalerank"] < 4
    ],
    "getSourcePosition": [-0.4531566, 51.4709959],  # London
    "getTargetPosition": "@@=geometry.coordinates",
    "getSourceColor": [0, 128, 200],
    "getTargetColor": [200, 0, 80],
    "getWidth": 2,
    "pickable": True,
}

m.add_deck_layers(
    [deck_geojson_layer, deck_arc_layer],
    tooltip={
        "airports": "{{ &properties.name }}",
        "arcs": "gps_code: {{ properties.gps_code }}",
    },
)

# Shiny Express
use_deckgl()


@render_maplibregl
def render_map():
    return m


if __name__ == "__main__":
    with open("docs/examples/deckgl_multiple_layers/app.html", "w") as f:
        f.write(m.to_html())
