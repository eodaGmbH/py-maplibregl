from maplibre import express as mx

path = "https://github.com/Toblerity/Fiona/files/11151652/coutwildrnp.zip"

filename = (
    mx.CoreLayer(path, layer_type="fill", color_column="STATE")
    .to_map(style=mx.basemaps.Carto.POSITRON)
    .save("/tmp/py-maplibre-express.html", preview=True)
)

print(filename)