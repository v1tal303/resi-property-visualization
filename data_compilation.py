import pandas as pd
import glob

path = r'C:\Users\murci\Documents\GitHub\resi-property-webscrape\csv' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

print(list(frame))

df = frame.drop_duplicates(subset=['URL'], keep=False)
print(len(frame))

df.loc[df['URL'].str.contains('zoopla'), 'sport'] = 'ball sport'


frame.to_csv("testing.csv")