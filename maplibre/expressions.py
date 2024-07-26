import itertools
from typing import Any, List, TypeVar

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
