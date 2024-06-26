export default class LayerSwitcherControl {
  constructor(options) {
    this._options = options || {};
  }

  onAdd(map) {
    this._map = map;
    this._container = document.createElement("div");
    // this._container.classList.add("maplibregl-ctrl", "maplibregl-ctrl-group");
    this._container.className = "maplibregl-ctrl maplibregl-ctrl-group";
    this._container.style.cssText = this._options.cssText || "";
    this._container.innerHTML = "We out here.";
    return this._container;
  }

  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}
