import pandas as pd
from compilation import MapPlotter
from geolocate import GeoLocate

df = pd.read_csv("dudley.csv")

return_locations = GeoLocate(df)

geo_located = return_locations.locate()
print(geo_located)

df_located = pd.read_csv(geo_located)


# Clean prices, latitude, longitude
nums = pd.to_numeric(df_located['propertyPrice'], errors='coerce')
clean_num = df_located[(nums.notnull())]
lat = pd.to_numeric(clean_num['latitude'], errors='coerce')
clean_lat = clean_num[(lat.notnull())]
lon = pd.to_numeric(clean_lat['longitude'], errors='coerce')
clean_lon = clean_lat[(lon.notnull())]
clean_data = clean_lon.drop(clean_lon.columns[0], axis=1)

map = MapPlotter(clean_data)

map.generate_map("test123.html")

