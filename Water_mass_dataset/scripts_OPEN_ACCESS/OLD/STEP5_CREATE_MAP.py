"""
I want to see a map of all the 14C data that's out there, this will be Figure 1.
"""
# IMPORT MODULES
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec


# read in the sheet that was written in the above section of the code.
df = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP3_data_workup/STEP3_WATER_MASSES_ASSIGNED.xlsx')

maxlat = 90
minlat = -90
max_lon = 180
min_lon = -180

# res = 'i'  # todo switch to i for intermediate
size1 = 50

# initialize the figure and subplots.
fig = plt.figure(1, figsize=(8, 8))
gs = gridspec.GridSpec(8, 8)
gs.update(wspace=.75, hspace=1)

import matplotlib.gridspec as gridspec
# initalize the map
xtr_subsplot = fig.add_subplot(gs[0:4, 0:8])
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=min_lon, urcrnrlon=max_lon)
map.etopo()
map.drawcoastlines()
map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 40), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
df1 = df.loc[df['Project Name'] == "GO-SHIP"]
expos = df1['EXPOCODE'].astype(str)
names = np.unique(expos)
for i in range(0, len(names)):
    # grab the first cruise
    thiscruise = df1.loc[df1['EXPOCODE'] == names[i]]

    # grab its lats and lons
    lats = thiscruise['LATITUDE']
    lons = thiscruise['LONGITUDE']

    z, a = map(lons,  lats)
    map.scatter(z, a, marker='o', s = 3.5, color='crimson', edgecolor='crimson')


xtr_subsplot = fig.add_subplot(gs[4:8, 0:8])
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=min_lon, urcrnrlon=max_lon)
map.etopo()
map.drawcoastlines()
map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 40), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
df2 = df.loc[df['Project Name'] == "GLODAP"]
expos = df2['EXPOCODE'].astype(str)
names = np.unique(expos)
for i in range(0, len(names)):
    # grab the first cruise
    thiscruise = df2 .loc[df2 ['EXPOCODE'] == names[i]]

    # grab its lats and lons
    lats = thiscruise['LATITUDE']
    lons = thiscruise['LONGITUDE']

    z, a = map(lons,  lats)
    map.scatter(z, a, marker='o', s = 3.5, color='yellow', edgecolor='yellow')


plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP5_create_map/Map.jpg', dpi=300, bbox_inches="tight")
