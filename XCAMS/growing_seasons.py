"""
Lets see if I can get wintertime averages
"""
import matplotlib as mpl
import numpy as np
import pandas as pd
import datetime as dt
import seaborn as sns

df = pd.read_excel(r'H:\Science\Datasets\heidelberg_MQA.xlsx', skiprows=0)

def growing_season(df):
    dates = df['Average of Dates']
    season_array = []
    for i in range(0, len(dates)):
        currentrow = dates.iloc[i]
        month = currentrow.month
        year = currentrow.year

        if str(month) in ['9', ' 10', '11', '12']:
            season_array.append(f"growing_season_{year}_{year + 1}")

        elif str(month) in ['1', '2', '3', '4']:
            season_array.append(f"growing_season_{year - 1}_{year}")

        else:
            season_array.append('non-growing')

    return(season_array)

x = growing_season(df)
df['season_category'] = x

means = df.groupby('season_category').mean().reset_index()
# means = df.groupby('season_category').apply(np.mean)
means = pd.DataFrame(means)
means.to_excel(r'H:\Science\Datasets\testingmeans.xlsx')
