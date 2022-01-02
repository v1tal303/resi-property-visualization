import googlemaps
import pandas as pd
import re
import numpy as np

KEY = "AIzaSyBbkunl8NeA_6vd8l3fSCxh9FgelUb0o2g"
gmaps = googlemaps.Client(key=KEY)

df = pd.read_csv("test2.csv")
address = df["propertyAddress"]


def get_coordinates(address):
    geocode_result = gmaps.geocode(str(address))
    if len(geocode_result) > 0:
        return list(geocode_result[0]['geometry']['location'].values())
    else:
        return [np.NaN, np.NaN]


coordinates = df['propertyAddress'].apply(lambda x: pd.Series(get_coordinates(x), index=['Latitude', 'Longitude']))
house_prices_df = pd.concat([df[:], coordinates[:]], axis="columns")

house_prices_df.to_csv("test2.csv")

print(df)