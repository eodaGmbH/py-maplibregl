import PyMapLibreGL from "./pymaplibregl";

console.log("Welcome to pymaplibregl!");

if (Shiny) {
  class MapLibreGLOutputBinding extends Shiny.OutputBinding {
    find(scope) {
      console.log("I am here!");
      return scope.find(".shiny-maplibregl-output");
    }

    renderValue(el, payload) {
      console.log("id:", el.id, "payload:", payload);
      const pyMapLibreGL = new PyMapLibreGL(
        Object.assign({ container: el.id }, payload.mapData.mapOptions),
      );
      pyMapLibreGL.render(payload.mapData.calls);
    }
  }

  Shiny.outputBindings.register(
    new MapLibreGLOutputBinding(),
    "shiny-maplibregl-output",
  );
}
