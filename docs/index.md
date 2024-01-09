# MapLibre for Python

[MapLibre for Python](https://github.com/eodaGmbH/py-maplibregl) provides Python bindings for [MapLibre GL JS](https://github.com/maplibre/maplibre-gl-js).

It integrates seamlessly into [Shiny for Python](https://github.com/posit-dev/py-shiny) and [Jupyter](https://jupyter.org/).

## Installation

```bash
# Stable
pip install git+https://github.com/eodaGmbH/py-maplibregl

# Dev
pip install git+https://github.com/eodaGmbH/py-maplibregl@dev
```

## Basic usage

### Standalone

```python
-8<-- "getting_started/basic_usage.py"
```

### Shiny integration

```python
-8<-- "getting_started/basic_usage_shiny.py"
```

### Jupyter widget

```Python
from maplibre.ipywidget import MapWidget as Map

m = Map()
m
```