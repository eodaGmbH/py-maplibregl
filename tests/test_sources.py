from __future__ import annotations

from maplibre.sources import *


def test_geojson_source():
    # Prepare
    data = "https://raw.githubusercontent.com"

    # Act
    geojson_source = GeoJSONSource(data=data, cluster_radius=2, cluster_min_points=10)

    # print(geojson_source.model_dump(exclude_none=True, by_alias=True))
    print(geojson_source.to_dict())
    # print(dict(geojson_source))

    # Assert
    assert geojson_source.to_dict() == {
        "type": "geojson",
        "data": data,
        "clusterRadius": 2,
        "clusterMinPoints": 10,
    }


def test_vector_tile_source():
    # Prepare
    tiles = ["https://demotiles.maplibre.org/tiles/{z}/{x}/{y}.pbf"]
    min_zoom = 0
    max_zoom = 6

    # Act
    vector_tile_source = VectorTileSource(
        tiles=tiles, min_zoom=min_zoom, max_zoom=max_zoom
    )
    print(vector_tile_source)
    print(vector_tile_source.to_dict())

    # Assert
    assert vector_tile_source.to_dict() == {
        "maxzoom": max_zoom,
        "minzoom": min_zoom,
        "tiles": tiles,
        "type": "vector",
    }
