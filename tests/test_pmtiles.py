from maplibre.pmtiles_utils import (
    DemoPMTiles,
    PMTiles,
    PMTilesMetaData,
    get_pmtiles_header,
    get_pmtiles_metadata,
)


def test_get_pmtiles_header():
    # Prepare
    path = DemoPMTiles.r2_public_protomaps_com_us_zcta

    # Act
    header = get_pmtiles_header(path)
    print(header)

    # Assert
    assert header["version"] == 3


def test_get_pmtiles_metadata():
    # Prepare
    # path = DemoPMTiles.r2_public_protomaps_com_us_zcta
    path = DemoPMTiles.data_source_coop_openstreetmap

    # Act
    metadata = get_pmtiles_metadata(path)
    print(metadata.keys())

    metadata_model = PMTilesMetaData(**metadata)
    print(metadata_model)
    print(metadata_model.layer_ids)


def test_pmtiles_class():
    # Prepare
    path = DemoPMTiles.data_source_coop_openstreetmap

    tiles = PMTiles(path)
    print(tiles.header)
    # print(tiles.meta_data)
