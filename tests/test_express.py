import maplibre.express as mx
from maplibre.layer import Layer
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
