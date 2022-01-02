import geopandas as gpd
import pandas as pd
from shapely.ops import nearest_points
from shapely.geometry import LineString

# Loading house prices dataframe - Assumed that user is using downloaded data, if following from the top
# of the article, ignore this line and use the house_prices_df from above.
house_prices_df = pd.read_csv("test2.csv")


# airbnb df - downloaded data
airbnb_df = pd.read_csv("listings.csv")
airbnb_df = airbnb_df[['name','neighbourhood','latitude','longitude','room_type','price']]

# Ensures that we only get private rooms, not whole flats
airbnb_df = airbnb_df[airbnb_df.room_type.str.contains("Private room")].reset_index(drop= True)
