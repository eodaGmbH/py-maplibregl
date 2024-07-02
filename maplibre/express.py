from __future__ import annotations

# from .basemaps import Carto
from .colors import ColorPalette, create_color_palette
from .controls import *
from .layer import Layer, LayerType
from .map import Map, MapOptions
from .settings import default_layer_styles, default_layer_types
from .sources import GeoJSONSource
from .utils import geopandas_to_geojson

try:
    from geopandas import GeoDataFrame
except ImportError as e:
    print(e)
    GeoDataFrame = None

try:
    import pandas as pd
except ImportError as e:
    print(e)
    pd = None

COLOR_COLUMN = "_color"


class GeoDataFrameML(GeoDataFrame):
    def to_maplibre_layer(self):
        pass

    def to_maplibre_map(self):
        pass


"""
def rgb_to_hex(rgb: tuple) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)
"""


# TODO: Use bins instead of n
"""
def cut(data: pd.DataFrame, column: str, n: int = None) -> tuple:
    n = n or 10
    categories, bins = pd.cut(data[column], n, retbins=True, labels=False)
    return categories, bins
"""

"""
def create_color_column(
    data: pd.DataFrame,
    column: str,
    n: int = None,
    source_color: str = "yellow",
    target_color: str = "red",
) -> pd.DataFrame:
    categories, bins = cut(data, column, n)
    colors = create_color_palette(source_color, target_color, n)
    return pd.DataFrame(
        dict(color=categories.apply(lambda i: colors[i]), category=categories)
    )
"""


def create_layer_from_geo_data_frame(
    data: GeoDataFrame,
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
        # filter=filter_ or [],
    )
    if id_:
        layer.id = id_

    if filter_:
        layer.filter = filter_

    return layer


def create_map(
    data: GeoDataFrame,
    # style=Carto.DARK_MATTER,
    controls: list = [NavigationControl()],
    fit_bounds: bool = True,
    tooltip: bool = True,
    color: str = None,
    map_options: MapOptions = MapOptions(),
    map_class=Map,
    layer_id: str = None,
    ret_layer_id: bool = False,
    **kwargs,
) -> Map | tuple:
    # map_options = MapOptions(**kwargs)
    if fit_bounds:
        map_options.bounds = data.total_bounds

    m = map_class(map_options)

    for control in controls:
        m.add_control(control)

    layer = create_layer_from_geo_data_frame(data, color=color, id_=layer_id, **kwargs)
    m.add_layer(layer)

    if tooltip:
        m.add_tooltip(layer.id)

    if ret_layer_id:
        return m, layer.id

    return m
