import webbrowser

from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.sources import RasterTileSource

SOURCE_ID = "wms-test-source"
LAYER_ID = "wms-test-layer"

wms_source = RasterTileSource(
    tiles=[
        "https://img.nj.gov/imagerywms/Natural2015?bbox={bbox-epsg-3857}&format=image/png&service=WMS&version=1.1.1&request=GetMap&srs=EPSG:3857&transparent=true&width=256&height=256&layers=Natural2015"
    ],
    tile_size=256,
)
wms_layer = Layer(type=LayerType.RASTER, source=SOURCE_ID, id=LAYER_ID)

map_options = MapOptions(zoom=8, center=(-74.5447, 40.6892))

m = Map(map_options=map_options)
m.add_source(SOURCE_ID, wms_source)
m.add_layer(wms_layer)

temp_file = "/tmp/pymaplibregl.html"

with open(temp_file, "w") as f:
    f.write(m.to_html(style="height: 800px;"))

webbrowser.open(temp_file)
