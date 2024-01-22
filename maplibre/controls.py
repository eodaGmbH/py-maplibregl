""" Markers and controls

See also https://docs.mapbox.com/mapbox-gl-js/api/markers/
"""
from enum import Enum
from typing import Literal, Union

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field

from ._utils import BaseModel


class PopupOptions(BaseModel):
    """Popup options"""

    anchor: str = None
    close_button: bool = Field(False, serialization_alias="closeButton")
    close_on_click: bool = Field(None, serialization_alias="closeOnClick")
    close_on_move: bool = Field(None, serialization_alias="closeOnMove")
    max_width: int = Field(None, serialization_alias="maxWidth")
    offset: Union[int, list, dict] = None


class Popup(BaseModel):
    """Popup

    Attributes:
        text: The Text of the popup.
        options (PopupOptions | dict): Popup options.
    """

    text: str
    options: Union[PopupOptions, dict] = {}


class MarkerOptions(BaseModel):
    """Marker options"""

    anchor: str = None
    color: str = None
    draggable: bool = None
    offset: Union[tuple, list] = None
    pitch_alignment: str = Field(None, serialization_alias="pitchAlignment")
    rotation: int = None
    rotation_alignment: str = Field(None, serialization_alias="rotationAlignment")
    scale: int = None


class Marker(BaseModel):
    """Marker

    Attributes:
        lng_lat (tuple |list): **Required.** The longitude and latitude of the marker.
        popup (Popup | dict): The Popup that is displayed when a user clicks on the marker.
        options (MarkerOptions | dict): Marker options.
    """

    lng_lat: Union[tuple, list] = Field(None, serialization_alias="lngLat")
    popup: Union[Popup, dict] = None
    options: Union[MarkerOptions, dict] = {}


class ControlType(Enum):
    NAVIGATION = "NavigationControl"
    SCALE = "ScaleControl"
    FULLSCREEN = "FullscreenControl"
    GEOLOCATE = "GeolocateControl"
    ATTRIBUTION = "AttributionControl"


class ControlPosition(Enum):
    """Control position

    Attributes:
        TOP_LEFT: top-left
        TOP_RIGHT: top-right
        BOTTOM_LEFT: bottom-left
        BOTTOM_RIGHT: bottom-right
    """

    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"


class Control(BaseModel):
    @property
    def type(self):
        return self.__class__.__name__


class AttributionControl(Control):
    """Attribution control"""

    # _name: str = ControlType.ATTRIBUTION.value
    compact: bool = None
    custom_attribution: Union[str, list] = Field(
        None, serialization_alias="customAttribution"
    )


class FullscreenControl(Control):
    """Fullscreen control

    Examples:
        >>> from maplibre import Map
        >>> from maplibre.controls import FullscreenControl, ControlPosition

        >>> map = Map()
        >>> map.add_control(FullscreenControl(), ControlPosition.BOTTOM_LEFT)
    """

    # _name: str = ControlType.FULLSCREEN.value
    pass


class GeolocateControl(Control):
    """Geolocate control"""

    # _name: str = ControlType.GEOLOCATE.value
    position_options: dict = Field(None, serialization_alias="positionOptions")
    show_accuracy_circle: bool = Field(True, serialization_alias="showAccuracyCircle")
    show_user_heading: bool = Field(False, serialization_alias="showUserHeading")
    show_user_location: bool = Field(True, serialization_alias="showUserLocation")
    track_user_location: bool = Field(False, serialization_alias="trackUserLocation")


class NavigationControl(Control):
    """Navigation control"""

    # _name: str = ControlType.NAVIGATION.value
    show_compass: bool = Field(True, serialization_alias="showCompass")
    show_zoom: bool = Field(True, serialization_alias="showZoom")
    visualize_pitch: bool = Field(False, serialization_alias="visualizePitch")


class ScaleUnit(Enum):
    IMPERIAL = "imperial"
    METRIC = "metric"
    NAUTICAL = "nautical"


class ScaleControl(Control):
    """Scale control"""

    # _name: str = ControlType.SCALE.value
    max_width: int = Field(None, serialization_alias="maxWidth")
    unit: Literal["imperial", "metric", "nautical"] = "metric"
