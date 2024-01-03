html_template = """<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8">
<title>Pymaplibregl</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://unpkg.com/maplibre-gl/dist/maplibre-gl.js"></script>
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl/dist/maplibre-gl.css"/>
<body>
<div id="pymaplibregl" style="{{ style|default('height:600px;') }}"></div>
<script>
{{ js|safe }}
</script>
</body>
</html>
"""

js_template = """// ...
(() => {
    var data = {{ data|safe }};
    pymaplibregl(data);
})();
"""
