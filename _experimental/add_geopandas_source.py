# from maplibre.sources import SimpleFeatures
import maplibre.expressions as expr
from geopandas import read_file
from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.basemaps import Carto
from maplibre.controls import ControlPosition, NavigationControl, ScaleControl

# path = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"
# path = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
path = "/home/stefan/tmp/vancouver-blocks.json"

data = read_file(path)

m = Map(
    MapOptions(style=Carto.POSITRON, bounds=data.total_bounds),
    # layers=[Layer(type=LayerType.FILL, source=data, id="states")],
    layers=[
        Layer(
            type=LayerType.FILL,
            source=data,
            id="states",
            paint={
                # "fill-color": expr.interpolate_linear("growth", [0, 1.0], ["yellow", "red"])
                "fill-color": expr.color_quantile_step_expr(
                    "growth", [0.1, 0.25, 0.5, 0.75], values=data.growth
                )
            },
        )
    ],
    controls=[NavigationControl(), ScaleControl(position=ControlPosition.BOTTOM_LEFT)],
)
m.add_tooltip("states")
# m.set_data("states", data[data.growth < 0.3])
# m.add_control(NavigationControl(position="top-left"))
# m.add_source("states", data)
# m.add_layer(Layer(type=LayerType.LINE, source="states"))
# m.add_layer(Layer(type=LayerType.LINE, source=data))
m.save("/tmp/py-maplibre-express.html")
