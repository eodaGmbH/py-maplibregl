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
    return ["#%06X" % randint(0, 0xFFFFF) for i in range(n)]


def color_to_rgb(color):
    return ImageColor.getrgb(color)


def rgb_to_hex(rgb: tuple) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def create_rgb_color_palette(
    source_rgb_color: tuple,
    target_rgb_color: tuple,
    n: int,
    max_value: int = 255,
) -> list[tuple]:
    n = n - 1
    steps = tuple(map(lambda i, j: (i - j) / n, target_rgb_color, source_rgb_color))
    r, g, b = source_rgb_color
    step_r, step_g, step_b = steps
    result = [
        (r + (i * step_r), g + (i * step_g), b + (i * step_b)) for i in range(n)
    ] + [target_rgb_color]
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
    def __init__(self, source_color: str = "yellow", target_color: str = "darkred"):
        self.source_color = source_color
        self.target_color = target_color

    def pal(self, n: int) -> list[str]:
        return create_color_palette(self.source_color, self.target_color, n)

    def get_colors(self, codes: Any, n: int):
        pal = self.pal(n)
        return [pal[code] for code in codes]

    def numeric(self, values: Any, n: int) -> tuple:
        codes, borders = pd.cut(values, n, retbins=True, labels=False)
        return self.get_colors(codes, n), codes, borders

    def factor(self, values: Any) -> tuple:
        values_ = pd.Categorical(values)
        codes, categories = values_.codes, values_.categories
        return self.get_colors(codes, len(categories)), codes, categories
