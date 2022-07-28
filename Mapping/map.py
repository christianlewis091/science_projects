"""
This file shows some examples of how to use the basemap class to make nice maps
# https://basemaptutorial.readthedocs.io/en/latest/first_map.html
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

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
nmy_x = -70.65  # S
nmy_y = 8.2  # E


# make up some data for scatter plot
# lats = np.random.randint(-75, 75, size=20)
# lons = np.random.randint(-179, 179, size=20)

fig = plt.gcf()
fig.set_size_inches(8, 6.5)

m = Basemapm = Basemap(projection='ortho',lon_0=180,lat_0=-90,resolution='c')
m.drawcoastlines()
m.bluemarble(scale=0.2)   # full scale will be overkill
m.drawcoastlines(color='white', linewidth=0.2)  # add coastlines

x, y = m(samoa_x, samoa_y)  # transform coordinates
m.scatter(x, y, 10, marker='o', color='Red', zorder=3)

plt.show()