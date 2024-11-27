import warnings
warnings.filterwarnings('ignore')
import numpy as np
import cartopy.feature as cf
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

"""
https://nbviewer.org/github/jsimkins2/geog473-673/blob/master/Python/Cartopy_tutorial.ipynb
"""

central_lat = 37.5
central_lon = -96
extent = [-120, -70, 24, 50.5]
central_lon = np.mean(extent[:2])
central_lat = np.mean(extent[2:])

rivers_50m = cf.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '50m')

plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.AlbersEqualArea(central_lon, central_lat))
ax.set_extent(extent)

ax.add_feature(cf.OCEAN)
ax.add_feature(cf.LAND, edgecolor='black')
ax.add_feature(rivers_50m, facecolor='None', edgecolor='b')
ax.gridlines()
plt.show()