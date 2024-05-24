from maplibre import Map
from maplibre.shiny import MapLibreRenderer
from shiny.express import ui

ui.h1("Hello world!")


@MapLibreRenderer
def mapylibre():
    return Map()
