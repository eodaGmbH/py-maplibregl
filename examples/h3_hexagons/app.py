import h3
import pandas as pd

# import shapely
from pymaplibregl import (
    Layer,
    LayerType,
    Map,
    MapContext,
    output_maplibregl,
    render_maplibregl,
)
from pymaplibregl.basemaps import Carto
from pymaplibregl.utils import GeometryType, df_to_geojson, get_bounds
from shiny import App, reactive, ui

LAYER_ID = "motor_vehicle_collisions"


def create_h3_hexagons(df: pd.DataFrame, lng: str = "lng", lat: str = "lat"):
    df = (
        df.apply(lambda x: h3.geo_to_h3(x[lat], x[lng], resolution=7), axis=1)
        .to_frame("h3")
        .groupby("h3", as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )

    df["hexagon"] = df.apply(
        lambda x: [h3.h3_to_geo_boundary(x["h3"], geo_json=True)], axis=1
    )

    return df


motor_vehicle_collisions_data = pd.read_csv(
    "https://github.com/crazycapivara/mapboxer/raw/master/data-raw/motor_vehicle_collisions.csv",
    sep=";",
)
motor_vehicle_collisions_source = {
    "type": "geojson",
    "data": df_to_geojson(
        motor_vehicle_collisions_data,
        properties=["date", "time", "injured", "killed"],
    ),
}

# ### h3

H3_LAYER_ID = "h3-hexagons"
h3_source = {
    "type": "geojson",
    "data": df_to_geojson(
        create_h3_hexagons(motor_vehicle_collisions_data),
        "hexagon",
        "Polygon",
        properties=["count"],
    ),
}
h3_layer = Layer(
    LayerType.FILL,
    id_=H3_LAYER_ID,
    source=h3_source,
    paint={
        "fill-color": [
            "step",
            ["get", "count"],
            "yellow",
            5,
            "orange",
            10,
            "red",
            25,
            "darkred",
        ],
        "fill-opacity": 0.4,
    },
)

h3_fill_extrusion_layer = Layer(
    LayerType.FILL_EXTRUSION,
    source=h3_source,
    paint={
        "fill-extrusion-color": [
            "step",
            ["get", "count"],
            "yellow",
            5,
            "orange",
            10,
            "red",
            25,
            "darkred",
        ],
        "fill-extrusion-opacity": 0.7,
        "fill-extrusion-height": ["*", ["to-number", ["get", "count"]], 300],
    },
)
# ###

"""
bbox = shapely.bounds(
    shapely.from_geojson(json.dumps(motor_vehicle_collisions_source["data"]))
)
"""
# bbox = get_bounds(motor_vehicle_collisions_source["data"])
bbox = get_bounds(h3_source["data"])
print(bbox)


motor_vehicle_collisions_layer = Layer(
    LayerType.CIRCLE,
    id_=LAYER_ID,
    source=motor_vehicle_collisions_source,
    paint={
        "circle-color": [
            "match",
            ["get", "injured"],
            0,
            "yellow",
            1,
            "orange",
            "darkred",
        ]
    },
)

app_ui = ui.page_fluid(
    ui.panel_title("Motor Vehicle Collisions NYC"),
    output_maplibregl("maplibre", height=600),
    # ui.input_slider("radius", "Radius", value=CIRCLE_RADIUS, min=1, max=5),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(
            style=Carto.POSITRON,
            pitch=30,
            bounds=list(bbox),
            fitBoundsOptions={"padding": 20},
        )
        # m.add_layer(flights_layer)
        # m.add_layer(h3_layer)
        # m.add_layer(motor_vehicle_collisions_layer)
        # m.add_popup(H3_LAYER_ID, "count")
        m.add_layer(h3_fill_extrusion_layer)
        return m

    """
    @reactive.Effect
    @reactive.event(input.radius, ignore_init=True)
    async def radius():
        async with MapContext("maplibre") as m:
            m.set_paint_property(LAYER_ID, "circle-radius", input.radius())
    """


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
