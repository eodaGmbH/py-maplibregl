from __future__ import annotations

from shiny.render.transformer import (
    TransformerMetadata,
    ValueFn,
    output_transformer,
    resolve_value_fn,
)
from shiny.session import get_current_session

from .map import Map


async def maplibre_render(id_: str = None, color: str = "black") -> None:
    session = get_current_session()
    opts = {"id": id_, "color": color}
    await session.send_custom_message("maplibre", opts)


@output_transformer
async def render_maplibregl(
    _meta: TransformerMetadata,
    _fn: ValueFn[Map | None],
):
    res = await resolve_value_fn(_fn)
    if res is None:
        return None

    if not isinstance(res, Map):
        raise TypeError(f"Expected a Map, got {type(res)}.")

    return {
        "mapData": res.to_dict(),
    }
