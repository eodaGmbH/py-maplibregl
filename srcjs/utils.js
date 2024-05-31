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

function renderPickingObject(template, object, layerId) {
  // console.log("Trying to get tooltip for layerId = " + layerId);
  const default_style = {
    background: "white",
    color: "black",
    "border-radius": "5px",
  };
  if (typeof template === "object") {
    return (
      template[layerId] && {
        html: mustache.render(template[layerId], object),
        style: default_style,
      }
    );
  }

  return {
    html: mustache.render(template, object),
    style: default_style,
  };
}

// Just as a POC, maybe set tooltip via onHover using Popups from maplibregl
function getDeckTooltip(template) {
  return ({ layer, object }) => {
    return object && renderPickingObject(template, object, layer.id);
  };
}

// Exp
function deckLayerOnHover(map, tooltip_template) {
  const popup = new maplibregl.Popup({
    closeOnClick: false,
    closeButton: false,
  });
  map.on("mouseout", (e) => popup.remove());
  return ({ layer, coordinate, object }) => {
    if (object) {
      console.log(tooltip_template);
      popup
        .setHTML(mustache.render(tooltip_template, object))
        .setLngLat(coordinate);
      popup.addTo(map);
    } else popup.remove();
  };
}

export { getTextFromFeature, getDeckTooltip, deckLayerOnHover };
