export default class PyMapLibreGL {
  constructor(mapOptions) {
    this._id = mapOptions.container;
    this._map = new maplibregl.Map(mapOptions);

    // TODO: Do not add by default
    this._map.addControl(new maplibregl.NavigationControl());
  }

  getMap() {
    return this._map;
  }

  // TODO: Rename to "applyMapMethod"
  applyFunc({ funcName, params }) {
    this._map[funcName](...params);
  }

  addControl({ type, options, position }) {
    this._map.addControl(new maplibregl[type](options), position);
  }

  addMarker({ lngLat, popup, options }) {
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

  addLayer(data) {
    this._map.addLayer(data);

    // Add event listener
    if (typeof Shiny !== "undefined") {
      this._map.on("click", data.id, (e) => {
        console.log(e, e.features[0]);
        const layerId_ = data.id.replaceAll("-", "_");
        const inputName = `${this._id}_layer_${layerId_}`;
        const feature = {
          // coords: e.lngLat,
          props: e.features[0].properties,
          layer_id: data.id,
        };
        console.log(inputName, feature);
        Shiny.onInputChange(inputName, feature);
      });
    }
  }

  addPopup({ layerId, property }) {
    const popupOptions = {
      closeButton: false,
      closeOnClick: false,
    };
    const popup = new maplibregl.Popup(popupOptions);
    this._map.on("mousemove", layerId, (e) => {
      const feature = e.features[0];
      const text = feature.properties[property];
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
}
