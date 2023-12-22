(() => {
  // srcjs/pymaplibregl.js
  var PyMapLibreGL = class {
    constructor(mapOptions) {
      console.log("Awesome");
      this._map = new maplibregl.Map(mapOptions);
      this._map.addControl(new maplibregl.NavigationControl());
    }
    getMap() {
      return this._map;
    }
    render() {
      console.log("Render it!");
    }
  };

  // srcjs/index.js
  console.log("Welcome to pymaplibregl!");
  if (Shiny) {
    class MapLibreGLOutputBinding extends Shiny.OutputBinding {
      find(scope) {
        console.log("I am here!");
        return scope.find(".shiny-maplibregl-output");
      }
      renderValue(el, payload) {
        console.log(el.id, payload);
        const pyMapLibreGL = new PyMapLibreGL(
          Object.assign({ container: el.id }, payload.data.mapOptions)
        );
        pyMapLibreGL.render();
        this.map = pyMapLibreGL.getMap();
        this.map.on(
          "load",
          () => payload.data.markers.forEach(({ lngLat, popup, options }) => {
            console.log(lngLat, popup, options);
            const marker = new maplibregl.Marker(options).setLngLat(lngLat);
            if (popup) {
              const popup_ = new maplibregl.Popup().setText(popup);
              marker.setPopup(popup_);
            }
            marker.addTo(this.map);
          })
        );
        this.map.on(
          "load",
          () => payload.data.layers.forEach((props) => {
            console.log(props);
            this.map.addLayer(props);
          })
        );
      }
    }
    Shiny.outputBindings.register(
      new MapLibreGLOutputBinding(),
      "shiny-maplibregl-output"
    );
  }
})();
