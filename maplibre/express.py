from __future__ import annotations

from .basemaps import Carto
from .colors import ColorPalette
from .controls import *
from .layer import Layer, LayerType
from .map import Map, MapOptions
from .settings import default_layer_styles, default_layer_types
from .sources import GeoJSONSource
from .utils import geopandas_to_geojson

try:
    import geopandas as gpd
except ImportError as e:
    print(e)
    gpd = None

COLOR_COLUMN = "_color"


class _GeoDataFrameML(gpd.GeoDataFrame):
    def to_maplibre_layer(self):
        pass

    def to_maplibre_map(self):
        pass


# TODO: Use this class as parameter in 'create_map'?
class _GPDLayerOptions:
    color: str = None  # Maybe do not put this one to the options
    pal: ColorPalette = None
    n: int
    paint: dict = None
    type: str = None
    id: str = None
    filter: list = None


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
    """Create a layer from a geo(pandas) data frame"""
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


def _create_tooltip_template(tooltip_props) -> str:
    template = "<br>".join([f"{prop}: " + "{{" + prop + "}}" for prop in tooltip_props])
    return template


# TODO: How to add control positions
def create_map(
    data: gpd.GeoDataFrame | str,
    style=Carto.POSITRON,
    controls: list = [NavigationControl()],
    fit_bounds: bool = True,
    tooltip: bool = True,
    tooltip_props: list = None,
    map_options: MapOptions = MapOptions(),
    map_class=Map,
    # layer options
    color: str = None,
    layer_id: str = None,
    layer_type: str = None,
    ret_layer_id: bool = False,
    **layer_kwargs,
) -> Map | tuple[Map, str]:
    """Create a map and add a layer from a geo(pandas) data frame"""
    if type(data) is str:
        data = gpd.read_file(data)

    if fit_bounds:
        map_options.bounds = data.total_bounds

    if style:
        map_options.style = style

    m = map_class(map_options)

    for control in controls:
        m.add_control(control)

    layer = create_layer_from_geo_data_frame(
        data, color=color, id_=layer_id, type_=layer_type, **layer_kwargs
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
