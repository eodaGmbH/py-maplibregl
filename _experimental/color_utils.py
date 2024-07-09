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


# TODO: Rename to create categorical_color_expression
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


# TODO: Allow to pass colors
def create_numeric_color_expression_from_steps(
    column_name: str, steps: list, cmap="viridis"
) -> list | None:
    colors = color_brewer(cmap, len(steps))
    # TODO: Extract this step to helper function
    expression = (
        ["step", ["get", column_name]]
        + list(
            chain.from_iterable([[color, step] for color, step in zip(colors, steps)])
        )
        + [FALLBACK_COLOR]
    )
    return expression


def create_numeric_color_expression(
    values: Any, n: int, column_name: str, cmap: str = "viridis"
) -> tuple | None:
    step = (max(values) - min(values)) / n
    breaks = [min(values) + i * step for i in range(n)]
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
