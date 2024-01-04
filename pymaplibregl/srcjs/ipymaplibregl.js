import maplibregl from "https://esm.sh/maplibre-gl@3.6.2";

export function render({ model, el }) {
  console.log("maplibregl", maplibregl.version);
  const ID = "pymaplibregl";
  const container = document.createElement("div");
  container.id = ID;
  container.style.height = model.get("height");
  const mapOptions = Object.assign(
    { container: container },
    model.get("map_options"),
  );
  console.log(mapOptions);
  const map = new maplibregl.Map(mapOptions);
  map.addControl(new maplibregl.NavigationControl());
  map.once("load", () => {
    map.resize();
  });
  el.appendChild(container);

  model.on("change:test", () => {
    const test = model.get("test");
    console.log(test);
  });
}
