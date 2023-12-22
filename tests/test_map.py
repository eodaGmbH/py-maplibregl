import pymaplibregl as maplibre


def test_map_options():
    # Prepare
    map_options = {"center": [0, 0], "zoom": 2}

    # Act
    map = maplibre.Map(**map_options)

    # Assert
    assert map.data["mapOptions"]["zoom"] == 2


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
    assert len(map.data["calls"]) == 1


def test_map_markers():
    # Prepare
    marker = {
        "lngLat": [0, 0],
        "color": "green",
        "popup": "Hello PyMapLibreGL!",
    }

    # Act
    map = maplibre.Map()
    map.add_marker(marker)
    markers = map.markers

    # Assert
    assert len(markers) == 1
    assert markers[0]["lngLat"] == [0, 0]
