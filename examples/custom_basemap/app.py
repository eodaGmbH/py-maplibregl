import webbrowser

from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.basemaps import construct_basemap_style
from maplibre.controls import NavigationControl
from maplibre.sources import GeoJSONSource

file_name = "docs/examples/custom_basemap/app.html"

bg_layer = Layer(
    type=LayerType.BACKGROUND,
    id="background",
    source=None,
    paint={"background-color": "darkblue", "background-opacity": 0.8},
)

countries_source = GeoJSONSource(
    data="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_0_countries.geojson"
)

lines_layer = Layer(
    type=LayerType.LINE,
    source="countries",
    paint={"line-color": "white", "line-width": 1.5},
)

polygons_layer = Layer(
    type=LayerType.FILL,
    source="countries",
    paint={"fill-color": "darkred", "fill-opacity": 0.8},
)

custom_basemap = construct_basemap_style(
    layers=[bg_layer, polygons_layer, lines_layer],
    sources={"countries": countries_source},
)


map_options = MapOptions(
    style=custom_basemap,
    center=(0, 0),
    zoom=2,
)


def create_map():
    m = Map(map_options)
    m.add_control(NavigationControl())
    m.add_layer(
        Layer(
            type=LayerType.CIRCLE,
            id="earthquakes",
            source=GeoJSONSource(
                data="https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson"
            ),
            paint={"circle-color": "yellow", "circle-radius": 5},
        )
    )
    m.add_popup("earthquakes", "mag")
    return m


if __name__ == "__main__":
    m = create_map()
    with open(file_name, "w") as f:
        f.write(m.to_html())

    webbrowser.open(file_name)
