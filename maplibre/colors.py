from __future__ import annotations

from typing import Any

from .expressions import match_expr, quantile_step_expr, step_expr

try:
    from branca.utilities import color_brewer as branca_color_brewer
except ImportError as e:
    print(e)
    branca_color_brewer = None

CMAPS_JSON = "https://raw.githubusercontent.com/python-visualization/branca/main/branca/_schemes.json"
# FALLBACK_COLOR = "#000000"
DEFAULT_CMAP = "viridis"


def color_brewer(cmap: str, n: int) -> list:
    n = int(n)
    if n == 2:
        colors = branca_color_brewer(cmap)
        return [colors[i] for i in [0, -1]]

    return branca_color_brewer(cmap, n)


def list_cmaps() -> list | None:
    try:
        import requests
    except ImportError as e:
        print(e)
        return

    return list(requests.get(CMAPS_JSON).json().keys())


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


def color_quantile_expr(column: str, probs: list, values: Any, cmap="viridis") -> list:
    n = len(probs)
    colors = color_brewer(cmap, n + 1)
    return quantile_step_expr(
        column, probs, outputs=colors[0:n], fallback=colors[-1], values=values
    )
