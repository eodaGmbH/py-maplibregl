from __future__ import annotations

from enum import Enum

from ._utils import fix_keys


class SourceType(Enum):
    RASTER = "raster"
    VECTOR = "vector"
    RASTER_DEM = "raster-dem"
    GEOJSON = "geojson"
    IMAGE = "image"
    VIDEO = "video"


class Source(object):
    def __init__(self, type_: [str | SourceType], **kwargs):
        self._data = {"type": SourceType(type_).value}
        # self._data = {"type": type_}
        self._data.update(kwargs)
        self._data = fix_keys(self._data)

    @property
    def data(self):
        return self._data


class GeojsonSource(Source):
    def __init__(
        self,
        data: [dict | str],
        cluster: bool = None,
        cluster_radius: int = None,
        cluster_min_points: int = None,
        cluster_max_zoom: int = None,
        **kwargs,
    ):
        super().__init__(
            SourceType.GEOJSON,
            # "geojson",
            data=data,
            cluster=cluster,
            clusterRadius=cluster_radius,
            clusterMinPoints=cluster_min_points,
            clusterMaxZoom=cluster_max_zoom,
            **kwargs,
        )
