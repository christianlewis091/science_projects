"""
Purpose:

Use the harmonized Southern Hemisphere dataset to see if we can find shifts in SOAR tree rings
to understand Southern ocean upwelling.

Outcome:
Currently in DEV mode.

"""
# TODO Index based on the flags in the dataset!
# Import all the basic libraries that I'll be using
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dataset_harmonization import harmonized
from miller_curve_algorithm import ccgFilter
from my_functions import monte_carlo_randomization_trend
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from functools import reduce
from matplotlib.patches import Polygon
pd.options.mode.chained_assignment = None  # default='warn'  # https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
"""
These next few lines appear often at the top of my codes. 
These next lines set some initial parameters that figures in the code will follow
and imports some nice colors that we'll use. 
"""
plt.close()
colors = sns.color_palette("rocket", 6)  # import sns color pallet rocket
colors2 = sns.color_palette("mako", 6)  # import sns color pallet mako.
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10

df = pd.read_excel(r'H:\The Science\Datasets'
                   r'\SOARTreeRingData2022-02-01.xlsx')  # read in the Tree Ring data.
df = df.dropna(subset='∆14C').reset_index(drop=True)  # drop any data rows that doesn't have 14C data.
# df = df.loc[(df['C14Flag']) != 'A..']


# TODO edit harmonized dataset to use yearly averages from November to February. Plot this as an add on to the plots
# remove all data that's not between November and February (11, 12, 1, 2).


L = np.linspace(0, 1, 365)
# add the number that is 1/2 of the previous month plus the current month
Jan = 31 / 365
Feb = ((28 / 2) + 31) / 365
Mar = ((31 / 2) + 31 + 28) / 365
Apr = ((30 / 2) + 31 + 28 + 31)/ 365
May = ((31 / 2) + 31 + 28 + 31 + 30)/ 365
June = ((30 / 2) + 31 + 28 + 31 + 30 + 31)/ 365
July = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30)/ 365
August = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31)/ 365
Sep = ((30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31)/ 365
Oct = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30)/ 365
Nov = ((30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30)/ 365
Dec = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30 + 30)/ 365
print(Nov)
print(Dec)
print(Jan)
print(Feb)
harmonized['test'] = harmonized['Decimal_date']
mt_array = []
harmonized = harmonized.reset_index(drop=True)
for i in range(0, len(harmonized)):
    row = harmonized.iloc[i]
    element = row['Decimal_date']
    element = str(element)                      # convert to string to slice
    element = element[4:9:1]
    # print(type(element))
    element = np.float_(element)                # convert back to float for indexing a few lines later

    mt_array.append(element)

indexed = pd.DataFrame(mt_array)

df2 = pd.concat([harmonized, indexed], axis=1)
df2 = df2.loc[((df2[0]) < .124) | ((df2[0]) > .870)]
df2.to_excel('test.xlsx')


array = []
for i in range(0,10000):
    rand = np.random.normal(10, 2, size=None)
    array.append(rand)
plt.hist(array, bins=100)
plt.show()






