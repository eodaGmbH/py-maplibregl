class Popup(object):
    def __init__(self, text: str = None, options: dict = {}):
        self._data = {"text": text, "options": options}

    @property
    def data(self):
        return self._data
