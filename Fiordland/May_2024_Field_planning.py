"""
Here, I'm making some figures to help me plan for May 2024 Field season with Moy and Co.
"""
# IMPORT MODULES
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

# READ IN DATA
df = pd.read_csv(f'H:\Science\Datasets\Fiordland\May_2024_Field_Season\Planning\Stanton_1981_DoS_Bathymetry.csv')
plan = pd.read_excel(f'H:\Science\Datasets\Fiordland\May_2024_Field_Season\Planning\Sample_Plan.xlsx')

# SET UP BATHYMETRY PLOT
x = df['km']
y = df['dbar']
size1 = 50
size2 = 100

fig = plt.figure(figsize=(16, 8))
plt.plot(x, y)
plt.ylim(460, 0)
plt.xlim(0, max(x))
plt.fill_between(x, y, color='lightblue', alpha=0.3)  # ocean fill color
plt.fill_between(x, y, y2=np.max(y), color='saddlebrown', alpha=0.3)  # bottom fill color
plt.axhline(y=5, color='red', linestyle='--', label='LSL') # lot salinity layer

# ADD PROJECTED PROFILES
dic = plan.loc[plan['SampleType'] == 'DIC14C']
stations = np.unique(dic['Station'])
for i in range(0, len(stations)):
    stn = dic.loc[dic['Station'] == stations[i]]
    duplicates = stn.loc[stn['Duplicate'] == 'Duplicate']
    plt.scatter(stn['km'], stn['Depth'], color='black', marker='o', label='DIC14C', s=size2)

doc = plan.loc[plan['SampleType'] == 'DOC14C']
stations = np.unique(doc['Station'])
for i in range(0, len(stations)):
    stn = doc.loc[doc['Station'] == stations[i]]
    duplicates = stn.loc[stn['Duplicate'] == 'Duplicate']
    plt.scatter(stn['km'], stn['Depth'], color='indianred', marker='X', label='DIC14C', s=size2)
    # plt.scatter(duplicates['km'], duplicates['Depth'], color='red', marker='o', s=size2)
    # plt.plot(stn['km'], stn['Depth'], color='black')

doc = plan.loc[plan['SampleType'] == 'SPE14C']
stations = np.unique(doc['Station'])
for i in range(0, len(stations)):
    stn = doc.loc[doc['Station'] == stations[i]]
    duplicates = stn.loc[stn['Duplicate'] == 'Duplicate']
    plt.scatter(stn['km'], stn['Depth'], color='blue', marker='D', label='DIC14C', s=size2)


# FINISH FORMATTING FIGURE
plt.xlabel('km from 0: Stanton 1981')
plt.ylabel('dbar')
plt.title('Doubtful Sound Sample Plan')
plt.savefig('H:\Science\Datasets\Fiordland\May_2024_Field_Season\Planning/DoS_plan.png',
            dpi=300, bbox_inches="tight")
plt.close()


