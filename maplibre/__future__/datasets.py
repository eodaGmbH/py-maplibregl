from typing import Optional, Union

import geopandas as gpd

# from geopandas import read_file
from maplibre.sources import GeoJSONSource
from pydantic import BaseModel


class DataSet(BaseModel):
    url: str
    name: Optional[str] = None
    geometry_type: Union[str, list, None] = None
    bounds: Optional[tuple] = None

    @property
    def source(self) -> GeoJSONSource:
        return GeoJSONSource(data=self.url)

    def read_bounds(self) -> tuple:
        return read_file(self.url).total_bounds

    def read_data(self) -> gpd.GeoDataFrame:
        return gpd.read_file(self.url)


# TODO: Create DataSets from yaml file
class DataSets:
    vancouver_blocks: DataSet = DataSet(
        url="https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json",
        name="vancouver_blocks",
        geometry_type="Polygon",
        bounds=(-123.2639151, 49.1995174, -123.0234703, 49.295612),
    )

    indoor_3d_map: DataSet = DataSet(
        url="https://maplibre.org/maplibre-gl-js/docs/assets/indoor-3d-map.geojson",
        name="indoor_3d_map",
        bounds=(-87.618347, 41.865559, -87.615411, 41.866868),
    )

    urban_areas: DataSet = DataSet(
        url="https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson",
        name="urban_areas",
        bounds=(-157.98399472, -46.26844166, 174.97002323, 69.35127106),
    )

    earthquakes: DataSet = (
        DataSet(
            url="https://docs.mapbox.com/mapbox-gl-js/assets/earthquakes.geojson",
            name="earthquakes",
            bounds=None,
        ),
    )

    bart: DataSet = DataSet(
        url="https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart.geo.json",
        name="bart",
        geometry_type=["Point", "MultiLineString", "Polygon"],
    )
