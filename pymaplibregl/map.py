from __future__ import annotations

from typing import List

from .basemaps import carto_dark_matter


class Map(object):
    data: dict

    def __init__(
        self,
        # style: str = "https://demotiles.maplibre.org/style.json",
        style: str = carto_dark_matter(),
        center: [list | tuple] = [0, 0],
        zoom: int = 1,
        **kwargs,
    ):
        self._map_options = {
            "style": style,
            "center": center,
            "zoom": zoom,
        }
        self._map_options.update(kwargs)
        self._layers = []
        self._markers = []

    @property
    def shiny_data(self):
        return {
            "mapOptions": self._map_options,
            "layers": self._layers,
            "markers": self._markers,
        }

    def add_layer(self, layer_options: dict) -> None:
        self._layers.append(layer_options)

    def add_marker(
        self, lng_lat: List[float, float], popup: str = None, **kwargs
    ) -> None:
        self._markers.append({"lngLat": lng_lat, "popup": popup, "options": kwargs})
