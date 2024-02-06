from __future__ import annotations

from shiny.render.transformer import (
    TransformerMetadata,
    ValueFn,
    output_transformer,
    resolve_value_fn,
)

from .map import Map


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
