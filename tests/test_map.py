import pymaplibregl as maplibre
from pymaplibregl.basemaps import Carto, construct_carto_basemap_url
from pymaplibregl.map import MapOptions


# TODO: Remove when refactoring of Map class is finished
def test_kwargs_map_options():
    # Prepare
    map_options = {"center": [0, 0], "zoom": 2}

    # Act
    map = maplibre.Map(**map_options)
    print("dict map", dict(map))

    # Assert
    assert map.to_dict()["mapOptions"] == map_options | {
        "style": "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
    }


def test_default_map_options():
    map_options = MapOptions()

    assert (
        map_options.to_dict()["style"]
        == "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
    )


def test_map_options():
    # Prepare
    style = Carto.POSITRON
    # print(style)
    # basemap_url = construct_carto_basemap_url(style)

    # Act
    map_options = MapOptions(style=style)
    # print(map_options)
    print(map_options.to_dict())

    # Assert
    assert (
        map_options.to_dict()["style"]
        == "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
    )


def test_map_layers():
    # Prepare
    layer = {"id": "test", "type:": "fill"}
    map = maplibre.Map()

    # Act
    map.add_layer(layer)
    layers = map.layers

    # Assert
    assert len(layers) == 1
    assert layers[0]["id"] == "test"
    assert len(map.to_dict()["calls"]) == 1


def test_map_markers():
    # Prepare
    marker = maplibre.controls.Marker(lng_lat=(0, 0), popup={"text": "Hello"})

    # Act
    map = maplibre.Map()
    map.add_marker(marker)
    markers = [
        item["data"] for item in map.to_dict()["calls"] if item["name"] == "addMarker"
    ]
    print(markers)

    # Assert
    assert len(markers) == 1
    assert markers[0]["lngLat"] == (0, 0)
