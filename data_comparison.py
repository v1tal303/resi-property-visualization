import pandas as pd
import numpy as np
import requests

# Load in the data

main_data = pd.read_csv("testing.csv", index_col=None, header=0)
pc_data = pd.read_csv("postcode_data.csv", index_col=None, header=0)

# Retain Full postcode

main_data["FullPostcode"] = main_data["Postcode"]

# First line of postcode

main_data["Postcode"] = main_data["Postcode"].str.split().str[0]

# Merge two datasets together

mergeddata = pd.merge(main_data, pc_data, on=['Postcode'], how='inner')

# Clean Avg asking price by removing "," and convert to numeric

mergeddata['Avg asking price'] = pd.to_numeric(mergeddata['Avg asking price'].replace({",":""}, regex=True))
# mergeddata["FullPostcode"] = mergeddata["FullPostcode"].replace({" ":""}, regex=True)

# Add Difference from average price

mergeddata["PricefromAverage"] = mergeddata['Price'] - mergeddata["Avg asking price"]

postcode_endpoint = "https://api.postcodes.io/postcodes?q="+mergeddata["FullPostcode"][0]

response = requests.get(url=postcode_endpoint)

results = response.json()


print(results)








print(mergeddata)

mergeddata.to_csv("testing3.csv")
