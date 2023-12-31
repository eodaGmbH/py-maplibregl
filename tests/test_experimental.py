from pymaplibregl.experimental import PydanticSer


def test_pydantic_model():
    m = PydanticSer(a=1, b=2)

    print(m)
    print(m.model_dump())
    print(dict(m))
    print(m.to_dict())
