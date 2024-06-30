import { createToggleLayerLink } from "../utils";

import "../css/custom-opacity-control.css";

function createLabel(layerId) {
  const label = document.createElement("span");
  label.innerHTML = layerId;
  return label;
}

function getOpacityPropName(map, layerId) {
  const layer = map.getLayer(layerId);
  return `${layer.type}-opacity`;
}

function createSlider(
  map,
  layerId,
  toggleLayers = false,
  flexDirection = "column",
) {
  const label = toggleLayers
    ? createToggleLayerLink(map, layerId)
    : createLabel(layerId);
  const slider = document.createElement("input");
  slider.type = "range";
  slider.min = "0";
  slider.max = "1.0";
  slider.step = "0.1";

  // This might fail if layer is not already added to the map
  // TODO: Put it in a try catch statement
  const prop = getOpacityPropName(map, layerId);
  const currentValue = map.getPaintProperty(layerId, prop) || 1;
  console.log("currentValue", currentValue);
  slider.value = currentValue;
  // -------------------------

  slider.style.width = "100px";
  slider.oninput = function (e) {
    const prop = getOpacityPropName(map, layerId);
    const value = parseFloat(this.value);
    console.log(prop, value);
    map.setPaintProperty(layerId, prop, value);
  };
  const div = document.createElement("div");
  div.id = "menu";
  div.style.flexDirection = flexDirection;
  if (div.style.flexDirection === "row") {
    div.appendChild(slider);
    div.appendChild(label);
    return div;
  }

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
    this._container.className =
      "maplibregl-ctrl maplibregl-ctrl-group layer-switcher-ctrl-simple layer-opacity-ctrl";
    this._container.style.cssText = this._options.cssText || "padding: 5px;";
    const layerIds = this._options.layerIds || [];
    const toggleLayers = this._options.toggleLayers || false;
    const flexDirection = this._options.flexDirection || "column";
    for (const layerId of layerIds) {
      const slider = createSlider(map, layerId, toggleLayers, flexDirection);
      this._container.appendChild(slider);
    }
    return this._container;
  }

  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}
