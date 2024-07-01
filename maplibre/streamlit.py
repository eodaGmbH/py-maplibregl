from __future__ import annotations

import base64

from .map import Map

try:
    import streamlit.components.v1 as st_components
except ImportError as e:
    print(e)
    st_components = None


# TODO: Usually it should work with the 'html' component but for some reason it does not work
def st_maplibre(map: Map, height: int = 500, width: int = None) -> None:
    if st_components is None:
        return

    html_b64 = base64.b64encode(
        map.to_html(style=f"height: {height}px;").encode("utf-8")
    ).decode("utf-8")
    st_components.iframe(
        src=f"data:text/html;base64,{html_b64}",
        height=height + 16,
        scrolling=True,
        width=width,
    )
