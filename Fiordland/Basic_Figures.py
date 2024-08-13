import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap

df = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/02_SPEDOC/SPE_Processing_and_Data.xlsx', sheet_name='Cruise_Data_Sheet_ALL', comment='#')
df = df.loc[df['Qflag'] != '.X.']

"""
DIC concentrations
"""
colors = ['sienna','SeaGreen','Teal','deepskyblue','Blue']
dudes = ['o','D','^','s','X']



fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(2, 2)
gs.update(wspace=0.1, hspace=0.25)

"""
DOUBTFUL SOUND
"""

# first subplot, concentrations
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])

dbt_station = [1,2,3,4]
dic = df.loc[((df['Sample'] == 'DIC') | (df['Sample'] == 'DIC Duplicate')) & (df['My Station Name'].isin(dbt_station))]
dic = dic.dropna(subset='TDIC (mmol kgH20)')
stations = np.unique(dic['My Station Name'])

for i in range(0, len(stations)):
    this_stn = dic.loc[dic['My Station Name'] == stations[i]].sort_values(by='Depth')
    plt.plot(this_stn['TDIC (mmol kgH20)'], this_stn['Depth'], color=colors[i])
    plt.errorbar(this_stn['TDIC (mmol kgH20)'], this_stn['Depth'], xerr=this_stn['TDICerr'], marker='o', label=f'{stations[i]}', color=colors[i])
plt.ylim(350,-10)
plt.xlim(.5, 2.5)
plt.axhline(y=0, color='black', alpha=0.15) #note the surface
plt.xlabel('TDIC (mmol kgH20)')
plt.ylabel('Depth (m)')
plt.legend()

# second subplot - map
xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
maxlat = -45.0
minlat = -46
nz_max_lon = 167.25
nz_min_lon = 166.25
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h')
map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.1)
map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.1)
map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
map.drawmapboundary(fill_color="#DDEEFF")
map.drawcoastlines()
for i in range(0, len(stations)):
    this_stn = dic.loc[dic['My Station Name'] == stations[i]].reset_index(drop=True)

    lat = this_stn['Latitude_N_decimal']
    lon = this_stn['Longitude_E_decimal']
    lat = lat[0]
    lon = lon[0]
    x, y = map(lon, lat)
    map.scatter(x, y, label=f'{stations[i]}', color=colors[i])
plt.legend()

xtr_subsplot = fig.add_subplot(gs[1:2, 0:1])


"""
DUSKY SOUND
"""
dbt_station = [5,6,7,8,9]
dic = df.loc[((df['Sample'] == 'DIC') | (df['Sample'] == 'DIC Duplicate')) & (df['My Station Name'].isin(dbt_station))]
dic = dic.dropna(subset='TDIC (mmol kgH20)')
stations = np.unique(dic['My Station Name'])

for i in range(0, len(stations)):
    this_stn = dic.loc[dic['My Station Name'] == stations[i]].sort_values(by='Depth')
    plt.plot(this_stn['TDIC (mmol kgH20)'], this_stn['Depth'], color=colors[i])
    plt.errorbar(this_stn['TDIC (mmol kgH20)'], this_stn['Depth'], xerr=this_stn['TDICerr'], marker='o', label=f'{stations[i]}', color=colors[i])
plt.ylim(350,-10)
plt.xlim(.5, 2.5)
plt.axhline(y=0, color='black', alpha=0.15) #note the surface
plt.xlabel('TDIC (mmol kgH20)')
plt.ylabel('Depth (m)')
plt.legend()


xtr_subsplot = fig.add_subplot(gs[1:2, 1:2])
maxlat = -45.0
minlat = -46
nz_max_lon = 167.25
nz_min_lon = 166.25
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h')
map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.1)
map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.1)
map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
map.drawmapboundary(fill_color="#DDEEFF")
map.drawcoastlines()
for i in range(0, len(stations)):
    this_stn = dic.loc[dic['My Station Name'] == stations[i]].reset_index(drop=True)

    lat = this_stn['Latitude_N_decimal']
    lon = this_stn['Longitude_E_decimal']
    lat = lat[0]
    lon = lon[0]
    x, y = map(lon, lat)
    map.scatter(x, y, label=f'{stations[i]}', color=colors[i])
plt.legend()

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/DIC_conc.png', dpi=300, bbox_inches="tight")
plt.close()



"""
SPE-DOC
August 5, 2024: What yields are we getting from secondary standards on the SPE cartridge? 
"""

fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(1, 2)
gs.update(wspace=0.2, hspace=0.35)


xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# first I want to see the raw data...

# grab the data
tannic = df.loc[(df['STD_ONLY_type'] == 'tannic acid')]
t_x = tannic['STD_ONLY_mg C added']
t_x = np.array(t_x)
t_y = tannic['processing mg C']
t_y = np.array(t_y)

sal = df.loc[(df['STD_ONLY_type'] == 'salicylic acid')]
s_x = sal['STD_ONLY_mg C added']
s_x = np.array(s_x)
s_y = sal['processing mg C']
s_y = np.array(s_y)

# regress the data
slope, intercept, rvalue, pvalue, stderr = stats.linregress(t_x, t_y)
sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(s_x, s_y)

# plot the data and trendlines
plt.scatter(t_x, t_y, label='Tannic Acid', marker='D', color='black')
plt.scatter(s_x, s_y, label='Salicylic Acid', marker='o', color='brown')
plt.plot(t_x, slope*t_x+intercept)
plt.plot(s_x, sslope*s_x+sintercept)
plt.annotate("Tannic: y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2), xy=(0.07, 0.7), xycoords='figure fraction')
plt.annotate("Salicylic: y=%.3fx+%.3f\R$^2$=%.3f"%(sslope, sintercept,srvalue**2), xy=(0.07, 0.65), xycoords='figure fraction')
plt.xlabel('mg C added to standard solution')
plt.ylabel('mg C from Processing Line')
plt.legend()

xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])

# grab the data
tannic = df.loc[(df['STD_ONLY_type'] == 'tannic acid')]
t_x = tannic['STD_ONLY_mg C added']
t_x = np.array(t_x)
t_y = tannic['SPE % Recovery']
t_y = np.array(t_y)

sal = df.loc[(df['STD_ONLY_type'] == 'salicylic acid')]
s_x = sal['STD_ONLY_mg C added']
s_x = np.array(s_x)
s_y = sal['SPE % Recovery']
s_y = np.array(s_y)

# regress the data
slope, intercept, rvalue, pvalue, stderr = stats.linregress(t_x, t_y)
sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(s_x, s_y)
print("y=%.3fx+%.3f"%(slope, intercept))
print("y=%.3fx+%.3f"%(sslope, sintercept))

# plot the data and trendlines
plt.scatter(t_x, t_y, label='Tannic Acid', marker='D', color='black')
plt.scatter(s_x, s_y, label='Salicylic Acid', marker='o', color='brown')
plt.plot(t_x, slope*t_x+intercept)
plt.plot(s_x, sslope*s_x+sintercept)
plt.annotate("Tannic: y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2), xy=(0.52, 0.35), xycoords='figure fraction')
plt.annotate("Salicylic: y=%.3fx+%.3f\R$^2$=%.3f"%(sslope, sintercept,srvalue**2), xy=(0.52, 0.3), xycoords='figure fraction')
plt.xlabel('mg C added to standard solution')
plt.ylabel('SPE % Recovery')
plt.ylim(0, 110)
plt.legend()


plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/Secondaries_Yields.png', dpi=300, bbox_inches="tight")



