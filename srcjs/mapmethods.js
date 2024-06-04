import { MapboxOverlay } from "@deck.gl/mapbox";
import { JSONConfiguration, JSONConverter } from "@deck.gl/json";
import * as deckLayerCatalog from "./deck-layers";

import { getTextFromFeature, getDeckTooltip } from "./utils";

const jsonConverter = new JSONConverter({
  configuration: new JSONConfiguration({ layers: deckLayerCatalog }),
});

function applyMapMethod(map, call) {
  const [methodName, params] = call;
  console.log(methodName, params);
  map[methodName](...params);
}

function _convertDeckLayer(deckLayers) {
  return deckLayers.map((deckLayer) =>
    jsonConverter.convert(
      Object.assign(deckLayer, {
        onHover: ({ object }) => console.log(object),
      }),
    ),
  );
}

// TODO: Duplicated code, use for Shiny and Ipywidget
// Custom map methods
function getCustomMapMethods(maplibregl, map) {
  let deckOverlay = null;

  return {
    addTooltip: function (layerId, property = null, template = null) {
      const popupOptions = {
        closeButton: false,
        closeOnClick: false,
      };
      const popup = new maplibregl.Popup(popupOptions);

      map.on("mousemove", layerId, (e) => {
        const feature = e.features[0];

        // const text = feature.properties[property];
        const text = getTextFromFeature(feature, property, template);
        popup.setLngLat(e.lngLat).setHTML(text).addTo(map);
      });

      map.on("mouseleave", layerId, () => {
        popup.remove();
      });
    },

    addControl: function (type, options, position) {
      map.addControl(new maplibregl[type](options), position);
    },

    addPopup: function (layerId, property = null, template = null) {
      const popupOptions = {
        closeButton: false,
      };
      const popup = new maplibregl.Popup(popupOptions);
      map.on("click", layerId, (e) => {
        const feature = e.features[0];

        // const text = feature.properties[property];
        const text = getTextFromFeature(feature, property, template);
        popup.setLngLat(e.lngLat).setHTML(text).addTo(map);
      });
    },

    addMarker: function ({ lngLat, popup, options }) {
      const marker = new maplibregl.Marker(options).setLngLat(lngLat);
      if (popup) {
        const popup_ = new maplibregl.Popup(popup.options).setHTML(popup.text);
        marker.setPopup(popup_);
      }
      marker.addTo(map);
    },

    setSourceData: function (sourceId, data) {
      map.getSource(sourceId).setData(data);
    },

    addDeckOverlay: function (deckLayers, tooltip = null) {
      const layers = _convertDeckLayer(deckLayers);
      // console.log("deckLayers", layers);
      deckOverlay = new MapboxOverlay({
        interleaved: true,
        layers: layers,
        getTooltip: tooltip ? getDeckTooltip(tooltip) : null,
      });
      map.addControl(deckOverlay);
    },

    setDeckLayers: function (deckLayers, tooltip = null) {
      console.log("Updating Deck.GL layers");
      const layers = _convertDeckLayer(deckLayers);
      // console.log("deckLayers", layers);
      deckOverlay.setProps({
        layers,
        getTooltip: tooltip ? getDeckTooltip(tooltip) : null,
      });
    },
  };
}

export { applyMapMethod, getCustomMapMethods };
