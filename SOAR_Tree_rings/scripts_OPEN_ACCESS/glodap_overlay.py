"""
22-09-2023
From my last meeting with Erik and Sara, we saw that Campbell island's HYSPLIT back-trajectory goes into the
most southerly region of the polar front. We asked, can we quantify/qualify this a little bit better?
To do so, I can overlay GLODAP data on top of the ORSI 1995 fronts, and I can overlay the 14C data, to compare upwellings

Luckily, I had already been working on a compilation of GLODAP and GO-SHIP data for my '14C-Water Mass Project',
so I already have a file of the webscraped data from the python file called "water_mass_dataset_creator.py".

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# EXTRACT THE DATA FROM THE EXCEL SHEETS
# df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_20rows.xlsx')
df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')

# ACC FRONT DATA
acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')

# CREATE THE MAP
m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
m.drawcoastlines()
m.shadedrelief()


"""
PLOT HYDROGRAPHIC DATA
"""
# Extract latitude, longitude, and NITRATE columns from HYDROGRAPHIC DATA

df = df.loc[df['NITRAT'] > -990]
latitudes = df['LATITUDE']
longitudes = df['LONGITUDE']
sst_values = df['NITRAT']  # SST values (sea surface temperature)
# Convert latitudes and longitudes to map coordinates
x, y = m(longitudes.values, latitudes.values)
# Plot the SST data as scatter points, color-coded by temperature
m.scatter(x, y, c=sst_values, cmap='coolwarm', s=50, edgecolor='k', linewidth=0.5)
cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)
cbar.set_label('Nitrate')

"""
PLOT THE FRONTS
"""
fronts = np.unique(acc_fronts['front_name'])
fronts = ['PF','SAF','STF','Boundary']
line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']

for i in range(0, len(fronts)):
    this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
    latitudes = this_one['latitude']
    longitudes = this_one['longitude']
    x, y = m(longitudes.values, latitudes.values)
    m.plot(x, y, color='black', label=f'{fronts[i]}', linestyle=line_sys[i])

plt.show()






# fronts = np.unique(acc_fronts['front_name'])
# fronts = ['PF','SAF','STF','Boundary']
#
#
#
#
#
#
#
#
# # EXTRACT DATA FOR FRONTS
# pf = acc_fronts.loc[acc_fronts['front_name'] == 'PF']
# saf = acc_fronts.loc[acc_fronts['front_name'] == 'SAF']
# stf = acc_fronts.loc[acc_fronts['front_name'] == 'STF']
# boundary = acc_fronts.loc[acc_fronts['front_name'] == 'Boundary']
#
#
#
# # CREATE THE MAP
# m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
#
# # Convert latitudes and longitudes to map coordinates
# x, y = m(longitudes.values, latitudes.values)
#
# # Plot the SST data as scatter points, color-coded by temperature
# plt.figure(figsize=(10, 10))
# m.scatter(x, y, c=sst_values, cmap='coolwarm', s=50, edgecolor='k', linewidth=0.5)
#
# # Add coastlines and a colorbar
# m.drawcoastlines()
# cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)
# cbar.set_label('SST (°C)')
#
# # Set a title for the plot
# plt.title('Sea Surface Temperature (SST) Map')
#
# # Show the plot or save it to a file
# plt.show()
#
#



#
# """
# COPIED AND PASTED THE MAP FROM THE BOTTOM OF MAIN_ANALYSIS.PY
# THE BELOW CODE WORKS. I'm going to test plotting the glodap data above and then bring it into the plot below
# """
#
# #
# # LOAD HYSPLOT DATA
# easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/easy_access2 - Copy.xlsx')
# acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
# fronts = np.unique(acc_fronts['front_name'])
# fronts = ['PF','SAF','STF','Boundary']
#
# # FIND THE MEAN OF THE TRAJECTORIES FOR EACH SITE, OVER TIME.
# means_dataframe_100_1 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2005_2006.xlsx')
# means_dataframe_100_2 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2010_2011.xlsx')
# means_dataframe_100_3 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2015_2016.xlsx')
# means_dataframe_100_4 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2020_2021.xlsx')
#
# means_dataframe_100 = pd.concat([means_dataframe_100_1, means_dataframe_100_2, means_dataframe_100_3, means_dataframe_100_4])
# codenames = np.unique(means_dataframe_100['Codename'])
# time_integrated_means = pd.DataFrame()
# for i in range(0,len(codenames)):
#
#     # LOCATE FIRST SITE
#     site1 = means_dataframe_100.loc[means_dataframe_100['Codename'] == codenames[i]]
#     means1 = site1.groupby('timestep', as_index=False).mean()
#     means1['Codename'] = codenames[i]
#
#     time_integrated_means = pd.concat([time_integrated_means, means1]).reset_index(drop=True)
#
# # ADDING PROPER SITE NAMES FOR THE FOLLOWING LOOP TO READ
# time_integrated_means = time_integrated_means.merge(easy_access)
#
# # SEE hysplit_make_plots_GNS.py
# timemin = -(6*24)
# time_integrated_means = time_integrated_means.loc[time_integrated_means['timestep'] > timemin]
# # fronts = ['PF','SAF','STF']
#
# """
# BEGIN PLOTTING THE FIGURE
# """
#
# line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
#
# # LOOP THROUGH FIGURES STYLES
#
# fig = plt.figure(figsize=(16, 16))
# map = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
# map.drawcoastlines(linewidth=0.1)
#
# map.shadedrelief()
# map.drawmapboundary(fill_color='#A6CAE0')
# map.fillcontinents(color='#69b2a2',lake_color='#A6CAE0')
#
#     # PLOTTING THE ACC FRONTS
# pf = acc_fronts.loc[acc_fronts['front_name'] == 'PF']
# saf = acc_fronts.loc[acc_fronts['front_name'] == 'SAF']
# stf = acc_fronts.loc[acc_fronts['front_name'] == 'STF']
# boundary = acc_fronts.loc[acc_fronts['front_name'] == 'Boundary']
#
# pflat = pf['latitude']
# pflon = pf['longitude']
# lat1, lon1 = map(pflon, pflat)
#
# stflat = stf['latitude']
# stflon = stf['longitude']
# lat2, lon2 = map(stflon, stflat)
#
# for i in range(0, len(fronts)):
#     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#
#     lat = this_one['latitude']
#     lon = this_one['longitude']
#     z, a = map(list(lon), list(lat))
#
#     map.plot(z, a, color='black', label=f'{fronts[i]}', linestyle=line_sys[i])
#     plt.legend(bbox_to_anchor=(1.1, 1.05))
#
#     # PLOTTING CHILEAN SITES
# for i in range(0, len(locs1)):
#     slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
#     lat = slice['NewLat']
#     lat = lat[0]
#     lon = slice['new_Lon']
#     lon = lon[0]
#     x, y = map(lon, lat)
#     map.scatter(x, y, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')
#     print(locs1[i])
#
#     site_mean_100 = time_integrated_means.loc[time_integrated_means['Site'] == str(locs1[i])].reset_index(drop=True)
#     chile_lat = site_mean_100['y']
#     chile_lon = site_mean_100['x']
#     print(type(chile_lon))
#     z, a = map(list(chile_lon), list(chile_lat))
#
#     map.plot(z, a, color=colors[i])
#
#     # PLOTTING NZ SITES
# for i in range(0, len(locs2)):
#
#     slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
#     lat = slice['NewLat']
#     lat = lat[0]
#     lon = slice['NewLon']
#     lon = lon[0]
#     x, y = map(lon, lat)
#     # print(x, y)
#     map.scatter(x, y, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')
#
#     site_mean_100 = time_integrated_means.loc[time_integrated_means['Site'] == str(locs2[i])].reset_index(drop=True)
#     chile_lat = site_mean_100['y']
#     chile_lon = site_mean_100['x']
#     print(type(chile_lon))
#     z, a = map(list(chile_lon), list(chile_lat))
#     map.plot(z, a, color=colors[i])
#
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/glodap_overlay/test.png',
#             dpi=300, bbox_inches="tight")
# plt.close()