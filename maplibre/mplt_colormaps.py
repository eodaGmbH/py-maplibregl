from typing import Any

try:
    import pandas as pd
    from matplotlib import colormaps
    from matplotlib.colors import to_hex, to_rgb
except ImportError as e:
    print(e)
    pd = None
    colormaps = None
    to_hex = None
    to_rgb = None


def pal(name: str = "viridis", n: int = 6, ret_hex: bool = True) -> list:
    # colors = colormaps[name].resampled(n).colors
    cmap = colormaps[name]
    colors = [cmap(i) for i in range(n)]
    if ret_hex:
        return [to_hex(color) for color in colors]

    return colors
    # if ret_hex:
    # return [to_hex(color) for color in colors]

    # return colors


class Pal(object):
    def __init__(self, name: str = "viridis"):
        self.name = name

    def map_colors(self, codes: Any, ret_hex: bool = True) -> list[str]:
        n = max(codes) + 1
        return [pal(self.name, n, ret_hex)[code] for code in codes]


# values: list, array or pd.Series of type str
def pal_numeric(values: Any, bins: Any, p=Pal()) -> tuple:
    codes, breaks = pd.cut(values, bins, retbins=True, labels=False)
    return p.map_colors(codes), codes, breaks


# values: list, array or pd.Series of type str
def pal_factor(values: Any, p=Pal()) -> tuple:
    values = pd.Categorical(values)
    codes, categories = values.codes, values.categories
    return p.map_colors(codes), codes, categories
