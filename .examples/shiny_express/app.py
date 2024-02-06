from maplibre import Map
from maplibre.shiny import render_maplibre
from shiny.express import ui

ui.h1("Hello world!")


@render_maplibre
def mapylibre():
    return Map()
