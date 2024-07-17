from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.controls import LayerSwitcherControl
from maplibre.pmtiles_utils import DemoPMTiles, PMTiles

tiles = PMTiles(DemoPMTiles.pmtiles_io_vector_firenze_base_layer)
style = tiles.to_basemap_style(
    [
        ["water", LayerType.FILL, "blue"],
        ["roads", LayerType.LINE, "black"],
        ["buildings", LayerType.FILL, "darkred"],
        ["transit", LayerType.LINE, "yellow"],
        ["pois", LayerType.CIRCLE, "pink"],
    ]
)

map_options = MapOptions(style=style, bounds=tiles.header.bounds)
m = Map(map_options)
m.add_control(
    LayerSwitcherControl(
        layer_ids=["water", "roads", "buildings", "transit", "pois"], theme="simple"
    ),
    position="top-left",
)

m.save("/tmp/py-maplibre-express.html", preview=True)
