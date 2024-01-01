from __future__ import annotations

from pymaplibregl.sources import *


def test_geojson_source():
    # Prepare
    data = "https://raw.githubusercontent.com"

    # Act
    geojson_source = GeoJSONSource(
        data=data, test="test", cluster_radius=2, cluster_min_points=10
    )

    print(geojson_source.model_dump(exclude_none=True, by_alias=True))
    print(geojson_source.to_dict())
    print(dict(geojson_source))
