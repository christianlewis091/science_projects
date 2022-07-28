from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
fig = plt.figure(4, figsize=(8, 8))

# Heather Graven's data, to be corrected accroding to the offset from SIO/LLNL:
# AMERICAN SAMOA
samoa_x = -170
samoa_y = -14
# PALMER STATION ANTARCTICA
palmer_x = -64
palmer_y = -64.77
# SOUTH POLE ANTARCTICA
south_pole_x = -180
south_pole_y = -90

# Heidelberg Data that we will correct using the Heidelberg Cape Grim data:
# NEUMAYER STATION
neumayer_x = -8.2
neumayer_y = -70
# MCQUARIE ISLAND
mcq_x = 158
mcq_y = -54
# CAPE GRIM
cgo_x = 144.6
cgo_y = -40.6

# Chile data from the Magallanes Group that we will be comparing with Monte Tarn
montetarn_x = -71
montetarn_y = -54

# SOAR TREE RING DATA
Lats = [-52.52, -46.926417, -46.437, -43.85, -41.068, -39.483, -36.828, -54.926, -52.531, -47.81, -43.79]
Lons = [169, 167.795867, 168.234, 169.0, 174.145, 174.134, 174.432, -67.439, -72.089, -73.586, -72.946]

map = Basemap(projection='ortho',
              lat_0=-90, lon_0=-180)

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()

x, y = map(samoa_x, samoa_y)
a, b = map(palmer_x, palmer_y)
c, d = map(south_pole_x, south_pole_y)
e, f = map(mcq_x, mcq_y)
g, h = map(neumayer_x, neumayer_y)
i, j = map(montetarn_x, montetarn_y)
k, l = map(Lons, Lats)
m, n = map(cgo_x, cgo_y)

map.scatter(x, y, marker='D',color='tab:blue', label = 'SIO/LLNL')
map.scatter(a, b, marker='D',color='tab:blue')
map.scatter(c, d, marker='D',color='tab:blue')

map.scatter(e, f, marker='o',color='tab:red', label = 'Uni. Heidelberg')
map.scatter(g, h, marker='o',color='tab:red')
map.scatter(m, n, marker = 'o', color='tab:red')

map.scatter(i, j, marker='^', color='tab:green', label = 'Uni. Magallanes')

map.scatter(k, l, marker='X', color='black', label = 'SOAR Tree Rings')
plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/newmap.png',
            dpi=300, bbox_inches="tight")