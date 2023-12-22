from pymaplibregl import Layer


def test_layer():
    # Act
    layer = Layer(
        "fill", source="test", source_layer="countries", paint={"fill_color": "red"}
    )

    # print(layer.data)

    # Assert
    assert "source-layer" in layer.data
    assert "fill-color" in layer.data["paint"]
