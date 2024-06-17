import requests
from maplibre import (Layer, LayerType, Map, MapContext, MapOptions,
                      output_maplibregl, render_maplibregl)
from maplibre.controls import NavigationControl
from maplibre.sources import GeoJSONSource
from shiny import App, reactive, ui

MAX_FEATURES = 30
SOURCE_ID_ISS_POSITION = "iss_position"
SOURCE_ID_ISS_LAST_POSITIONS = "iss-last-positions"


def where_is_the_iss() -> tuple:
    r = requests.get("https://api.wheretheiss.at/v1/satellites/25544").json()
    return (r["longitude"], r["latitude"])


def create_feature(lng_lat: tuple) -> dict:
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": lng_lat,
        },
        "properties": {"coords": ", ".join(map(str, lng_lat))},
    }


lng_lat = where_is_the_iss()
feature = create_feature(where_is_the_iss())
feature_collection = {"type": "FeatureCollection", "features": [feature]}

app_ui = ui.page_fluid(
    ui.panel_title("Where is the ISS"),
    ui.div("Click on Update to get the current position of the ISS."),
    ui.div(
        "The yellow dots show the positions before. Hover the blue dot to display the coordinates."
    ),
    output_maplibregl("mapylibre", height=600),
    ui.input_action_button("update", "Update"),
)


def server(input, output, session):
    @render_maplibregl
    def mapylibre():
        m = Map(MapOptions(center=lng_lat, zoom=3))
        m.add_control(NavigationControl())
        m.set_paint_property("water", "fill-color", "darkblue")
        m.add_source(
            SOURCE_ID_ISS_LAST_POSITIONS, GeoJSONSource(data=feature_collection)
        )
        m.add_layer(
            Layer(
                type=LayerType.CIRCLE,
                source=SOURCE_ID_ISS_LAST_POSITIONS,
                paint={"circle-color": "yellow", "circle-radius": 5},
            ),
        )
        m.add_source(SOURCE_ID_ISS_POSITION, GeoJSONSource(data=feature))
        m.add_layer(
            Layer(
                type=LayerType.CIRCLE,
                id="iss-position",
                source=SOURCE_ID_ISS_POSITION,
                paint={"circle-color": "lightblue", "circle-radius": 7},
            )
        )
        m.add_tooltip("iss-position", "coords")
        return m

    @reactive.Effect
    @reactive.event(input.update)
    async def update():
        print("Fetching new position")
        lng_lat = where_is_the_iss()
        print(lng_lat)
        if len(feature_collection["features"]) == MAX_FEATURES:
            feature_collection["features"] = []

        async with MapContext("mapylibre") as m:
            feature = create_feature(lng_lat)
            m.set_data(SOURCE_ID_ISS_POSITION, feature)
            feature_collection["features"].append(feature)
            m.set_data(SOURCE_ID_ISS_LAST_POSITIONS, feature_collection)
            m.add_call("flyTo", {"center": lng_lat, "speed": 0.5})


app = App(app_ui, server)
