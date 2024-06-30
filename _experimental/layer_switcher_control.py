# Shiny Express App

import json
import webbrowser

from maplibre import Layer, LayerType, Map, MapOptions, render_maplibregl
from maplibre.basemaps import Carto
from maplibre.controls import (
    ControlPosition,
    InfoBoxControl,
    LayerSwitcherControl,
    NavigationControl,
    ScaleControl,
)
from maplibre.sources import GeoJSONSource
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
layer_id = "this-is-a-very-log-id-for-my-awesome-layer"
m.add_layer(
    Layer(
        type=LayerType.LINE,
        id=layer_id,
        source=GeoJSONSource(
            data="https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart.geo.json"
        ),
        paint={"line-width": 4, "line-color": "red", "line-opacity": 0.55},
    )
)
m.add_control(NavigationControl())
m.add_control(ScaleControl(), ControlPosition.BOTTOM_LEFT)

m.add_call(
    "addControl",
    "LayerOpacityControl",
    {
        "layerIds": ["water", layer_id],
        "toggleLayers": True,
        # "cssText": "padding: 20px; font-size: 20px;font-family: monospace;",
        # "content": "<h1>Awesome control.</h1><p>And some text.</p>",
    },
    ControlPosition.TOP_LEFT.value,
)

m.add_control(InfoBoxControl(content="Toggle layers"), ControlPosition.TOP_LEFT)
m.add_control(
    LayerSwitcherControl(
        layer_ids=["water", layer_id],
        theme="default",
        # css_text="padding: 10px; border: 1px solid black; border-radius: 3x;font-size: 15px;",
    ),
    ControlPosition.TOP_LEFT,
)


@render_maplibregl
def maplibre():
    return m


@render.code
def selected_features():
    obj = input.maplibre_draw_features_selected()
    print(obj)
    return json.dumps(obj["features"], indent=2) if obj else "Pick some features!"


if __name__ == "__main__":
    filename = "docs/examples/mapbox_draw_plugin/app.html"
    with open(filename, "w") as f:
        f.write(m.to_html())

    webbrowser.open(filename)
