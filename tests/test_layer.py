import pytest
from pymaplibregl import Layer
from pymaplibregl.layer import LayerModel, LayerType


def test_layer():
    # Act
    layer = Layer(
        "fill", source="test", source_layer="countries", paint={"fill_color": "red"}
    )

    # print(layer.data)

    # Assert
    assert "source-layer" in layer.data
    assert "fill-color" in layer.data["paint"]


def test_layer_model():
    # Act
    layer = LayerModel(
        type=LayerType.FILL,
        source="test",
        source_layer="countries",
        paint={"fill_color": "red"},
        layout={"some_key": "some_value"},
    )

    print(layer.to_dict())

    # Assert
    assert "source-layer" in layer.to_dict()
    assert "fill-color" in layer.to_dict()["paint"]
    assert "some-key" in layer.to_dict()["layout"]


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
