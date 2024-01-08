// srcjs/ipywidget.js
import maplibregl from "https://esm.sh/maplibre-gl@3.6.2";

// srcjs/mapmethods.js
function applyMapMethod(map, call) {
  const [methodName, params] = call;
  console.log(methodName, params);
  map[methodName](...params);
}
function getCustomMapMethods(maplibregl2, map) {
  return {
    addTooltip: function(layerId, property) {
      const popupOptions = {
        closeButton: false,
        closeOnClick: false
      };
      const popup = new maplibregl2.Popup(popupOptions);
      map.on("mousemove", layerId, (e) => {
        const feature = e.features[0];
        const text = feature.properties[property];
        popup.setLngLat(e.lngLat).setHTML(text).addTo(map);
      });
      map.on("mouseleave", layerId, () => {
        popup.remove();
      });
    },
    addControl: function(type, options, position) {
      map.addControl(new maplibregl2[type](options), position);
    },
    addPopup: function(layerId, property) {
      const popupOptions = {
        closeButton: false
      };
      const popup = new maplibregl2.Popup(popupOptions);
      map.on("click", layerId, (e) => {
        const feature = e.features[0];
        const text = feature.properties[property];
        popup.setLngLat(e.lngLat).setHTML(text).addTo(map);
      });
    }
  };
}

// srcjs/ipywidget.js
function createContainer(model) {
  const id = "pymaplibregl";
  const container = document.createElement("div");
  container.id = id;
  container.style.height = model.get("height");
  return container;
}
function createMap(mapOptions, model) {
  const map = new maplibregl.Map(mapOptions);
  map.addControl(new maplibregl.NavigationControl());
  map.on("mouseover", () => {
    map.getCanvas().style.cursor = "pointer";
  });
  map.on("mouseout", () => {
    map.getCanvas().style.cursor = "";
  });
  map.on("click", (e) => {
    model.set("lng_lat", e.lngLat);
    model.save_changes();
  });
  map.once("load", () => {
    map.resize();
  });
  return map;
}
function render({ model, el }) {
  console.log("maplibregl", maplibregl.version);
  const container = createContainer(model);
  const mapOptions = Object.assign(
    { container },
    model.get("map_options")
  );
  console.log(mapOptions);
  const map = createMap(mapOptions, model);
  const customMapMethods = getCustomMapMethods(maplibregl, map);
  map.on("load", () => {
    model.set("_rendered", true);
    model.save_changes();
  });
  model.on("msg:custom", (msg) => {
    console.log("custom msg", msg);
    msg.calls.forEach((call) => {
      if (Object.keys(customMapMethods).includes(call[0])) {
        console.log("internal call", call);
        const [name, params] = call;
        customMapMethods[name](...params);
        return;
      }
      applyMapMethod(map, call);
    });
  });
  el.appendChild(container);
}
export {
  render
};
