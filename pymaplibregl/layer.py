from uuid import uuid4

from ._utils import fix_keys


class Layer(object):
    def __init__(self, type_: str, id_: str = None, **kwargs):
        self._data = {
            "id": id_ or str(uuid4()),
            "type": type_,
        }
        kwargs = fix_keys(kwargs)
        for k, v in kwargs.items():
            if k in ["paint", "layout"]:
                kwargs[k] = fix_keys(kwargs[k])
        self._data.update(kwargs)

    @property
    def data(self) -> dict:
        return self._data
