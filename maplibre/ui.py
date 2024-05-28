### TODO: move to 'shiny.py'

from __future__ import annotations

from htmltools import HTMLDependency, Tag
from shiny import ui
from shiny.module import resolve_id

from ._constants import __version__, _shiny_output_class

maplibregl_dep = HTMLDependency(
    "maplibregl",
    version="3.6.2",
    source={"package": "maplibre", "subdir": "srcjs"},
    script={"src": "maplibre-gl.js", "type": "module"},
    stylesheet={"href": "maplibre-gl.css"},
    all_files=False,
)

pymaplibregl_dep = HTMLDependency(
    "pymaplibregl",
    version=__version__,
    source={"package": "maplibre", "subdir": "srcjs"},
    script={"src": "index.js", "type": "module"},
    all_files=False,
)


def output_maplibregl(id_: str, height: [int | str] = 200) -> Tag:
    if isinstance(height, int):
        height = f"{height}px"

    return ui.div(
        maplibregl_dep,
        pymaplibregl_dep,
        # Use resolve_id so that our component will work in a module
        id=resolve_id(id_),
        class_=_shiny_output_class,
        style=f"height: {height}",
    )


DECKGL_VERSION = "9.0.16"

deckgl_dep = HTMLDependency(
    name="deck.gl",
    version=DECKGL_VERSION,
    source={"href": f"https://unpkg.com/deck.gl@{DECKGL_VERSION}/"},
    script={"src": "dist.min.js", "type": "module"},
)


def use_deckgl() -> Tag:
    return ui.div(deckgl_dep)
