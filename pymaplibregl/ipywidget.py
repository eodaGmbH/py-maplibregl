from os.path import join
from pathlib import Path

import traitlets
from anywidget import AnyWidget

from .layer import Layer
from .map import MapOptions
from .sources import Source


# TODO: Use this class as base class for map.Map as well
class BaseMap(object):
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
class MapWidget(AnyWidget, BaseMap):
    _esm = join(Path(__file__).parent, "srcjs", "ipymaplibregl.js")
    _css = join(Path(__file__).parent, "srcjs", "maplibre-gl.css")
    _rendered = traitlets.Bool(False, config=True).tag(sync=True)
    map_options = traitlets.Dict().tag(sync=True)
    height = traitlets.Union([traitlets.Int(), traitlets.Unicode()]).tag(sync=True)
    test = traitlets.Unicode().tag(sync=True)
    lng_lat = traitlets.Dict().tag(sync=True)

    def __init__(self, map_options=MapOptions(), **kwargs) -> None:
        self.map_options = map_options.to_dict()
        self._message_queue = []
        super().__init__(**kwargs)
        # AnyWidget.__init__(self, **kwargs)

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

    def add_call(self, method_name: str, *args) -> None:
        call = [method_name, args]
        if not self._rendered:
            self._message_queue.append(call)
            return

        self.send({"calls": [call], "msg": "custom call"})
