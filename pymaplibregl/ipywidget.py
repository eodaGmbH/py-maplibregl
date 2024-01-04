import traitlets
from anywidget import AnyWidget

from ._utils import get_internal_file_path
from .map import MapOptions

_esm = """import maplibregl from "https://esm.sh/maplibre-gl@3.6.2";

export function render({model, el}) {
    console.log('maplibregl', maplibregl.version);
    
    // console.log(mapOptions);
    const ID = "pymaplibregl"
    const container = document.createElement('div');
    container.id = ID;
    container.style.height="600px";
    // container.style.width = "900px";
    // container.style.background = "yellow";
    
    const mapOptions = Object.assign({ container: container }, model.get("map_options"));
    /*
    const mapOptions = {
        container: container,
        style: "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
        center: [1, 2],
        zoom: 2
    };
    */
    
    console.log(mapOptions);
    
    const map = new maplibregl.Map(mapOptions);
    map.addControl(new maplibregl.NavigationControl());
    map.once("load", () => {
        map.resize();
    });
    
    el.appendChild(container);
}
"""


class MaplibreWidget(AnyWidget):
    _esm = _esm
    _css = "https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css"
    # _css = get_internal_file_path("src", "maplibregl-gl.css")

    map_options = traitlets.Dict(MapOptions().to_dict()).tag(sync=True)

    def __init__(self, map_options=MapOptions(), *args, **kwargs):
        self.map_options = map_options.to_dict()
        super().__init__(*args, **kwargs)
