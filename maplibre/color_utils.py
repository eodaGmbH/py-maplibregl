from __future__ import annotations

from itertools import chain
from typing import Any

try:
    from branca.utilities import color_brewer as branca_color_brewer
except ImportError as e:
    print(e)
    branca_color_brewer = None

CMAPS_JSON = "https://raw.githubusercontent.com/python-visualization/branca/main/branca/_schemes.json"

# TODO: Move to options
FALLBACK_COLOR = "#000000"


def color_brewer(cmap: str, n: int) -> list:
    n = int(n)
    if n == 2:
        colors = branca_color_brewer(cmap)
        return [colors[i] for i in [0, -1]]

    return branca_color_brewer(cmap, n)


def create_categorical_color_expression(
    values: Any, column_name: str, cmap: str = "viridis"
) -> tuple:
    unique_values = sorted(list(set(values)))
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
    return expression, unique_values, colors


# TODO: Allow to pass colors
def create_numeric_color_expression_from_breaks(
    column_name: str, breaks: list, cmap="viridis"
) -> tuple:
    n = len(breaks)
    colors = color_brewer(cmap, n + 1)
    expression = (
        ["step", ["get", column_name]]
        + list(
            chain.from_iterable(
                [[color, step] for color, step in zip(colors[0:n], breaks)]
            )
        )
        + [colors[-1]]
    )
    return expression, breaks, colors


def create_numeric_color_expression(
    values: Any, n: int, column_name: str, cmap: str = "viridis"
) -> tuple:
    step = (max(values) - min(values)) / n
    # breaks = [min(values) + i * step for i in range(n)]
    breaks = [min(values) + step + i * step for i in range(n - 1)]
    return create_numeric_color_expression_from_breaks(column_name, breaks, cmap)


def create_numeric_color_expression_from_quantiles(
    values: Any, q: list, column_name: str, cmap: str = "viridis"
) -> tuple | None:
    try:
        import numpy as np
    except ImportError as e:
        print(e)
        return

    breaks = np.quantile(values, q)
    return create_numeric_color_expression_from_breaks(column_name, breaks, cmap)


def list_cmaps() -> list | None:
    try:
        import requests
    except ImportError as e:
        print(e)
        return

    return list(requests.get(CMAPS_JSON).json().keys())
