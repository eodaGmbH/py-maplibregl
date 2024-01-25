// import { getCustomMapMethods } from "./mapmethods";
import { getTextFromFeature } from "./utils";

export default class PyMapLibreGL {
  constructor(mapOptions) {
    this._id = mapOptions.container;
    this._map = new maplibregl.Map(mapOptions);

    this._map.on("mouseover", () => {
      this._map.getCanvas().style.cursor = "pointer";
    });

    this._map.on("mouseout", () => {
      this._map.getCanvas().style.cursor = "";
    });

    // TODO: Do not add by default
    this._map.addControl(new maplibregl.NavigationControl());
    // this.customMapMethods = getCustomMapMethods(maplibregl, this._map);
    // console.log("Custom methods", Object.keys(this.customMapMethods));
  }

  getMap() {
    return this._map;
  }

  applyMapMethod(name, params) {
    this._map[name](...params);
  }

  addControl(type, options, position) {
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

  addLayer(layer) {
    this._map.addLayer(layer);

    // Add event listener
    if (typeof Shiny !== "undefined") {
      this._map.on("click", layer.id, (e) => {
        console.log(e, e.features[0]);
        const layerId_ = layer.id.replaceAll("-", "_");
        const inputName = `${this._id}_layer_${layerId_}`;
        const feature = {
          props: e.features[0].properties,
          layer_id: layer.id,
        };
        console.log(inputName, feature);
        Shiny.onInputChange(inputName, feature);
      });
    }
  }

  addPopup(layerId, property = null, template = null) {
    const popupOptions = {
      closeButton: false,
    };
    const popup = new maplibregl.Popup(popupOptions);
    this._map.on("click", layerId, (e) => {
      const feature = e.features[0];
      // const text = feature.properties[property];
      const text = getTextFromFeature(feature, property, template);
      popup.setLngLat(e.lngLat).setHTML(text).addTo(this._map);
    });
  }

  addTooltip(layerId, property = null, template = null) {
    const popupOptions = {
      closeButton: false,
      closeOnClick: false,
    };
    const popup = new maplibregl.Popup(popupOptions);
    this._map.on("mousemove", layerId, (e) => {
      const feature = e.features[0];
      const text = getTextFromFeature(feature, property, template);
      popup.setLngLat(e.lngLat).setHTML(text).addTo(this._map);
    });

    this._map.on("mouseleave", layerId, () => {
      popup.remove();
    });
  }

  setSourceData(sourceId, data) {
    this._map.getSource(sourceId).setData(data);
  }

  render(calls) {
    calls.forEach(([name, params]) => {
      // Custom method
      if (
        [
          "addLayer",
          "addPopup",
          "addTooltip",
          "addMarker",
          "addPopup",
          "addControl",
          "setSourceData",
        ].includes(name)
      ) {
        console.log("Custom method", name, params);
        this[name](...params);
        return;
      }

      console.log("Map method", name);

      // this._map[name](...params);
      this.applyMapMethod(name, params);
    });
  }
}
