from __future__ import annotations

import gzip
import json
from typing import Optional

from pmtiles.reader import MemorySource, Reader
from pmtiles.tile import Compression, deserialize_header
from pydantic import BaseModel

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


def range_request(path: str, offset: int, length: int) -> requests.Response:
    headers = {"Range": f"bytes={offset}-{offset+length}"}
    return requests.get(path, headers=headers)


def get_pmtiles_header(path: str) -> dict:
    response = range_request(path, PMTILES_HEADER_OFFSET, PMTILES_HEADER_LENGTH)
    return deserialize_header(response.content)


def get_pmtiles_metadata(path: str) -> dict:
    header = get_pmtiles_header(path)
    response = range_request(path, header["metadata_offset"], header["metadata_length"])
    get_bytes = MemorySource(response.content)
    metadata = get_bytes(0, header["metadata_length"])
    if header["internal_compression"] == Compression.GZIP:
        metadata = gzip.decompress(metadata)

    return json.loads(metadata)


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


class PMTiles(object):
    def __init__(self, path: str):
        self.path = path

    @property
    def header(self) -> dict:
        return get_pmtiles_header(self.path)

    @property
    def meta_data(self) -> PMTilesMetaData:
        metadata = get_pmtiles_metadata(self.path)
        return PMTilesMetaData(**metadata)

    def layers(self, layer_ids: list = None) -> list:
        pass
