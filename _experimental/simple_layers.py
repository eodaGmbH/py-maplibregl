from __future__ import annotations

from typing import TypeVar

from maplibre import Layer, LayerType
from maplibre._utils import fix_keys
from maplibre.sources import GeoDataFrame, Source

MLSource = TypeVar("MLSource", Source, dict, GeoDataFrame)

DEFAULT_COLOR = "darkred"


class SimpleLayer(object):
    _layer: Layer

    def __init__(
        self, layer_type, paint_created: dict, id: str = None, **kwargs
    ) -> None:
        self._layer = Layer(type=layer_type, **kwargs)
        if id:
            self._layer.id = id

        self._layer.paint = fix_keys(paint_created)

    def to_dict(self) -> dict:
        return self._layer.to_dict()

    def set_paint_properties(self, **props) -> SimpleLayer:
        self._layer.paint.update(fix_keys(props))
        return self

    @property
    def layer(self):
        return self._layer


class Line(SimpleLayer):
    def __init__(
        self,
        line_color: str | list = None,
        line_width: int | float = 1,
        line_opacity: float = 1.0,
        source: MLSource = None,
        id: str = None,
        **kwargs,
    ):
        line_color = line_color or DEFAULT_COLOR
        paint = dict(
            line_color=line_color, line_width=line_width, line_opacity=line_opacity
        )
        super().__init__(LayerType.LINE, paint, id, source=source, **kwargs)


class Fill(SimpleLayer):
    def __init__(
        self,
        fill_color: str | list = None,
        fill_opacity: float = 1.0,
        id: str = None,
        **kwargs,
    ):
        paint = dict(
            fill_color=(fill_color or DEFAULT_COLOR), fill_opacity=fill_opacity
        )
        super().__init__(LayerType.FILL, paint, id, **kwargs)


class Circle(SimpleLayer):
    def __init__(self, circle_radius: int | float = 1.0, id: str = None, **kwargs):
        pass


class TestLayer(Layer):
    def set_paint_properties(self, **props) -> TestLayer:
        self.paint.update(fix_keys(props))
        return self

    def set_paint_properties_(
        self,
        line_color: str | list = None,
        line_opacity: int | float = 1.0,
        line_width: int | float | list = None,
        fill_color: str | list = None,
        fill_opacity: int | float = 1.0,
        fill_outline_color: str | list = None,
        **kwargs,
    ) -> TestLayer:
        props = dict(
            filter(lambda item: item[0].startswith(self.type), locals().items())
        )
        if self.paint is None:
            self.paint = fix_keys(props)
        else:
            self.paint.update(props)

        return self
