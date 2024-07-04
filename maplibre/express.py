from __future__ import annotations

from typing import Any

from pydantic import BaseModel as PydanticBaseModel

from .basemaps import Carto

# from .colors import ColorPalette
from .controls import *
from .layer import Layer, LayerType
from .map import Map, MapOptions
from .mplt_colormaps import ColorBrewer
from .settings import default_layer_styles, default_layer_types
from .sources import GeoJSONSource
from .utils import geopandas_to_geojson

try:
    import geopandas as gpd
except ImportError as e:
    print(e)
    gpd = None

COLOR_COLUMN = "_color"


def get_centroid(data: gpd.GeoDataFrame) -> tuple:
    centroid = data.dissolve().centroid[0]
    return centroid.x, centroid.y


class LayerOptions(PydanticBaseModel):
    color_column: str = None
    cmap: str = "YlOrRd"
    bins: Any = 10
    paint: dict = None
    type: str = None
    id: str = None
    filter: list = None


def create_layer(
    data: gpd.GeoDataFrame,
    color_column: str = None,
    options: LayerOptions = LayerOptions(),
) -> Layer:
    if str(data.crs) != "EPSG:4326":
        data = data.to_crs("EPSG:4326")

    if color_column:
        if type(data[color_column][0]) is not str:
            data[COLOR_COLUMN], codes, _ = ColorBrewer(options.cmap).numeric(
                data[color_column], options.bins
            )
        else:
            data[COLOR_COLUMN], codes, _ = ColorBrewer().factor(data[color_column])

    layer_type = options.type or default_layer_types[data.type[0].lower()]
    paint = options.paint or default_layer_styles[layer_type]["paint"]
    if color_column:
        paint[f"{layer_type}-color"] = ["get", COLOR_COLUMN]

    layer = Layer(
        type=LayerType(layer_type).value,
        source=GeoJSONSource(data=geopandas_to_geojson(data)),
        paint=paint,
    )

    if options.id:
        layer.id = options.id

    if options.filter:
        layer.filter = options.filter

    return layer


class GeoDataFrame(gpd.GeoDataFrame):
    def to_maplibre_source(self) -> GeoJSONSource:
        return GeoJSONSource(data=geopandas_to_geojson(self))

    def to_maplibre_layer(
        self, color_column=None, layer_options: LayerOptions = LayerOptions()
    ) -> Layer:
        return create_layer(self, color_column, layer_options)

    def to_maplibre_map(self) -> Map:
        pass


def read_file(filename: Any, **kwargs) -> GeoDataFrame:
    data = gpd.read_file(filename, **kwargs)
    return GeoDataFrame(data)


"""
def create_layer_from_geo_data_frame(
    data: gpd.GeoDataFrame,
    color: str = None,
    pal: ColorPalette = None,
    n: int = None,
    paint: dict = None,
    type_: str = None,
    id_: str = None,
    filter_: list = None,
) -> Layer:
    
    if str(data.crs) != "EPSG:4326":
        data = data.to_crs("EPSG:4326")

    if color:
        pal = pal or ColorPalette()
        n = n or 6
        if type(data[color][0]) in [int, float]:
            data[COLOR_COLUMN], codes, _ = pal.numeric(data[color], n)
        else:
            data[COLOR_COLUMN], codes, _ = pal.factor(data[color])

    type_ = type_ or default_layer_types[data.type[0].lower()]
    paint = paint or default_layer_styles[type_]["paint"]
    if color:
        paint[f"{type_}-color"] = ["get", COLOR_COLUMN]

    layer = Layer(
        type=LayerType(type_).value,
        source=GeoJSONSource(data=geopandas_to_geojson(data)),
        paint=paint,
        # TODO: Allow 'None' for 'filter' attribute in 'Layer' class
        # filter=filter_ or [],
    )
    if id_:
        layer.id = id_

    if filter_:
        layer.filter = filter_

    return layer
"""


def _create_tooltip_template(tooltip_props) -> str:
    template = "<br>".join([f"{prop}: " + "{{" + prop + "}}" for prop in tooltip_props])
    return template


def create_map(
    data: gpd.GeoDataFrame | str,
    color_column: str = None,
    style=Carto.POSITRON,
    controls: list = [NavigationControl()],
    fit_bounds: bool = True,
    tooltip: bool = True,
    tooltip_props: list = None,
    map_class=Map,
    layer_options: LayerOptions = LayerOptions(),
    ret_layer_id: bool = False,
    **kwargs,
) -> Map | tuple[Map, str]:
    map_options = MapOptions(style=style, **kwargs)
    # map_options.style = style
    if type(data) is str:
        data = gpd.read_file(data)

    if fit_bounds:
        map_options.bounds = data.total_bounds

    m = map_class(map_options)
    for control in controls:
        m.add_control(control)

    layer = create_layer(data, color_column, layer_options)
    m.add_layer(layer)

    if tooltip:
        template = None
        if tooltip_props:
            template = _create_tooltip_template(tooltip_props)

        m.add_tooltip(layer.id, template=template)

    if ret_layer_id:
        return m, layer.id

    return m
