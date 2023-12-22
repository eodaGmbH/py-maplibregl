export default class PyMapLibreGL {
  constructor(mapOptions) {
    console.log("Awesome");
    this._map = new maplibregl.Map(mapOptions);
    this._map.addControl(new maplibregl.NavigationControl());
  }

  getMap() {
    return this._map;
  }

  addMarker() {}

  addLayer(props) {
    console.log(props);
    this.map.addLayer(props);
  }

  render(layers) {
    console.log("Render it!");
    layers.forEach((props) => {
      console.log(props);
      this._map.addLayer(props);
    });
  }
}
