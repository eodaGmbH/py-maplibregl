from __future__ import annotations

from typing import Annotated, List

from .popup import Popup


class Marker(object):
    def __init__(
        self, lng_lat: Annotated[List[float], 2], popup: [Popup | dict] = None, **kwargs
    ) -> None:
        if isinstance(popup, Popup):
            popup = popup.data

        self._data = {"lngLat": lng_lat, "popup": popup, "options": kwargs}

    @property
    def data(self) -> dict:
        return self._data
