export default class PyMapLibreGL {
  constructor(mapOptions) {
    console.log("Awesome");
    this._map = new maplibregl.Map(mapOptions);
    this._map.addControl(new maplibregl.NavigationControl());
  }

  getMap() {
    return this._map;
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

  addLayer(data) {
    console.log(data);
    this._map.addLayer(data);
  }

  render(calls) {
    console.log("Render it!");
    calls.forEach(({ name, data }) => {
      console.log(name);
      this[name](data);
    });
  }
}
