from enum import Enum
from typing import Union

from pydantic import BaseModel


class DeckLayer(Enum):
    HEXAGON_LAYER = "HexagonLayer"


class PaintProperties(BaseModel):
    line_color: Union[str, list, None]
    line_opacity: Union[float, int, None]
    line_width: Union[float, int, None]
    fill_color: Union[str, list, None]
    fill_opacity: Union[float, int, None]
    fill_outline_color: Union[str, list, None]
    fill_extrusion_color: Union[str, list, None]
    fill_extrusion_opacity: Union[float, int, None]
    circle_color: Union[str, list, None]
    circle_opacity: Union[float, int, None]
    circle_stroke_color: Union[str, list, None]
    circle_radius: Union[float, int, None]
