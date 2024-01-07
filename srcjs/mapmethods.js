function applyMapMethod(map, call) {
  const [methodName, params] = call;
  console.log(methodName, params);
  map[methodName](...params);
}

// TODO: Duplicated code, use for Shiny and Ipywidget
// Custom map methods
function getCustomMapMethods(maplibregl, map) {
  return {
    addPopup: function ([layerId, property]) {
      // const map = this;
      const popupOptions = {
        closeButton: false,
        closeOnClick: false,
      };
      const popup = new maplibregl.Popup(popupOptions);

      map.on("mousemove", layerId, (e) => {
        const feature = e.features[0];
        const text = feature.properties[property];
        popup.setLngLat(e.lngLat).setHTML(text).addTo(map);
      });

      map.on("mouseleave", layerId, () => {
        popup.remove();
      });
    },

    addControl: function ([type, options, position]) {
      map.addControl(new maplibregl[type](options), position);
    },
  };
}

export { applyMapMethod, getCustomMapMethods };
