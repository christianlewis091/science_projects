import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap
import warnings
warnings.simplefilter("ignore")

# set initial figure settings
mako = sns.color_palette("mako", 6)
colors_dbt = ['SeaGreen','Teal','deepskyblue','Blue']
colors_dus = ['SeaGreen','Sienna','Teal','deepskyblue','Blue']
marks = ['o','D','^','s','X']


"""
Collate Final Data sheet by mergeing my sampling log with RLIMS OUTPUT! 
"""
# df = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/02_SPEDOC/SPE_Processing_and_Data.xlsx', sheet_name='Cruise_Data_Sheet_ALL', comment='#')
# df = df[['My Station Name', 'Cruise Station Name','Latitude_N_decimal','Longitude_E_decimal','Bottom Depth (m)','Depth','Qflag','Sample','TP']]
# df = df.loc[df['Qflag'] != '.X.']
# dic = df.loc[((df['Sample'] == 'DIC') | (df['Sample'] == 'DIC Duplicate'))]
#
# tw3530 = pd.read_excel('H:/Science/Datasets/Fiordland/TW3530_export.xlsx')
# tw3530 = tw3530.loc[tw3530['Samples::Sample Description'] == 'Fiordland DIC samples from SFCS2405'] # remove oxalics, kapunis, etc
#
# df = dic.merge(tw3530, on='TP')
#
# df.to_excel('H:/Science/Datasets/Fiordland/Fiordland_DIC_14C_2024.xlsx')

"""
Re-read in sheet and make plots
"""
df = pd.read_excel('H:/Science/Datasets/Fiordland/Fiordland_DIC_14C_2024.xlsx', sheet_name='Duplicates_Removed', comment='#')
df = df.rename(columns={'Latitude_N_decimal': 'lat', 'Longitude_E_decimal': 'lon'})

# I need to analyze these data, at least initally, as seperate "things" as 1) river water and 2) marine water
df['River_Ocean'] = 'Ocean' # set inital status to ocean
df.loc[(df['Depth'] == 1), 'River_Ocean'] = 'River'

# add Sound labels
df['Sound'] = 'Dusky' # set initial status to Dusky
dbt_station = [1,2,3,4]
df.loc[(df['My Station Name'].isin(dbt_station)), 'Sound'] = 'Doubtful'

dus_riv = df.loc[(df['Sound'] == 'Dusky') & (df['River_Ocean'] == 'River')]
dbt_riv = df.loc[(df['Sound'] == 'Doubtful') & (df['River_Ocean'] == 'River')]

# Regression of surface data
dus_riv_x = dus_riv['lon']
dus_riv_x = np.array(dus_riv_x)
dus_riv_y = dus_riv['DELTA14C']
dus_riv_y = np.array(dus_riv_y)
#
dbt_riv_x = dbt_riv['lon']
dbt_riv_x = np.array(dbt_riv_x)
dbt_riv_y = dbt_riv['DELTA14C']
dbt_riv_y = np.array(dbt_riv_y)

# regress the data
slope, intercept, rvalue, pvalue, stderr = stats.linregress(dus_riv_x, dus_riv_y)
print("Dusky Surface: y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2))

sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(dbt_riv_x, dbt_riv_y)
print("Doubtful Surface: y=%.3fx+%.3f\R$^2$=%.3f"%(sslope, sintercept,srvalue**2))

# quick look at surface data:
fig = plt.figure()
plt.errorbar(dus_riv['lon'], dus_riv['DELTA14C'], yerr=dus_riv['DELTA14C_Error'], label='Dusky', marker='o', linestyle='', color='black', capsize=5)
plt.errorbar(dbt_riv['lon'], dbt_riv['DELTA14C'], yerr=dbt_riv['DELTA14C_Error'], label='Doubtful', marker='D', linestyle='', color='seagreen', capsize=5)
plt.plot(dus_riv_x, slope*dus_riv_x+intercept, color='black', alpha= 0.5)
plt.plot(dbt_riv_x, sslope*dbt_riv_x+sintercept, color='seagreen', alpha= 0.5)
plt.xlabel('Longitude (E)')
plt.ylabel('DELTA14C')
plt.legend()
plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/Figure1.png', dpi=300, bbox_inches="tight")
plt.close()

fig = plt.figure()
plt.errorbar(dus_riv['delta13C_IRMS'], dus_riv['DELTA14C'], yerr=dus_riv['DELTA14C_Error'], label='Dusky', marker='o', linestyle='', color='black', capsize=5)
plt.errorbar(dbt_riv['delta13C_IRMS'], dbt_riv['DELTA14C'], yerr=dbt_riv['DELTA14C_Error'], label='Doubtful', marker='D', linestyle='', color='seagreen', capsize=5)
plt.plot(dus_riv_x, slope*dus_riv_x+intercept, color='black', alpha= 0.5)
plt.plot(dbt_riv_x, sslope*dbt_riv_x+sintercept, color='seagreen', alpha= 0.5)
plt.xlabel('13C IRMS')
plt.ylabel('DELTA14C')
plt.xlim(-2, 1)
plt.legend()
plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/Figure2.png', dpi=300, bbox_inches="tight")
plt.close()

"""
Now lets look closer at the deeper water...
"""
dus_oc = df.loc[(df['Sound'] == 'Dusky') & (df['River_Ocean'] == 'Ocean')]
dbt_oc = df.loc[(df['Sound'] == 'Doubtful') & (df['River_Ocean'] == 'Ocean')]

dbt_station = [1, 2, 3, 4]  # arranging in longirude order, not sampling order, more imp for Dusky
dus_station = [7, 5, 6, 9, 8]
size1 = 70

fig = plt.figure(figsize=(10, 10))

# Create a GridSpec with 3 rows and 2 columns
gs = gridspec.GridSpec(2, 2)
gs.update(wspace=.2, hspace=0.05)

# Add subplots to the GridSpec
ax3 = fig.add_subplot(gs[0, 0])
ax4 = fig.add_subplot(gs[0, 1])
ax1 = fig.add_subplot(gs[1, 0])
ax2 = fig.add_subplot(gs[1, 1])


for i in range(0, len(dbt_station)):
    site = dbt_oc.loc[dbt_oc['My Station Name'] == dbt_station[i]]
    ax1.errorbar(site['DELTA14C'], site['Depth'], xerr=site['DELTA14C_Error'], color=colors_dbt[i], marker=marks[i], label=f'{dbt_station[i]}', capsize=5)

    # Plotting map on ax3
    # dbt
    maxlat = -45.1
    minlat = -45.5
    nz_max_lon = 167.25
    nz_min_lon = 166.75

    map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h', ax=ax3)
    map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.1)
    map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.1)
    map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
    map.drawmapboundary(fill_color="#DDEEFF")
    map.drawcoastlines()

    lat = site['lat']
    lon = site['lon']
    x, y = map(lon, lat)
    ax3.scatter(x, y, label=f'{dbt_station[i]}', color=colors_dbt[i], s=size1, zorder=2, marker=marks[i])

for i in range(0, len(dus_station)):
    site = dus_oc.loc[dus_oc['My Station Name'] == dus_station[i]]
    ax2.errorbar(site['DELTA14C'], site['Depth'],  xerr=site['DELTA14C_Error'], color=colors_dus[i], marker=marks[i], label=f'{dus_station[i]}', capsize=5)

    # Plotting map on ax4
    # dbt
    maxlat = -45.5
    minlat = -45.9
    nz_max_lon = (166.3+.75)
    nz_min_lon = 166.3
    map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h', ax=ax4)
    map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.1)
    map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.1)
    map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
    map.drawmapboundary(fill_color="#DDEEFF")
    map.drawcoastlines()

    lat = site['lat']
    lon = site['lon']
    x, y = map(lon, lat)
    ax4.scatter(x, y, label=f'{dus_station[i]}', color=colors_dus[i], s=size1, zorder=2, marker=marks[i])


ax1.set_ylabel('Depth')
ax1.set_ylim(350, 0)
ax1.set_xlim(22, 36)
ax1.set_xlabel('\u0394$^1$$^4$C (\u2030)')
ax1.legend()

ax2.set_ylim(350, 0)
ax2.set_xlim(22, 36)
ax2.set_xlabel('\u0394$^1$$^4$C (\u2030)')
ax2.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/Figure3.png', dpi=300, bbox_inches="tight")
plt.close()
