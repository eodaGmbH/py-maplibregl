import maplibregl from "https://esm.sh/maplibre-gl@3.6.2";

function createContainer(model) {
  const ID = "pymaplibregl";
  const container = document.createElement("div");
  container.id = ID;
  container.style.height = model.get("height");
  return container;
}

function createMap(mapOptions, model) {
  const map = new maplibregl.Map(mapOptions);
  map.addControl(new maplibregl.NavigationControl());

  map.on("click", (e) => {
    model.set("lng_lat", e.lngLat);
    model.save_changes();
  });

  map.once("load", () => {
    map.resize();
  });
  return map;
}

function applyMapMethod(map, call) {
  const [methodName, params] = call;
  console.log(methodName, params);
  map[methodName](...params);
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

  const calls = model.get("calls");
  console.log("init calls", calls);
  map.on("load", () => {
    // calls.forEach((call) => applyMapMethod(map, call));
  });

  model.on("change:test", () => {
    const test = model.get("test");
    console.log(test);
  });

  model.on("change:calls", () => {
    let calls = model.get("calls");
    console.log("update calls", calls)
    // calls.forEach((call) => applyMapMethod(map, call));
  });

  el.appendChild(container);

  model.set("rendered", true);
  model.save_changes();
}
