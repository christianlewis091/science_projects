import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap
import numpy as np
import seaborn as sns
from matplotlib.patches import Polygon

"""
First, initialize the figure and prepare to draw the sqares
"""
# initialize where the boxes will go, and where my figures a and b will be drawn.
maxlat = -30
minlat = -60
nz_max_lon = 180
nz_min_lon = 160
chile_max_lon = -60
chile_min_lon = -80

# initialize the figure and subplots.
fig = plt.figure()
plt.subplots_adjust(wspace=.2)
res = 'l'  # todo switch to i for intermediate

"""
Add first subplot: the globe centered around antarctica
"""

ax = fig.add_subplot(131)
map = Basemap(lat_0=-90, lon_0=0, resolution=res, projection='ortho')
map.drawcoastlines(linewidth=0.5)
map.drawmapboundary(fill_color='paleturquoise', linewidth=0.1)
map.fillcontinents(color='darkolivegreen', lake_color='aqua')
map.drawcountries(linewidth=0.5)
plt.text(2, 16, r'(a)', fontsize=10)

# plot where my new zealand subplot is on the globe
x1, y1 = map(nz_min_lon, maxlat)
x2, y2 = map(nz_max_lon, maxlat)
x3, y3 = map(nz_max_lon, minlat)
x4, y4 = map(nz_min_lon, minlat)
poly = Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)], facecolor="none", edgecolor='black',linewidth=1)
plt.gca().add_patch(poly)

# plot where my chile subplot is on the globe
x5, y5 = map(chile_min_lon, maxlat)
x6, y6 = map(chile_max_lon, maxlat)
x7, y7 = map(chile_max_lon, minlat)
x8, y8 = map(chile_min_lon, minlat)
poly2 = Polygon([(x5,y5),(x6,y6),(x7,y7),(x8,y8)], facecolor="none",edgecolor='black',linewidth=1)
plt.gca().add_patch(poly2)


"""
Add second subplot
"""
ax = fig.add_subplot(132)
plt.subplots_adjust(wspace=.25)
# ax.set_title("Chilean Tree Ring Sites")
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=chile_min_lon, urcrnrlon=chile_max_lon, resolution=res)
# parameters to make the plot more beautiful
map.drawcoastlines(linewidth=0.5)
map.drawmapboundary(fill_color='paleturquoise', linewidth=0.5)
map.fillcontinents(color='coral', lake_color='aqua')
map.drawcountries(linewidth=0.5)
map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)

"""
Add third subplot
"""
ax = fig.add_subplot(133)
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution=res)
# parameters to make the plot more beautiful
map.drawcoastlines(linewidth=0.5)
map.drawmapboundary(fill_color='paleturquoise', linewidth=0.5)
map.fillcontinents(color='coral', lake_color='aqua')
map.drawcountries()
map.drawparallels(np.arange(-90, 90, 10), labels=[False, False, False, False], fontsize=7, linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)

# ax.set_title('New Zealand Tree Ring Sampling Sites')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/maptest.png',
            dpi=300, bbox_inches="tight")
# plt.close()
