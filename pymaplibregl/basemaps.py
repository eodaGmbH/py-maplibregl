from enum import Enum


class Carto(Enum):
    DARK_MATTER = "dark-matter"
    POSITRON = "positron"
    VOYAGER = "voyager"


def construct_carto_basemap_url(style_name: str = "dark-matter") -> str:
    return f"https://basemaps.cartocdn.com/gl/{Carto(style_name).value}-gl-style/style.json"
