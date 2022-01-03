import googlemaps
import pandas as pd
import re
import numpy as np
import config

KEY = config.google_key
gmaps = googlemaps.Client(key=KEY)


class GeoLocate:
    KEY = config.google_key
    gmaps = googlemaps.Client(key=KEY)

    def __init__(self, data):
        self.data = data
        self.address = self.data["propertyAddress"]

    def get_coordinates(self, address):
        geocode_result = gmaps.geocode(str(address))
        if len(geocode_result) > 0:
            return list(geocode_result[0]['geometry']['location'].values())
        else:
            return [np.NaN, np.NaN]

    def locate(self, name):
        coordinates = self.data['propertyAddress'].apply(lambda x: pd.Series(self.get_coordinates(x), index=['latitude', 'longitude']))
        house_prices_df = pd.concat([self.data[:], coordinates[:]], axis="columns")
        file_name = f"{name}.csv"
        house_prices_df.to_csv(file_name)
        return file_name
