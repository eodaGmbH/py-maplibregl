export default class PyMapLibreGL {
  constructor(mapOptions) {
    console.log("Awesome");
    this._id = mapOptions.container;
    this._map = new maplibregl.Map(mapOptions);

    // TODO: Do not add by default
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

    // ...
    if (Shiny) {
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

  render(calls) {
    console.log("Render it!");
    calls.forEach(({ name, data }) => {
      console.log(name);
      this[name](data);
    });
  }
}
