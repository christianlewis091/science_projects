import gsw
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import numpy as np
import cartopy.feature as cf
import matplotlib.gridspec as gridspec

# READ IN CTD DATA.
# HOW WAS THIS CTD DATA PREPARED? See C:\Users\clewis\IdeaProjects\GNS\Fiordland_all\SCRIPTS_SFCS2405/SFCS2405 CTD dataworkup.py
# AND See C:\Users\clewis\IdeaProjects\GNS\Fiordland_all\SCRIPTS_SFCS2405/RV_Sonne_S309.py
# before serious data analysis, make sure the codes are cleaned and in ONE SPOT! This fast and furious is for Fiordland catch up tmrw.
sun = pd.read_excel(f'H:\Science\Datasets\Fiordland\RVSONNE\STEP3/Concatonated_CTD_SONNE.xlsx')
moy = pd.read_excel('H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4/mystations.xlsx')

# exclude top 5 m for now because things get wonky see later
moy = moy.loc[moy['DepSM'] > 5]
sun = sun.loc[sun['depSM'] > 5]

# calculate potential temp for TS plot
sun['pt'] = gsw.conversions.pt_from_t(sun['sal00'],sun['t090C'], sun['depSM'],0)
moy['pt'] = gsw.conversions.pt_from_t(moy['Sal00'],moy['T090C'], moy['DepSM'],0)

o1_sun = sun.loc[sun['FileName'] == 'SO309-59-13_by_depth_1_m']
o2_sun = sun.loc[sun['FileName'] == 'SO309-53-1_by_depth_1_m']
o3_sun = sun.loc[sun['FileName'] == 'SO309-46-17_by_depth_1_m']
o1_moy = moy.loc[moy['FileName'] == 'DUS023_01CTD']
o2_moy = moy.loc[moy['FileName'] == 'DBT008_01CTD']
o3_moy = moy.loc[moy['FileName'] == 'DBT006_01CTD']


"""
COMPARE THE CTD CASTS IN A MONSTER FIG
"""
fig = plt.figure(figsize=(12, 12))
gs = gridspec.GridSpec(3, 3, width_ratios=[1, 1, 1])  # Adjust width ratios as needed

# First subplot: map with Cartopy
ax1 = plt.subplot(gs[0], projection=ccrs.PlateCarree())
ax1.set_extent((166.14, 167.89, -46.35, -44.31))
ax1.coastlines(resolution='10m',)


# grab data to pull from draw_maps.py to plot all sites, not just highlighted ones
df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/data/raw/Sampling_Log.xlsx')
sonne = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw/14C_samples_for_Christian_Lewis_GNS.xlsx', comment = '#')

# extract lat lons for Sonne and SFCS2405 cruises
lat = df['Latitude_N_decimal'].values
lon = df['Longitude_E_decimal'].values
lat_s = sonne['Lat_corrected'].values
lon_s = sonne['Lon'].values
#
# ax1.scatter(lon, lat, transform=ccrs.PlateCarree(), label='SFCS2405')  # Data is in lat/lon format)
# ax1.scatter(lon_s, lat_s, transform=ccrs.PlateCarree(), label='S309', color='red')  # Data is in lat/lon format)

# Plot your map points
ax1.scatter(o1_sun['longitude'].iloc[0], o1_sun['latitude'].iloc[0], color='red', marker='o', label='O1 SONNE')
ax1.scatter(o1_moy['Lon'].iloc[0], o1_moy['Lat'].iloc[0], color='red', marker='o', label='O1 MOY')
ax1.scatter(o2_sun['longitude'].iloc[0], o2_sun['latitude'].iloc[0], color='blue', marker='x', label='O2 SONNE')
ax1.scatter(o2_moy['Lon'].iloc[0], o2_moy['Lat'].iloc[0], color='blue', marker='x', label='O2 MOY')
ax1.scatter(o3_sun['longitude'].iloc[0], o3_sun['latitude'].iloc[0], color='green', marker='D', label='O3 SONNE')
ax1.scatter(o3_moy['Lon'].iloc[0], o3_moy['Lat'].iloc[0], color='green', marker='D', label='O3 MOY')
ax1.legend()

cmoy = 'blue'
cson = 'red'
# Second subplot: T-S diagram:
# TODO needs isopycnals
ax2 = fig.add_subplot(gs[1])
ax2.scatter(o1_moy['Sal00'], o1_moy['pt'], color=cmoy, label='SFCS2405')  # or 'plasma', 'coolwarm', etc.
ax2.scatter(o1_sun['sal00'], o1_sun['pt'], color=cson, label='S309')

# Third subplot: Oxygen
ax3 = fig.add_subplot(gs[2])
ax3.plot(o1_moy['Sbeox0Mg/L'], o1_moy['DepSM'],  color=cmoy)
ax3.plot(o1_sun['sbeox0MLL'], o1_sun['depSM'],color=cson)

# LEAVE OUT
# ax4 = fig.add_subplot(gs[3])

ax5 = fig.add_subplot(gs[4])
ax5.scatter(o2_moy['Sal00'], o2_moy['pt'], color=cmoy)  # or 'plasma', 'coolwarm', etc.
ax5.scatter(o2_sun['sal00'], o2_sun['pt'], color=cson)

ax6 = fig.add_subplot(gs[5])
ax6.plot(o2_moy['Sbeox0Mg/L'], o2_moy['DepSM'], color=cmoy)
ax6.plot(o2_sun['sbeox0MLL'], o2_sun['depSM'],  color=cson)


# ax7 = fig.add_subplot(gs[6])
ax8 = fig.add_subplot(gs[7])
ax8.scatter(o3_moy['Sal00'], o3_moy['pt'], color=cmoy)  # or 'plasma', 'coolwarm', etc.
ax8.scatter(o3_sun['sal00'], o3_sun['pt'], color=cson)

ax9 = fig.add_subplot(gs[8])
ax9.plot(o3_moy['Sbeox0Mg/L'], o3_moy['DepSM'], color=cmoy)
ax9.plot(o3_sun['sbeox0MLL'], o3_sun['depSM'],  color=cson)

ax9.set_ylim(350,0)

# ax2.plot(salinity, temperature, ...)  # Replace with your real data
ax2.set_title("Temperature vs. Salinity")
ax3.set_title("Dissolved Oxygen")

ax2.set_ylabel('Potential Temperature')
ax5.set_ylabel('Potential Temperature')
ax8.set_ylabel('Potential Temperature')

ax8.set_xlabel('Sal00')
ax9.set_xlabel('Dissolved OXygen Mg/L')

ax3.set_ylabel('dbar')
ax6.set_ylabel('dbar')
ax9.set_ylabel('dbar')

# SET O2 plot parametesr
ax3.set_ylim(200,0)
ax6.set_ylim(200,0)
ax9.set_ylim(200,0)

ax3.set_xlim(4,8)
ax6.set_xlim(4,8)
ax9.set_xlim(4,8)

# SET O2 plot parametesr
ax2.set_ylim(12,17)
ax5.set_ylim(12,17)
ax8.set_ylim(12,17)

ax2.set_xlim(33,36)
ax5.set_xlim(33,36)
ax8.set_xlim(33,36)

plt.tight_layout()
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/CTD_comparison_wes_color.png', dpi=300, bbox_inches="tight")
plt.show()


# # Second subplot: T-S diagram:
# # TODO needs isopycnals
# ax2 = fig.add_subplot(gs[1])
# ax2.scatter(o1_moy['Sal00'], o1_moy['pt'], c=o1_moy['DepSM'], cmap='viridis')  # or 'plasma', 'coolwarm', etc.
# ax2.scatter(o1_sun['sal00'], o1_sun['pt'], c=o1_sun['depSM'], cmap='viridis')  # or 'plasma', 'coolwarm', etc.
# cbar = plt.colorbar(sc)
# cbar.set_label('Depth (m)')