## Input and output

Use `output_maplibregl` in the UI and `render_maplibregl` in the server section of your [Shiny for Python](https://github.com/posit-dev/py-shiny) app:

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

### Input events

[MapLibre for Python](https://github.com/eodaGmbH/py-maplibregl) provides the following reactive inputs:

* `input.{output_id}_clicked`: Sends coordinates of the clicked location on the map.
* `input.{output_id}_feature_clicked`: Sends the properties of the clicked feature and its layer id.
* `input.{output_id}_view_state`: Sends the current view state. Fired when the view state is changed.

### Map updates

Use `MapContext` to update your `Map` object.

### Example

```python
-8<-- "getting_started/reactivity.py"
```

Run this example:

```bash
poetry run uvicorn docs.examples.getting_started.reactivity:app --reload
```
