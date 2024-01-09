# Pymaplibregl

Pymaplibregl provides Python bindings for [maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js).

It integrates seamlessly into [py-shiny](https://github.com/posit-dev/py-shiny) and [Jupyter](https://jupyter.org/).

## Installation

```bash
# Stable
pip install git+https://github.com/eodaGmbH/py-maplibregl

# Dev
pip install git+https://github.com/eodaGmbH/py-maplibregl@dev
```

## Getting started

* [Basic usage](https://eodagmbh.github.io/py-maplibregl/)
* [API Documentation](https://eodagmbh.github.io/py-maplibregl/api/map/)
* [Examples](https://eodagmbh.github.io/py-maplibregl/examples/every_person_in_manhattan/)

## Development

### Python

```bash
poetry install

poetry run uvicorn examples.circle_layer.app:app --reload

poetry run pytest

poetry run pytest --doctest-modules maplibre
```

### JavaScript

```bash
npm install

npm run prettier

npm run build
```
