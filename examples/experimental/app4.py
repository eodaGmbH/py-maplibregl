import pandas as pd
from pymaplibregl import Layer, Map, output_maplibregl, render_maplibregl
from pymaplibregl.basemaps import Carto
from shiny import App, reactive, render, ui

point_data = pd.read_json(
    "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/scatterplot/manhattan.json"
)
point_data.columns = ["lng", "lat", "sex"]

circle_layer = Layer(
    "circle",
    id_="counties",
    source={
        "type": "geojson",
        "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/arc/counties.json",
    },
    paint={"circle-color": "black", "circle-radius": 7},
)

center = [-118.0931, 33.78615]

app_ui = ui.page_fluid(
    ui.panel_title("Hello PyMapLibreGL!"),
    output_maplibregl("maplibre", height=500),
)


def server(input, output, session):
    @render_maplibregl
    async def maplibre():
        m = Map(style=Carto.POSITRON, center=[-73.987157, 40.729906], zoom=12)
        m.add_point_source(
            "every-person-in-manhattan", point_data.to_dict("split", index=False)
        )
        # m.add_layer(circle_layer)
        m.add_layer(
            Layer(
                "circle",
                source="every-person-in-manhattan",
                paint={"circle-color": "darkred"},
            )
        )
        return m


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
