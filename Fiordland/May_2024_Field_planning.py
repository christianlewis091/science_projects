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

# # READ IN DATA
# df = pd.read_csv(f'H:\Science\Datasets\Fiordland\May_2024_Field_Season\Planning\Stanton_1981_DoS_Bathymetry.csv')
# plan = pd.read_excel(f'H:\Science\Datasets\Fiordland\May_2024_Field_Season\Sampling_log\Sample_Plan.xlsx')
#
# # SET UP BATHYMETRY PLOT
# x = df['km']
# y = df['dbar']
# size1 = 50
# size2 = 100
#
# fig = plt.figure(figsize=(16, 8))
# plt.plot(x, y)
# plt.ylim(460, 0)
# plt.xlim(0, max(x))
# plt.fill_between(x, y, color='lightblue', alpha=0.3)  # ocean fill color
# plt.fill_between(x, y, y2=np.max(y), color='saddlebrown', alpha=0.3)  # bottom fill color
# plt.axhline(y=5, color='red', linestyle='--', label='LSL') # lot salinity layer
#
# # ADD PROJECTED PROFILES
# dic = plan.loc[plan['SampleType'] == 'DIC14C']
# stations = np.unique(dic['Station'])
# for i in range(0, len(stations)):
#     stn = dic.loc[dic['Station'] == stations[i]]
#     duplicates = stn.loc[stn['Duplicate'] == 'Duplicate']
#     plt.scatter(stn['km'], stn['Depth'], color='black', marker='o', label='DIC14C', s=size2)
#
# doc = plan.loc[plan['SampleType'] == 'DOC14C']
# stations = np.unique(doc['Station'])
# for i in range(0, len(stations)):
#     stn = doc.loc[doc['Station'] == stations[i]]
#     duplicates = stn.loc[stn['Duplicate'] == 'Duplicate']
#     plt.scatter(stn['km'], stn['Depth'], color='indianred', marker='X', label='DIC14C', s=size2)
#     # plt.scatter(duplicates['km'], duplicates['Depth'], color='red', marker='o', s=size2)
#     # plt.plot(stn['km'], stn['Depth'], color='black')
#
# doc = plan.loc[plan['SampleType'] == 'SPE14C']
# stations = np.unique(doc['Station'])
# for i in range(0, len(stations)):
#     stn = doc.loc[doc['Station'] == stations[i]]
#     duplicates = stn.loc[stn['Duplicate'] == 'Duplicate']
#     plt.scatter(stn['km'], stn['Depth'], color='blue', marker='D', label='DIC14C', s=size2)
#
#
# # FINISH FORMATTING FIGURE
# plt.xlabel('km from 0: Stanton 1981')
# plt.ylabel('dbar')
# plt.title('Doubtful Sound Sample Plan')
# plt.savefig('H:\Science\Datasets\Fiordland\May_2024_Field_Season\Planning/DoS_plan.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#

"""
CREATING A MAP TEMPLTE FOR THE PAPER IN THE FUTURE
"""
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
from matplotlib.patches import Polygon
# from Basemap import basemap-data-hires
import seaborn as sns

colors2 = sns.color_palette("mako", 30)
colors2 = list(reversed(colors2))
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D']

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/FINAL_merged.xlsx')

# were only going to be collecting from Doubtful and Dusky, so i'll only grab the figures from those sites
subset = df.loc[(df['ctdSampleLocation'] == 'DBT') | (df['ctdSampleLocation'] == 'DUS')]

# we'll loop through the filenames and create a marker for each one
filenames = np.unique(subset['FileName'])

plt.figure(figsize=(10, 8))
maxlat = -45.0
minlat = -46
nz_max_lon = 167.25
nz_min_lon = 166.25
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h')
map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.1)
map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.1)
map.fillcontinents(color="#FFDDCC", lake_color='#DDEEFF')
map.drawmapboundary(fill_color="#DDEEFF")
map.drawcoastlines()
plt.text(167.1, -45.5, 'Doubtful S.', fontsize=12)
plt.text(167, -45.75, 'Dusky S.', fontsize=12)

for i in range(0, len(filenames)):
    stn1 = subset.loc[subset['FileName'] == filenames[i]]
    lat = np.unique(stn1['latitude'])
    lon = np.unique(stn1['longitude'])
    x, y = map(lon, lat)
    x = x[0] # some of the DBT stations had weird errors where the lon showed up twice: [167.0944685 167.0944685]
    map.scatter(x, y, edgecolor='black', color=colors2[i], marker=markers[i])


maxlat2 = -30
minlat2 = -50
nz_max_lon2 = 180
nz_min_lon2 = 160

# Create the inset map
ax = plt.gca()
axin = ax.inset_axes([0.06, 0.65, 0.4, 0.4])  # [left, bottom, width, height]
inset_map = Basemap(llcrnrlat=minlat2, urcrnrlat=maxlat2, llcrnrlon=nz_min_lon2, urcrnrlon=nz_max_lon2, resolution='l', ax=axin)
inset_map.drawcoastlines()
inset_map.drawcountries()
inset_map.fillcontinents(color="#FFDDCC", lake_color='#DDEEFF')
inset_map.drawmapboundary(fill_color="#DDEEFF")
inset_map.drawparallels(range(-90, 91, 5), labels=[1, 0, 0, 0], linewidth=0.1)
inset_map.drawmeridians(range(-180, 181, 5), labels=[0, 0, 0, 1], linewidth=0.1)

# Define polygon coordinates in the inset map's projection
x1, y1 = inset_map(nz_min_lon, minlat)
x2, y2 = inset_map(nz_min_lon, maxlat)
x3, y3 = inset_map(nz_max_lon, minlat)
x4, y4 = inset_map(nz_max_lon, maxlat)

# Plot the polygon on the inset map
poly = Polygon([(x2, y2), (x1, y1), (x3, y3), (x4, y4)], facecolor='blue', edgecolor='yellow', linewidth=1)
axin.add_patch(poly)


plt.savefig('H:/Science/Current_Projects/03_coastal_carbon/May_2024_Cruise/Cruise Panning/Fiordland_DIC_Figure1.png',
            dpi=300, bbox_inches="tight")


















































