from __future__ import annotations

from pymaplibregl import Layer, LayerType
from pymaplibregl._utils import fix_keys
from pymaplibregl.sources import SourceType


class LineLayer(Layer):
    def __init__(self, source: [dict | str], id_: str = None, *args, **kwargs):
        super().__init__(LayerType.LINE, source=source, id_=id_, *args, **kwargs)


class Source(object):
    def __init__(self, type_: [str | SourceType], **kwargs):
        self._data = {"type": SourceType(type_).value}
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
