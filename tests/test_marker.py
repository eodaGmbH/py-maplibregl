from maplibre.controls import Marker, MarkerOptions, Popup


def test_marker():
    # Prepare
    options = MarkerOptions(color="green")

    # Act
    marker = Marker(lng_lat=(0, 0), options=options)
    print(marker.to_dict())

    # assert marker.to_dict()["options"] == {"color": "green"}
    assert marker.to_dict() == {"lngLat": (0, 0), "options": {"color": "green"}}


def test_marker_popup():
    popup = Popup(text="Hello World")
    print(popup.to_dict())

    marker = Marker(lng_lat=(0, 0), popup=popup)

    print(marker.to_dict())

    assert marker.to_dict()["popup"] == popup.to_dict()
