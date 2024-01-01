from pymaplibregl.controls import Marker, MarkerOptions


def test_marker():
    # Prepare
    options = MarkerOptions(color="green")

    # Act
    marker = Marker(lng_lat=(0, 0), options=options)
    print(marker.to_dict())

    # assert marker.to_dict()["options"] == {"color": "green"}
    assert marker.to_dict() == {"lngLat": (0, 0), "options": {"color": "green"}}
