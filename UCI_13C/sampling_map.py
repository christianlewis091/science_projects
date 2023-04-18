import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Polygon


# df = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\Cleaned_data.xlsx').dropna(subset='Raw d13C')
# remade the sheet above to remove dups
df = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\Cleaned_data4map.xlsx').dropna(subset='Raw d13C')
# make sure no other plots are opened
plt.close()
"""
First, initialize the figure and prepare to draw the squares
"""

# initialize where the boxes will go, and where my figures a and b will be drawn.
maxlat = 60
minlat = -70
max_lon = 100
min_lon = -180

res = 'i'  # todo switch to i for intermediate
# what do i want the size of the dots to be where the tree rings are from?
size1 = 50

# data markers for each cruise
cruises = ['IO7N','P16N', 'P18']
colors = ['#d73027','#fc8d59','#4575b4']
symbol = ['o','^','D','s']


# initialize the figure and subplots.
fig = plt.figure(1, figsize=(8, 8))

# initalize the map
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=min_lon, urcrnrlon=max_lon, resolution=res)

# draw coastlines
map.drawmapboundary(fill_color='lightgrey')

#Fill the continents with the land color
map.fillcontinents(color='darkgrey')

map.drawcoastlines()

# decide where the map will be in lat lon space
map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 40), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)

for i in range(0, 3):
    # grab the first cruise
    thiscruise = df.loc[df['Cruise'] == cruises[i]]

    # grab its lats and lons
    lats = thiscruise['Latitude']
    lons = thiscruise['Longitude']

    z, a = map(lons,  lats)
    map.scatter(z, a, marker=symbol[i], s = size1, color=colors[i], edgecolor='black')



plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Version3/MapV3.png', dpi=300, bbox_inches="tight")
plt.close()

