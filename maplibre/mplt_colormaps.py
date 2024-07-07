from __future__ import annotations

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


from .branca_colormaps import create_colors


# Run 'list(colormaps)' to get available colormaps
def create_colors_(
    cmap_name: str = "viridis", n: int = 6, ret_hex: bool = True
) -> list:
    print("matplotlib cmaps")
    cmap = colormaps[cmap_name].resampled(n)
    colors = [cmap(i) for i in range(n)]
    if ret_hex:
        return [to_hex(color) for color in colors]

    return colors


def map_colors(cmap_name: str, codes: Any, ret_hex: bool = True) -> list[str]:
    n = max(codes) + 1
    colors = create_colors(cmap_name, n, ret_hex)
    return [colors[code] for code in codes]


class ColorBrewer(object):
    def __init__(self, cmap_name: str = "viridis"):
        self.cmap_name = cmap_name

    def numeric(self, values: Any, bins: Any) -> tuple:
        # values: list, np.array or pd.Series
        values = list(values)
        out = pd.cut(values, bins)
        return map_colors(self.cmap_name, out.codes), out.codes, out.categories

    def factor(self, values: Any) -> tuple:
        # values: list, array or pd.Series
        values = pd.Categorical(values)
        codes, categories = values.codes, values.categories
        return map_colors(self.cmap_name, codes), codes, categories
