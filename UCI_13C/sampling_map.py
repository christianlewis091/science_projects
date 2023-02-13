from data_cleaning import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

c1 = '#8073ac'
c2 = '#d73027'
c3 = '#e08214'
c1_line = '#542788'
c2_line = '#fdb863'
c3_line = '#b35806'
"""
First, initialize the figure and prepare to draw the squares
"""
# initialize where the boxes will go, and where my figures a and b will be drawn.
maxlat = 60
minlat = -70
max_lon = 100
min_lon = -180
plt.close()
# initialize the figure and subplots.
fig = plt.figure(1, figsize=(8, 8))

res = 'i'  # todo switch to i for intermediate
land = 'gray'
fillcol = 'white'
lakes = 'white'
# what do i want the size of the dots to be where the tree rings are from?
size1 = 55

map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=min_lon, urcrnrlon=max_lon, resolution=res)
# parameters to make the plot more beautiful
# map.drawcoastlines(linewidth=0.5)
# map.drawmapboundary(fill_color=fillcol, linewidth=0.5)
# map.fillcontinents(color=land, lake_color=lakes)
# map.drawcountries(linewidth=0.5)

map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 20), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
lats = df['Latitude']
lons = df['Longitude']

z, a = map(lons,  lats)
map.etopo()
map.scatter(z, a, edgecolor='black', marker='o', s = size1, color='yellow')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Full_map.png', dpi=300, bbox_inches="tight")
# plt.close()
