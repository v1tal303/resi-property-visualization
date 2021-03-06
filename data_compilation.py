import pandas as pd
import glob
import config


# Combine multiple csv into one dataframe

path = r'C:\Users\murci\Documents\GitHub\resi-property-webscrape\csv'
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)


# Clean the data and remove duplicate URL's

df = frame.drop_duplicates(subset=['URL'], keep=False).copy()
print(len(frame))

# Redirect the URL's

df['URL'] = df.URL.replace({config.zp: "https://www.zoopla.co.uk/for-sale/details/", config.otm: 'https://www.onthemarket.com/details/', config.rm:"https://www.rightmove.co.uk/properties/"}, regex=True)


# Save to csv

df.to_csv("testing.csv")