The `paint` and `layout` properties for the layers depend on the [type](/api/layer/#pymaplibregl.LayerType) of the layer.
They are passed as a `dict` corresponding to the [Layer Style Spec](https://maplibre.org/maplibre-style-spec/layers/).

For example, to set the radius and the color for a circle layer, the `paint` property looks like this:

```python
paint = {
    "circle-radius": 5,
    "circle-color": "yellow"
}
```

The value for any `layout` property, `paint` property, or `filter` may also be specified as an expression.
For details see [Expressions](https://maplibre.org/maplibre-style-spec/expressions/).

For example, if the source of your layer has a `color` property that contains the color of the feature,
you can use the following expression:

```python
paint = {
    "circle-radius": 5,
    "circle-color": ["get", "color"]
}
```

A more complex expression where the color depends on the `type` property of the layer's source might look like this:

```python
paint={
        "circle-color": [
            "match",
            ["get", "type"],
            # darkred if type == "mid"
            "mid",
            "darkred",
            # darkgreen if type == "major"
            "major",
            "darkgreen",
            # else blue
            "darkblue",
        ]
}
```

Filter features of a source according to its `magnitude` property:

```python
# Only show features where magnitude >= 5
filter = [">=", ["get", "magnitude"], 5]
```
