// Mapbox Draw Plugin: https://github.com/mapbox/mapbox-gl-draw
import MapboxDraw from "https://esm.sh/@mapbox/mapbox-gl-draw@1.4.3";
// import "https://esm.sh/@mapbox/mapbox-gl-draw@1.4.3/dist/mapbox-gl-draw.css";
import "./css/mapbox-gl-draw.css";

MapboxDraw.constants.classes.CONTROL_BASE = "maplibregl-ctrl";
MapboxDraw.constants.classes.CONTROL_PREFIX = "maplibregl-ctrl-";
MapboxDraw.constants.classes.CONTROL_GROUP = "maplibregl-ctrl-group";

export default MapboxDraw;
