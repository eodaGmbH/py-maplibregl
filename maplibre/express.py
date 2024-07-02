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


# TODO: Use bins instead of n
def cut(data: pd.DataFrame, column: str, n: int = None) -> tuple:
    n = n or 10
    categories, bins = pd.cut(data[column], n, retbins=True, labels=False)
    return categories, bins


def create_color_column(
    data: pd.DataFrame,
    column: str,
    n: int = None,
    source_color: str = "yellow",
    target_color: str = "red",
) -> pd.DataFrame:
    categories, bins = cut(data, column, n)
    colors = color_palette(source_color, target_color, n)
    return pd.DataFrame(
        dict(color=categories.apply(lambda i: colors[i]), category=categories)
    )


# TODO: Rename create layer from geopandas
def create_layer(
    data: GeoDataFrame,
    color: str = None,
    n_bins: int = None,
    source_color: str = "yellow",
    target_color: str = "darkred",
    layer_type: str = None,
    paint: dict = None,
    layer_id: str = None,
) -> Layer:
    if str(data.crs) != "EPSG:4326":
        data = data.to_crs("EPSG:4326")

    if color:
        if data[color].apply(type).unique()[0] in [int, float]:
            categories, bins = pd.cut(data[color], n_bins, retbins=True, labels=False)
            colors = color_palette(source_color, target_color, len(bins))
            data["_color"] = [colors[value] for value in categories]
            data["_category"] = categories

            """"
            data[["_color", "_category"]] = create_color_column(
                data,
                color,
                n=n_bins,
                source_color=source_color,
                target_color=target_color,
            )
            """
        else:
            categories = list(pd.Categorical(data[color]).codes)
            # pd.Categorical(data[color]).categories
            colors = color_palette(source_color, target_color, len(categories))
            data["_color"] = [colors[value] for value in categories]
            data["_category"] = categories

    layer_type = layer_type or default_layer_types[data.type[0].lower()]
    paint = paint or default_layer_styles[layer_type]["paint"]
    if color:
        paint[f"{layer_type}-color"] = ["get", "_color"]

    layer = Layer(
        type=LayerType(layer_type).value,
        source=GeoJSONSource(data=geopandas_to_geojson(data)),
        paint=paint,
    )
    if layer_id:
        layer.id = layer_id

    return layer


def create_map(
    data: GeoDataFrame = None,
    controls: list = [NavigationControl()],
    fit_bounds: bool = True,
    tooltip: bool = True,
    color: str = None,
    n_bins: int = 10,
    map_class=Map,
    layer_options: dict = {},
    **kwargs,
) -> Map:
    map_options = MapOptions(**kwargs)
    if fit_bounds:
        map_options.bounds = data.total_bounds

    m = map_class(map_options)

    for control in controls:
        m.add_control(control)

    layer = create_layer(data, color=color, n_bins=n_bins, **layer_options)
    m.add_layer(layer)

    if tooltip:
        m.add_tooltip(layer.id)

    return m
