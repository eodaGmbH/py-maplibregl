from shiny.session import Session, require_active_session

from .map import Map


class MapContext(Map):
    """MapContext

    Use this class to update a `Map` instance in a Shiny app.
    Must be used inside an async function.

    See `maplibre.Map` for available methods.

    Args:
        id (string): The id of the map to be updated.
        session (Session): A Shiny session.
            If `None`, the active session is used.
    """

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
