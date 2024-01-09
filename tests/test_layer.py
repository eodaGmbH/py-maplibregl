# import pytest
from maplibre.layer import Layer, LayerType
from maplibre.sources import GeoJSONSource, Source


def test_layer_keys():
    # Act
    layer = Layer(
        type=LayerType.FILL,
        source="test",
        source_layer="test-layer",
        paint={"some_paint_key": "test_value"},
        layout={"some_layout_key": "test_value"},
    )

    layer_dict = layer.to_dict()
    print(layer_dict)

    # Assert
    assert "source-layer" in layer_dict
    assert layer_dict["paint"] == {"some-paint-key": "test_value"}
    assert layer_dict["layout"] == {"some-layout-key": "test_value"}


def test_layer_geojson_source():
    # Prepare
    source = GeoJSONSource(data="https://raw.githubusercontent.com")

    # Act
    layer = Layer(type=LayerType.FILL, source=source)
    print(layer)

    # Assert
    assert layer.to_dict()["source"] == {
        "type": "geojson",
        "data": "https://raw.githubusercontent.com",
    }


def test_layer_str_source():
    # Prepare
    source_id = "some-id"

    # Act
    layer = Layer(type=LayerType.CIRCLE, source=source_id)
    print(layer.to_dict())

    assert layer.to_dict()["source"] == source_id


def test_layer_dict_source():
    # Prepare
    source = {"type": "geojson", "data": "https://raw.githubusercontent.com"}

    # Act
    layer = Layer(type="fill-extrusion", source=source)
    print(layer.to_dict())

    # Assert
    assert layer.to_dict()["source"] == source
