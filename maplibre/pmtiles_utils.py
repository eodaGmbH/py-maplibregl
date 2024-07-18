from __future__ import annotations

import gzip
import json
from typing import Optional

from pmtiles.reader import MemorySource
from pmtiles.tile import Compression, TileType, deserialize_header
from pydantic import BaseModel

from .basemaps import construct_basemap_style
from .layer import Layer, LayerType
from .sources import RasterTileSource, VectorTileSource

try:
    import requests
except ImportError as e:
    print(e)
    requests = None

# See https://github.com/protomaps/PMTiles/blob/main/spec/v3/spec.md for specs

PMTILES_HEADER_OFFSET = 0
PMTILES_HEADER_LENGTH = 127


class DemoPMTiles(object):
    data_source_coop_openstreetmap = (
        "https://data.source.coop/protomaps/openstreetmap/tiles/v3.pmtiles"
    )
    pmtiles_io_stamen = "https://pmtiles.io/stamen_toner(raster)CC-BY+ODbL_z3.pmtiles"
    r2_public_protomaps_com_us_zcta = "https://r2-public.protomaps.com/protomaps-sample-datasets/cb_2018_us_zcta510_500k.pmtiles"
    pmtiles_io_ugs_mt_whitney = (
        "https://pmtiles.io/usgs-mt-whitney-8-15-webp-512.pmtiles"
    )
    pmtiles_io_vector_firenze_base_layer = (
        "https://pmtiles.io/protomaps(vector)ODbL_firenze.pmtiles"
    )


class PMTilesHeader(BaseModel):
    version: int
    metadata_offset: int
    metadata_length: int
    min_lon_e7: int
    min_lat_e7: int
    max_lon_e7: int
    max_lat_e7: int
    min_zoom: int
    max_zoom: int
    tile_type: TileType

    @property
    def bounds(self):
        return tuple(
            [
                v / 1e7
                for v in [
                    self.min_lon_e7,
                    self.min_lat_e7,
                    self.max_lon_e7,
                    self.max_lat_e7,
                ]
            ]
        )


class PMTilesMetaData(BaseModel):
    # bounds: tuple
    name: Optional[str] = None
    description: Optional[str] = None
    attribution: Optional[str] = None
    type: Optional[str] = None
    version: Optional[str] = None
    vector_layers: Optional[list] = None

    @property
    def layer_ids(self) -> list:
        return [vector_layer["id"] for vector_layer in self.vector_layers]


def range_request(path: str, offset: int, length: int) -> requests.Response:
    headers = {"Range": f"bytes={offset}-{offset+length}"}
    return requests.get(path, headers=headers)


def get_pmtiles_header(path: str) -> dict:
    response = range_request(path, PMTILES_HEADER_OFFSET, PMTILES_HEADER_LENGTH)
    return deserialize_header(response.content)


def get_pmtiles_metadata(path: str) -> tuple:
    header = get_pmtiles_header(path)
    response = range_request(path, header["metadata_offset"], header["metadata_length"])
    get_bytes = MemorySource(response.content)
    metadata = get_bytes(0, header["metadata_length"])
    if header["internal_compression"] == Compression.GZIP:
        metadata = gzip.decompress(metadata)

    return header, json.loads(metadata)


class PMTiles(object):
    def __init__(self, path: str):
        self.path = path
        self._header, self._metadata = get_pmtiles_metadata(path)

    @property
    def header(self) -> PMTilesHeader:
        return PMTilesHeader(**self._header)

    @property
    def metadata(self) -> PMTilesMetaData:
        return PMTilesMetaData(**self._metadata)

    @property
    def protocol_url(self) -> str:
        return f"pmtiles://{self.path}"

    def layers(self, layer_ids: list = None) -> list:
        pass

    def to_source(self, **kwargs):
        if self.header.tile_type in [TileType.PNG, TileType.JPEG, TileType.WEBP]:
            source = RasterTileSource(url=self.protocol_url)
            if self.metadata.attribution:
                source.attribution = self.metadata.attribution

            return source

        elif self.header.tile_type == TileType.MVT:
            source = VectorTileSource(url=self.protocol_url)
            if self.metadata.attribution:
                source.attribution = self.metadata.attribution

            return source

        return

    def to_basemap_style(self, layer_styles: list) -> dict:
        source_id = self.metadata.name or "pmtiles"
        default_opacity = 1.0
        # Simple layer specs / props
        # layers: [layer_id (source_layer), layer_type, color, opacity]
        layers = []
        for layer_style in layer_styles:
            if len(layer_style) == 3:
                layer_style.append(default_opacity)

            layer_id, layer_type, color, opacity = layer_style
            layer_type = LayerType(layer_type).value
            layers.append(
                Layer(
                    id=layer_id,
                    source=source_id,
                    source_layer=layer_id,
                    type=layer_type,
                    paint={
                        f"{layer_type}-color": color,
                        f"{layer_type}-opacity": opacity,
                    },
                )
            )
        return construct_basemap_style(
            sources={source_id: self.to_source()}, layers=layers
        )