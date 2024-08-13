import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.basemap import Basemap
import numpy as np

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland/formap.xlsx')
lucy = df.loc[df['Owner'] == 'Lucy'].reset_index(drop=True)
c1 = df.loc[df['Owner'] == 'Cathy Catalyst'].reset_index(drop=True)
c2 = df.loc[df['Owner'] == 'Cathy RPO CCE'].reset_index(drop=True)
cbl = df.loc[df['Owner'] == 'CBL'].reset_index(drop=True)
print(max(df['Latitude'].astype(str)))

plt.figure(figsize=(10, 8))
maxlat = -45.00
minlat = -46.26
nz_max_lon = 167.5
nz_min_lon = 166.25
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h')
map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.1)
map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.1)
map.fillcontinents(color="mediumaquamarine", lake_color='#DDEEFF')
map.drawmapboundary(fill_color="#DDEEFF")
map.drawcoastlines()

set = [lucy, c1, c2, cbl]
labels1 = ['Lucy', 'Cat', 'CCE','CBL']
markers1 = ['o','D','X','^']
for i in range(0, len(set)):
    set_1 = set[i]
    lat = set_1['Latitude']
    lon = set_1['Longitude']
    x, y = map(lon, lat)
    map.scatter(x, y, edgecolor='black', label=f'{labels1[i]}', marker=markers1[i], alpha=1)
plt.legend()

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/Map4lucy.png',
            dpi=300, bbox_inches="tight")
