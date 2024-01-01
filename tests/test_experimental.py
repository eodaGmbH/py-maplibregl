from pymaplibregl.experimental import PydanticSer
from pymaplibregl.layer import Layer, LayerType


def test_pydantic_model():
    m = PydanticSer(a=1, b=2)

    print(m)
    print(m.model_dump())
    print(dict(m))
    print(m.to_dict())


def test_layer():
    layer = Layer(type=LayerType.LINE)
    print("line", LayerType(LayerType.LINE).value)

    print(layer.model_dump())
    # print(layer.to_dict())
