import pandas as pd
import numpy as np
from matplotlib import cm
from mpl_toolkits.basemap import Basemap
import matplotlib.tri as tri
import matplotlib.pyplot as plt
from numpy import linspace, meshgrid


df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/water_mass_database_cleaned.csv')
df = df.loc[df['DELC14'] > -999]
df = df.loc[df['Water Mass'] != 'Error: No Water Mass Assigned']

# df.to_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/water_mass_database_cleaned.csv')
pacific = df.loc[df['Ocean_Label'] == 'Pacific']
names = np.unique(pacific['Water Mass'])


this_wm = pacific.loc[pacific['Water Mass'] == 'Western North Pacific Central Water']

x = this_wm['LATITUDE'].array
y = this_wm['CTDPRS'].array
z = this_wm['DELC14'].array
l = int(len(z)/3)
l2 = int(len(z)/4)

plt.contour(x.reshape(l, l2), y.reshape(l, l2), z.reshape(l, l2))
# plt.scatter(x, y, c=z, cmap=cm.coolwarm)
# plt.colorbar(),
# plt.ylim(4000, 0)
# plt.xlim(-70, 70)
# plt.ylabel('Depth (CTD Pressure)')
# plt.xlabel('Latitude')
plt.show()


# data coordinates must conform to the projection


# GENERATE RANDOM X AND Y DATA
x = np.random.random((30))
y = np.random.random((30))
z = x * y

# MAP THE Y TO 30 DEGREES OF LATITUDE
yn = 30*x
# MAP THE X TO 80 DEGREES OF LON
xn = 80 + 30*y

# CREATE TRIANGULAR MESH GRID
tri = Triangulation(xn,yn)

fig = plt.figure(figsize=(7, 7))
m = Basemap(projection = 'cyl',
            llcrnrlat = 0,
            urcrnrlat = 30,
            llcrnrlon = 80,
            urcrnrlon = 110,
            resolution = 'l')

ctf = plt.tricontourf(tri, z, cmap=cm.coolwarm, zorder=10, alpha=0.75)
#plt.tricontour(tri, z, )
plt.scatter(xn, yn, c='g', zorder=13)

m.drawparallels(np.arange(-90, 90,10), labels=[1,0,0,0])
m.drawmeridians(np.arange(-180, 180, 10), labels = [0,0,0,1])
m.drawcoastlines(linewidth=0.8, color='blue', zorder=12)
m.fillcontinents(color='#C0C0C0', lake_color='#7093DB')

cbar = plt.colorbar(ctf, orientation='horizontal', fraction=.045, pad=0.08)
plt.show()



