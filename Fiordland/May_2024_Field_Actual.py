import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
from matplotlib.patches import Polygon
# from Basemap import basemap-data-hires
import seaborn as sns
import pandas as pd
import re
size1 = 90
size2 = 1.5*size1
colors2 = sns.color_palette("mako", 30)
colors2 = list(reversed(colors2))
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D']

df = pd.read_excel('C:/2024_Polaris_II/Sampling_Log.xlsx')
df_cat = pd.read_excel('H:/Science/Current_Projects/03_coastal_carbon/May_2024_Cruise/2024_Polaris_II/sfcs2311RpoGrabs.xlsx')
stns = np.unique(df['My Station Name'])

plt.figure(figsize=(10, 8))
maxlat = -45.0
minlat = -46
nz_max_lon = 167.25
nz_min_lon = 166.25
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h')
map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.1)
map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.1)
map.fillcontinents(color="mediumaquamarine", lake_color='#DDEEFF')
map.drawmapboundary(fill_color="#DDEEFF")
map.drawcoastlines()


plt.text(167.1, -45.5, 'Doubtful S.', fontsize=12)
plt.text(167, -45.75, 'Dusky S.', fontsize=12)
#
for i in range(0, len(stns)):
    subdf = df.loc[df['My Station Name'] == stns[i]].reset_index(drop=True)

    lat = subdf['Latitude_N_decimal']
    lon = subdf['Longitude_E_decimal']
    lat = lat[0]
    lon = lon[0]
    x, y = map(lon, lat)
    map.scatter(x, y, color='blue', edgecolor='black', label='DIC only', s=size2, marker='^')


# not all stations have DOC though, so I"m going to plot DOC overtop
docs_df = df.loc[df['Sample'] == 'DOC']
stns = np.unique(docs_df['My Station Name'])
for i in range(0, len(stns)):
    subdf = docs_df.loc[docs_df['My Station Name'] == stns[i]].reset_index(drop=True)
    lat = subdf['Latitude_N_decimal']
    lon = subdf['Longitude_E_decimal']
    lat = lat[0]
    lon = lon[0]

    x, y = map(lon, lat)

    map.scatter(x, y, color='yellow', edgecolor='black', label='DOC and DIC', s=size1, marker='o')

print(df_cat.columns)
stns = np.unique(df_cat['siteNumber'])
for i in range(0, len(stns)):
    subdf = df_cat.loc[df_cat['siteNumber'] == stns[i]].reset_index(drop=True)
    lat = subdf['dropLatitude']
    lon = subdf['dropLongitude']
    lat = lat[0]
    lon = lon[0]

    x, y = map(lon, lat)

    map.scatter(x, y, color='red', edgecolor='black', label='DOC and DIC', s=size1, marker='D')


plt.savefig('C:/2024_Polaris_II/Map_actual_May29_2024_plus_cathys.png',
            dpi=300, bbox_inches="tight")





