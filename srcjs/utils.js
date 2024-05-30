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

function renderPickingObject(template, object) {
  return mustache.render(template, object);
}

// Just as a POC, maybe set tooltip via onHover using Popups from maplibregl
function getDeckTooltip(template) {
  return ({ layer, object }) => {
    return object && renderPickingObject(template, object);
  };
}
export { getTextFromFeature, getDeckTooltip };
