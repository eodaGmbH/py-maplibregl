from typing import Optional, Union

from geopandas import read_file
from maplibre.sources import GeoJSONSource
from pydantic import BaseModel


class DataSet(BaseModel):
    url: str
    name: Optional[str] = None
    geometry_type: Union[str, list, None] = None
    bounds: Optional[tuple] = None

    @property
    def source(self):
        return GeoJSONSource(data=self.url)

    def read_bounds(self) -> tuple:
        return read_file(self.url).total_bounds


class DataSets:
    vancouver_blocks: DataSet = DataSet(
        url="https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json",
        name="vancouver-blocks",
        geometry_type="Polygon",
        bounds=(-123.2639151, 49.1995174, -123.0234703, 49.295612),
    )

    indoor_3d_map: DataSet = DataSet(
        url="https://maplibre.org/maplibre-gl-js/docs/assets/indoor-3d-map.geojson",
        name="indoor_3d_map",
        bounds=(-87.618347, 41.865559, -87.615411, 41.866868),
    )
