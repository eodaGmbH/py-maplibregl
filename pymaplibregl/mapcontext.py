from shiny.session import Session, require_active_session

from .map import Map


class MapContext(Map):
    def __init__(self, id: str, session: Session = None) -> None:
        self.id = id
        self._session = require_active_session(session)
        self.map_options = {}
        self._message_queue = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.render()

    async def render(self):
        await self._session.send_custom_message(
            f"pymaplibregl-{self.id}", {"id": self.id, "calls": self._message_queue}
        )
