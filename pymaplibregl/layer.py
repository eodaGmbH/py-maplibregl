from enum import Enum
from uuid import uuid4

from ._utils import fix_keys


class LayerType(Enum):
    CIRCLE = "circle"
    FILL = "fill"
    FILL_EXTRUSION = "fill-extrusion"
    LINE = "line"


class Layer(object):
    def __init__(self, type_: str, id_: str = None, **kwargs):
        self._data = {
            "id": id_ or str(uuid4()),
            "type": type_,
        }
        kwargs = fix_keys(kwargs)
        for k, v in kwargs.items():
            if k in ["paint", "layout"]:
                kwargs[k] = fix_keys(kwargs[k])
        self._data.update(kwargs)
        self._data["type"] = LayerType(self._data["type"]).value

    @property
    def data(self) -> dict:
        return self._data

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def id(self) -> str:
        return self._data["id"]
