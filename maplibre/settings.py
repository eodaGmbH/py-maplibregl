import os
from typing import Optional

from pydantic import BaseModel


class Settings(BaseModel):
    cmap: Optional[str] = "viridis"
    fallback_color: Optional[str] = "black"

    fill_color: Optional[str] = "#3B9AB2"
    fill_opacity: Optional[float] = 0.5
    fill_outline_color: Optional[str] = None

    circle_color: Optional[str] = "#EBCC2A"
    circle_opacity: Optional[float] = 1.0
    circle_radius: Optional[float] = 5
    circle_stroke_color: Optional[str] = "#EBCC2A"

    maptiler_api_key_env_var: Optional[str] = "MAPTILER_API_KEY"

    layer_types: Optional[dict] = dict(
        Polygon="fill", LineString="line", Point="circle"
    )

    @property
    def maptiler_api_key(self) -> str:
        return os.environ.get(self.maptiler_api_key_env_var)

    def set_maptiler_api_key(self, api_key: str) -> None:
        os.environ[self.maptiler_api_key_env_var] = api_key

    def get_paint_props(self, layer_type: str) -> dict:
        pass


settings = Settings()
