import { MapboxOverlay } from "@deck.gl/mapbox";
import { JSONConfiguration, JSONConverter } from "@deck.gl/json";
// import * as coreLayers from "@deck.gl/layers";
// import * as aggLayers from "@deck.gl/aggregation-layers";
import * as deckLayerCatalog from "./deck-layers";

import { getTextFromFeature, getDeckTooltip } from "./utils";

function applyMapMethod(map, call) {
  const [methodName, params] = call;
  console.log(methodName, params);
  map[methodName](...params);
}

// TODO: Duplicated code, use for Shiny and Ipywidget
// Custom map methods
function getCustomMapMethods(maplibregl, map) {
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

    addDeckOverlay: function (deckLayers, tooltip_template = null) {
      const configuration = new JSONConfiguration({ layers: deckLayerCatalog });
      const jsonConverter = new JSONConverter({ configuration });
      // console.log("jsonConverter", jsonConverter);
      const layers = deckLayers.map((deckLayer) =>
        jsonConverter.convert(
          Object.assign(deckLayer, {
            onHover: ({ object }) => console.log(object),
          }),
        ),
      );

      console.log("deckLayers", layers);

      const deckOverlay = new MapboxOverlay({
        interleaved: true,
        layers: layers,
        getTooltip: tooltip_template ? getDeckTooltip(tooltip_template) : null,
      });
      map.addControl(deckOverlay);
    },
  };
}

export { applyMapMethod, getCustomMapMethods };
