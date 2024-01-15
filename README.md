# MapLibre for Python

MapLibre for Python provides Python bindings for [MapLibre GL JS](https://github.com/maplibre/maplibre-gl-js).

It integrates seamlessly into [Shiny for Python](https://github.com/posit-dev/py-shiny) and [Jupyter](https://jupyter.org/).

## Installation

```bash
# Stable
pip install git+https://github.com/eodaGmbH/py-maplibregl

# Dev
pip install git+https://github.com/eodaGmbH/py-maplibregl@dev

# Install with optional dependencies
pip install "maplibre[all] @ git+https://github.com/eodaGmbH/py-maplibregl"
```

## Getting started

* [Basic usage](https://eodagmbh.github.io/py-maplibregl/)
* [API Documentation](https://eodagmbh.github.io/py-maplibregl/api/map/)
* [Examples](https://eodagmbh.github.io/py-maplibregl/examples/every_person_in_manhattan/)

## Development

### Python

```bash
poetry install

poetry run pytest

poetry run pytest --doctest-modules maplibre
```

### JavaScript

```bash
npm install

npm run prettier

npm run build

npm run build-ipywidget
```
