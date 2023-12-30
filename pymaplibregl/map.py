from __future__ import annotations

import json
import os.path

from jinja2 import Template

from ._templates import html_template, js_template
from ._utils import get_output_dir, read_internal_file
from .basemaps import Carto, construct_carto_basemap_url
from .controls import ControlPosition, ControlType
from .layer import Layer
from .marker import Marker
from .sources import Source


class Map(object):
    MESSAGE = "not implemented yet"

    def __init__(
        self,
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
    def sources(self) -> list:
        return [item["data"] for item in self._calls if item["name"] == "addSource"]

    @property
    def layers(self) -> list:
        return [item["data"] for item in self._calls if item["name"] == "addLayer"]

    @property
    def markers(self) -> list:
        return [item["data"] for item in self._calls if item["name"] == "addMarker"]

    def add_call(self, func_name: str, params: list) -> None:
        self._calls.append(
            {"name": "applyFunc", "data": {"funcName": func_name, "params": params}}
        )

    def add_control(
        self,
        type_: [str | ControlType],
        options: dict = {},
        position: [str | ControlPosition] = ControlPosition.TOP_RIGHT,
    ) -> None:
        self._calls.append(
            {
                "name": "addControl",
                "data": {
                    "type": ControlType(type_).value,
                    "options": options,
                    "position": ControlPosition(position).value,
                },
            }
        )

    def add_source(self, id_: str, source: [Source | dict]) -> None:
        if isinstance(source, Source):
            source = source.to_dict()

        self._calls.append({"name": "addSource", "data": {"id": id_, "source": source}})

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

    def add_popup(self, layer_id: str, property_: str) -> None:
        self._calls.append(
            {"name": "addPopup", "data": {"layerId": layer_id, "property": property_}}
        )

    def set_filter(self, layer_id: str, filter_: list):
        self.add_call("setFilter", [layer_id, filter_])

    def set_paint_property(self, layer_id: str, prop: str, value: any) -> None:
        self.add_call("setPaintProperty", [layer_id, prop, value])

    def set_layout_property(self, layer_id: str, prop: str, value: any) -> None:
        self.add_call("setLayoutProperty", [layer_id, prop, value])

    def to_html(self, output_dir: str = None, **kwargs) -> str:
        js_lib = read_internal_file("srcjs", "index.js")
        js_snippet = Template(js_template).render(data=json.dumps(self.data))
        output = Template(html_template).render(
            js="\n".join([js_lib, js_snippet]), **kwargs
        )
        if output_dir == "skip":
            return output

        file_name = os.path.join(get_output_dir(output_dir), "index.html")
        with open(file_name, "w") as f:
            f.write(output)

        return file_name
