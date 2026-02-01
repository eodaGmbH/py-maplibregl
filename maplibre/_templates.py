# MAPLIBRE_JS_VERSION = "5.3.1"

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{{ title|default('My MapLibre Map')}}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<!--
<script src="https://unpkg.com/maplibre-gl@{{ maplibre_version|default('5.3.0')}}/dist/maplibre-gl.js"></script>
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@{{ maplibre_version|default('5.3.0')}}/dist/maplibre-gl.css"/>
-->
{% for header in headers|default([]) -%}
{{ header }}
{% endfor -%}
<style>
html, body { margin: 0; padding: 0; width: 100%; height: 100%; }
#pymaplibregl { width: 100%; height: 100%; {{ style|default('') }} }
</style>
</head>
<body>
<div id="pymaplibregl"></div>
<script>
{{ js|safe }}
</script>
</body>
</html>
"""

js_template = """// ...
(() => {
    var data = {{ data|safe }};
    // RTL Text Plugin (bundled for offline support)
    var rtlPluginBlob = new Blob([{{ rtl_plugin_js|tojson }}], {type: 'application/javascript'});
    var rtlPluginUrl = URL.createObjectURL(rtlPluginBlob);
    maplibregl.setRTLTextPlugin(rtlPluginUrl, true);
    pymaplibregl(data);
})();
"""
