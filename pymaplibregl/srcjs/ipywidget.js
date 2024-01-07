// srcjs/ipywidget.js
import maplibregl from "https://esm.sh/maplibre-gl@3.6.2";
function render({ model, el }) {
  console.log("ipywidget");
  console.log(maplibregl.version);
}
export {
  render
};
