import h3
import pandas as pd

# import shapely
from maplibre import (
    Layer,
    LayerType,
    Map,
    MapContext,
    output_maplibregl,
    render_maplibregl,
)
from maplibre.basemaps import Carto
from maplibre.utils import GeometryType, df_to_geojson, get_bounds
from shiny import App, reactive, ui

LAYER_ID = "motor_vehicle_collisions"

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
motor_vehicle_collisions_data["h3_index"] = motor_vehicle_collisions_data.apply(
    lambda x: h3.geo_to_h3(x["lat"], x["lng"], resolution=7), axis=1
)

df_aggr = (
    motor_vehicle_collisions_data[["h3_index", "injured", "killed"]]
    .groupby("h3_index", as_index=False)
    .sum()
)
df_aggr["hexagon"] = df_aggr.apply(
    lambda x: [h3.h3_to_geo_boundary(x["h3_index"], geo_json=True)], axis=1
)
H3_LAYER_ID = "h3-hexagons"
h3_source = {
    "type": "geojson",
    "data": df_to_geojson(df_aggr, "hexagon", "Polygon", properties=["injured"]),
}
h3_layer = Layer(
    LayerType.FILL,
    id_=H3_LAYER_ID,
    source=h3_source,
    paint={
        "fill-color": [
            "step",
            ["get", "injured"],
            "yellow",
            2,
            "orange",
            5,
            "darkred",
            15,
            "black",
        ],
        "fill-opacity": 0.4,
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
            bounds=list(bbox),
            fitBoundsOptions={"padding": 20},
        )
        # m.add_layer(flights_layer)
        m.add_layer(h3_layer)
        m.add_layer(motor_vehicle_collisions_layer)
        m.add_popup(H3_LAYER_ID, "injured")
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
