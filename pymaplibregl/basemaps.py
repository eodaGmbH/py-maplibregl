from enum import Enum

from .layer import Layer, LayerType


class Carto(Enum):
    DARK_MATTER = "dark-matter"
    POSITRON = "positron"
    VOYAGER = "voyager"


def construct_carto_basemap_url(style_name: str = "dark-matter") -> str:
    return f"https://basemaps.cartocdn.com/gl/{Carto(style_name).value}-gl-style/style.json"


def background(color: str = "black", opacity: float = 1.0) -> dict:
    bg_layer = Layer(
        LayerType.BACKGROUND,
        source=None,
        paint={"background-color": color, "background-opacity": opacity},
    ).data
    style = {"version": 8, "sources": {}, "layers": [bg_layer]}
    return style
