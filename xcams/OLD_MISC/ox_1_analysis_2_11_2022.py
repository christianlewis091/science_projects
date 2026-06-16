import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt


df = pd.read_excel('H:/Science/Current_Projects/04_ams_data_quality/OX1_analyses/oxs_as_of_1_11_2022.xlsx')
df = df[['Ratio to standard', 'Date Run','TW']].dropna(subset='Ratio to standard')
df = df.loc[df['TW'] > 3360]
tws = np.unique(df['TW'])

arr = []
tw = []
for i in range(0, len(tws)):
    x = int(tws[i])
    wheel = df.loc[df['TW'] == int(tws[i])]
    std = np.std(wheel['Ratio to standard'])
    arr.append(std*1000)  # expressed as per mil
    tw.append(x)

x = pd.DataFrame({"TW":tw, "Ratio to standard": arr})
x = x.loc[x['Ratio to standard'] < 3]

plt.scatter(x['TW'], x['Ratio to standard'])
plt.title('Variability of OX-1 STD over time; red line = TW3460')

plt.xlabel('TW Wheel Number')
plt.ylabel('OX-1 Variability (\u2030)')

font = {'color':  'black', 'weight': 'normal', 'size': 12}
plt.text(3360, 1.3, 'Mean', fontdict=font)
plt.axhline(y=np.mean(x['Ratio to standard']), color="black", linestyle="--")

font = {'color':  'darkred', 'weight': 'normal', 'size': 12}
plt.axhline(y=(np.std([.99955, 1.00157, 1.00127, .99802, .99958, 1.00014])*1000), color="darkred", linestyle="-")
plt.text(3360, 1.0, '3460', fontdict=font)

font = {'color':  'darkviolet', 'weight': 'normal', 'size': 12}
plt.text(3360, 1.37, '3472', fontdict=font)
plt.axhline(1.37, color="darkviolet", linestyle="-")

plt.savefig('H:/Science/Current_Projects/04_ams_data_quality/OX1_analyses/oxs.png',
            dpi=300, bbox_inches="tight")


"""
August 29, 2022.
We had a wheel (TW3428) with a slightly low OX-1. I want to know if this low OX is statistically out of bounds.
For example, in the three sigma rule (68-95-99.7), there should be only 0.3% outside of 3 sigma. Where is my low OX-1,
and is it outside of 3-sigma?
"""

import pandas as pd
import numpy as np
from PyAstronomy import pyasl
import matplotlib.pyplot as plt

def long_date_to_decimal_date(x):
    array = []  # define an empty array in which the data will be stored
    for i in range(0, len(x)):  # initialize the for loop to run the length of our dataset (x)
        j = x[i]  # assign j: grab the i'th value from our dataset (x)
        decy = pyasl.decimalYear(j)  # The heavy lifting is done via this Py-astronomy package
        decy = float(decy)  # change to a float - this may be required for appending data to the array
        array.append(decy)  # append it all together into a useful column of data
    return array  # return the new data


df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\TW3428_ox_1_history.xlsx')  # export the file from RLIMS containing TW DATA
df = df.dropna(subset='Ratio to standard').reset_index(drop=True)  # clean up the file by dropping all the empty rows that come from the importation of the prepocessing data.
x = df['Date Run']
df['Date Run'] = long_date_to_decimal_date(x)
date_bound = max(df['Date Run']) - 1            # only take data from the past 1 year
df = df.loc[(df['Date Run'] > date_bound)]      # Index: find ONLY dates that are more recent than 1/2 year
df = df.loc[(df['Quality Flag'] != 'X..')]      # Index: drop everything that contains a quality flag
df = df.loc[(df['wtgraph'] > 0.3)]              # Drop everything that is smaller than 0.3 mg.

average = np.average(df['Ratio to standard'])
std = np.std(df['Ratio to standard'])
print("The average is {} w/ 1-sigma {}".format(average, std))
three_sig = 3*std
print("Three sigma is {} or {}".format((three_sig + average), (average - three_sig)))

ox_min = 0.995
ox_max = 1.005
df = df.loc[(ox_min < df['Ratio to standard'])]
df = df.loc[(ox_max > df['Ratio to standard'])]
# the histogram of the data
n, bins, patches = plt.hist(df['Ratio to standard'], 15, density=True, facecolor='g', alpha=0.75)

plt.xlabel('Ratio to standard')
plt.ylabel('Probability')
plt.title('OX-1 standards')
# plt.xlim(0.9, 1.1)
# plt.ylim(0, 0.03)
plt.grid(True)
# plt.show()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/XCAMS_data/ox_1s.png',
            dpi=300, bbox_inches="tight")