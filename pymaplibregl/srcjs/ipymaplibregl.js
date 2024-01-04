import maplibregl from "https://esm.sh/maplibre-gl@3.6.2";

function create_container(model) {
  const ID = "pymaplibregl";
  const container = document.createElement("div");
  container.id = ID;
  container.style.height = model.get("height");
  return container;
}

function create_map(mapOptions) {
  const map = new maplibregl.Map(mapOptions);
  map.addControl(new maplibregl.NavigationControl());
  map.once("load", () => {
    map.resize();
  });
  return map;
}

export function render({ model, el }) {
  console.log("maplibregl", maplibregl.version);

  const container = create_container(model);
  el.appendChild(container);
  const mapOptions = Object.assign(
    { container: container },
    model.get("map_options"),
  );
  console.log(mapOptions);
  const map = create_map(mapOptions);

  model.on("change:test", () => {
    const test = model.get("test");
    console.log(test);
  });
}
