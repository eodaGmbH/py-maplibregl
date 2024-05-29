# Shiny Express App

import requests as req
from maplibre import Layer, LayerType, Map, MapOptions, render_maplibregl
from maplibre.basemaps import Carto, construct_carto_basemap_url
from maplibre.sources import GeoJSONSource
from maplibre.ui import use_deckgl
from shiny.express import input, render, ui

style = req.get(construct_carto_basemap_url(Carto.VOYAGER)).json()


symbol_ids = [layer["id"] for layer in style["layers"] if layer["type"] == "symbol"]
# print(symbol_ids)

urban_areas = GeoJSONSource(
    data="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson"
)

m = Map(
    MapOptions(
        style=style,
        center=(0.45, 51.47),
        # center=(-88.13734351262877, 35.137451890638886),
        zoom=11,
        hash=True,
    )
)


m.add_deck_layer(
    {
        "@@type": "ScatterplotLayer",
        "id": "deck-circle",
        "data": [{"position": [0.45, 51.47]}],
        "getPosition": "@@=position",
        "getFillColor": [255, 0, 0, 100],
        "getRadius": 100,
    }
)

"""
m.add_layer(
    Layer(
        id="urban-areas-fill",
        type=LayerType.FILL,
        source=urban_areas,
        paint={"fill-color": "pink", "fill-opacity": 1.0},
    ),
    before_id=symbol_ids[0],
)
"""

for symbol_id in symbol_ids:
    m.set_paint_property(symbol_id, "text-color", "purple")


use_deckgl()


@render_maplibregl
def render_map():
    return m


if __name__ == "__main__":
    with open("docs/examples/layer_order/app.html", "w") as f:
        f.write(m.to_html())
