from typing import Optional, Union

from geopandas import read_file
from pydantic import BaseModel

from maplibre.sources import GeoJSONSource


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


class PaintProperties(BaseModel):
    line_color: Union[str, list, None]
    line_opacity: Union[float, int, None]
    line_width: Union[float, int, None]
    fill_color: Union[str, list, None]
    fill_opacity: Union[float, int, None]
    fill_outline_color: Union[str, list, None]
    fill_extrusion_color: Union[str, list, None]
    fill_extrusion_opacity: Union[float, int, None]
    circle_color: Union[str, list, None]
    circle_opacity: Union[float, int, None]
    circle_stroke_color: Union[str, list, None]
    circle_radius: Union[float, int, None]
