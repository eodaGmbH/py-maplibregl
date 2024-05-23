from htmltools import Tag
from shiny.render.renderer import Renderer

from .map import Map
from .ui import output_maplibregl


class MapLibreRenderer(Renderer[Map]):
    def auto_output_ui(self) -> Tag:
        return output_maplibregl(self.output_id, height=600)

    async def transform(self, value: Map) -> dict:
        return {"mapData": value.to_dict()}
