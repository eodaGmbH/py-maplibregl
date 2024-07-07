# from geopandas import read_file

from maplibre.express import create_map, read_file

print("takes time")

data = read_file(
    "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
)
print(data)
# print(data)
m = data.maplibre.to_map(
    "growth",
    # bins=5,
)
# m = create_map(data, "growth")
# m.save("/tmp/py-maplibre-gl-express.html", preview=True)
