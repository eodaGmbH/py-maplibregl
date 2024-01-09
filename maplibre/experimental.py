from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_serializer

from maplibre import Layer, LayerType


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


class LayoutProperties(BaseModel):
    visibility: Literal["visible", "none"] = None
    #
    fill_sort_key: list = None  # Example: ["get", "priority"]
    #
    line_cap: Literal["butt", "round", "square"] = None
    line_join: Literal["bevel", "round", "miter"] = None
    line_miter_limit: int = None
    line_round_limit: float = None
    line_sort_key: int = None


class PaintProperties(BaseModel):
    background_color: str = None
    background_emissive_strength: int = None
    background_opacity: int = None
    background_pattern: str = None
