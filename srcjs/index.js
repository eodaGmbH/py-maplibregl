import PyMapLibreGL from "./pymaplibregl";
import { getViewState } from "./utils";

const version = "0.2.6.1";
console.log("py-maplibregl", version);

if (typeof Shiny === "undefined") {
  window.pymaplibregl = function ({ mapOptions, calls }) {
    const id = "pymaplibregl";
    const container = document.getElementById(id);
    const pyMapLibreGL = new PyMapLibreGL(
      Object.assign({ container: container.id }, mapOptions),
    );
    const map = pyMapLibreGL.getMap();
    map.on("load", () => {
      pyMapLibreGL.render(calls);
    });
  };
}

if (typeof Shiny !== "undefined") {
  class MapLibreGLOutputBinding extends Shiny.OutputBinding {
    find(scope) {
      return scope.find(".shiny-maplibregl-output");
    }

    renderValue(el, payload) {
      console.log("id:", el.id, "payload:", payload);
      const pyMapLibreGL = (window._maplibreWidget = new PyMapLibreGL(
        Object.assign({ container: el.id }, payload.mapData.mapOptions),
      ));

      const map = pyMapLibreGL.getMap();
      map.on("load", () => {
        pyMapLibreGL.render(payload.mapData.calls);
      });

      // ...
      map.on("click", (e) => {
        // console.log(e);
        const inputName = `${el.id}_clicked`;
        const data = { coords: e.lngLat, point: e.point };
        console.log(inputName, data);
        Shiny.onInputChange(inputName, data);
      });

      for (const event of ["load", "zoomend", "moveend"]) {
        map.on(event, (e) => {
          const inputName = `${el.id}_view_state`;
          Shiny.onInputChange(inputName, getViewState(map));
        });
      }

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
