from __future__ import annotations

try:
    from geopandas import GeoDataFrame, read_file
except ImportError as e:
    print(e)
    GeoDataFrame = None
    read_file = None

from . import basemaps
from .color_utils import *
from .controls import *
from .layer import Layer, LayerType
from .map import Map, MapOptions
from .sources import GeoJSONSource
from .utils import geopandas_to_geojson


class CoreLayer(object):
    def __init__(
        self,
        data: GeoDataFrame | str,
        layer_type: LayerType | str,
        color_column: str = None,
        cmap: str = "viridis",
        **kwargs,
    ):
        if isinstance(data, str):
            data = read_file(data)

        self.bounds = data.total_bounds
        kwargs["type"] = layer_type
        self._layer = Layer(**kwargs)
        if color_column:
            self._color_expression = create_categorical_color_expression(
                values=data[color_column], column_name=color_column, cmap=cmap
            )
            self._layer.paint = {f"{layer_type}-color": self._color_expression}

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
