(() => {
  // srcjs/pymaplibregl.js
  var PyMapLibreGL = class {
    constructor(mapOptions) {
      console.log("Awesome");
      this._id = mapOptions.container;
      this._map = new maplibregl.Map(mapOptions);
      this._map.addControl(new maplibregl.NavigationControl());
    }
    getMap() {
      return this._map;
    }
    addControl({ type, options, position }) {
      console.log(type, options, position);
      this._map.addControl(new maplibregl[type](options), position);
    }
    addMarker({ lngLat, popup, options }) {
      console.log(lngLat, popup, options);
      const marker = new maplibregl.Marker(options).setLngLat(lngLat);
      if (popup) {
        const popup_ = new maplibregl.Popup().setText(popup);
        marker.setPopup(popup_);
      }
      marker.addTo(this._map);
    }
    addSource({ id, source }) {
      this._map.addSource(id, source);
    }
    addLayer(data) {
      console.log(data);
      this._map.addLayer(data);
      if (Shiny) {
        this._map.on("click", data.id, (e) => {
          console.log(e, e.features[0]);
          const layerId_ = data.id.replaceAll("-", "_");
          const inputName = `maplibregl_${this._id}_layer_${layerId_}`;
          const feature = {
            // coords: e.lngLat,
            props: e.features[0].properties,
            layer_id: data.id
          };
          console.log(inputName, feature);
          Shiny.onInputChange(inputName, feature);
        });
      }
    }
    render(calls) {
      console.log("Render it!");
      this._map.on("load", () => {
        calls.forEach(({ name, data }) => {
          console.log(name);
          this[name](data);
        });
      });
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
        console.log("id:", el.id, "payload:", payload);
        const pyMapLibreGL = new PyMapLibreGL(
          Object.assign({ container: el.id }, payload.mapData.mapOptions)
        );
        pyMapLibreGL.render(payload.mapData.calls);
        const map = pyMapLibreGL.getMap();
        map.on("click", (e) => {
          console.log(e);
          const inputName = `maplibregl_${el.id}`;
          const data = { coords: e.lngLat, point: e.point };
          console.log(inputName, data);
          Shiny.onInputChange(inputName, data);
        });
      }
    }
    Shiny.outputBindings.register(
      new MapLibreGLOutputBinding(),
      "shiny-maplibregl-output"
    );
  }
})();
