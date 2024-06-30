import marimo

__generated_with = "0.6.23"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo

    return (mo,)


@app.cell
def __():
    from maplibre.controls import NavigationControl, ScaleControl
    from maplibre.ipywidget import MapOptions, MapWidget

    return MapOptions, MapWidget, NavigationControl, ScaleControl


@app.cell
def __():
    deck_grid_layer = {
        "@@type": "GridLayer",
        "id": "GridLayer",
        "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf-bike-parking.json",
        "extruded": True,
        "getPosition": "@@=COORDINATES",
        "getColorWeight": "@@=SPACES",
        "getElevationWeight": "@@=SPACES",
        "elevationScale": 4,
        "cellSize": 200,
        "pickable": True,
    }
    return (deck_grid_layer,)


@app.cell
def __(MapOptions):
    map_options = MapOptions(
        center=(-122.4, 37.74),
        zoom=12,
        hash=True,
        pitch=40,
    )
    return (map_options,)


@app.cell
def __(MapWidget, NavigationControl, deck_grid_layer, map_options):
    m = MapWidget(map_options)
    m.use_message_queue(False)
    m.add_control(NavigationControl())
    m.add_deck_layers([deck_grid_layer])
    m
    return (m,)


@app.cell
def __(m):
    m.clicked
    return


@app.cell
def __(m):
    m.zoom
    return


@app.cell
def __(m):
    m.center
    return


@app.cell
def __(ScaleControl, m):
    m.add_control(ScaleControl())
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
