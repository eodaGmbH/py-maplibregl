from os.path import join
from pathlib import Path
from uuid import uuid4

import traitlets
from anywidget import AnyWidget
from shiny import App

from .layer import Layer
from .map import MapOptions


class MaplibreWidget(AnyWidget):
    _esm = join(Path(__file__).parent, "srcjs", "ipymaplibregl.js")
    _css = join(Path(__file__).parent, "srcjs", "maplibre-gl.css")
    _rendered = traitlets.Bool(False, config=True).tag(sync=True)
    # rendered = traitlets.Bool(False, config=True).tag(sync=True)
    _message_queue = []
    map_options = traitlets.Dict().tag(sync=True)
    height = traitlets.Union([traitlets.Int(), traitlets.Unicode()]).tag(sync=True)
    test = traitlets.Unicode().tag(sync=True)
    calls = traitlets.List().tag(sync=True)
    _calls = []
    # controls = traitlets.List().tag(sync=True)
    # sources = traitlets.List().tag(sync=True)
    # layers = traitlets.List().tag(sync=True)

    lng_lat = traitlets.Dict().tag(sync=True)

    def __init__(self, map_options=MapOptions(), **kwargs) -> None:
        self.map_options = map_options.to_dict()
        super().__init__(**kwargs)

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
        # self.calls = self._message_queue
        # assert self.calls == self._message_queue
        # del self._calls
        self.send({"calls": self._message_queue})
        self._message_queue = []

    def add_call(self, method_name: str, *args) -> None:
        call = [method_name, args]
        if not self._rendered:
            self._message_queue = self._message_queue + [call]
            return

        self.calls = [call]

    def add_layer(self, layer: Layer) -> None:
        self.add_call("addLayer", layer.to_dict())
