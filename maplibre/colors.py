from __future__ import annotations

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
