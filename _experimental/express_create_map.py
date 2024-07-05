import webbrowser

import geodatasets
import maplibre.express as mx

path = "https://github.com/Toblerity/Fiona/files/11151652/coutwildrnp.zip"
path = geodatasets.get_path("geoda.airbnb")
# airbnb = mx.read_file(geodatasets.get_path("geoda.airbnb"))
gdf = mx.read_file(path)


path = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"

m, layer_id = mx.create_map(
    path,
    # color_column="community",
    color_column="region",
    ret_layer_id=True,
    layer_options=mx.LayerOptions(
        type="fill-extrusion",
        paint={"fill-extrusion-height": ["*", 10000, ["get", "adm0_sr"]]},
    ),
    map_options=mx.MapOptions(pitch=35),
)
print(layer_id)
print(m.map_options)

filename = "/tmp/py-maplibre-express.html"
with open(filename, "w") as f:
    f.write(m.to_html())

webbrowser.open(filename)
