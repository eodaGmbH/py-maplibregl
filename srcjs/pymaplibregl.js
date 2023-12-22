export default class PyMapLibreGL {
  constructor(mapOptions) {
    console.log("Awesome");
    this._map = new maplibregl.Map(mapOptions);
    this._map.addControl(new maplibregl.NavigationControl());
  }
  getMap() {
    return this._map;
  }
  render() {
    console.log("Render it!");
  }
}
