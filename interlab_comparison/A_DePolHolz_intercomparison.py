import matplotlib as mpl
import numpy as np
import pandas as pd
import datetime
import seaborn as sns
from B_CGO_BHD_harmonization import harmonized
from B_CGO_BHD_harmonization import harmonized_summer
import matplotlib.pyplot as plt
from scipy import stats

colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5
# Currently the data for dePolHolz has dates as YYYY, while Soar tree rings has


# read in our data for the SOAR Tree Rings
df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\SOARTreeRingData_CBL_cleaned.xlsx')  # read in the Tree Ring data that already has flagged data removed

df = df.dropna(subset='∆14C').reset_index(drop=True)  # drop any data rows that doesn't have 14C data.
df = df.loc[(df['Site'] == 'Monte Tarn, Punta Arenas')]

# need to chop the decimals off of the DecimalDate in order to link it to DePolHolz Montetarn data
array = []
for i in range(0, len(df)):
    row = df.iloc[i]           # grab the first row
    date = row['DecimalDate']  # grab the DecimalDate
    date = str(date)           # convert it to a string
    date = date[0:4]           # grab the first 4 digits
    date = np.float64(date)    # convert back to float64
    array.append(date)

df['MergeDate'] = array

# Read in de Pol Holz data
df2 = pd.read_excel(r'H:\The Science\Datasets\Jocelyn Chile tree data 1980-2016.xlsx')
df2 = df2.loc[(df2['Sheet']) == 4]  # grab the data from Monte Tarn ONLY
df2['MergeDate'] = np.float64(df2['Year of Growth'])  # add a new date column in the form of float.

combine = df.merge(df2)
# combine.to_excel('testing.xlsx')

# Rename columns to avoid confusion

combine = combine.rename(columns={"F14C": "RRL_F14C"})
combine = combine.rename(columns={"F14Cerr": "RRL_F14Cerr"})
combine = combine.rename(columns={"∆14C": "RRL_∆14C"})
combine = combine.rename(columns={"∆14Cerr": "RRL_∆14Cerr"})
combine = combine.rename(columns={"D14C": "DPH_∆14C"})
combine = combine.rename(columns={"D14Cerr": "DPH_∆14Cerr"})
combine = combine.rename(columns={"FM": "DPH_F14C"})
combine = combine.rename(columns={"Fmerr": "DPH_F14Cerr"})
# # Reorder the columns in an order that makes more sense
combine = combine[['MergeDate', 'RRL_F14C', 'RRL_F14Cerr','RRL_∆14C', 'RRL_∆14Cerr',
                                'DPH_F14C', 'DPH_F14Cerr','DPH_∆14C', 'DPH_∆14Cerr']]
# combine.to_excel('testing.xlsx')
X = stats.ttest_rel(combine['RRL_F14C'], combine['DPH_F14C'])  # No difference.
y = stats.ttest_rel(combine['RRL_∆14C'], combine['DPH_∆14C'])  # No difference.
print(X)
print(y)
# testing

size = 50

plt.errorbar(combine['MergeDate'], combine['RRL_∆14C'], label='RRL', yerr=combine['RRL_∆14Cerr'],
             fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.errorbar(combine['MergeDate'], combine['DPH_∆14C'], label='Uni Magallanes', yerr=combine['DPH_∆14Cerr'],
             fmt='D', color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2)
plt.legend(fontsize=7.5)
# plt.xlim(1980, 2020)
# plt.ylim(.95, 1.3)
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/reading_group_pres/MagallanesvRRL.png',
    dpi=300, bbox_inches="tight")

