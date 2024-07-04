try:
    from branca.utilities import color_brewer
except ImportError as e:
    print(e)
    color_brewer = None


def create_colors(cmap_name: str = "YlOrRd", n: int = 3) -> list[str]:
    return color_brewer(cmap_name, n)
