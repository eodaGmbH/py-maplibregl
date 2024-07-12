import "../css/custom-layer-switcher-control.css";

const THEMES = {
  default: "layer-switcher-ctrl",
  simple: "layer-switcher-ctrl-simple",
};

function createLayerLink(map, layerId) {
  const link = document.createElement("a");
  link.id = layerId;
  link.href = "#";
  link.textContent = layerId;
  const visibility = map.getLayoutProperty(layerId, "visibility");
  if (typeof visibility === "undefined" || visibility === "visible") {
    link.className = "active";
  }

  link.onclick = function (e) {
    const layerIdClicked = this.textContent;
    const visibility = map.getLayoutProperty(layerIdClicked, "visibility");
    console.log(layerIdClicked, visibility);
    if (typeof visibility === "undefined" || visibility === "visible") {
      map.setLayoutProperty(layerIdClicked, "visibility", "none");
      this.className = "";
      return;
    }

    map.setLayoutProperty(layerIdClicked, "visibility", "visible");
    this.className = "active";
  };
  return link;
}

function createMenu(map, layerIds) {
  const menu = document.createElement("div");
  menu.id = "layer-switcher-menu";
  for (const layerId of layerIds) {
    /*
    const link = document.createElement("a");
    link.id = layerId;
    link.href = "#";
    link.textContent = layerId;
    const visibility = map.getLayoutProperty(layerId, "visibility");
    if (typeof visibility === "undefined" || visibility === "visible") {
      link.className = "active";
    }

    link.onclick = function (e) {
      const layerIdClicked = this.textContent;
      const visibility = map.getLayoutProperty(layerIdClicked, "visibility");
      console.log(layerIdClicked, visibility);
      if (typeof visibility === "undefined" || visibility === "visible") {
        map.setLayoutProperty(layerIdClicked, "visibility", "none");
        this.className = "";
        return;
      }

      map.setLayoutProperty(layerIdClicked, "visibility", "visible");
      this.className = "active";
    };
    */
    const link = createLayerLink(map, layerId);
    menu.appendChild(link);
  }
  return menu;
}

export default class LayerSwitcherControl {
  constructor(options) {
    this._options = options;
  }

  onAdd(map) {
    this._map = map;
    this._container = document.createElement("div");
    this._container.classList.add("maplibregl-ctrl");
    this._container.classList.add(THEMES[this._options.theme || "default"]);
    this._container.style.cssText = this._options.cssText || "";
    const layerIds = this._options.layerIds;
    this._container.appendChild(createMenu(map, layerIds));
    return this._container;
  }

  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }

  getDefaultPosition() {
    return "top-left";
  }
}
