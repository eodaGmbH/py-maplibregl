# py-maplibregl

## Installation

```bash
# Stable
pip install git+https://github.com/eodaGmbH/py-maplibregl

# Dev
pip install git+https://github.com/eodaGmbH/py-maplibregl@dev
```

## Getting started

```bash
curl -O https://raw.githubusercontent.com/eodaGmbH/py-maplibregl/main/examples/app1/app.py

uvicorn app:app --reload
```

## Usage

```python
from pymaplibregl import Map, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import carto_positron
from shiny import App, ui

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("map", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def map():
        m = Map(style=carto_positron(), center=[9.54, 51.31667], zoom=9)
        marker = {
            "lng_lat": [9.54, 51.31667],
            "color": "green",
            "popup": "Hello PyMapLibreGL!",
        }
        m.add_marker(**marker)
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
```

## Development

### Python

```bash
poetry install

poetry run python examples/app1/app.py

poetry run pytest
```

### JavaScript

```bash
npm install

npm run build
```
