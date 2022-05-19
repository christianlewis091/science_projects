# multipanel basemap plot:
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib as mpl
import seaborn as sns
# mpl.rcParams['pdf.fonttype'] = 42
# mpl.rcParams['font.size']=8

#Prepare multipanel plot
fig = plt.figure(1)
gs = gridspec.GridSpec(6,4)
# gs.update(wspace=0.1, hspace=0.25)

#Generate first panel
#remember, the grid spec is rows, then columns
xtr_subsplot= fig.add_subplot(gs[0:2,0:2])
map = Basemap(projection='ortho',
              lat_0=-90, lon_0=0)
# map = Basemap(llcrnrlat=-90, urcrnrlat=0, llcrnrlon=-120, urcrnrlon=190)
# parameters to make the plot more beautiful
map.drawcoastlines()
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()
map.drawcountries()

# here is the data I want to plot
# map.drawparallels(np.arange(-90,90,5),labels=[False,False,False,False]) # (Labels = left y-axis,
# map.drawmeridians(np.arange(-180,180,10),labels=[False,False,False,False])


#generate second panel
xtr_subsplot = fig.add_subplot(gs[2:4,0:2])
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


#generate third panel
xtr_subsplot = fig.add_subplot(gs[2:4,2:4])
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


plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/maptest.png',
            dpi=300, bbox_inches="tight")

#Export figure
