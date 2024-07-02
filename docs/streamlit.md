Use `maplibre.streamlit.st_maplibre` to add a MapLibre map to your [Streamlit](https://streamlit.io/) app:

```python
import streamlit as st
from maplibre import Map, MapOptions
from maplibre.basemaps import Carto
from maplibre.controls import NavigationControl
from maplibre.streamlit import st_maplibre


def create_layer(cell_size: int = 200) -> dict:
    return {
        "@@type": "GridLayer",
        "id": "GridLayer",
        "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf-bike-parking.json",
        "extruded": True,
        "getPosition": "@@=COORDINATES",
        "getColorWeight": "@@=SPACES",
        "getElevationWeight": "@@=SPACES",
        "elevationScale": 4,
        "cellSize": cell_size,
        "pickable": True,
    }


map_options = MapOptions(
    style=Carto.POSITRON,
    center=(-122.4, 37.74),
    zoom=12,
    hash=True,
    pitch=40,
)


st.title("SF Bike Parking")

cell_size = st.slider("cell size", 100, 600, value=200, step=5)

m = Map(map_options)
m.add_control(NavigationControl())
m.add_deck_layers([create_layer(cell_size)], tooltip="Number of points: {{ count }}")

st_maplibre(m)
```
