import maplibre.express as mx

path = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_shp.geojson"

data = mx.read_file(path)  # [["name", "region", "geometry"]]
print(data)

m = data.maplibre.to_map(
    "region",
    tooltip_props=["name", "region"],
    cmap="YlOrRd",
    controls=[
        mx.NavigationControl(),
        mx.ScaleControl(),
        # mx.GeolocateControl(),
    ],
    extrusion_column=["*", 100, ["get", "diss_me"]],
)
filename = m.save("/tmp/py-maplibre-gl-express.html", preview=True)
print(filename)
