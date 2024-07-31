from maplibre import express as mx
from maplibre.expressions import interpolate
from maplibre.settings import settings

settings.line_width = 2
settings.line_color = "green"

# data = "https://docs.maptiler.com/sdk-js/assets/Mean_age_of_women_at_first_marriage_in_2019.geojson"
# data = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_urban_areas.geojson"
# data = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_1_states_provinces_scale_rank.geojson"
# data = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_1_states_provinces.geojson"
data = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_railroads_north_america.geojson"

mx.line(data).to_map(hash=True).save("/tmp/py-maplibre-express.html")
