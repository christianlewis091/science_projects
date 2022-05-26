"""
This file shows some examples of how to use the basemap class to make nice maps

# https://basemaptutorial.readthedocs.io/en/latest/first_map.html
"""
#
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
fig=plt.figure()

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
