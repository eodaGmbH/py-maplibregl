import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from maplibre import Layer, LayerType, Map
from maplibre.sources import GeoJSONSource
from maplibre.utils import df_to_geojson, get_bounds


def st_maplibre(map: Map, height: int = 500) -> Map:
    components.html(
        map.to_html(style=f"height: {height}px;"),
        height=height + 16,
        scrolling=True,
        width=800,
    )


st.title("Uber pickups in NYC")

DATE_COLUMN = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/"
    "streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)


@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


data_load_state = st.text("Loading data...")
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox("Show raw data"):
    st.subheader("Raw data")
    st.write(data)

st.subheader("Number of pickups by hour")
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider("hour", 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader("Map of all pickups at %s:00" % hour_to_filter)
# st.map(filtered_data)

s = GeoJSONSource(data=df_to_geojson(filtered_data, ["lon", "lat"]))
m = Map(bounds=get_bounds(s.data))
l = Layer(type=LayerType.CIRCLE, source=s, paint={"circle-color": "red"})
m.add_layer(l)

st_maplibre(m)
