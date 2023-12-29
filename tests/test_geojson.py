import pytest
from pandas import read_json
from pymaplibregl.utils import GeometryType, df_to_geojson, get_bounds


@pytest.mark.skip("enable me")
def test_geojson_line():
    # Prepare
    heathrow_flight_url = "https://github.com/visgl/deck.gl-data/raw/master/examples/line/heathrow-flights.json"

    # Act
    df = read_json(heathrow_flight_url).head()
    print("data")
    print(df)

    geojson = df_to_geojson(
        df, ["start", "end"], GeometryType.LINE_STRING, properties=["name"]
    )
    print(geojson)


def test_geojson_bounds():
    airports_url = (
        "https://github.com/visgl/deck.gl-data/raw/master/examples/line/airports.json"
    )
    df = read_json(airports_url)
    print(df.head())

    geojson = df_to_geojson(df, "coordinates")

    bbox = get_bounds(geojson)

    print(bbox)
