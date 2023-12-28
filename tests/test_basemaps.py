from pymaplibregl.basemaps import Carto, construct_carto_basemap_url


def test_carto_basemaps():
    # Act
    basemap_url = construct_carto_basemap_url(Carto.DARK_MATTER)

    # Assert
    assert (
        basemap_url
        == "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
    )
