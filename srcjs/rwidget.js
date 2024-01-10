import PyMapLibreGL from "./pymaplibregl";
const MapLibreWidget = PyMapLibreGL;

function mapLibre4R(widgetElement, width, height) {
  let map = null;

  function renderValue(widgetData) {
    console.log(widgetData);
    widgetData.mapOptions.container = widgetElement.id;
    const mapLibreWidget = new MapLibreWidget(widgetData.mapOptions);
    const map = mapLibreWidget.getMap();
    map.on("load", () => {
      mapLibreWidget.render(widgetData.calls);
    });
  }

  function resize(width, height) {
    // not implemented yet
  }

  return { renderValue, resize };
}

HTMLWidgets.widget({
  name: "maplibre",
  type: "output",
  factory: mapLibre4R,
});
