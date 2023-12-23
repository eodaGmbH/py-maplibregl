# py-maplibregl

This repository provides [py-shiny](https://github.com/posit-dev/py-shiny) bindings for [maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js).

## Installation

```bash
# Stable
pip install git+https://github.com/eodaGmbH/py-maplibregl

# Dev
pip install git+https://github.com/eodaGmbH/py-maplibregl@dev
```

## Getting started

```bash
curl -O https://raw.githubusercontent.com/eodaGmbH/py-maplibregl/main/examples/circle_layer/app.py

uvicorn app:app --reload
```

## Examples

* [Marker](examples/marker/app.py)
* [Circle Layer](examples/circle_layer/app.py)
* [Fill Layer](examples/fill_layer/app.py)
* [Fill-Extrusion Layer](examples/fill_extrusion_layer/app.py)

## Usage

```python
from pymaplibregl import Layer, Map, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import Carto
from shiny import App, ui

circle_layer = Layer(
    "circle",
    source={
        "type": "geojson",
        "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/arc/counties.json",
    },
    paint={"circle-color": "black"},
)

center = [-118.0931, 33.78615]

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("map", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def map():
        m = Map(style=Carto.POSITRON, center=center, zoom=7)
        m.add_layer(circle_layer)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
```

## Development

### Python

```bash
poetry install

poetry run uvicorn examples.circle_layer.app:app --reload

poetry run pytest
```

### JavaScript

```bash
npm install

npm run prettier

npm run build
```
