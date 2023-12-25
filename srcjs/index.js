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
      // pyMapLibreGL.render(payload.mapData.calls);

      // ...
      const map = pyMapLibreGL.getMap();
      map.on("load", () => {pyMapLibreGL.render(payload.mapData.calls);});

      map.on("click", (e) => {
        console.log(e);
        const inputName = `${el.id}`;
        const data = { coords: e.lngLat, point: e.point };
        console.log(inputName, data);
        Shiny.onInputChange(inputName, data);
      });

      const messageHandlerName = `pymaplibregl-${el.id}`;
      console.log(messageHandlerName);
      Shiny.addCustomMessageHandler(messageHandlerName, ({ id, calls }) => {
        console.log(id, calls);
        pyMapLibreGL.render(calls);
      });
    }
  }

  Shiny.outputBindings.register(
    new MapLibreGLOutputBinding(),
    "shiny-maplibregl-output",
  );
}
