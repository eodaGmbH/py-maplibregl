import geopandas as gpd
from geodatasets import get_path
from maplibre.express import create_map


def test_create_map():
    data = gpd.read_file(get_path("ny.bb"))
    m = create_map(data, fit_bounds=False, zoom=4)

    print(m.map_options)
    print(m._message_queue)

    assert m.map_options["zoom"] == 4
