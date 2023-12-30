from __future__ import annotations

from pymaplibregl import Layer, LayerType
from pymaplibregl._utils import fix_keys
from pymaplibregl.sources import SourceType


class LineLayer(Layer):
    def __init__(self, source: [dict | str], id_: str = None, *args, **kwargs):
        super().__init__(LayerType.LINE, source=source, id_=id_, *args, **kwargs)
