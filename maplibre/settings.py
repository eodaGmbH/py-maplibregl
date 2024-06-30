from .layer import LayerType

default_layer_types = {
    "polygon": LayerType.FILL.value,
    "multipolygon": LayerType.FILL.value,
    "linestring": LayerType.LINE.value,
    "multilinestring": LayerType.LINE.value,
    "point": LayerType.CIRCLE,
}
default_layer_styles = {
    LayerType.FILL.value: {
        "paint": {"fill-color": "darkred", "fill-outline-color": "white"}
    },
    LayerType.LINE.value: {"paint": {"line-color": "steelblue"}},
    LayerType.CIRCLE.value: {"paint": {"circle-color": "darkgreen"}},
}
