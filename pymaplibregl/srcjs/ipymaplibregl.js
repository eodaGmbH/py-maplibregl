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

const _this = {
  addPopup: ([map, layerId, prop]) => {
    console.log("addPopup", map, layerId, prop);
  },
};

export function render({ model, el }) {
  console.log("maplibregl", maplibregl.version);

  // _this["addPopup"]();
  console.log(Object.keys(_this));

  const container = createContainer(model);
  const mapOptions = Object.assign(
    { container: container },
    model.get("map_options"),
  );
  console.log(mapOptions);
  const map = createMap(mapOptions, model);
  map.on("load", () => {
    model.set("_rendered", true);
    model.save_changes();
  });

  model.on("msg:custom", (msg) => {
    console.log("custom msg", msg);
    msg.calls.forEach((call) => {
      if (Object.keys(_this).includes(call[0])) {
        console.log("internal call", call);
        const [name, params] = call;
        _this[name]([map].concat(params));
        return;
      }

      applyMapMethod(map, call);
    });
  });

  // TODO: Remove
  model.on("change:test", () => {
    const test = model.get("test");
    console.log(test);
  });

  el.appendChild(container);
}
