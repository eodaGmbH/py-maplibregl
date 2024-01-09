from maplibre.basemaps import (Carto, background, construct_basemap_style,
                               construct_carto_basemap_url)


def test_carto_basemaps():
    # Act
    basemap_url = construct_carto_basemap_url(Carto.DARK_MATTER)

    # Assert
    assert (
        basemap_url
        == "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
    )


def test_background_style():
    # Prepare
    color = "white"

    # Act
    style = background(color=color)
    print(style)

    # Assert
    assert style["layers"][0]["paint"]["background-color"] == color
