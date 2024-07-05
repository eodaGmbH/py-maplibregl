from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel as PydanticBaseModel

from .basemaps import Carto
from .controls import *
from .layer import Layer, LayerType
from .map import Map, MapOptions
from .mplt_colormaps import ColorBrewer
from .settings import default_layer_styles, default_layer_types
from .sources import GeoJSONSource
from .utils import geopandas_to_geojson

try:
    import geopandas as gpd
    import pandas as pd
    from geopandas import read_file
except ImportError as e:
    print(e)
    gpd = None
    pd = None

COLOR_COLUMN = "_color"
DEFAULT_CMAP = "viridis"


def get_centroid(data: gpd.GeoDataFrame) -> tuple:
    centroid = data.dissolve().centroid[0]
    return centroid.x, centroid.y


class LayerOptions(PydanticBaseModel):
    paint: Optional[dict] = None
    type: Optional[str] = None
    id: Optional[str] = None
    filter: Optional[list] = None


def create_layer(
    data: gpd.GeoDataFrame,
    color_column: str = None,
    bins: Any = None,
    cmap: str = DEFAULT_CMAP,
    options: LayerOptions = LayerOptions(),
) -> Layer:
    if str(data.crs) != "EPSG:4326":
        data = data.to_crs("EPSG:4326")

    if color_column:
        if bins:
            data[COLOR_COLUMN], codes, _ = ColorBrewer(cmap).numeric(
                data[color_column], bins
            )
        else:
            data[COLOR_COLUMN], codes, _ = ColorBrewer(cmap).factor(data[color_column])

    layer_type = options.type or default_layer_types[data.type[0].lower()]
    paint = options.paint or default_layer_styles[layer_type]["paint"]
    if color_column:
        paint[f"{layer_type}-color"] = ["get", COLOR_COLUMN]

    layer = Layer(
        id=options.id,
        type=LayerType(layer_type).value,
        source=GeoJSONSource(data=geopandas_to_geojson(data)),
        paint=paint,
        filter=options.filter,
    )

    return layer


@pd.api.extensions.register_dataframe_accessor("maplibre")
class _MapLibreGL(object):
    def __init__(self, gdf: gpd.GeoDataFrame):
        self._gdf = gdf

    def to_source(self) -> GeoJSONSource:
        return GeoJSONSource(data=geopandas_to_geojson(self._gdf))

    def to_layer(
        self,
        color_column: str = None,
        bins: Any = None,
        cmap: str = DEFAULT_CMAP,
        layer_options: LayerOptions = LayerOptions(),
    ) -> Layer:
        return create_layer(
            self._gdf, color_column, bins=bins, cmap=cmap, options=layer_options
        )

    def to_map(self, color_column: str = None, bins: Any = None, **kwargs) -> Map:
        return create_map(self._gdf, color_column, bins, **kwargs)


def _create_tooltip_template(tooltip_props) -> str:
    template = "<br>".join([f"{prop}: " + "{{" + prop + "}}" for prop in tooltip_props])
    return template


def create_map(
    data: gpd.GeoDataFrame | str,
    color_column: str = None,
    bins: Any = None,
    cmap: str = DEFAULT_CMAP,
    style=Carto.POSITRON,
    controls: list = [NavigationControl()],
    fit_bounds: bool = True,
    tooltip: bool = True,
    tooltip_props: list = None,
    map_class=Map,
    layer_options: LayerOptions = LayerOptions(),
    ret_layer_id: bool = False,
    map_options=None,
) -> Map | tuple[Map, str]:
    if type(data) is str:
        data = gpd.read_file(data)

    map_options = map_options or MapOptions()
    if style:
        map_options.style = style

    if fit_bounds:
        map_options.bounds = data.total_bounds

    m = map_class(map_options)
    for control in controls:
        m.add_control(control)

    layer = create_layer(
        data, color_column, bins=bins, cmap=cmap, options=layer_options
    )
    m.add_layer(layer)

    if tooltip:
        template = None
        if tooltip_props:
            template = _create_tooltip_template(tooltip_props)

        m.add_tooltip(layer.id, template=template)

    if ret_layer_id:
        return m, layer.id

    return m
