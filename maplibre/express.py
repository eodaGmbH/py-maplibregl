from __future__ import annotations

from typing import Any

from pydantic import Field, model_validator

from maplibre.colors import color_brewer
from maplibre.controls import NavigationControl
from maplibre.expressions import (
    GeometryType,
    color_match_expr,
    color_quantile_step_expr,
    color_step_expr,
    geometry_type_filter,
    interpolate,
)
from maplibre.layer import Layer, LayerType
from maplibre.map import Map, MapOptions
from maplibre.settings import settings
from maplibre.sources import GeoJSONSource, SimpleFeatures

try:
    import geopandas as gpd
except ImportError as e:
    print(e)
    gpd = None


# ---------------
def path_is_geojson_url(path: str) -> bool:
    if path is None:
        return False

    path = path.lower()
    return path.startswith("http") and path.endswith("json")


class SimpleLayer(Layer):
    sf: SimpleFeatures = Field(exclude=True)

    @model_validator(mode="before")
    def validate_this(cls, data: Any) -> Any:
        sf_path = data["sf"].path
        if path_is_geojson_url(sf_path):
            data["source"] = GeoJSONSource(data=sf_path)
        else:
            data["source"] = data["sf"].to_source()

        if "paint" not in data:
            layer_type = LayerType(data["type"]).value
            data["paint"] = {f"{layer_type}-color": settings.fallback_color}

        return data

    def _set_paint_property(self, prop, value):
        layer_type = LayerType(self.type).value
        self.paint[f"{layer_type}-{prop}"] = value

    def color(self, value: str | list) -> SimpleLayer:
        self._set_paint_property("color", value)
        return self

    def opacity(self, value: float) -> SimpleLayer:
        self._set_paint_property("opacity", value)
        return self

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

    def color_bin(
        self, column: str, stops: list = None, n: int = None, cmap=settings.cmap
    ) -> SimpleLayer:
        if stops is None and n is None:
            pass
        expr = color_step_expr(column, stops, cmap)
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


def circle(data: gpd.GeoDataFrame | str, **kwargs) -> SimpleLayer:
    return SimpleLayer(type=LayerType.CIRCLE, sf=SimpleFeatures(data), **kwargs)


def line(data: gpd.GeoDataFrame | str, **kwargs) -> SimpleLayer:
    pass


# TODO: Add default layers to settings
def fill_line_circle(source_id: str, colors: list = None) -> list:
    if colors is not None:
        assert len(colors) == 3
    else:
        colors = color_brewer(settings.cmap, 3)

    fill_color, line_color, circle_color = colors

    fill_layer = Layer(
        type=LayerType.FILL,
        source=source_id,
        filter=geometry_type_filter(GeometryType.POLYGON),
    ).set_paint_props(
        fill_color=fill_color, fill_outline_color=settings.fill_outline_color
    )

    line_layer = Layer(
        type=LayerType.LINE,
        source=source_id,
        filter=geometry_type_filter(GeometryType.LINE_STRING),
    ).set_paint_props(line_color=line_color)

    circle_layer = Layer(
        type=LayerType.CIRCLE,
        source=source_id,
        filter=geometry_type_filter(GeometryType.POINT),
    ).set_paint_props(circle_color=circle_color)

    return [fill_layer, line_layer, circle_layer]


def map_this(data: gpd.GeoDataFrame | str, tooltip: bool = True, **kwargs) -> Map:
    sf = SimpleFeatures(data)
    layers = fill_line_circle(sf.source_id)
    kwargs["bounds"] = sf.bounds
    map_options = MapOptions(**kwargs)
    m = Map(
        map_options,
        sources=sf.to_sources_dict(),
        layers=layers,
        controls=[NavigationControl()],
    )
    if tooltip:
        for layer in layers:
            m.add_tooltip(layer.id)

    return m
