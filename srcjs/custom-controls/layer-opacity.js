function createSlider(map, layerId) {
  const label = document.createElement("span");
  label.innerHTML = layerId;
  const slider = document.createElement("input");
  slider.type = "range";
  slider.min = "0";
  slider.max = "1.0";
  slider.step = "0.1";
  slider.style.width = "100px";
  slider.oninput = function (e) {
    const layer = map.getLayer(layerId);
    const prop = `${layer.type}-opacity`;
    const value = parseFloat(this.value);
    console.log(prop, value);
    // layer.setPaintProperty(prop, value);
    map.setPaintProperty(layerId, prop, value);
  };
  const div = document.createElement("div");
  div.style.cssText =
    "display: flex; flex-direction: column; align-items: center; border-bottom: 1px solid black; padding-bottom: 10px;";
  div.appendChild(label);
  div.appendChild(slider);
  return div;
}

export default class LayerOpacityControl {
  constructor(options) {
    this._options = options;
  }

  onAdd(map) {
    this._map = map;
    this._container = document.createElement("div");
    this._container.className = "maplibregl-ctrl maplibregl-ctrl-group";
    this._container.style.cssText = this._options.cssText || "padding: 5px;";
    const layerIds = this._options.layerIds || [];
    for (const layerId of layerIds) {
      const slider = createSlider(map, layerId);
      this._container.appendChild(slider);
    }
    return this._container;
  }

  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}
