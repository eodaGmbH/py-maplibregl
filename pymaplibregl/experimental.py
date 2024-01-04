from __future__ import annotations

from pydantic import BaseModel, Field, model_serializer

from pymaplibregl import Layer, LayerType


class LineLayer(Layer):
    def __init__(self, source: [dict | str], id_: str = None, *args, **kwargs):
        super().__init__(LayerType.LINE, source=source, id_=id_, *args, **kwargs)


class PydanticSer(BaseModel):
    a: int = Field(..., serialization_alias="aa")
    b: int

    # @model_serializer
    def to_dict(self):
        return self.model_dump() | {"type": self.__class__.__name__}

    # @model_serializer
    def model_dump(self):
        return super().model_dump(by_alias=True) | {"type": self.__class__.__name__}
