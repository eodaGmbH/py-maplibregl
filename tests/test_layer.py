import pytest
from pymaplibregl import Layer
from pymaplibregl.layer import LayerModel, LayerType
from pymaplibregl.sources import GeoJSONSource, Source


def test_layer():
    # Act
    layer = Layer(
        "fill", source="test", source_layer="countries", paint={"fill_color": "red"}
    )

    # print(layer.data)

    # Assert
    assert "source-layer" in layer.data
    assert "fill-color" in layer.data["paint"]


def test_layer_model_keys():
    # Act
    layer = LayerModel(
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


def test_layer_model_geojson_source():
    # Prepare
    source = GeoJSONSource(data="https://raw.githubusercontent.com")

    # Act
    layer = LayerModel(type=LayerType.FILL, source=source)
    print(layer)

    # Assert
    assert layer.to_dict()["source"] == {
        "type": "geojson",
        "data": "https://raw.githubusercontent.com",
    }


def test_layer_model_str_source():
    # Prepare
    source_id = "some-id"

    # Act
    layer = LayerModel(type=LayerType.CIRCLE, source=source_id)
    print(layer.to_dict())

    assert layer.to_dict()["source"] == source_id


def test_layer_model_dict_source():
    # Prepare
    source = {"type": "geojson", "data": "https://raw.githubusercontent.com"}

    # Act
    layer = LayerModel(type="fill-extrusion", source=source)
    print(layer.to_dict())

    # Assert
    assert layer.to_dict()["source"] == source


def test_layer_type():
    # Prepare
    source = "test"

    # Act
    layer = Layer("fill", source)

    # Assert
    assert layer.type == "fill"


def test_bad_layer_type():
    # Prepare
    source = "test"

    # Act
    with pytest.raises(ValueError) as e:
        _ = Layer("block", source)

    # Assert
    assert str(e.value) == "'block' is not a valid LayerType"
