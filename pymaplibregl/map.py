class Map(object):
    data: dict

    def __init__(self, **kwargs):
        self._data = {
            "style": "https://demotiles.maplibre.org/style.json",
            "center": [0, 0],
            "zoom": 1,
        }
        self._data.update(kwargs)

    @property
    def shiny_data(self):
        return self._data
