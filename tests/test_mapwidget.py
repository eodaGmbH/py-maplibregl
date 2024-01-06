import pytest
from pymaplibregl.ipywidget import MaplibreWidget


# @pytest.mark.skip("enable me")
def test_maplibre_widget():
    widget = MaplibreWidget(height=200)
    print(widget.map_options)
    print(widget.height)

    assert widget.height == "200px"
