from __future__ import annotations

from enum import Enum
from uuid import uuid4

from ._utils import fix_keys


class LayerType(Enum):
    CIRCLE = "circle"
    FILL = "fill"
    FILL_EXTRUSION = "fill-extrusion"
    LINE = "line"
    SYMBOL = "symbol"
    RASTER = "raster"
    HEATMAP = "heatmap"
    HILLSHADE = "hillshade"
    BACKGROUND = "background"


class Layer(object):
    def __init__(
        self,
        type_: str,
        source: [dict | str],
        id_: str = None,
        paint: dict = {},
        layout: dict = {},
        **kwargs,
    ):
        self._data = {
            "id": id_ or str(uuid4()),
            "type": type_,
            "source": source,
            "paint": paint,
            "layout": layout,
        }
        kwargs = fix_keys(kwargs)
        self._data.update(kwargs)
        self._data["type"] = LayerType(self._data["type"]).value
        for k in self._data.keys():
            if k in ["paint", "layout"]:
                self.data[k] = fix_keys(self._data[k])

    @property
    def data(self) -> dict:
        return self._data

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def id(self) -> str:
        return self._data["id"]
