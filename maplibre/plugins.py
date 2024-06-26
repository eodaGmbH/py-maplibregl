from __future__ import annotations

from pydantic import Field

from ._utils import BaseModel


class MapboxDrawControls(BaseModel):
    """MapboxDraw controls"""

    point: bool = False
    line_string: bool = False
    polygon: bool = False
    trash: bool = False
    combine_features: bool = False
    uncombine_features: bool = False


class MapboxDrawOptions(BaseModel):
    """MapboxDraw Options"""

    display_controls_default: bool = Field(
        True, serialization_alias="displayControlsDefault"
    )
    controls: MapboxDrawControls = None
    box_select: bool = Field(True, serialization_alias="boxSelect")
