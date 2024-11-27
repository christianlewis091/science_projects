import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
from matplotlib.patches import Polygon
import seaborn as sns
import pandas as pd

import pyproj
print(pyproj.datadir.get_data_dir())

size1 = 90
size2 = 1.5*size1
colors2 = sns.color_palette("mako", 30)
colors2 = list(reversed(colors2))
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D']

# df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/Fiordland/Ginnane_Catalyst_2024.csv')

lat = [-45.458, -45.303, -45.76, -45.708, -46.065, -46.028]
lon = [167.155, 166.929, 166.564, 166.95, 166.685, 166.718]

plt.figure(figsize=(10, 8))
maxlat = -45.0
minlat = -46.3
nz_max_lon =166+1.3
nz_min_lon = 166.25
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h')
map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
map.drawmapboundary(fill_color="#DDEEFF")
map.drawcoastlines()
plt.text(167.1, -45.5, 'Doubtful S.', fontsize=12)
plt.text(167, -45.75, 'Dusky S.', fontsize=12)
plt.text(166.95, -45.95, 'Long S.', fontsize=12)

# Add latitude and longitude labels
map.drawparallels(np.arange(minlat, maxlat, 0.2), labels=[1, 0, 0, 0], fontsize=10, color="gray")
map.drawmeridians(np.arange(nz_min_lon, nz_max_lon, 0.2), labels=[0, 0, 0, 1], fontsize=10, color="gray")


maxlat2 = -30
minlat2 = -50
nz_max_lon2 = 180
nz_min_lon2 = 160

# Create the inset map
ax = plt.gca()
axin = ax.inset_axes([0.06, 0.65, 0.4, 0.4])  # [left, bottom, width, height]
inset_map = Basemap(llcrnrlat=minlat2, urcrnrlat=maxlat2, llcrnrlon=nz_min_lon2, urcrnrlon=nz_max_lon2, resolution='h', ax=axin)
inset_map.drawcoastlines()
inset_map.drawcountries()
inset_map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
inset_map.drawmapboundary(fill_color="#DDEEFF")
inset_map.drawcoastlines()

# inset_map.drawparallels(range(-90, 91, 5), labels=[1, 0, 0, 0], linewidth=0.1)
# inset_map.drawmeridians(range(-180, 181, 5), labels=[0, 0, 0, 1], linewidth=0.1)

# Define polygon coordinates in the inset map's projection
x1, y1 = inset_map(nz_min_lon, minlat)
x2, y2 = inset_map(nz_min_lon, maxlat)
x3, y3 = inset_map(nz_max_lon, minlat)
x4, y4 = inset_map(nz_max_lon, maxlat)

# Plot the polygon on the inset map
poly = Polygon([(x2, y2), (x1, y1), (x3, y3), (x4, y4)], facecolor='blue', edgecolor='black', linewidth=1)
axin.add_patch(poly)



x, y = map(lon, lat)
map.scatter(x, y, edgecolor='black', zorder=2, s=50, color='red', marker='D', label='Proposed')

plt.savefig(f"K:/0_THIS_WEEK/Ginnane/map1.png", dpi=300, bbox_inches="tight")
