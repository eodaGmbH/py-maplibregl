# Shiny Express App

import requests as req
from maplibre import Layer, LayerType, Map, MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.sources import GeoJSONSource
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

maplibre_circle_layer = Layer(
    type=LayerType.CIRCLE,
    id="circles",
    paint={
        "circle-color": "orange",
        "circle-opacity": 0.7,
        "circle-radius": ["-", 11, ["get", "scalerank"]],
    },
    source=GeoJSONSource(data=data),
)

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
    "beforeId": "circles",
}

m.add_layer(maplibre_circle_layer)
m.add_tooltip("circles", "name")
m.add_deck_layers(
    [deck_arc_layer],
    tooltip={
        "arcs": "gps_code: {{ properties.gps_code }}",
    },
)

# Shiny Express
use_deckgl()


@render_maplibregl
def render_map():
    return m


if __name__ == "__main__":
    with open("docs/examples/deckgl_layer/app.html", "w") as f:
        f.write(m.to_html())
