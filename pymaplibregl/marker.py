from __future__ import annotations

from typing import List


class Marker(object):
    def __init__(
        self, lng_lat: List[float, float], popup: str = None, **kwargs
    ) -> None:
        self._data = {"lngLat": lng_lat, "popup": popup, "options": kwargs}

    @property
    def data(self) -> dict:
        return self._data
