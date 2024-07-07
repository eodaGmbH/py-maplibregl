import maplibregl from "https://esm.sh/maplibre-gl@3.6.2";
import { Protocol } from "https://esm.sh/pmtiles@3.0.6";

import "./css/maplibre-gl.css";

let protocol = new Protocol();
maplibregl.addProtocol("pmtiles", protocol.tile);

// Add custom controls
import InfoBoxControl from "./custom-controls/info-box";
import LayerSwitcherControl from "./custom-controls/layer-switcher";
maplibregl.LayerSwitcherControl = LayerSwitcherControl;
maplibregl.InfoBoxControl = InfoBoxControl;

import { applyMapMethod, getCustomMapMethods } from "./mapmethods";

function createContainer(model) {
  const id = "pymaplibregl";
  const container = document.createElement("div");
  container.id = id;
  container.style.height = model.get("height");
  return container;
}

function updateModel(model, map) {
  const viewState = {
    center: map.getCenter(),
    zoom: map.getZoom(),
    bounds: map.getBounds(),
    bearing: map.getBearing(),
    pitch: map.getPitch(),
  };
  model.set("view_state", viewState);
  model.save_changes();
}

function createMap(mapOptions, model) {
  const map = new maplibregl.Map(mapOptions);
  /*
  if (mapOptions.navigationControl === undefined) {
    mapOptions.navigationControl = true;
  }

  if (mapOptions.navigationControl) {
    map.addControl(new maplibregl.NavigationControl());
  }
  */
  map.on("mouseover", () => {
    map.getCanvas().style.cursor = "pointer";
  });

  map.on("mouseout", () => {
    map.getCanvas().style.cursor = "";
  });

  map.on("click", (e) => {
    model.set("clicked", e.lngLat);
    model.save_changes();
  });

  map.on("zoomend", (e) => {
    updateModel(model, map);
  });

  map.on("moveend", (e) => {
    updateModel(model, map);
  });

  map.once("load", () => {
    map.resize();
    updateModel(model, map);
  });

  map.on("draw.selectionchange", (e) => {
    const features = e.features;
    console.log("selection changed", features);
    model.set("draw_features_selected", features);
    model.save_changes();
  });

  return map;
}

function render({ model, el }) {
  console.log("maplibregl", maplibregl.version);

  const container = createContainer(model);
  const mapOptions = Object.assign(
    { container: container },
    model.get("map_options"),
  );
  console.log(mapOptions);
  const map = createMap(mapOptions, model);

  // As a  Workaround we need to pass maplibregl module to customMapMethods
  // to avoid duplicated imports (current bug in esbuild)
  const customMapMethods = getCustomMapMethods(maplibregl, map);

  // Add event listeners for MapboxDraw
  // TODO: Only add listeners if 'addMapboxDraw is called'
  const drawEvents = [
    "draw.create",
    "draw.update",
    "draw.delete",
    "draw.render",
  ];
  for (let i in drawEvents) {
    map.on(drawEvents[i], (e) => {
      const draw = customMapMethods.getMapboxDraw();
      console.log("features", draw.getAll());
      model.set("draw_feature_collection_all", draw.getAll());
      model.save_changes();
    });
  }

  const apply = (calls) => {
    calls.forEach((call) => {
      // Custom map call
      if (Object.keys(customMapMethods).includes(call[0])) {
        console.log("internal call", call);
        const [name, params] = call;
        customMapMethods[name](...params);
        return;
      }

      applyMapMethod(map, call);
    });
  };

  const calls = model.get("calls");

  map.on("load", () => {
    console.log("init calls", calls);
    apply(calls);
    model.set("_rendered", true);
    model.save_changes();
  });

  model.on("msg:custom", (msg) => {
    console.log("custom msg", msg);
    apply(msg.calls);
  });

  el.appendChild(container);
}

export default { render };
