import pytest
from maplibre.ipywidget import MapWidget


@pytest.mark.skip("enable me")
def test_maplibre_widget():
    widget = MapWidget(height=200)
    print(widget.map_options)
    print(widget.height)

    assert widget.height == "200px"
