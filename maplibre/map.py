from __future__ import annotations

import json
import os.path
from typing import Union

from jinja2 import Template
from pydantic import ConfigDict, Field, field_validator

from ._templates import html_template, js_template
from ._utils import BaseModel, get_output_dir, read_internal_file
from .basemaps import Carto, construct_carto_basemap_url
from .controls import Control, ControlPosition, Marker
from .layer import Layer
from .sources import Source


class MapOptions(BaseModel):
    """Map options

    Note:
        See [mapOptions](https://maplibre.org/maplibre-gl-js/docs/API/types/maplibregl.MapOptions/) for more details.
    """

    model_config = ConfigDict(
        validate_assignment=True, extra="forbid", use_enum_values=False
    )
    antialias: bool = None
    attribution_control: bool = Field(None, serialization_alias="attributionControl")
    bearing: int = None
    bearing_snap: int = Field(None, serialization_alias="bearingSnap")
    bounds: tuple = None
    box_zoom: bool = Field(None, serialization_alias="boxZoom")
    center: tuple = None
    click_tolerance: int = Field(None, serialization_alias="clickTolerance")
    custom_attribution: bool = Field(None, serialization_alias="customAttribution")
    double_click_zoom: bool = Field(None, serialization_alias="doubleClickZoom")
    fade_duration: int = Field(None, serialization_alias="fadeDuration")
    fit_bounds_options: dict = Field(None, serialization_alias="fitBoundsOptions")
    hash: Union[bool, str] = None
    interactive: bool = None
    keyword: bool = None
    max_bounds: tuple = Field(None, serialization_alias="maxBounds")
    max_pitch: int = Field(None, serialization_alias="maxPitch")
    max_zoom: int = Field(None, serialization_alias="maxZoom")
    min_pitch: int = Field(None, serialization_alias="minPitch")
    min_zoom: int = Field(None, serialization_alias="minZoom")
    pitch: int = None
    scroll_zoom: bool = Field(None, serialization_alias="scrollZoom")
    style: Union[str, Carto, dict] = construct_carto_basemap_url(Carto.DARK_MATTER)
    zoom: int = None

    @field_validator("style")
    def validate_style(cls, v):
        if isinstance(v, Carto):
            return construct_carto_basemap_url(v)

        return v


class Map(object):
    """Map

    Args:
        map_options (MapOptions): Map options.
        **kwargs: Keyword arguments that are appended to the `MapOptions` object.

    Examples:
        >>> from maplibre.map import Map, MapOptions

        >>> map_options = MapOptions(center=(9.5, 51.31667), zoom=8)
        >>> map = Map(map_options)
        >>> dict(map)
        {'mapOptions': {'center': (9.5, 51.31667), 'style': 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json', 'zoom': 8}, 'calls': []}
    """

    MESSAGE = "not implemented yet"

    def __init__(self, map_options: MapOptions = MapOptions(), **kwargs):
        self.map_options = map_options.to_dict() | kwargs
        self._message_queue = []

    def __iter__(self):
        for k, v in self.to_dict().items():
            yield k, v

    def to_dict(self) -> dict:
        return {"mapOptions": self.map_options, "calls": self._message_queue}

    """
    @property
    def sources(self) -> list:
        return [item["data"] for item in self._calls if item["name"] == "addSource"]

    @property
    def layers(self) -> list:
        return [item["data"] for item in self._calls if item["name"] == "addLayer"]
    """

    # TODO: Rename to add_map_call
    def add_call_(self, func_name: str, params: list) -> None:
        self._message_queue.append(
            {"name": "applyFunc", "data": {"funcName": func_name, "params": params}}
        )

    def add_call(self, method_name: str, *args) -> None:
        """Add a method call that is executed on the map instance

        Args:
            method_name (str): The name of the map method to be executed.
            *args (any): The arguments to be passed to the map method.
        """
        # TODO: Pass as dict? {"name": method_name, "args": args}
        call = [method_name, args]
        self._message_queue.append(call)

    def add_control(
        self,
        control: Control,
        position: [str | ControlPosition] = ControlPosition.TOP_RIGHT,
    ) -> None:
        """Add a control to the map

        Args:
            control (Control): The control to be added to the map.
            position (str | ControlPosition): The position of the control.
        """
        self.add_call(
            "addControl",
            control.type,
            control.to_dict(),
            ControlPosition(position).value,
        )

    def add_source(self, id: str, source: [Source | dict]) -> None:
        """Add a source to the map"""
        if isinstance(source, Source):
            source = source.to_dict()

        self.add_call("addSource", id, source)

    def add_layer(self, layer: [Layer | dict]) -> None:
        """Add a layer to the map

        Args:
            layer (Layer | dict): The Layer to be added to the map.
        """
        if isinstance(layer, Layer):
            layer = layer.to_dict()

        self.add_call("addLayer", layer)

    def add_marker(self, marker: Marker) -> None:
        """Add a marker to the map

        Args:
            marker (Marker): The marker to be added to the map.
        """
        self.add_call("addMarker", marker.to_dict())

    def add_popup(self, layer_id: str, prop: str = None, template: str = None) -> None:
        """Add a popup to the map

        Args:
            layer_id (str): The layer to which the popup is added.
            prop (str): The property of the source to be displayed. If `None`, all properties are displayed.
            template (str): A mustache template. If supplied, `prop` is ignored.
        """
        self.add_call("addPopup", layer_id, prop, template)

    def add_tooltip(
        self, layer_id: str, prop: str = None, template: str = None
    ) -> None:
        """Add a tooltip to the map

        Args:
            layer_id (str): The layer to which the tooltip is added.
            prop (str): The property of the source to be displayed. If `None`, all properties are displayed.
            template (str): A mustache template. If supplied, `prop` is ignored.

        Examples:
            >>> map = Map()
            >>> # ...
            >>> map.add_tooltip("test-layer", template="Name: {{ name }}")
        """
        self.add_call("addTooltip", layer_id, prop, template)

    def set_filter(self, layer_id: str, filter_: list):
        """Update the filter of a layer

        Args:
            layer_id (str): The name of the layer to be updated.
            filter_ (list): The filter expression that is applied to the source of the layer.
        """
        self.add_call("setFilter", layer_id, filter_)

    def set_paint_property(self, layer_id: str, prop: str, value: any) -> None:
        """Update the paint property of a layer

        Args:
            layer_id (str): The name of the layer to be updated.
            prop (str): The name of the paint property to be updated.
            value (any): The new value of the paint property.
        """
        self.add_call("setPaintProperty", layer_id, prop, value)

    def set_layout_property(self, layer_id: str, prop: str, value: any) -> None:
        """Update a layout property of a layer

        Args:
            layer_id (str): The name of the layer to be updated.
            prop (str): The name of the layout property to be updated.
            value (any): The new value of the layout property.
        """
        self.add_call("setLayoutProperty", layer_id, prop, value)

    def set_data(self, source_id: str, data: dict) -> None:
        """Update the data of a GeoJSON source

        Args:
            source_id (str): The name of the source to be updated.
            data (dict): The data of the source.
        """
        self.add_call("setSourceData", source_id, data)

    def set_visibility(self, layer_id: str, visible: bool = True) -> None:
        """Update the visibility of a layer

        Args:
            layer_id (str): The name of the layer to be updated.
            visible (bool): Whether the layer is visible or not.
        """
        value = "visible" if visible else "none"
        self.add_call("setLayoutProperty", layer_id, "visibility", value)

    def to_html(self, **kwargs) -> str:
        """Render to html

        Args:
            **kwargs (Any): Additional keyword arguments that are passed to the template.
                Currently, `style` is the only supported keyword argument.

        Examples:
            >>> from maplibre import Map

            >>> map = Map()
            >>> with open("/tmp/map.html", "w") as f:
            ...     f.write(map.to_html(style="height: 800px;") # doctest: +SKIP
        """
        js_lib = read_internal_file("srcjs", "index.js")
        js_snippet = Template(js_template).render(data=json.dumps(self.to_dict()))
        output = Template(html_template).render(
            js="\n".join([js_lib, js_snippet]), **kwargs
        )
        return output
