export default class InfoBoxControl {
  constructor(options) {
    this._options = options || {};
  }

  onAdd(map) {
    this._map = map;
    this._container = document.createElement("div");
    this._container.className = "maplibregl-ctrl maplibregl-ctrl-group";
    this._container.style.cssText = this._options.cssText || "padding: 10px;";
    this._container.innerHTML = this._options.content || "We out here.";
    return this._container;
  }

  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}
