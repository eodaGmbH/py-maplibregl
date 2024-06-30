import geopandas as gpd
from maplibre.express import create_map


def test_create_map():
    data = gpd.read_file(gpd.datasets.get_path("nybb"))
    m = create_map(data, fit_bounds=False, zoom=4)

    print(m.map_options)
    print(m._message_queue)

    assert m.map_options["zoom"] == 4
