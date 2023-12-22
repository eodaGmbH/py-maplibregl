from uuid import uuid4

from ._utils import fix_keys


class Layer(object):
    def __init__(self, type_: str, id_: str = None, **kwargs):
        self._data = {
            "id": id_ or uuid4(),
            "type": type_,
        }
        self._data = fix_keys(kwargs)
        for k, v in self._data.items():
            if k in ["paint", "layout"]:
                self._data[k] = fix_keys(kwargs[k])

    @property
    def data(self) -> dict:
        return self._data
