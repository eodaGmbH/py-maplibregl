from __future__ import annotations

import itertools
from typing import Any, List, TypeVar

from maplibre.colors import color_brewer

T = TypeVar("T")


def get_column(column: str) -> list:
    return ["get", column]


# TODO: Support property params (like ['zoom'])
def interpolate_linear(column: str, stops: list, outputs: list) -> list:
    return [
        "interpolate",
        ["linear"],
        get_column(column),
    ] + list(
        itertools.chain.from_iterable(
            [[stop, output] for stop, output in zip(stops, outputs)]
        )
    )


def match_expr(column: str, categories: list, outputs: list[T], fallback: T) -> list:
    return (
        ["match", get_column(column)]
        + list(
            itertools.chain.from_iterable(
                [[category, output] for category, output in zip(categories, outputs)]
            )
        )
        + [fallback]
    )


def step_expr(column: str, stops: list, outputs: list[T], fallback: T) -> list:
    return (
        ["step", get_column(column)]
        + list(
            itertools.chain.from_iterable(
                [[output, stop] for output, stop in zip(outputs, stops)]
            )
        )
        + [fallback]
    )


def quantile_step_expr(
    column: str, probs: list, outputs: list[T], fallback: T, values: list
) -> list:
    try:
        import numpy as np
    except ImportError as e:
        print(e)
        return []

    stops = np.quantile(values, probs)
    return step_expr(column, stops, outputs, fallback)


def color_quantile_step_expr(
    column: str, probs: list, values: Any, cmap="viridis"
) -> list:
    n = len(probs)
    colors = color_brewer(cmap, n + 1)
    return quantile_step_expr(
        column, probs, outputs=colors[0:n], fallback=colors[-1], values=values
    )


def color_step_expr(column: str, stops: list, cmap="viridis") -> list:
    n = len(stops)
    colors = color_brewer(cmap, n + 1)
    return step_expr(column, stops, outputs=colors[0:n], fallback=colors[-1])


def color_match_expr(column: str, categories: Any, cmap: str = "viridis"):
    categories = sorted(list(set(categories) - {None}))
    n = len(categories)
    colors = color_brewer(cmap, n + 1)
    return match_expr(column, categories, outputs=colors[0:n], fallback=colors[-1])


def color_interpolate_linear(column: str, stops: list, cmap: str = "viridis"):
    pass
