# DEPRECATED:
# See maplibre.__future__.express for new version

from __future__ import annotations

try:
    import pandas as pd
    from geopandas import GeoDataFrame, read_file
except ImportError as e:
    print(e)
    pd = None
    GeoDataFrame = None
    read_file = None

from maplibre.controls import *
from maplibre.layer import Layer, LayerType
from maplibre.map import Map, MapOptions
from maplibre.sources import GeoJSONSource
from maplibre.utils import geopandas_to_geojson

from _deprecated.color_utils import *

CRS = "EPSG:4326"
DEFAULT_COLOR = "darkred"

if pd is not None:

    @pd.api.extensions.register_dataframe_accessor("maplibre")
    class MapLibreAccessor(object):
        def __init__(self, gdf: GeoDataFrame):
            self._gdf = gdf

        def to_source(self) -> GeoJSONSource:
            return GeoJSONSource(data=geopandas_to_geojson(self._gdf))


class GeoJSON(object):
    def __init__(
        self,
        data: GeoDataFrame | str,
        layer_type: LayerType | str,
        color_column: str = None,
        cmap: str = "viridis",
        n: int = None,
        q: list = None,
        breaks: list = None,
        **kwargs,
    ):
        if isinstance(data, str):
            data = read_file(data)

        if str(data.crs) != CRS:
            data = data.to_crs(CRS)

        self.bounds = data.total_bounds

        # Create layer
        layer_type = LayerType(layer_type).value
        kwargs["type"] = layer_type
        if "paint" not in kwargs:
            kwargs["paint"] = {f"{layer_type}-color": DEFAULT_COLOR}

        self._layer = Layer(**kwargs)

        # Set color expression
        # TODO: Extract this step to separate function
        if color_column:
            _breaks = None
            _categories = None
            if n is not None:
                color_expression, _breaks, _colors = create_numeric_color_expression(
                    values=data[color_column], n=n, column_name=color_column, cmap=cmap
                )
            elif breaks is not None:
                color_expression, _breaks, _colors = (
                    create_numeric_color_expression_from_breaks(
                        column_name=color_column, breaks=breaks, cmap=cmap
                    )
                )
            elif q is not None:
                color_expression, _breaks, _colors = (
                    create_numeric_color_expression_from_quantiles(
                        values=data[color_column],
                        q=q,
                        column_name=color_column,
                        cmap=cmap,
                    )
                )
            else:
                color_expression, _categories, _colors = (
                    create_categorical_color_expression(
                        values=data[color_column], column_name=color_column, cmap=cmap
                    )
                )

            self._layer.paint[f"{layer_type}-color"] = color_expression

        self._layer.source = GeoJSONSource(data=geopandas_to_geojson(data))

    @property
    def layer(self):
        return self._layer

    def to_map(
        self,
        fit_bounds: bool = True,
        tooltip: bool = True,
        controls: list = [NavigationControl()],
        before_id: str = None,
        **kwargs,
    ):
        map_options = MapOptions(**kwargs)
        if fit_bounds:
            map_options.bounds = self.bounds

        m = Map(map_options)
        for control in controls:
            m.add_control(control)

        m.add_layer(self._layer, before_id)
        if tooltip:
            m.add_tooltip(self._layer.id)

        return m


class Circle(GeoJSON):
    def __init__(
        self,
        data: GeoDataFrame | str,
        color_column: str = None,
        cmap: str = "viridis",
        n: int = None,
        q: list = None,
        breaks: list = None,
        **kwargs,
    ):
        super().__init__(
            data, LayerType.CIRCLE, color_column, cmap, n, q, breaks, **kwargs
        )


class Fill(GeoJSON):
    def __init__(
        self,
        data: GeoDataFrame | str,
        color_column: str = None,
        cmap: str = "viridis",
        n: int = None,
        q: list = None,
        breaks: list = None,
        fill_outline_color: str = None,
        **kwargs,
    ):
        if "paint" not in kwargs and fill_outline_color is not None:
            kwargs["paint"] = {"fill-outline-color": fill_outline_color}

        super().__init__(
            data, LayerType.FILL, color_column, cmap, n, q, breaks, **kwargs
        )


class Line(GeoJSON):
    def __init__(
        self,
        data: GeoDataFrame | str,
        color_column: str = None,
        cmap: str = "viridis",
        n: int = None,
        q: list = None,
        breaks: list = None,
        **kwargs,
    ):
        super().__init__(
            data, LayerType.LINE, color_column, cmap, n, q, breaks, **kwargs
        )


class FillExtrusion(GeoJSON):
    def __init__(
        self,
        data: GeoDataFrame | str,
        color_column: str = None,
        cmap: str = "viridis",
        n: int = None,
        q: list = None,
        breaks: list = None,
        fill_extrusion_height: Any = None,
        # fill_extrusion_base: Any = None
        **kwargs,
    ):
        super().__init__(
            data, LayerType.FILL_EXTRUSION, color_column, cmap, n, q, breaks, **kwargs
        )
        if fill_extrusion_height:
            if isinstance(fill_extrusion_height, str):
                fill_extrusion_height = ["get", fill_extrusion_height]

            self._layer.paint["fill-extrusion-height"] = fill_extrusion_height
