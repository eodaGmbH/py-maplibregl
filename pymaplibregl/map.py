from __future__ import annotations

from .basemaps import Carto, construct_carto_basemap_url
from .layer import Layer
from .marker import Marker


class Map(object):
    def __init__(
        self,
        # style: str = "https://demotiles.maplibre.org/style.json",
        style: [str | Carto] = Carto.DARK_MATTER,
        center: [list | tuple] = [0, 0],
        zoom: int = 1,
        **kwargs,
    ):
        if isinstance(style, Carto):
            style = construct_carto_basemap_url(style)

        self._map_options = {
            "style": style,
            "center": center,
            "zoom": zoom,
        }
        self._map_options.update(kwargs)
        self._calls = []

    @property
    def data(self):
        return {
            "mapOptions": self._map_options,
            "calls": self._calls,
        }

    @property
    def layers(self) -> list:
        return [item["data"] for item in self._calls if item["name"] == "addLayer"]

    @property
    def markers(self) -> list:
        return [item["data"] for item in self._calls if item["name"] == "addMarker"]

    def add_control(self):
        print("Not implemented yet")

    def add_layer(self, layer: [Layer | dict]) -> None:
        if isinstance(layer, Layer):
            layer = layer.data

        self._calls.append({"name": "addLayer", "data": layer})

    def add_marker(self, marker: [Marker | dict]) -> None:
        if isinstance(marker, Marker):
            marker = marker.data

        self._calls.append(
            {
                "name": "addMarker",
                "data": marker,
            }
        )
