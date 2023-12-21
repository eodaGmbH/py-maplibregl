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
from shiny import App, ui

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("map", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def map():
        m = Map(zoom=4)
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
