_points = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/scatterplot/manhattan.json"
_geojson = "https://docs.mapbox.com/mapbox-gl-js/assets/indoor-3d-map.geojson"


class Layer(object):
    def __init__(self, id_: str, type_: str, **kwargs):
        self._properties = {
            "id": id_,
            "type": type_,
        }
        self._properties.update(kwargs)

    def to_dict(self) -> dict[str, str]:
        return self._properties
