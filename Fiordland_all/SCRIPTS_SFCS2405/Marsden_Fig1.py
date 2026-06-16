
import gsw
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import numpy as np
import cartopy.feature as cf
import matplotlib.gridspec as gridspec

sun = pd.read_excel(f'H:\Science\Datasets\Fiordland\RVSONNE\STEP3/Concatonated_CTD_SONNE.xlsx')
moy = pd.read_excel('H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4/mystations.xlsx')

# exclude top 5 m for now
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

# CTD profiles looked odd, want to make sure via map that they are indeed overlapping properly (the Sonne vs Polaris stns)
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import cartopy.feature as cf

fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 1])  # Adjust width ratios as needed

# First subplot: map with Cartopy
ax1 = plt.subplot(gs[0], projection=ccrs.PlateCarree())
ax1.set_extent((166.3, 168.25, -46.0, -44))
ax1.add_feature(cf.GSHHSFeature(scale="l"))

# Plot your map points
ax1.scatter(o1_sun['longitude'].iloc[0], o1_sun['latitude'].iloc[0], color='red', marker='o', label='O1 SONNE')
ax1.scatter(o1_moy['Lon'].iloc[0], o1_moy['Lat'].iloc[0], color='red', marker='o', label='O1 MOY')
ax1.scatter(o2_sun['longitude'].iloc[0], o2_sun['latitude'].iloc[0], color='blue', marker='x', label='O2 SONNE')
ax1.scatter(o2_moy['Lon'].iloc[0], o2_moy['Lat'].iloc[0], color='blue', marker='x', label='O2 MOY')
ax1.scatter(o3_sun['longitude'].iloc[0], o3_sun['latitude'].iloc[0], color='green', marker='D', label='O3 SONNE')
ax1.scatter(o3_moy['Lon'].iloc[0], o3_moy['Lat'].iloc[0], color='green', marker='D', label='O3 MOY')
ax1.legend()

# Second subplot: T-S diagram
ax2 = fig.add_subplot(gs[1])
sc = ax2.scatter(o1_moy['Sal00'], o1_moy['pt'], c=o1_moy['DepSM'], cmap='viridis')  # or 'plasma', 'coolwarm', etc.
ax2.scatter(o1_sun['sal00'], o1_sun['pt'], c=o1_sun['depSM'], cmap='viridis')  # or 'plasma', 'coolwarm', etc.
cbar = plt.colorbar(sc)
cbar.set_label('Depth (m)')

# Third subplot: Oxygen
ax3 = fig.add_subplot(gs[2])
ax3.plot(o1_sun['sbeox0MLL'], o1_sun['depSM'], label='Your Label', color='red')
ax3.plot(o1_moy['Sbeox0Mg/L'], o1_moy['DepSM'], label='Your Label', color='red', alpha=0.5)


# ax2.plot(salinity, temperature, ...)  # Replace with your real data
ax2.set_title("Temperature-Salinity")

# ax3.plot(depth, oxygen, ...)  # Replace with your real data
ax3.set_title("Oxygen Profile")

plt.tight_layout()
plt.savefig(f'H:\Science\Datasets\Fiordland\RVSONNE/example_fig.png', dpi=300, bbox_inches="tight")









"""
Things go wonky if you include top 5 m
"""
# quick test

o3_moy = o3_moy.loc[o3_moy['DepSM'] > 5]
o3_sun = o3_sun.loc[o3_sun['depSM'] > 5]

# sc = plt.scatter(o3_moy['Sal00'], o3_moy['pt'], c=o3_moy['DepSM'], cmap='viridis')  # or 'plasma', 'coolwarm', etc.
# sc2 = plt.scatter(o3_sun['sal00'], o3_sun['pt'], c=o3_sun['depSM'], cmap='viridis')  # or 'plasma', 'coolwarm', etc.

sc = plt.scatter(o3_moy['Sal00'], o3_moy['pt'])  # or 'plasma', 'coolwarm', etc.
sc2 = plt.scatter(o3_sun['sal00'], o3_sun['pt'])  # or 'plasma', 'coolwarm', etc.


plt.gca().invert_yaxis()  # optional: if plotting pt vs depth-like behavior

plt.xlabel('Salinity (Sal00)')
plt.ylabel('Potential Temperature (°C)')
plt.title('T-S Diagram Colored by Depth')

cbar = plt.colorbar(sc)
cbar.set_label('Depth (m)')
plt.savefig(f'H:\Science\Datasets\Fiordland\RVSONNE/o3_moy.png', dpi=300, bbox_inches="tight")





#
#
#
#
#
#
#
#
#
#
# import matplotlib.pyplot as plt
# import numpy as np
#
# # Create figure and axes
# fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 6), sharey=False)
#
# # Plot a) Temperature-Salinity diagram
# ax1.set_title("a)")
# ax1.set_xlabel("Salinity")
# ax1.set_ylabel("Potential Temperature [°C]")
# # ax1.set_xlim(33.5, 35.5)
# # ax1.set_ylim(5, 25)
#
# # Example contour lines (isopycnals placeholder)
# # for sigma in np.arange(23, 29, 1):
# #     ax1.plot(salinity, 1000 + 0 * salinity - sigma, 'k--', linewidth=0.5)  # Replace with actual isopycnals
# ax1.plot(interest1_sun['sal00'], interest1_sun['pt'], label='Your Label', color='red')
# ax1.plot(interest1_moy['Sal00'], interest1_moy['pt'], label='Your Label', color='red', alpha=0.5)
# ax1.plot(interest2_sun['sal00'], interest2_sun['pt'], label='Your Label', color='blue')
# ax1.plot(interest2_moy['Sal00'], interest2_moy['pt'], label='Your Label', color='blue', alpha=0.5)
# ax1.plot(interest3_sun['sal00'], interest3_sun['pt'], label='Your Label', color='green')
# ax1.plot(interest3_moy['Sal00'], interest3_moy['pt'], label='Your Label', color='green', alpha=0.5)
#
# # Plot b) Oxygen vs Depth
# ax2.set_title("b)")
# ax2.set_xlabel("Oxygen [μmol/kg]")
# ax2.set_ylabel("Depth [m]")
# # ax2.set_xlim(0, 300)
# ax2.set_ylim(250, 0)
# ax2.plot(interest1_sun['sbeox0MLL'], interest1_sun['depSM'], label='Your Label', color='red')
# ax2.plot(interest1_moy['Sbeox0Mg/L'], interest1_moy['DepSM'], label='Your Label', color='red', alpha=0.5)
# ax2.plot(interest2_sun['sbeox0MLL'], interest2_sun['depSM'], label='Your Label', color='blue')
# ax2.plot(interest2_moy['Sbeox0Mg/L'], interest2_moy['DepSM'], label='Your Label', color='blue', alpha=0.5)
# ax2.plot(interest3_sun['sbeox0MLL'], interest3_sun['depSM'], label='Your Label', color='green')
# ax2.plot(interest3_moy['Sbeox0Mg/L'], interest3_moy['DepSM'], label='Your Label', color='green', alpha=0.5)
#
# plt.tight_layout()
# plt.savefig(f'H:\Science\Datasets\Fiordland\RVSONNE/CTD_comparison_.png', dpi=300, bbox_inches="tight")
#
