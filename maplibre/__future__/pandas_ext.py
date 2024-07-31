import geopandas as gpd
import maplibre.express as mx
import pandas as pd

from ..sources import GeoJSONSource, SimpleFeatures


@pd.api.extensions.register_dataframe_accessor("maplibre")
class MapLibreAccessor(object):
    def __init__(self, gdf: gpd.GeoDataFrame):
        self._gdf = gdf

    def to_source(self) -> GeoJSONSource:
        return SimpleFeatures(self._gdf).to_source()

    def fill(self) -> mx.SimpleLayer:
        return mx.fill(self._gdf)
