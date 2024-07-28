from typing import Optional

from pydantic import BaseModel


class Settings(BaseModel):
    cmap: Optional[str] = "viridis"
    fallback_color: Optional[str] = "black"
    fill_color: Optional[str] = "steelblue"
    fill_opacity: Optional[float] = 0.7


settings = Settings()
