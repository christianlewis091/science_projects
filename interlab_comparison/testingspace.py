from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

map = Basemap(projection='cyl')

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()

x1,y1 = map(-25,-25)
x2,y2 = map(-25,25)
x3,y3 = map(25,25)
x4,y4 = map(25,-25)
poly = Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)],facecolor='red',edgecolor='green',linewidth=3)
plt.gca().add_patch(poly)

plt.show()