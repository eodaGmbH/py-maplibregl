import webbrowser

from pymaplibregl import Layer, LayerType, Map, MapOptions
from pymaplibregl.sources import GeoJSONSource

vancouver_blocks = GeoJSONSource(
    data="https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json",
)

map_options = MapOptions(center=(-123.1256, 49.24658), zoom=12, hash=True, pitch=35)

m = Map(map_options)
m.add_layer(
    Layer(
        type=LayerType.LINE,
        source=vancouver_blocks,
        paint={"line-color": "white"},
    )
)

temp_file = "/tmp/pymaplibregl.html"

with open(temp_file, "w") as f:
    f.write(m.to_html(style="height: 800px;"))

webbrowser.open(temp_file)
