from __future__ import annotations

from .controls import ControlPosition
from .map import Map


def add_mapbox_draw(
    map_: Map,
    options: dict = None,
    position: str | ControlPosition = ControlPosition.TOP_LEFT,
    geojson: dict = None,
) -> None:
    map_.add_call(
        "addMapboxDraw", options or {}, ControlPosition(position).value, geojson
    )
