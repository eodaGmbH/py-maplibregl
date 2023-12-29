from pandas import read_json
from pymaplibregl.utils import GeometryType, df_to_geojson


def test_geojson_line():
    # Prepare
    heathrow_flight_url = "https://github.com/visgl/deck.gl-data/raw/master/examples/line/heathrow-flights.json"

    # Act
    df = read_json(heathrow_flight_url).head()
    print("data")
    print(df)

    geojson = df_to_geojson(
        df, ["start", "end"], GeometryType.LINE, properties=["name"]
    )
    print(geojson)
