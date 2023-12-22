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

  render(calls) {
    console.log("Render it!");
    calls.forEach(({ name, data }) => {
      console.log(name, data);
      this._map[name](data);
    });
  }
}
