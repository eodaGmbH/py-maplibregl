from __future__ import annotations

from os.path import join
from pathlib import Path

import traitlets
from anywidget import AnyWidget

from .controls import Control, ControlPosition
from .layer import Layer
from .map import Map, MapOptions
from .sources import Source


class MapWidget(AnyWidget, Map):
    """MapWidget

    Use this class to display and update maps in Jupyter Notebooks.

    See `maplibre.Map` for available methods.

    Examples:
        >>> from maplibre import MapOptions
        >>> from maplibre.ipywidget import MapWidget as Map
        >>> m = Map(MapOptions(center=(-123.13, 49.254), zoom=11, pitch=45))
        >>> m # doctest: +SKIP
    """

    _esm = join(Path(__file__).parent, "srcjs", "ipywidget.js")
    _css = join(Path(__file__).parent, "srcjs", "maplibre-gl.css")
    _use_message_queue = False
    _rendered = traitlets.Bool(False, config=True).tag(sync=True)
    map_options = traitlets.Dict().tag(sync=True)
    calls = traitlets.List().tag(sync=True)
    height = traitlets.Union([traitlets.Int(), traitlets.Unicode()]).tag(sync=True)
    lng_lat = traitlets.Dict().tag(sync=True)

    def __init__(self, map_options=MapOptions(), **kwargs) -> None:
        self.calls = []
        AnyWidget.__init__(self, **kwargs)
        Map.__init__(self, map_options, **kwargs)

    @traitlets.default("height")
    def _default_height(self):
        return "400px"

    @traitlets.validate("height")
    def _validate_height(self, proposal):
        height = proposal["value"]
        if isinstance(height, int):
            return f"{height}px"

        return height

    @traitlets.observe("_rendered")
    def _on_rendered(self, change):
        self.send({"calls": self._message_queue, "msg": "init"})
        self._message_queue = []

    def use_message_queue(self, value: bool = True) -> None:
        self._use_message_queue = value

    def add_call(self, method_name: str, *args) -> None:
        call = [method_name, args]
        if not self._rendered:
            if not self._use_message_queue:
                self.calls = self.calls + [call]
                return

            self._message_queue.append(call)
            return

        self.send({"calls": [call], "msg": "custom call"})
