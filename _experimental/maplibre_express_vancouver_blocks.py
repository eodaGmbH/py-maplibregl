from _deprecated import express as mx

path = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
blocks = mx.read_file(path)
breaks = blocks.valuePerSqm.quantile([0.25, 0.5, 0.75, 0.9]).to_list()

filename = (
    mx.FillExtrusion(
        blocks,
        color_column="valuePerSqm",
        q=[0.25, 0.5, 0.75, 0.9],
        cmap="YlOrRd",
        fill_extrusion_height=["*", 10, ["sqrt", ["get", "valuePerSqm"]]],
    )
    .to_map(style=mx.basemaps.Carto.POSITRON, pitch=35)
    .save("/tmp/py-maplibre-express.html", preview=True)
)

print(filename)
