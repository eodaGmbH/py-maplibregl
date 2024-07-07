from __future__ import annotations

from random import randint
from typing import Any

from PIL import ImageColor

try:
    import pandas as pd
except ImportError as e:
    print(e)
    pd = None


def create_random_color_palette(n: int) -> list:
    return [rgb_to_hex(tuple([randint(0, 255) for _ in range(3)])) for _ in range(n)]


def color_to_rgb(color) -> tuple:
    return ImageColor.getrgb(color)


# int(x * 255.9999) if rgb between 0 and 1
def rgb_to_hex(rgb: tuple) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def create_rgb_color_palette(
    source_rgb: tuple,
    target_rgb: tuple,
    n: int,
    max_value: int = 255,
) -> list[tuple]:
    n = n - 1
    steps = tuple(map(lambda i, j: (i - j) / n, target_rgb, source_rgb))
    r, g, b = source_rgb
    step_r, step_g, step_b = steps
    result = [
        (r + (i * step_r), g + (i * step_g), b + (i * step_b)) for i in range(n)
    ] + [target_rgb]
    if max_value == 255:
        return [tuple([round(item) for item in rgb]) for rgb in result]

    return result


def create_color_palette(source_color: str, target_color: str, n: int) -> list[str]:
    return [
        rgb_to_hex(color)
        for color in create_rgb_color_palette(
            color_to_rgb(source_color), color_to_rgb(target_color), n
        )
    ]


class ColorPalette(object):
    def __init__(self, color1: str = None, color2: str = None):
        self.color1 = color1
        self.color2 = color2

    def pal(self, n: int) -> list[str]:
        if self.color1 is None or self.color2 is None:
            return create_random_color_palette(n)

        return create_color_palette(self.color1, self.color2, n)

    # codes: list, array or pd.Series of type int
    def get_colors(self, codes: Any):
        n = max(codes) + 1
        pal = self.pal(n)
        return [pal[code] for code in codes]

    # values: list, array or pd.Series of type str
    def numeric(self, values: Any, n: int) -> tuple:
        codes, breaks = pd.cut(values, n, retbins=True, labels=False)
        return self.get_colors(codes), codes, breaks

    # values: list, array or pd.Series of type str
    def factor(self, values: Any) -> tuple:
        values = pd.Categorical(values)
        codes, categories = values.codes, values.categories
        return self.get_colors(codes), codes, categories
