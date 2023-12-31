# see also https://docs.mapbox.com/mapbox-gl-js/api/markers/#fullscreencontrol
from enum import Enum
from typing import Literal, Union

from pydantic import Field

from ._utils import BaseModel


class ControlType(Enum):
    NAVIGATION = "NavigationControl"
    SCALE = "ScaleControl"
    FULLSCREEN = "FullscreenControl"
    GEOLOCATE = "GeolocateControl"
    ATTRIBUTION = "AttributionControl"


class ControlPosition(Enum):
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"


class Control(BaseModel):
    pass


class AttributionControl(BaseModel):
    _name: str = ControlType.ATTRIBUTION.value
    compact: bool = None
    custom_attribution: Union[str, list] = Field(
        None, serialization_alias="customAttribution"
    )


class FullscreenControl(Control):
    _name: str = ControlType.FULLSCREEN.value


class GeolocateControl(Control):
    _name: str = ControlType.GEOLOCATE.value
    position_options: dict = Field(None, serialization_alias="positionOptions")
    show_accuracy_circle: bool = Field(True, serialization_alias="showAccuracyCircle")
    show_user_heading: bool = Field(False, serialization_alias="showUserHeading")
    show_user_location: bool = Field(True, serialization_alias="showUserLocation")
    track_user_location: bool = Field(False, serialization_alias="trackUserLocation")


class NavigationControl(Control):
    _name: str = ControlType.NAVIGATION.value
    sho_compass: bool = Field(True, serialization_alias="showCompass")
    show_zoom: bool = Field(True, serialization_alias="showZoom")
    visualize_pitch: bool = Field(False, serialization_alias="visualizePitch")


"""
class Unit(Enum):
    IMPERIAL = "imperial"
    METRIC = "metric"
    NAUTICAL = "nautical"
"""


class ScaleControl(Control):
    _name: str = ControlType.SCALE.value
    max_width: int = Field(None, serialization_alias="maxWidth")
    unit: Literal["imperial", "metric", "nautical"] = "metric"
