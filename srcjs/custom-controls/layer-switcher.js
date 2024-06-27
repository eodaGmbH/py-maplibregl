function createSelect(layers) {
  const select = document.createElement("select");
  select.id = "layer-switcher";
  select.style.padding = "5px";
  select.multiple = true;
  // select.size = 1;
  for (let layer of layers) {
    const option = document.createElement("option");
    option.innerHTML = layer;
    select.appendChild(option);
  }

  return select;
}

function createMenu(layerIds, map) {
  const menu = document.createElement("div");
  menu.id = "layer-switcher-menu";
  for (const id of layerIds) {
    const link = document.createElement("a");
    link.id = id;
    link.href = "#";
    link.textContent = id;
    link.style.cssText =
      "display: block; text-align: center; background-color: white; padding: 5px; border-bottom: 1px solid rgba(0, 0, 0, 0.25); text-decoration: none";
    link.onclick = function (e) {
      const idClicked = this.textContent;
      console.log(idClicked);
      const visibility = map.getLayoutProperty(idClicked, "visibility");
      console.log(visibility);
      if (visibility === "visible") {
        map.setLayoutProperty(idClicked, "visibility", "none");
        return;
      }

      map.setLayoutProperty(idClicked, "visibility", "visible");
    };
    menu.appendChild(link);
  }
  return menu;
}

export default class LayerSwitcherControl {
  constructor(options) {
    this._options = options || {};
  }

  onAdd(map) {
    this._map = map;
    this._container = document.createElement("div");
    // this._container.classList.add("maplibregl-ctrl", "maplibregl-ctrl-group");
    // this._container.className = "maplibregl-ctrl maplibregl-ctrl-group";
    this._container.className = "maplibregl-ctrl";
    this._container.style.cssText = this._options.cssText || "padding: 5px;";
    // this._container.innerHTML = "We out here.";

    // const layers = ["lay1", "layer2", "lay3", "awesome", "nice", "happy"];
    const layerIds = this._options.layerIds; // ["landcover", "water", "landuse", "boundary_state"];
    /*
    for (let i in layers) {
      const input = document.createElement("input");
      input.type = "checkbox";
      input.id = input.value = layers[i];
      const label = document.createElement("label");
      label.for = label.innerText = layers[i];
      this._container.appendChild(input);
      this._container.appendChild(label);
    }
    */
    // this._container.appendChild(createSelect(layers));
    this._container.appendChild(createMenu(layerIds, map));

    return this._container;
  }

  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}
