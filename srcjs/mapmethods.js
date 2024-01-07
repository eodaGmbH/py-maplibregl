// TODO: Duplicated code, use for Shiny and Ipywidget
// Custom map methods
function getCustomMapMethods(maplibregl) {
  return {
    addPopup: function ([layerId, property]) {
      const map = this;
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
  };
}

export { getCustomMapMethods };
