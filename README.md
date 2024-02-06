# MapLibre for Python

[![Release](https://img.shields.io/github/v/release/eodaGmbH/py-maplibregl)](https://img.shields.io/github/v/release/eodaGmbH/py-maplibregl)
[![pypi](https://img.shields.io/pypi/v/maplibre.svg)](https://pypi.python.org/pypi/maplibre)
[![Build status](https://img.shields.io/github/actions/workflow/status/eodaGmbH/py-maplibregl/pytest.yml?branch=main)](https://img.shields.io/github/actions/workflow/status/eodaGmbH/py-maplibregl/pytest.yml?branch=main)
[![License](https://img.shields.io/github/license/eodaGmbH/py-maplibregl)](https://img.shields.io/github/license/eodaGmbH/py-maplibregl)

MapLibre for Python provides Python bindings for [MapLibre GL JS](https://github.com/maplibre/maplibre-gl-js).

It integrates seamlessly into [Shiny for Python](https://github.com/posit-dev/py-shiny) and [Jupyter](https://jupyter.org/).

## Installation

```bash
# Stable
pip install maplibre

pip install "maplibre[all]"

# Dev
pip install git+https://github.com/eodaGmbH/py-maplibregl@dev

pip install "maplibre[all] @ git+https://github.com/eodaGmbH/py-maplibregl@dev"
```

## Getting started

```bash
docker run --rm -p 8050:8050 ghcr.io/eodagmbh/py-maplibregl/vancouver-blocks:latest
```

* [Basic usage](https://eodagmbh.github.io/py-maplibregl/)
* [API Documentation](https://eodagmbh.github.io/py-maplibregl/api/map/)
* [Examples](https://eodagmbh.github.io/py-maplibregl/examples/every_person_in_manhattan/)

## Development

### Python

```bash
poetry install

poetry run pytest

poetry run pytest --ignore=maplibre/ipywidget.py --doctest-modules maplibre
```

### JavaScript

```bash
npm install

npm run prettier

npm run build

npm run build-ipywidget
```
