from __future__ import annotations

import itertools
from enum import Enum
from typing import Any, TypeVar

from maplibre.colors import color_brewer

T = TypeVar("T")


class GeometryType(Enum):
    POINT = "Point"
    LINE_STRING = "LineString"
    POLYGON = "Polygon"


def get_column(column: str) -> list:
    return ["get", column]


def get_geometry_type() -> list:
    return ["geometry-type"]


def geometry_type_filter(geom_type: GeometryType | str) -> list:
    return ["==", get_geometry_type(), GeometryType(geom_type).value]


def interpolate(
    property: str | list, stops: list, outputs: list, type: list = ["linear"]
) -> list:
    assert len(stops) == len(outputs)
    return [
        "interpolate",
        type,
        get_column(property) if isinstance(property, str) else property,
    ] + list(
        itertools.chain.from_iterable(
            [[stop, output] for stop, output in zip(stops, outputs)]
        )
    )


def match_expr(column: str, categories: list, outputs: list[T], fallback: T) -> list:
    assert len(categories) == len(outputs)
    return (
        ["match", get_column(column)]
        + list(
            itertools.chain.from_iterable(
                [[category, output] for category, output in zip(categories, outputs)]
            )
        )
        + [fallback]
    )


# Property examples:
# - ["zoom"],
# - ["get", "column_name"]  same as "column_name"
def step_expr(
    property: str | list,
    stops: list,
    outputs: list[T],
    fallback: T,
) -> list:
    assert len(stops) == len(outputs)
    return (
        [
            "step",
            get_column(property) if isinstance(property, str) else property,
        ]
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
    assert len(probs) == len(outputs)
    try:
        import numpy as np
    except ImportError as e:
        print(e)
        return []

    stops = np.quantile(values, probs)
    return step_expr(column, stops, outputs, fallback)


# -----
# ----- COLOR expression -------------------------
# -----


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


"""
def color_interpolate(
    column: str,
    stops: list,
    cmap: str = "Blues",
    colors: list = None,
    type: list = list("linear"),
) -> list:
    n = len(stops)
    colors = colors or color_brewer(cmap, n)
    return interpolate(column, stops, outputs=colors, type=type)
"""


def equal_bins_step_expr():
    pass


def filter_expr(column: str, operator: str, value: Any) -> list:
    return [operator, get_column(column), value]


def range_filter(
    column, values: tuple | list, operators: tuple | list = (">=", "<=")
) -> list:
    assert len(values) == len(operators) == 2
    return ["all"] + [[operators[i], get_column(column), values[i]] for i in range(2)]
