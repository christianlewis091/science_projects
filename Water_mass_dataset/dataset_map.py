import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
from matplotlib.patches import Polygon


# df = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\Cleaned_data.xlsx').dropna(subset='Raw d13C')
# remade the sheet above to remove dups
# df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_testing.xlsx')
df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\test.xlsx')
# changing parameters to make a plot for ellen
maxlat = 90
minlat = -90
max_lon = 180
min_lon = -180

# res = 'i'  # todo switch to i for intermediate
size1 = 50

# initialize the figure and subplots.
fig = plt.figure(1, figsize=(8, 8))
gs = gridspec.GridSpec(6, 4)
gs.update(wspace=.75, hspace=1)

# initalize the map
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=min_lon, urcrnrlon=max_lon)
map.etopo()
map.drawcoastlines()
map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 40), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)

expos = df['EXPOCODE'].astype(str)
names = np.unique(expos)
print(names)

print(names)
for i in range(0, len(names)):
    # grab the first cruise
    thiscruise = df.loc[df['EXPOCODE'] == names[i]]
    print(thiscruise)

    # grab its lats and lons
    lats = thiscruise['LATITUDE']
    lons = thiscruise['LONGITUDE']

    z, a = map(lons,  lats)
    map.scatter(z, a, marker='o', s = size1, color='black', edgecolor='black')

plt.show()
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Version3/forEllen.png', dpi=300, bbox_inches="tight")
# plt.close()






plt.show()