import PyMapLibreGL from "./pymaplibregl";

console.log("Welcome to pymaplibregl!");

/*
if (Shiny) {
	console.log("Shiny");
	Shiny.addCustomMessageHandler("maplibregl", (payload) => {
		console.log(payload);
	});
}
*/

if (Shiny) {
  class MapLibreGLOutputBinding extends Shiny.OutputBinding {
    find(scope) {
      console.log("I am here!");
      return scope.find(".shiny-maplibregl-output");
    }

    renderValue(el, payload) {
      console.log(el.id, payload);
      const pyMapLibreGL = new PyMapLibreGL(
        Object.assign({ container: el.id }, payload.data.mapOptions),
      );
      pyMapLibreGL.render();
      this.map = pyMapLibreGL.getMap();

      // Add markers
      this.map.on("load", () =>
        payload.data.markers.forEach(({ lngLat, popup, options }) => {
          console.log(lngLat, popup, options);
          const marker = new maplibregl.Marker(options).setLngLat(lngLat);
          if (popup) {
            const popup_ = new maplibregl.Popup().setText(popup);
            marker.setPopup(popup_);
          }
          marker.addTo(this.map);
        }),
      );

      // Add layers
      this.map.on("load", () =>
        payload.data.layers.forEach((props) => {
          console.log(props);
          this.map.addLayer(props);
        }),
      );
    }
  }

  Shiny.outputBindings.register(
    new MapLibreGLOutputBinding(),
    "shiny-maplibregl-output",
  );
}
