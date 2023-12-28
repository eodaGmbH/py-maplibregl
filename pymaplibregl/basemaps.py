from enum import Enum

from .layer import Layer, LayerType


class Carto(Enum):
    DARK_MATTER = "dark-matter"
    POSITRON = "positron"
    VOYAGER = "voyager"


def construct_carto_basemap_url(style_name: str = "dark-matter") -> str:
    return f"https://basemaps.cartocdn.com/gl/{Carto(style_name).value}-gl-style/style.json"


def construct_basemap_style(
    name: str = "nice-style", sources: dict = {}, layers: list = []
) -> dict:
    layers = [layer.data if isinstance(layer, Layer) else layer for layer in layers]
    return {"name": name, "version": 8, "sources": sources, "layers": layers}


def background(color: str = "black", opacity: float = 1.0) -> dict:
    bg_layer = Layer(
        LayerType.BACKGROUND,
        source=None,
        paint={"background-color": color, "background-opacity": opacity},
    )
    return construct_basemap_style(layers=[bg_layer])
