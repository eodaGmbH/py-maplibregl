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

export { getTextFromFeature };
