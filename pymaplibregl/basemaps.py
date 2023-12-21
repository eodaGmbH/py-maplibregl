def _construct_carto_basemap_url(style_name: str = "dark-matter") -> str:
    return f"https://basemaps.cartocdn.com/gl/{style_name}-gl-style/style.json"


def carto_positron() -> str:
    return _construct_carto_basemap_url("positron")


def carto_dark_matter() -> str:
    return _construct_carto_basemap_url("dark-matter")


def carto_voyager() -> str:
    return _construct_carto_basemap_url("voyager")
