"""
This file shows some examples of how to use the basemap class to make nice maps

# https://basemaptutorial.readthedocs.io/en/latest/first_map.html
"""
#
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
fig=plt.figure()

"""
Keeping the block of code below as my first map! 
"""

# add the first subplot - chile
ax = fig.add_subplot(121)
plt.subplots_adjust(wspace=.1)
# ax.set_title("Chilean Tree Ring Sites")
maxlat = -30
minlat = -60
nz_max_lon = 190
nz_min_lon = 150
chile_max_lon = -50
chile_min_lon = -90


map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=chile_min_lon, urcrnrlon=chile_max_lon)
# parameters to make the plot more beautiful
map.drawcoastlines()
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()
map.drawcountries()

# here is the data I want to plot
map.drawparallels(np.arange(-90,90,5),labels=[True,False,False,False])
map.drawmeridians(np.arange(-180,180,10),labels=[1,1,0,1])

# add the second subplot - nz
ax = fig.add_subplot(122)
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon)
# parameters to make the plot more beautiful
map.drawcoastlines()
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()
map.drawcountries()

# here is the data I want to plot
map.drawparallels(np.arange(-90,90,5),labels=[False,False,False,False]) # (Labels = left y-axis,
map.drawmeridians(np.arange(-180,180,10),labels=[1,1,0,1])

# ax.set_title('New Zealand Tree Ring Sampling Sites')
plt.show()
plt.close()

"""
What are the lat lon's I want to plot for my presentation? 
"""

samoa_y = 14  # S
samoa_x = 170  # West
palmer_y = 64  # S
palmer_x = 64  # West
pole_x = 90  # S
pole_y = 180  # W
mcq_x = 54  # S
mcq_y = 158  # W
cgo_x = 40  # S
cgo_y = 144  # E
nmy_x = 70.65  # S
nmy_y = 8.2  # E


# initialize the figure and subplots.
fig = plt.figure()
plt.subplots_adjust(wspace=.2)
res = 'i'  # todo switch to i for intermediate
land = 'coral'
# what do i want the size of the dots to be where the tree rings are from?
size1 = 10
"""
Add first subplot: the globe centered around antarctica
"""

ax = fig.add_subplot(131)
map = Basemap(lat_0=-90, lon_0=0, resolution=res, projection='ortho')
map.drawcoastlines(linewidth=0.5)
map.drawmapboundary(fill_color='paleturquoise', linewidth=0.1)
map.fillcontinents(color=land, lake_color='aqua')
map.drawcountries(linewidth=0.5)
plt.show()
# map.scatter(z, a, marker='D',color='m', s = size1)















































#
# ax = fig.add_subplot(132)
# plt.subplots_adjust(wspace=.25)
# # ax.set_title("Chilean Tree Ring Sites")
# map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=chile_min_lon, urcrnrlon=chile_max_lon, resolution=res)
# # parameters to make the plot more beautiful
# map.drawcoastlines(linewidth=0.5)
# map.drawmapboundary(fill_color='paleturquoise', linewidth=0.5)
# map.fillcontinents(color=land, lake_color='aqua')
# map.drawcountries(linewidth=0.5)
# map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
# map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
#
# """
# Add third subplot
# """
# ax = fig.add_subplot(133)
# map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution=res)
# # parameters to make the plot more beautiful
# map.drawcoastlines(linewidth=0.5)
# map.drawmapboundary(fill_color='paleturquoise', linewidth=0.5)
# map.fillcontinents(color=land, lake_color='aqua')
# map.drawcountries()
# map.drawparallels(np.arange(-90, 90, 10), labels=[False, False, False, False], fontsize=7, linewidth=0.5)
# map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
#
# # ax.set_title('New Zealand Tree Ring Sampling Sites')
# plt.show()
# # plt.close()
#
