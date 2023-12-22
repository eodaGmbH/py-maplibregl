import pymaplibregl as maplibre


def test_map_properties():
    # Prepare
    map_options = {"center": [0, 0], "zoom": 2}

    # Act
    map = maplibre.Map(map_options=map_options)

    # Assert
    map.data["mapOptions"]["zoom"] == 4
