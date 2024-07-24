from __future__ import annotations

from geopandas import GeoDataFrame
from maplibre.layer import Layer
from maplibre.map import Map, MapOptions
from maplibre.sources import SimpleFeatures

"""
class Fill(Layer):
    def __init__(self, data: GeoDataFrame | str, **kwargs):
        source = SimpleFeatures(data).to_source()
"""


class MapLibre(SimpleFeatures):
    def to_map(
        self, map_options: MapOptions = MapOptions(), fit_bounds: bool = True, **kwargs
    ) -> Map | None:

        bounds = self.bounds
        if fit_bounds and bounds:
            map_options.bounds = bounds

        return Map(map_options, layers=[self], **kwargs)
