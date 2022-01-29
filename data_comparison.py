import pandas as pd
import numpy as np

# Load in the data

main_data = pd.read_csv("testing.csv", index_col=None, header=0)
pc_data = pd.read_csv("postcode_data.csv", index_col=None, header=0)

# Retain Full postcode

main_data["FullPostcode"] = main_data["Postcode"]

# First line of postcode

main_data["Postcode"] = main_data["Postcode"].str.split().str[0]

# Merge two datasets together

mergeddata = pd.merge(main_data, pc_data, on=['Postcode'], how='inner')

mergeddata["PriceAverageDifference"] = mergeddata['Price'].sub(mergeddata['Avg asking price'], axis = 0)

print(mergeddata)

mergeddata.to_csv("testing2.csv")


# (np.where(main_data["Price"] < pc_data["Avg asking price"], "Below Average", "Above Average"))
#
# main_data['priceData'] = np.where(main_data['Postcode2'] == pc_data['Postcode'], "True", 'False')