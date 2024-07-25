# from maplibre.sources import SimpleFeatures
from geopandas import read_file
from maplibre import Layer, LayerType, Map, MapOptions
from maplibre.basemaps import Carto
from maplibre.colors import color_match_expr
from maplibre.controls import ControlPosition, NavigationControl, ScaleControl
from maplibre.expressions import interpolate_linear

path = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"
# path = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
# path = "/home/stefan/tmp/vancouver-blocks.json"

data = read_file(path)

m = Map(
    MapOptions(style=Carto.POSITRON, bounds=data.total_bounds),
    # layers=[Layer(type=LayerType.FILL, source=data, id="states")],
    layers=[
        Layer(
            type=LayerType.FILL,
            source=data,
            id="states",
            # paint={"fill-color": color_match_expr("name", categories=data.name)},
            paint={"fill-color": color_match_expr("region", categories=data.region)},
        )
    ],
    controls=[NavigationControl(), ScaleControl(position=ControlPosition.BOTTOM_LEFT)],
)
m.add_tooltip("states")
m.save("/tmp/py-maplibre-express.html")
