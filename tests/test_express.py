import maplibre.express as mx
from maplibre.layer import Layer
from maplibre.settings import settings
from maplibre.sources import SimpleFeatures


def test_circle():
    # Prepare
    data_url = "https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson"

    # Act
    layer = mx.circle(data_url)
    print(layer.source)
    print(layer)

    # Assert
    assert isinstance(layer, Layer)
    assert layer.source["data"] == data_url
    assert isinstance(layer.sf, SimpleFeatures)


def test_fill():
    # Prepare
    settings.fill_outline_color = None
    data_url = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_1_states_provinces.geojson"

    # Act
    layer = mx.fill(data_url)
    print(layer.paint)

    assert isinstance(layer, Layer)
    assert "fill-outline-color" not in layer.paint
