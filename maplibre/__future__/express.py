from __future__ import annotations

from typing import Any, Optional, Union

from pydantic import Field, model_validator

from ..controls import NavigationControl
from ..expressions import color_match_expr, color_quantile_step_expr, interpolate
from ..layer import Layer, LayerType
from ..map import Map, MapOptions
from ..settings import settings
from ..sources import GeoJSONSource, SimpleFeatures

try:
    import geopandas as gpd
except ImportError as e:
    print(e)
    gpd = None


# ---------------
class SimpleLayer(Layer):
    sf: SimpleFeatures = Field(exclude=True)

    @model_validator(mode="before")
    def validate_this(cls, data: Any) -> Any:
        data["source"] = data["sf"].to_source()
        if "paint" not in data:
            layer_type = LayerType(data["type"]).value
            data["paint"] = {f"{layer_type}-color": settings.fallback_color}

        return data

    def _set_paint_property(self, prop, value):
        layer_type = LayerType(self.type).value
        self.paint[f"{layer_type}-{prop}"] = value

    def color_category(self, column: str, cmap: str = settings.cmap) -> SimpleLayer:
        expr = color_match_expr(column, categories=self.sf.data[column], cmap=cmap)
        self._set_paint_property("color", expr)
        return self

    def color_quantile(
        self,
        column: str,
        probs: list = [0.1, 0.25, 0.5, 0.75],
        cmap: str = settings.cmap,
    ) -> SimpleLayer:
        expr = color_quantile_step_expr(
            column, probs, values=self.sf.data[column], cmap=cmap
        )
        self._set_paint_property("color", expr)
        return self

    def interpolate_color(
        self, column: str, stops=None, colors=("yellow", "red")
    ) -> SimpleLayer:
        stops = stops or [f(self.sf.data[column]) for f in [min, max]]
        expr = interpolate(column, stops, colors)
        self._set_paint_property("color", expr)
        return self

    def to_map(
        self,
        mao_options: MapOptions = MapOptions(),
        controls: list = None,
        tooltip: bool = True,
    ) -> Map:
        controls = controls or [NavigationControl()]
        mao_options.bounds = self.sf.bounds
        m = Map(mao_options, layers=[self], controls=controls)
        if tooltip:
            m.add_tooltip(self.id)

        return m


def _create_prop_key(layer_type: str, prop: str) -> str:
    return "-".join([layer_type, prop])


def fill(data: gpd.GeoDataFrame | str, **kwargs) -> SimpleLayer:
    return SimpleLayer(type=LayerType.FILL, sf=SimpleFeatures(data), **kwargs)
