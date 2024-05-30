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
  console.log("Trying to get tooltip for layerId = " + layerId);
  if (typeof template === "object") {
    return template[layerId] && mustache.render(template[layerId], object);
  }

  return mustache.render(template, object);
}

// Just as a POC, maybe set tooltip via onHover using Popups from maplibregl
function getDeckTooltip(template) {
  return ({ layer, object }) => {
    return object && renderPickingObject(template, object, layer.id);
  };
}
export { getTextFromFeature, getDeckTooltip };
