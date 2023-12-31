from __future__ import annotations

import os
import pathlib
from tempfile import mkdtemp

from pydantic import BaseModel as BaseModel_
from pydantic import ConfigDict


def fix_keys(d: dict) -> dict:
    return {k.replace("_", "-"): v for k, v in d.items() if v is not None}


def get_output_dir(output_dir: str = None, prefix: str = "pymaplibregl_") -> str:
    if not output_dir:
        output_dir = mkdtemp(prefix=prefix)
    else:
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    return output_dir


def get_internal_file_path(*args):
    print(os.path.dirname(__file__))
    return os.path.join(os.path.dirname(__file__), *args)


def read_internal_file(*args):
    with open(get_internal_file_path(*args)) as f:
        content = f.read()

    return content


class BaseModel(BaseModel_):
    model_config = ConfigDict(
        validate_assignment=True, extra="allow", use_enum_values=True
    )

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)
