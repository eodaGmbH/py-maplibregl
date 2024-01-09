[MapLibre for Python](https://github.com/eodaGmbH/py-maplibregl) integrates seamlessly into [Shiny for Python](https://github.com/posit-dev/py-shiny).

## Adding UI output

```python
from shiny import App, ui
from maplibre import output_maplibregl

app_ui = ui.page_fluid(
    ui.panel_title("MapLibre"),
    output_maplibregl("maplibre", height=600)
)


def server(input, output, session):
    pass


app = App(app_ui, server)
```

## Adding server logic

```python
from shiny import App, ui
from maplibre import output_maplibregl, render_maplibregl, Map

app_ui = ui.page_fluid(
    ui.panel_title("MapLibre"),
    output_maplibregl("maplibre", height=600)
)


def server(input, output, session):
    @render_maplibregl
    def maplibre():
        m = Map()
        return m


app = App(app_ui, server)
```

## Reactivity

### Inputs

[py-maplibregl](https://github.com/eodaGmbH/py-maplibregl) provides the following reactive inputs:

* `map-on-click` event: Sends the coordinates of the location that was clicked on. The name of the __input__ event corresponds to the __output id__.
    For `output_maplibregl("maplibre")` you need to listen to `input.maplibre`.
* `feature-on-click` event: Sends the properties of the feature that was clicked on. The name of the __ìnput__ is made up of the __output id__ + `layer` + __layer id__. 
    For `output_maplibregl("maplibre")` and a layer with `id=test` you need to listen to `input.maplibre_layer_test`.

### Updates

Use `MapContext` to update your map object.

### Example using inputs and updates

```python
-8<-- "getting_started/reactivity.py"
```

Run this example:

```bash
poetry run uvicorn docs.examples.getting_started.reactivity:app --reload
```
