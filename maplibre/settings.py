import os
from typing import Optional

from pydantic import BaseModel


class Settings(BaseModel):
    cmap: Optional[str] = "viridis"
    fallback_color: Optional[str] = "#000000"

    fill_color: Optional[str] = "#3B9AB2"
    fill_opacity: Optional[float] = 0.5
    fill_outline_color: Optional[str] = "#FFFFFF"

    line_color: Optional[str] = "#F21A00"
    line_opacity: Optional[float] = 1.0
    line_width: Optional[float] = 1.0

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

    @property
    def paint_probs(self) -> dict:
        return dict(
            fill={
                "fill-color": self.fill_color,
                "fill-opacity": self.fill_opacity,
                "fill-outline-color": self.fill_outline_color,
            },
            line={
                "line-color": self.line_color,
                "line-opacity": self.line_opacity,
                "line-width": self.line_width,
            },
            circle={
                "circle-color": self.circle_color,
                "circle-opacity": self.circle_opacity,
                "circle-radius": self.circle_radius,
                "circle-stroke-color": self.circle_stroke_color,
            },
        )

    def set_maptiler_api_key(self, api_key: str) -> None:
        os.environ[self.maptiler_api_key_env_var] = api_key


settings = Settings()
