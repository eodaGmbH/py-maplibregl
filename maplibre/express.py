from .controls import *
from .layer import Layer, LayerType
from .map import Map, MapOptions
from .settings import default_layer_styles, default_layer_types
from .sources import GeoJSONSource
from .utils import geopandas_to_geojson

try:
    from geopandas import GeoDataFrame
except ImportError:
    GeoDataFrame = None


def create_map(
    data: GeoDataFrame = None,
    controls: list = [NavigationControl()],
    fit_bounds: bool = True,
    tooltip: bool = True,
    map_class=Map,
    **kwargs
) -> Map:
    if str(data.crs) != "EPSG:4326":
        data = data.to_crs("EPSG:4326")

    source = GeoJSONSource(data=geopandas_to_geojson(data))
    map_options = MapOptions(**kwargs)
    if fit_bounds:
        map_options.bounds = data.total_bounds

    m = map_class(map_options)

    for control in controls:
        m.add_control(control)

    layer_type = default_layer_types[data.type[0].lower()]
    layer = Layer(
        type=LayerType(layer_type).value,
        source=source,
        paint=default_layer_styles[layer_type]["paint"],
    )
    m.add_layer(layer)

    # Add tooltip
    if tooltip:
        m.add_tooltip(layer.id)

    return m
