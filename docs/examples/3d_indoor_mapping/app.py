import webbrowser

from pymaplibregl import Layer, LayerType, Map, MapOptions
from pymaplibregl.basemaps import background
from pymaplibregl.sources import GeoJSONSource, RasterTileSource

TEMP_FILE = "/tmp/pymaplibregl_temp.html"
FLOORPLAN_SOURCE_ID = "floorplan"

raster_source = RasterTileSource(
    tiles=["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
    tile_size=256,
    min_zoom=0,
    max_zoom=19,
)

raster_layer = Layer(type=LayerType.RASTER, source=raster_source)

floorplan_source = GeoJSONSource(
    data="https://maplibre.org/maplibre-gl-js/docs/assets/indoor-3d-map.geojson"
)

floorplan_layer = Layer(
    type=LayerType.FILL_EXTRUSION,
    id="floorplan",
    source=FLOORPLAN_SOURCE_ID,
    paint={
        "fill-extrusion-color": ["get", "color"],
        "fill-extrusion-height": ["get", "height"],
        "fill-extrusion-base": ["get", "base_height"],
        "fill-extrusion-opacity": 0.5,
    },
)

map_options = MapOptions(
    style=background("yellow"),
    center=(-87.61694, 41.86625),
    zoom=17,
    pitch=40,
    bearing=20,
    antialias=True,
)


def create_map():
    m = Map(map_options)
    m.add_layer(raster_layer)
    m.add_source(FLOORPLAN_SOURCE_ID, floorplan_source)
    m.add_layer(floorplan_layer)
    return m


if __name__ == "__main__":
    m = create_map()
    with open(TEMP_FILE, "w") as f:
        f.write(m.to_html())

    webbrowser.open(TEMP_FILE)
