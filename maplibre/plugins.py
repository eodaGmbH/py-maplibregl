from __future__ import annotations

from pydantic import Field

from ._core import MapLibreBaseModel


class MapboxDrawControls(MapLibreBaseModel):
    """MapboxDraw controls"""

    point: bool = False
    line_string: bool = False
    polygon: bool = False
    trash: bool = False
    combine_features: bool = False
    uncombine_features: bool = False


class MapboxDrawOptions(MapLibreBaseModel):
    """MapboxDraw Options"""

    display_controls_default: bool = Field(
        True, serialization_alias="displayControlsDefault"
    )
    controls: MapboxDrawControls = None
    box_select: bool = Field(True, serialization_alias="boxSelect")
