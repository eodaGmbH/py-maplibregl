import { getTextFromFeature } from "./utils";

function applyMapMethod(map, call) {
  const [methodName, params] = call;
  console.log(methodName, params);
  map[methodName](...params);
}

// TODO: Duplicated code, use for Shiny and Ipywidget
// Custom map methods
function getCustomMapMethods(maplibregl, map) {
  return {
    addTooltip: function (layerId, property = null, template = null) {
      const popupOptions = {
        closeButton: false,
        closeOnClick: false,
      };
      const popup = new maplibregl.Popup(popupOptions);

      map.on("mousemove", layerId, (e) => {
        const feature = e.features[0];

        // const text = feature.properties[property];
        const text = getTextFromFeature(feature, property, template);
        popup.setLngLat(e.lngLat).setHTML(text).addTo(map);
      });

      map.on("mouseleave", layerId, () => {
        popup.remove();
      });
    },

    addControl: function (type, options, position) {
      map.addControl(new maplibregl[type](options), position);
    },

    addPopup: function (layerId, property = null, template = null) {
      const popupOptions = {
        closeButton: false,
      };
      const popup = new maplibregl.Popup(popupOptions);
      map.on("click", layerId, (e) => {
        const feature = e.features[0];

        // const text = feature.properties[property];
        const text = getTextFromFeature(feature, property, template);
        popup.setLngLat(e.lngLat).setHTML(text).addTo(map);
      });
    },

    addMarker: function ({ lngLat, popup, options }) {
      const marker = new maplibregl.Marker(options).setLngLat(lngLat);
      if (popup) {
        const popup_ = new maplibregl.Popup(popup.options).setHTML(popup.text);
        marker.setPopup(popup_);
      }
      marker.addTo(map);
    },

    setSourceData: function (sourceId, data) {
      map.getSource(sourceId).setData(data);
    },
  };
}

export { applyMapMethod, getCustomMapMethods };
