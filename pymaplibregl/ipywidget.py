from os.path import join
from pathlib import Path

import traitlets
from anywidget import AnyWidget

from .map import MapOptions


class MaplibreWidget(AnyWidget):
    _esm = join(Path(__file__).parent, "srcjs", "ipymaplibregl.js")

    map_options = traitlets.Dict().tag(sync=True)
    height = traitlets.Union([traitlets.Int(), traitlets.Unicode()]).tag(sync=True)
    test = traitlets.Unicode().tag(sync=True)

    def __init__(self, map_options=MapOptions(), **kwargs):
        self.map_options = map_options.to_dict()
        super().__init__(**kwargs)

    @traitlets.default("height")
    def _default_height(self):
        return "400px"

    @traitlets.validate("height")
    def _validate_height(self, proposal):
        height = proposal["value"]
        if isinstance(height, int):
            return f"{height}px"

        return height
