import geopandas as gpd
from geodatasets import get_path
from maplibre.colors import ColorPalette
from maplibre.express import (
    Layer,
    MapOptions,
    create_layer_from_geo_data_frame,
    create_map,
)


def test_create_map():
    data = gpd.read_file(get_path("ny.bb"))
    m = create_map(data, fit_bounds=False, map_options=MapOptions(zoom=4))

    print(m.map_options)
    # print(m._message_queue)
    print(m._message_queue[0])

    assert m.map_options["zoom"] == 4


def test_create_layer_from_geo_data_frame():
    data = gpd.read_file(get_path("ny.bb"))
    print(data)

    layer = create_layer_from_geo_data_frame(
        data,
        color="BoroCode",
        pal=ColorPalette("yellow", "green"),
        id_="geo-pandas-data-frame",
    )
    print(layer.source["data"]["features"][0]["properties"])
    layer.source = None
    print(layer)

    assert layer.id == "geo-pandas-data-frame"
