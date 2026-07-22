"""
20-11-23

I'm trying to write a proposal for the ASP Opportunities Fund. I want to figure out how many cruises have
gone into the Suothern Ocean over different timescales?

"""
import numpy as np
import pandas as pd

# read in the dataset that has been cropped to only include the top 100m so it reads in 75% faster
df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_ALLDATA100m.xlsx')

# only find data this is below Southern Ocean line
spans = [-30, -45, -60, -75]
for j in range(0, len(spans)):
    df = df.loc[df['LATITUDE'] <= spans[j]]

    # what's the minimum date?
    datemin = min(np.unique(df['DATE']))

    nums = []
    other = []
    for i in range(0, len(df)):
        row = df.iloc[i]
        expo = row['EXPOCODE']
        expo = str(expo)

        if expo.isnumeric():
            nums.append(expo)
        else:
            other.append(expo)

    print(f'There have been {len(np.unique(nums))+len(np.unique(other))} cruises that have sampled below {spans[j]} since {datemin}')
