"""
This script is primarily for exploring the new DIC data.
I'll have to make a final script for more polished figures later on, once we've determined what figures we're giong to keep in wherever we're
going with this stuff.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap
import warnings
warnings.simplefilter("ignore")

"""
Collate Final Data sheet by mergeing my sampling log with RLIMS OUTPUT! 
"""
# df = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/02_Results_and_Data/DATA_PROCESSING_RAW.xlsx', sheet_name='Cruise_Data_Sheet_ALL', comment='#')
# df = df[['My Station Name', 'Cruise Station Name','Latitude_N_decimal','Longitude_E_decimal','Bottom Depth (m)','Depth','Qflag','Sample','TP']]
# df = df.loc[df['Qflag'] != '.X.']
# dic = df.loc[((df['Sample'] == 'DIC') | (df['Sample'] == 'DIC Duplicate'))]
#
# tw3530 = pd.read_excel('H:/Science/Datasets/Fiordland/TW3530_export.xlsx')
# tw3530 = tw3530.loc[tw3530['Samples::Sample Description'] == 'Fiordland DIC samples from SFCS2405'] # remove oxalics, kapunis, etc
#
# df = dic.merge(tw3530, on='TP')
#
# df.to_excel('H:/Science/Current_Projects/03_CCE_24_25/02_Results_and_Data/Finalized_Results/DI14C_FINAL.xlsx')


"""
SPEND SOME LINES GETTING THE DATA READY FOR PLOTTING
CREATE SOME EXTRA LABELS AND SUBSETS FOR EACH FJORD
"""
df = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/02_Results_and_Data/Finalized_Results/DI14C_FINAL.xlsx', comment='#')
df = df.rename(columns={'Latitude_N_decimal': 'lat', 'Longitude_E_decimal': 'lon','Water Carbonate CO2 Evolution::TDIC':'tdic_processing'})
ctd = pd.read_excel('H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4\mystations.xlsx')

# I need to analyze these data, at least initally, as seperate "things" as 1) river water and 2) marine water
df['River_Ocean'] = 'Ocean' # set inital status to ocean
df.loc[(df['Depth'] == 1), 'River_Ocean'] = 'River'

df['Sound'] = 'Dusky'
ctd['Sound'] = 'Dusky' # set inital state to Dusky

dbt_station = [1, 2, 3, 4]  # Change these locations to Sound = Doubtful
dus_station = [7, 6, 5, 9, 8]

df.loc[(df['My Station Name'].isin(dbt_station)), 'Sound'] = 'Doubtful'
ctd.loc[(ctd['My Station Name'].isin(dbt_station)), 'Sound'] = 'Doubtful'

doubt_df = df.loc[df['Sound'] == 'Doubtful']
dusky_df = df.loc[df['Sound'] == 'Dusky']

doubt_ctd = ctd.loc[ctd['Sound'] == 'Doubtful']
dusky_ctd = ctd.loc[ctd['Sound'] == 'Dusky']


# SET UP SOME THINGS FOR THE FIGURES...
# set initial figure settings
mako = sns.color_palette("mako", 6)
colors_dbt = ['SeaGreen','Teal','deepskyblue','Blue']
colors_dus = ['SeaGreen','Teal','Sienna','deepskyblue','Blue']
marks = ['o','D','^','s','X']

#
sports = dusky_ctd.loc[dusky_ctd['My Station Name'] == 5] # spotsman's cove
print(sports.columns)

fig, ax1 = plt.subplots()
plt.title('Sportmans Cove CTD')
# Plot salinity with its x-axis
ax1.plot(sports['Sal00'], sports['DepSM'], 'b-', label='Salinity')
ax1.set_xlabel('Salinity (Sal00)', color='b')
ax1.set_ylabel('Depth')
ax1.set_ylim(40,0)

ax2 = ax1.twiny()
sports['Sbeox0_umol/kg'] = sports['Sbeox0Mg/L']*(1000/32)


ax2.plot(sports['Sbeox0_umol/kg'], sports['DepSM'], 'r-', label='Salinity')
ax2.set_xlabel('Dissolved Oxygen (umol/kg)', color='r')

plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/SportmansCoveCTD.png", dpi=300, bbox_inches="tight")
plt.close()

# print(sports)

# """
# CTD_SUPPLEMENTARY
# """
#
# fig = plt.figure(figsize=(12, 8))
# gs = gridspec.GridSpec(3, 2)
# gs.update(wspace=0.1, hspace=0)
#
# # plot structure
# xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# for i in range(0, len(dbt_station)):
#     stn_df = doubt_df.loc[doubt_df['My Station Name'] == dbt_station[i]]
#     stn_ctd = doubt_ctd.loc[doubt_ctd['My Station Name'] == dbt_station[i]]
#     plt.plot(stn_ctd['Sbeox0Mg/L'], stn_ctd['DepSM'], color=colors_dbt[i])
#     plt.scatter(stn_df['Sbeox0Mg/L'], stn_df['DepSM'], color=colors_dbt[i], s=100, label=f"{dbt_station[i]}", marker=marks[i])
# plt.title('Doubtful Sound')
# plt.ylim(50,0)
# plt.legend()
# plt.xticks([])
# xtr_subsplot = fig.add_subplot(gs[1:3, 0:1])
# for i in range(0, len(dbt_station)):
#     stn_df = doubt_df.loc[doubt_df['My Station Name'] == dbt_station[i]]
#     stn_ctd = doubt_ctd.loc[doubt_ctd['My Station Name'] == dbt_station[i]]
#     plt.plot(stn_ctd['Sbeox0Mg/L'], stn_ctd['DepSM'], color=colors_dbt[i])
#     plt.scatter(stn_df['Sbeox0Mg/L'], stn_df['DepSM'], color=colors_dbt[i], s=100, label=f"{dbt_station[i]}", marker=marks[i])
# plt.ylim(400,50)
# plt.ylabel('Depth (m)')
# plt.xlabel('Sbeox0Mg/L')
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# for i in range(0, len(dus_station)):
#     stn_df = dusky_df.loc[dusky_df['My Station Name'] == dus_station[i]]
#     stn_ctd = dusky_ctd.loc[dusky_ctd['My Station Name'] == dus_station[i]]
#     plt.plot(stn_ctd['Sbeox0Mg/L'], stn_ctd['DepSM'], color=colors_dus[i])
#     plt.scatter(stn_df['Sbeox0Mg/L'], stn_df['DepSM'], color=colors_dus[i], s=100, label=f"{dus_station[i]}", marker=marks[i])
# plt.title('Dusky Sound')
# plt.ylim(50,0)
# plt.legend()
# plt.xticks([])
# xtr_subsplot = fig.add_subplot(gs[1:3, 1:2])
# for i in range(0, len(dbt_station)):
#     stn_df = dusky_df.loc[dusky_df['My Station Name'] == dus_station[i]]
#     stn_ctd = dusky_ctd.loc[dusky_ctd['My Station Name'] == dus_station[i]]
#     plt.plot(stn_ctd['Sbeox0Mg/L'], stn_ctd['DepSM'], color=colors_dus[i])
#     plt.scatter(stn_df['Sbeox0Mg/L'], stn_df['DepSM'], color=colors_dus[i], s=100, label=f"{dus_station[i]}", marker=marks[i])
# plt.ylim(400,50)
# plt.xlabel('Sbeox0Mg/L')
#
# plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/CTD.png", dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# Surface_DIC_vs_Longitude
# """
#
# # LSL
# dus_riv = df.loc[(df['Sound'] == 'Dusky') & (df['River_Ocean'] == 'River')]
# dbt_riv = df.loc[(df['Sound'] == 'Doubtful') & (df['River_Ocean'] == 'River')]
# # Subsurface
# dus_oc = df.loc[(df['Sound'] == 'Dusky') & (df['River_Ocean'] == 'Ocean')]
# dbt_oc = df.loc[(df['Sound'] == 'Doubtful') & (df['River_Ocean'] == 'Ocean')]
#
# # Regression of surface data
# dus_riv_x = dus_riv['lon']
# dus_riv_x = np.array(dus_riv_x)
# dus_riv_y = dus_riv['DELTA14C']
# dus_riv_y = np.array(dus_riv_y)
# #
# dbt_riv_x = dbt_riv['lon']
# dbt_riv_x = np.array(dbt_riv_x)
# dbt_riv_y = dbt_riv['DELTA14C']
# dbt_riv_y = np.array(dbt_riv_y)
#
# # regress the data
# slope, intercept, rvalue, pvalue, stderr = stats.linregress(dus_riv_x, dus_riv_y)
# print("Dusky Surface: y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2))
#
# sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(dbt_riv_x, dbt_riv_y)
# print("Doubtful Surface: y=%.3fx+%.3f\R$^2$=%.3f"%(sslope, sintercept,srvalue**2))
#
# fig = plt.figure()
# plt.errorbar(dus_riv['lon'], dus_riv['DELTA14C'], yerr=dus_riv['DELTA14C_Error'], label='Dusky', marker='o', linestyle='', color='black', capsize=5)
# plt.errorbar(dbt_riv['lon'], dbt_riv['DELTA14C'], yerr=dbt_riv['DELTA14C_Error'], label='Doubtful', marker='D', linestyle='', color='seagreen', capsize=5)
# plt.plot(dus_riv_x, slope*dus_riv_x+intercept, color='black', alpha= 0.5) # ONLY PLOT TRENDLINES FOR lon
# plt.plot(dbt_riv_x, sslope*dbt_riv_x+sintercept, color='seagreen', alpha= 0.5)
# plt.xlabel('Longitude (E)')
# plt.legend()
# plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
# plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/Surface_DIC_vs_Longitude.png", dpi=300, bbox_inches="tight")
# plt.close()
#
"""
Now lets look closer at the deeper water...
"""
dus_oc = df.loc[(df['Sound'] == 'Dusky') & (df['River_Ocean'] == 'Ocean')]
dbt_oc = df.loc[(df['Sound'] == 'Doubtful') & (df['River_Ocean'] == 'Ocean')]

fig = plt.figure(figsize=(10, 10))

# Create a GridSpec with 3 rows and 2 columns
gs = gridspec.GridSpec(2, 2)
gs.update(wspace=.2, hspace=0.05)

# Add subplots to the GridSpec
ax3 = fig.add_subplot(gs[0, 0])
ax4 = fig.add_subplot(gs[0, 1])
ax1 = fig.add_subplot(gs[1, 0])
ax2 = fig.add_subplot(gs[1, 1])
# ax5 = fig.add_subplot(gs[2, 0])
# ax6 = fig.add_subplot(gs[2, 1])

for i in range(0, len(dbt_station)):
    site = dbt_oc.loc[dbt_oc['My Station Name'] == dbt_station[i]]
    # if dbt_station[i] != 3:
    #     ax1.errorbar(site['DELTA14C'], site['Depth'], xerr=site['DELTA14C_Error'], color=colors_dbt[i], marker=marks[i], label=f'{dbt_station[i]}', capsize=5)
    # else:
    #     tiefighter=1
    # ax5.errorbar(site['DELTA14C'], site['Sbeox0Mg/L'], xerr=site['DELTA14C_Error'], color=colors_dbt[i], marker=marks[i], label=f'{dbt_station[i]}', capsize=5)

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
    ax3.scatter(x, y, label=f'{dbt_station[i]}', color=colors_dbt[i], s=60, zorder=2, marker=marks[i])

for i in range(0, len(dus_station)):
    site = dus_oc.loc[dus_oc['My Station Name'] == dus_station[i]]
    ax2.errorbar(site['DELTA14C'], site['Depth'],  xerr=site['DELTA14C_Error'], color=colors_dus[i], marker=marks[i], label=f'{dus_station[i]}', capsize=5)
    # ax6.errorbar(site['DELTA14C'], site['Sbeox0Mg/L'], xerr=site['DELTA14C_Error'], color=colors_dus[i], marker=marks[i], label=f'{dus_station[i]}', capsize=5)

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
    ax4.scatter(x, y, label=f'{dus_station[i]}', color=colors_dus[i], s=60, zorder=2, marker=marks[i])

ax1.set_ylabel('Depth (m)')
ax1.set_xlabel('\u0394$^1$$^4$C (\u2030)')
ax2.set_xlabel('\u0394$^1$$^4$C (\u2030)')
ax1.set_ylim(400,0)
ax2.set_ylim(300,0)
ax1.legend()
ax2.legend()

plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/Subsurface_nostn3.png", dpi=300, bbox_inches="tight")
plt.close()
#
#
# """
# Simpler way of seeing oxygen
# """
#
# fig = plt.figure(figsize=(12,8))
# gs = gridspec.GridSpec(1, 2)
# gs.update(wspace=0.1, hspace=0.2)
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# plt.scatter(doubt_df['Sbeox0Mg/L'], doubt_df['DELTA14C'], c=doubt_df['Depth'], label='Doubtful Sound', marker='s')
# plt.xlabel('Oxygen')
# plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# plt.scatter(dusky_df['Sbeox0Mg/L'], dusky_df['DELTA14C'], c=dusky_df['Depth'],  label='Dusky Sound', marker='o')
# plt.xlabel('Oxygen')
# plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
# plt.legend()
# plt.colorbar()
# plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/DO.png", dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# Simpler way of seeing oxygen
# """
#
# fig = plt.figure(figsize=(8,4))
# gs = gridspec.GridSpec(1, 2)
# gs.update(wspace=0.3, hspace=0.2)
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# plt.scatter(doubt_df['delta13C_IRMS'], doubt_df['DELTA14C'], c=doubt_df['Sbeox0Mg/L'], label='Doubtful Sound', marker='s')
# plt.xlabel('delta13C_IRMS')
# plt.title('Doubtful Sound')
# plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# plt.scatter(dusky_df['delta13C_IRMS'], dusky_df['DELTA14C'], c=dusky_df['Sbeox0Mg/L'],  label='Dusky Sound', marker='o')
# plt.xlabel('delta13C_IRMS')
# plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
# plt.title('Dusky Sound')
# plt.colorbar()
# plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/13_14_DO.png", dpi=300, bbox_inches="tight")
# plt.close()
#
#
# """
# Simpler way of seeing oxygen
# """
#
# fig = plt.figure(figsize=(8,4))
# gs = gridspec.GridSpec(1, 2)
# gs.update(wspace=0.3, hspace=0.2)
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# plt.scatter(doubt_df['delta13C_IRMS'], doubt_df['Sbeox0Mg/L'], c=doubt_df['DELTA14C'], label='Doubtful Sound', marker='s')
# plt.xlabel('delta13C_IRMS')
# plt.title('Doubtful Sound')
# plt.xlim(-2, 1)
# plt.ylim(0, 9)
# plt.ylabel('Sbeox0Mg/L')  # label the y axis
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# plt.scatter(dusky_df['delta13C_IRMS'], dusky_df['Sbeox0Mg/L'], c=dusky_df['DELTA14C'],  label='Dusky Sound', marker='o')
# plt.xlabel('delta13C_IRMS')
# plt.ylabel('Sbeox0Mg/L')  # label the y axis
# plt.title('Dusky Sound')
# plt.colorbar()
# plt.xlim(-2, 1)
# plt.ylim(0, 9)
# plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/DO_13_14.png", dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# Simpler way of seeing oxygen
# """
#
# fig = plt.figure(figsize=(8,4))
# gs = gridspec.GridSpec(1, 2)
# gs.update(wspace=0.3, hspace=0.25)
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# plt.scatter(doubt_df['delta13C_IRMS'], doubt_df['Sbeox0Mg/L'], c=doubt_df['Sal00'], label='Doubtful Sound', marker='s')
# plt.xlabel('delta13C_IRMS')
# plt.title('Doubtful Sound')
# plt.ylabel('Sbeox0Mg/L')  # label the y axis
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# plt.scatter(dusky_df['delta13C_IRMS'], dusky_df['Sbeox0Mg/L'], c=dusky_df['Sal00'],  label='Dusky Sound', marker='o')
# plt.xlabel('delta13C_IRMS')
# plt.ylabel('Sbeox0Mg/L')  # label the y axis
# plt.title('Dusky Sound')
# plt.colorbar()
# plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/DO_13_SAL.png", dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# """
#
# fig = plt.figure(figsize=(8,4))
# gs = gridspec.GridSpec(1, 2)
# gs.update(wspace=0.3, hspace=0.25)
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# plt.scatter(doubt_df['delta13C_IRMS'], doubt_df['Sbeox0Mg/L'], c=doubt_df['Depth'], label='Doubtful Sound', marker='s')
# plt.xlabel('delta13C_IRMS')
# plt.title('Doubtful Sound')
# plt.ylabel('Sbeox0Mg/L')  # label the y axis
# plt.xlim(-2, 1)
# plt.ylim(0, 9)
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# plt.scatter(dusky_df['delta13C_IRMS'], dusky_df['Sbeox0Mg/L'], c=dusky_df['Depth'],  label='Dusky Sound', marker='o')
# plt.xlabel('delta13C_IRMS')
# plt.ylabel('Sbeox0Mg/L')  # label the y axis
# plt.title('Dusky Sound')
# plt.colorbar()
# plt.xlim(-2, 1)
# plt.ylim(0, 9)
# plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Basic_Figures/DO_13_Depth.png", dpi=300, bbox_inches="tight")
# plt.close()
