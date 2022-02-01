import pandas as pd
import numpy as np
import requests
from time import sleep

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

# Setup additional columns in the dataframe

postcode_endpoint = "https://api.postcodes.io/postcodes?q="+mergeddata["FullPostcode"][1]
response = requests.get(url=postcode_endpoint)
results = response.json()
result_data = results["result"][0]
result_data.pop("codes", None)
for key, value in result_data.items():
    mergeddata[key] = value

# Iterate over all postcodes

count = 0

for index, row in mergeddata.iterrows():
    print(mergeddata["FullPostcode"][index])
    postcode_endpoint = "https://api.postcodes.io/postcodes?q="+mergeddata["FullPostcode"][index]
    print(postcode_endpoint)
    response = requests.get(url=postcode_endpoint)
    results = response.json()
    result_data = results["result"][0]
    result_data.pop("codes", None)
    for key, value in result_data.items():
        mergeddata[key][index] = value
    print(index)
    count += 1
    if count % 10000 == 0:
        sleep(600)


mergeddata.to_csv("testing3.csv")


# TODO:
#  1) Clean up the code and add documentation
#  2) Find quicker methods to analyze postcode data by grouping as a lot of postcodes repeat.

