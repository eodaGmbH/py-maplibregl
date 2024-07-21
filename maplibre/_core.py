from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class MapLibreBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        extra="forbid",
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )

    def to_dict(self) -> dict:
        return self.model_dump(by_alias=True, exclude_none=True)
