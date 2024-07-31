import geopandas as gpd
from maplibre import express as mx
from maplibre.__future__.datasets import DataSets
from maplibre.sources import CRS

# print(DataSets.bart.url)
geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-121.353637, 40.584978],
                        [-121.284551, 40.584758],
                        [-121.275349, 40.541646],
                        [-121.246768, 40.541017],
                        [-121.251343, 40.423383],
                        [-121.32687, 40.423768],
                        [-121.360619, 40.43479],
                        [-121.363694, 40.409124],
                        [-121.439713, 40.409197],
                        [-121.439711, 40.423791],
                        [-121.572133, 40.423548],
                        [-121.577415, 40.550766],
                        [-121.539486, 40.558107],
                        [-121.520284, 40.572459],
                        [-121.487219, 40.550822],
                        [-121.446951, 40.56319],
                        [-121.370644, 40.563267],
                        [-121.353637, 40.584978],
                    ]
                ],
            },
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Point", "coordinates": [-121.415061, 40.506229]},
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Point", "coordinates": [-121.505184, 40.488084]},
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {"type": "Point", "coordinates": [-121.354465, 40.488737]},
        },
    ],
}

d = gpd.GeoDataFrame.from_features(geojson["features"], crs=CRS)
print(d)

data = DataSets.bart.url

m = mx.map_this(d)
m.save("/tmp/py-maplibre-express.html")
# print(m.map_options)
# print(m._message_queue)
