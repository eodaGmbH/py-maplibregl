import requests
from maplibre import (
    Layer,
    LayerType,
    Map,
    MapContext,
    MapOptions,
    output_maplibregl,
    render_maplibregl,
)
from maplibre.controls import Marker
from maplibre.sources import GeoJSONSource
from shiny import App, reactive, ui


def where_is_the_iss() -> tuple:
    r = requests.get("https://api.wheretheiss.at/v1/satellites/25544").json()
    return (r["longitude"], r["latitude"])


def create_feature(lng_lat) -> dict:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": lng_lat},
    }


lng_lat = where_is_the_iss()
print(lng_lat)
feature = create_feature(lng_lat)
print(feature)

app_ui = ui.page_fluid(
    ui.h1("Where is the ISS"),
    output_maplibregl("mapylibre", height=600),
    ui.input_action_button("update", "Update"),
)


def server(input, output, session):
    @render_maplibregl
    def mapylibre():
        m = Map(MapOptions(center=lng_lat, zoom=3))
        m.add_source("iss", GeoJSONSource(data=feature))
        m.add_layer(
            Layer(
                type=LayerType.CIRCLE,
                source="iss",
                paint={"circle-color": "yellow", "circle-radius": 5},
            ),
        )
        return m

    @reactive.Effect
    @reactive.event(input.update)
    async def update():
        print("Fetching new position")
        lng_lat = where_is_the_iss()
        print(lng_lat)
        async with MapContext("mapylibre") as m:
            # m.add_marker(Marker(lng_lat=lng_lat))
            m.add_call("setSourceData", "iss", create_feature(lng_lat))


app = App(app_ui, server)
