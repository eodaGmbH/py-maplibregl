from pymaplibregl import Layer, LayerType, Map
from pymaplibregl.source import SourceType

vancouver_blocks = {
    "type": SourceType.GEOJSON.value,
    "data": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json",
    "filter": ["<", ["get", "valuePerSqm"], 3000],
}

fill_extrusion_layer = Layer(
    LayerType.FILL_EXTRUSION,
    id_="vancouver-blocks",
    source=vancouver_blocks,
    paint={
        "fill-extrusion-color": {
            "property": "valuePerSqm",
            "stops": [[0, "lightgreen"], [1500, "darkred"]],
        },
        "fill-extrusion-opacity": 0.8,
        "fill-extrusion-height": ["*", ["to-number", ["get", "valuePerSqm"]], 0.5],
    },
)

center = [-123.0753056, 49.2686511]


def create_map():
    m = Map(center=center, zoom=11, pitch=35)
    m.add_layer(fill_extrusion_layer)
    # m.add_popup("vancouver-blocks", "valuePerSqm")
    return m.to_html(output_dir="skip", style="height: 800px;")


if __name__ == "__main__":
    file_name = create_map()
    print(file_name)
