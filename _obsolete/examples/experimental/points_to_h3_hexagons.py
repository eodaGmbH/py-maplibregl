import h3
import pandas as pd
from pandas import read_csv

df = read_csv(
    "https://github.com/crazycapivara/mapboxer/raw/master/data-raw/motor_vehicle_collisions.csv",
    sep=";",
)


def create_h3_hexagons(df: pd.DataFrame, lng: str = "lng", lat: str = "lat"):
    df = (
        df.apply(lambda x: h3.geo_to_h3(x[lat], x[lng], resolution=7), axis=1)
        .to_frame("h3")
        .groupby("h3", as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )

    df["hexagon"] = df.apply(
        lambda x: [h3.h3_to_geo_boundary(x["h3"], geo_json=True)], axis=1
    )

    return df


if __name__ == "__main__":
    df = create_h3_hexagons(df)
    print(df)
