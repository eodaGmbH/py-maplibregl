(() => {
  // node_modules/@turf/helpers/dist/es/index.js
  var earthRadius = 63710088e-1;
  var factors = {
    centimeters: earthRadius * 100,
    centimetres: earthRadius * 100,
    degrees: earthRadius / 111325,
    feet: earthRadius * 3.28084,
    inches: earthRadius * 39.37,
    kilometers: earthRadius / 1e3,
    kilometres: earthRadius / 1e3,
    meters: earthRadius,
    metres: earthRadius,
    miles: earthRadius / 1609.344,
    millimeters: earthRadius * 1e3,
    millimetres: earthRadius * 1e3,
    nauticalmiles: earthRadius / 1852,
    radians: 1,
    yards: earthRadius * 1.0936
  };
  var unitsFactors = {
    centimeters: 100,
    centimetres: 100,
    degrees: 1 / 111325,
    feet: 3.28084,
    inches: 39.37,
    kilometers: 1 / 1e3,
    kilometres: 1 / 1e3,
    meters: 1,
    metres: 1,
    miles: 1 / 1609.344,
    millimeters: 1e3,
    millimetres: 1e3,
    nauticalmiles: 1 / 1852,
    radians: 1 / earthRadius,
    yards: 1.0936133
  };
  function feature(geom, properties, options) {
    if (options === void 0) {
      options = {};
    }
    var feat = { type: "Feature" };
    if (options.id === 0 || options.id) {
      feat.id = options.id;
    }
    if (options.bbox) {
      feat.bbox = options.bbox;
    }
    feat.properties = properties || {};
    feat.geometry = geom;
    return feat;
  }
  function point(coordinates, properties, options) {
    if (options === void 0) {
      options = {};
    }
    if (!coordinates) {
      throw new Error("coordinates is required");
    }
    if (!Array.isArray(coordinates)) {
      throw new Error("coordinates must be an Array");
    }
    if (coordinates.length < 2) {
      throw new Error("coordinates must be at least 2 numbers long");
    }
    if (!isNumber(coordinates[0]) || !isNumber(coordinates[1])) {
      throw new Error("coordinates must contain numbers");
    }
    var geom = {
      type: "Point",
      coordinates
    };
    return feature(geom, properties, options);
  }
  function featureCollection(features, options) {
    if (options === void 0) {
      options = {};
    }
    var fc = { type: "FeatureCollection" };
    if (options.id) {
      fc.id = options.id;
    }
    if (options.bbox) {
      fc.bbox = options.bbox;
    }
    fc.features = features;
    return fc;
  }
  function isNumber(num) {
    return !isNaN(num) && num !== null && !Array.isArray(num);
  }

  // srcjs/pymaplibregl.js
  console.log(point([0, 0]));
  var PyMapLibreGL = class {
    constructor(mapOptions) {
      this._id = mapOptions.container;
      this._map = new maplibregl.Map(mapOptions);
      this._map.addControl(new maplibregl.NavigationControl());
    }
    getMap() {
      return this._map;
    }
    applyFunc({ funcName, params }) {
      this._map[funcName](...params);
    }
    addControl({ type, options, position }) {
      console.log(type, options, position);
      this._map.addControl(new maplibregl[type](options), position);
    }
    addMarker({ lngLat, popup, options }) {
      console.log(lngLat, popup, options);
      const marker = new maplibregl.Marker(options).setLngLat(lngLat);
      if (popup) {
        const popup_ = new maplibregl.Popup(popup.options).setHTML(popup.text);
        marker.setPopup(popup_);
      }
      marker.addTo(this._map);
    }
    addSource({ id, source }) {
      this._map.addSource(id, source);
    }
    addPointSource({ id, data }) {
      console.log(data);
      const d = featureCollection(
        data.data.map((item) => point([item[0], item[1]]))
      );
      console.log(d);
      this._map.addSource(id, { type: "geojson", data: d });
    }
    addLayer(data) {
      this._map.addLayer(data);
      if (typeof Shiny !== "undefined") {
        this._map.on("click", data.id, (e) => {
          console.log(e, e.features[0]);
          const layerId_ = data.id.replaceAll("-", "_");
          const inputName = `${this._id}_layer_${layerId_}`;
          const feature2 = {
            // coords: e.lngLat,
            props: e.features[0].properties,
            layer_id: data.id
          };
          console.log(inputName, feature2);
          Shiny.onInputChange(inputName, feature2);
        });
      }
    }
    addPopup({ layerId, property }) {
      const popupOptions = {
        closeButton: false,
        closeOnClick: false
      };
      const popup = new maplibregl.Popup(popupOptions);
      this._map.on("mouseenter", layerId, (e) => {
        const feature2 = e.features[0];
        const text = feature2.properties[property];
        popup.setLngLat(e.lngLat).setHTML(text).addTo(this._map);
      });
      this._map.on("mouseleave", layerId, () => {
        popup.remove();
      });
    }
    render(calls) {
      calls.forEach(({ name, data }) => {
        this[name](data);
      });
    }
  };

  // srcjs/index.js
  var version = "0.1.0";
  console.log("pymaplibregl", version);
  if (typeof Shiny === "undefined") {
    window.pymaplibregl = function({ mapOptions, calls }) {
      const id = "pymaplibregl";
      const container = document.getElementById(id);
      const pyMapLibreGL = new PyMapLibreGL(
        Object.assign({ container: container.id }, mapOptions)
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
        const pyMapLibreGL = new PyMapLibreGL(
          Object.assign({ container: el.id }, payload.mapData.mapOptions)
        );
        const map = pyMapLibreGL.getMap();
        map.on("load", () => {
          pyMapLibreGL.render(payload.mapData.calls);
        });
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
      "shiny-maplibregl-output"
    );
  }
})();
