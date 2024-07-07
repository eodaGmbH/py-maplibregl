try:
    from branca.utilities import color_brewer
except ImportError as e:
    print(e)
    color_brewer = None


def create_colors(cmap_name: str = "viridis", n: int = 3, *args) -> list[str]:
    print("branca cmaps")
    n = int(n)  # 'color_brewer' does not accept 'np.int*' types
    if n == 2:
        colors = color_brewer(cmap_name)
        return [colors[i] for i in [0, -1]]

    return color_brewer(cmap_name, n)
