import maplibregl from "https://esm.sh/maplibre-gl@3.6.2";
import { applyMapMethod, getCustomMapMethods } from "./mapmethods";

function createContainer(model) {
  const id = "pymaplibregl";
  const container = document.createElement("div");
  container.id = id;
  container.style.height = model.get("height");
  return container;
}

function createMap(mapOptions, model) {
  const map = new maplibregl.Map(mapOptions);
  if (mapOptions.navigationControl === undefined) {
    mapOptions.navigationControl = true;
  }

  if (mapOptions.navigationControl) {
    map.addControl(new maplibregl.NavigationControl());
  }

  map.on("mouseover", () => {
    map.getCanvas().style.cursor = "pointer";
  });

  map.on("mouseout", () => {
    map.getCanvas().style.cursor = "";
  });

  map.on("click", (e) => {
    model.set("lng_lat", e.lngLat);
    model.save_changes();
  });

  map.once("load", () => {
    map.resize();
  });

  return map;
}

export function render({ model, el }) {
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
