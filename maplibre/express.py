from random import randint

from .colors import color_palette
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


class GeoDataFrameML(GeoDataFrame):
    def to_maplibre_layer(self):
        pass

    def to_maplibre_map(self):
        pass


def random_colors(n: int) -> list:
    return ["#%06X" % randint(0, 0xFFFFF) for i in range(n)]


def rgb_to_hex(rgb: tuple) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def cut(data: pd.DataFrame, column: str, n: int = 10) -> tuple:
    categories, bins = pd.cut(data[column], n, retbins=True, labels=False)
    return categories, bins


def create_color_column(
    data: pd.DataFrame,
    column: str,
    n: int = 10,
    source_color: str = "yellow",
    target_color: str = "red",
) -> pd.DataFrame:
    categories, bins = cut(data, column, n)
    colors = color_palette(source_color, target_color, n)
    return pd.DataFrame(
        dict(color=categories.apply(lambda i: colors[i]), category=categories)
    )


def create_layer(data: GeoDataFrame, color: str = None):
    pass


def create_map(
    data: GeoDataFrame = None,
    controls: list = [NavigationControl()],
    fit_bounds: bool = True,
    tooltip: bool = True,
    color: str = None,
    color_column: str = None,
    map_class=Map,
    **kwargs,
) -> Map:
    if str(data.crs) != "EPSG:4326":
        data = data.to_crs("EPSG:4326")

    if color:
        df_color = create_color_column(data, color)
        data[["color", "category"]] = df_color
        color_column = "color"

    source = GeoJSONSource(data=geopandas_to_geojson(data))
    map_options = MapOptions(**kwargs)
    if fit_bounds:
        map_options.bounds = data.total_bounds

    m = map_class(map_options)

    for control in controls:
        m.add_control(control)

    layer_type = default_layer_types[data.type[0].lower()]
    paint = default_layer_styles[layer_type]["paint"]
    if color_column:
        paint[f"{layer_type}-color"] = ["get", color_column]

    layer = Layer(
        type=LayerType(layer_type).value,
        source=source,
        paint=paint,
    )
    m.add_layer(layer)

    # Add tooltip
    if tooltip:
        m.add_tooltip(layer.id)

    return m
