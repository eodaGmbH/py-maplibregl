from contextlib import asynccontextmanager
from typing import AsyncIterator

from shiny.session import Session, require_active_session

from .map import Map


class MapProxy(Map):
    def __init__(self, id_: str, session: Session = None) -> None:
        self.id = id_
        self._session = require_active_session(session)
        self._map_options = {}
        self._calls = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.render()

    async def render(self):
        await self._session.send_custom_message(
            f"pymaplibregl-{self.id}", {"id": self.id, "calls": self._calls}
        )

    def set_paint_property(self, layer_id: str, prop: str, value: any) -> None:
        self.add_call("setPaintProperty", [layer_id, prop, value])

    def set_layout_property(self, layer_id: str, prop: str, value: any) -> None:
        self.add_call("setLayoutProperty", [layer_id, prop, value])


@asynccontextmanager
async def maplibregl_context(
    id_: str, session: Session = None
) -> AsyncIterator[MapProxy]:
    map_ = MapProxy(id_, session)
    try:
        yield map_
    finally:
        await map_.render()
