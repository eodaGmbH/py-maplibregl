from enum import Enum


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
