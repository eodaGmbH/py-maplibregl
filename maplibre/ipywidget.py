from __future__ import annotations

from os.path import join
from pathlib import Path

import traitlets
from anywidget import AnyWidget

from .controls import Control, ControlPosition
from .layer import Layer
from .map import Map, MapOptions
from .sources import Source


# DEPRECATED: MapWidget now uses map.Map as base class
class BaseMap(object):
    def __init__(self, map_options=MapOptions(), **kwargs) -> None:
        self.map_options = map_options.to_dict() | kwargs

    # This method must be overwritten
    def add_call(self, method_name: str, *args) -> None:
        """Add a method call that is executed on the map instance

        Args:
            method_name (str): The name of the map method to be executed.
            *args (any): The arguments to be passed to the map method.
        """
        # TODO: Pass as dict? {"name": method_name, "args": args}
        call = [method_name, args]
        print(call)

    def add_source(self, source_id: str, source: Source) -> None:
        """Add a source to the map"""
        self.add_call("addSource", source_id, source.to_dict())

    def add_layer(self, layer: Layer) -> None:
        """Add a layer to the map"""
        self.add_call("addLayer", layer.to_dict())

    def add_control(
        self,
        control: Control,
        position: [str | ControlPosition] = ControlPosition.TOP_RIGHT,
    ) -> None:
        """Add a control to the map"""
        self.add_call(
            "addControl",
            control.type,
            control.to_dict(),
            ControlPosition(position).value,
        )

    def set_paint_property(self, layer_id: str, prop: str, value: any) -> None:
        """Update a paint property of a layer"""
        self.add_call("setPaintProperty", layer_id, prop, value)

    def set_layout_property(self, layer_id: str, prop: str, value: any) -> None:
        """Update a layout property of a layer"""
        self.add_call("setLayoutProperty", layer_id, prop, value)

    def add_tooltip(self, layer_id: str, prop: str) -> None:
        """Add a tooltip to the map"""
        self.add_call("addPopup", layer_id, prop)


# TODO: Rename to MapWidget or IpyMap
class MapWidget(AnyWidget, Map):
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
