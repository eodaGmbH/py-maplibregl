### TODO: move to 'shiny.py'

from __future__ import annotations

from htmltools import HTMLDependency, Tag
from shiny import ui
from shiny.module import resolve_id

from ._constants import __version__, _shiny_output_class

# TODO: extract maplibregl version
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
    script={"src": "pywidget.js", "type": "module"},
    stylesheet={"href": "pywidget.css"},
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
    name="deckgl",
    version=DECKGL_VERSION,
    source={"href": f"https://unpkg.com/deck.gl@{DECKGL_VERSION}/"},
    script={"src": "dist.min.js", "type": "module"},
)

# TODO: Remove duplicated constant
# DECKGL_VERSION = "9.0.16"

deckgl_json_dep = HTMLDependency(
    name="deckgljson",
    version=DECKGL_VERSION,
    source={"href": f"https://unpkg.com/@deck.gl/json@{DECKGL_VERSION}/"},
    script={"src": "dist.min.js", "type": "module"},
)


def use_deckgl() -> Tag:
    return ui.div(deckgl_dep, deckgl_json_dep)


MAPBOXGL_DRAW_VERSION = "1.4.3"

mapboxgl_draw_dep = HTMLDependency(
    name="mapbox-gl-draw-plugin",
    version=MAPBOXGL_DRAW_VERSION,
    source={
        "href": f"https://www.unpkg.com/@mapbox/mapbox-gl-draw@{MAPBOXGL_DRAW_VERSION}/dist/"
    },
    script={"src": "mapbox-gl-draw.js", "type": "module"},
    stylesheet={"href": "mapbox-gl-draw.css"},
)


def use_mapboxgl_draw() -> Tag:
    return ui.div(mapboxgl_draw_dep)
