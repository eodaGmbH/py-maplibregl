from .controls import *
from .layer import Layer
from .map import Map, MapOptions
from .sources import GeoJSONSource
from .utils import geopandas_to_geojson

try:
    from geopandas import GeoDataFrame
except Exception as e:
    GeoDataFrame = None

# TODO: Move to constants
DEFAULT_STYLES = {"fill": {"paint": {"fill-color": "darkred"}}}
DEFAULT_LAYER_TYPES = {"polygon": "fill", "multipolygon": "fill"}


def create_map(
    data: GeoDataFrame = None,
    controls: list = [NavigationControl()],
    fit_bounds: bool = True,
    tooltip: bool = True,
    map_class=Map,
    **kwargs
) -> Map:
    # Prepare data
    # if data is not None and isinstance(data, GeoDataFrame):
    if str(data.crs) != "EPSG:4326":
        data = data.to_crs("EPSG:4326")

    source = GeoJSONSource(data=geopandas_to_geojson(data))
    map_options = MapOptions(**kwargs)
    if fit_bounds:
        map_options.bounds = data.total_bounds

    m = map_class(map_options)
    for control in controls:
        m.add_control(control)
    # m.add_source(source)
    layer_type = DEFAULT_LAYER_TYPES[data.type[0].lower()]
    layer = Layer(
        type=layer_type, source=source, paint=DEFAULT_STYLES[layer_type]["paint"]
    )
    m.add_layer(layer)
    if tooltip:
        m.add_tooltip(layer.id)

    return m
