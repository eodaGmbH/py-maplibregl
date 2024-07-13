from maplibre import express as mx

path = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
blocks = mx.read_file(path)
breaks = blocks.valuePerSqm.quantile([0.25, 0.5, 0.75, 0.9]).to_list()

filename = (
    mx.CoreLayer(
        blocks,
        layer_type="fill",
        color_column="valuePerSqm",
        # breaks=breaks,
        q=[0.25, 0.5, 0.75, 0.9],
        cmap="YlOrRd",
    )
    .to_map(style=mx.basemaps.Carto.POSITRON, pitch=35)
    .save("/tmp/py-maplibre-express.html", preview=True)
)

print(filename)
