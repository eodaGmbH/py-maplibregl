import geopandas as gpd
from geodatasets import get_path
from maplibre.express import LayerOptions, create_layer, create_map


def test_create_map():
    data = gpd.read_file(get_path("ny.bb"))
    m = create_map(data, fit_bounds=False, zoom=4)

    print(m.map_options)
    # print(m._message_queue)
    print(m._message_queue[0])

    assert m.map_options["zoom"] == 4


def test_create_layer_from_geo_data_frame():
    layer_options = LayerOptions(id="geo-pandas-data-frame")
    data = gpd.read_file(get_path("ny.bb"))
    print(data)

    layer = create_layer(
        data,
        color_column="BoroCode",
        options=layer_options,
    )
    print(layer.source["data"]["features"][0]["properties"])
    layer.source = None
    print(layer)

    assert layer.id == "geo-pandas-data-frame"
