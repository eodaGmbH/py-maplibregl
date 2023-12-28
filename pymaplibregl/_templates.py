html_template = """<!DOCTYPE html>
<html lang="en">
<meta charset="UTF-8">
<title>PyMapLibreGL</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://unpkg.com/maplibre-gl/dist/maplibre-gl.js"></script>
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl/dist/maplibre-gl.css"/>
<body>
<script>
{{ js|safe }}
// ...
(() => {
    console.log("PyMapLibreGL!");
    var data = {{ data|safe }};
    // console.log(data.mapOptions);
    _pyMapLibreGL(data);
})();
</script>
</body>
</html>
"""
