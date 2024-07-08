from __future__ import annotations

from itertools import chain
from typing import Any

try:
    from branca.utilities import color_brewer as branca_color_brewer
except ImportError as e:
    print(e)
    branca_color_brewer = None

FALLBACK_COLOR = "#000000"


def color_brewer(cmap: str, n: int) -> list:
    n = int(n)
    if n == 2:
        colors = branca_color_brewer(cmap)
        return [colors[i] for i in [1, -1]]

    return branca_color_brewer(cmap, n)


def create_color_expression(
    values: Any, column_name: str, cmap: str = "viridis"
) -> list | None:
    if not color_brewer:
        return

    unique_values = list(set(values))
    colors = color_brewer(cmap, len(unique_values))
    expression = (
        ["match", ["get", column_name]]
        + list(
            chain.from_iterable(
                [[value, color] for value, color in zip(unique_values, colors)]
            )
        )
        + [FALLBACK_COLOR]
    )
    return expression
