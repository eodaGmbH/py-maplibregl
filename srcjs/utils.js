import mustache from "mustache";

function getTextFromFeature(feature, property, template) {
  if (template !== null) {
    return mustache.render(template, feature.properties);
  }

  if (property === null) {
    const text = Object.keys(feature.properties)
      .map((key) => `${key}: ${feature.properties[key]}`)
      .join("</br>");
    return text;
  }

  return feature.properties[property];
}

// Use build-in tooltip of Deck.GL
function getDeckTooltip(template) {
  const style = {
    background: "white",
    color: "black",
    "border-radius": "3px",
  };
  return ({ layer, object }) => {
    if (object) {
      const template_ =
        typeof template === "object" ? template[layer.id] : template;
      return (
        template_ && { html: mustache.render(template_, object), style: style }
      );
    }

    return null;
  };
}

// Use MapLibre Popup as tooltip for Deck.GL layers
function getDeckMapLibrePopupTooltip(map, tooltip) {
  const popup = new maplibregl.Popup({
    closeOnClick: false,
    closeButton: false,
  });
  map.on("mouseout", (e) => popup.remove());
  return ({ coordinate, object }) => {
    if (object) {
      // console.log(tooltip);
      popup.setHTML(mustache.render(tooltip, object)).setLngLat(coordinate);
      popup.addTo(map);
    } else popup.remove();
  };
}

// Used in controls
function createToggleLayerLink(map, layerId) {
  const link = document.createElement("a");
  link.id = layerId;
  link.href = "#";
  link.textContent = layerId;
  const visibility = map.getLayoutProperty(layerId, "visibility");
  if (typeof visibility === "undefined" || visibility === "visible") {
    link.className = "active";
  }

  link.onclick = function (e) {
    const layerIdClicked = this.textContent;
    const visibility = map.getLayoutProperty(layerIdClicked, "visibility");
    console.log(layerIdClicked, visibility);
    if (typeof visibility === "undefined" || visibility === "visible") {
      map.setLayoutProperty(layerIdClicked, "visibility", "none");
      this.className = "";
      return;
    }

    map.setLayoutProperty(layerIdClicked, "visibility", "visible");
    this.className = "active";
  };
  return link;
}

export {
  getTextFromFeature,
  getDeckTooltip,
  getDeckMapLibrePopupTooltip,
  createToggleLayerLink,
};
