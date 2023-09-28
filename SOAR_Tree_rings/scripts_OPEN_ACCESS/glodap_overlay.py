"""
28-09-23
We previously made a cool map showing the differences in 14C and nitrate along the different fronts.
Lets try to quantify it a little bit more. To do this, I'm going to comment out the section that makes the map until later,
to speed up the code.

22-09-2023
From my last meeting with Erik and Sara, we saw that Campbell island's HYSPLIT back-trajectory goes into the
most southerly region of the polar front. We asked, can we quantify/qualify this a little bit better?
To do so, I can overlay GLODAP data on top of the ORSI 1995 fronts, and I can overlay the 14C data, to compare upwellings

Luckily, I had already been working on a compilation of GLODAP and GO-SHIP data for my '14C-Water Mass Project',
so I already have a file of the webscraped data from the python file called "water_mass_dataset_creator.py".

In the first subplot, I want to plot nitrate to show upwelling, so I've created a dataset called _ALLDATA where I have not
filtered for only those which contain 14C.

I WILL filter for only those that contain 14C for the second subplot.

The third will be hyplsit data
"""

"""
QUANTIFICATION SECTION
"""

import pandas as pd
import numpy as np
from X_miller_curve_algorithm import ccgFilter
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.gridspec as gridspec
from X_my_functions import monte_carlo_randomization_trend
# from main_analysis import *

# df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_ALLDATA100m.xlsx')
# acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
#
# """
# I'll need to smooth the acc fronts to the lat/lons where there is data in order to do the differeceing.
# """
# # the smoothing will output latitude data wherever it sees longitude data on X
# datas = pd.DataFrame({'x': df['LONGITUDE'], 'y': df['LONGITUDE']}).sort_values(by=['x'], ascending=True).reset_index(drop=True)
#
# n = 3 # set the amount of times the code will iterate (set to 10,000 once everything is final)
# cutoff = 667  # FFT filter cutoff
#
# # Do this for each front
# fronts = np.unique(acc_fronts['front_name'])
# fronts = ['PF','SAF','STF','Boundary']
# line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
#
# #
# # m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
# # m.drawcoastlines()
# # m.shadedrelief()
#
# # create a smoothed front
# for i in range(0, len(fronts)):
#     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#     latitudes = this_one['latitude'].reset_index(drop=True)
#     longitudes = this_one['longitude'].reset_index(drop=True)
#     yerr = latitudes*.01
#
#     #dynamically name a variable
#     smoothed = ccgFilter(longitudes, latitudes, cutoff).getSmoothValue(datas['x'])
#     df[f'{fronts[i]}+smoothed'] = smoothed

    # test it by showing in a plot / works so i'm removing this
#     x, y = m(datas['x'], smoothed)
#     m.plot(x, y, color='black', label=f'{fronts[i]}', linestyle=line_sys[i])
# plt.legend()
# plt.show()
# print(df.columns)
# df.to_excel(r'H:\Science\Datasets\Hydrographic\test.xlsx')
# df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\test.xlsx')
#
# # subset data so that I only see data where the latitude of the pont is lower than STF
# df = df.loc[(df['LATITUDE'] <= df['STF+smoothed']) & (df['LATITUDE'] >= df['Boundary+smoothed'])]
# # columns_to_dropna = ['Boundary+smoothed', 'PF+smoothed','SAF+smoothed','STF+smoothed']
# # df = df.dropna(subset=columns_to_dropna, inplace=True)
# print(len(df))
# # loop through the DF and assign a "SURFACE FRONT" to each point based on its lat and lon...
# result_array = []
# for j in range(0, len(df)):
#     row = df.iloc[j]
#     print(row['LATITUDE'])
#     print(row['Boundary+smoothed'])
#     print(row['PF+smoothed'])
#     print(row['SAF+smoothed'])
#     print(row['STF+smoothed'])
#
#     # assign label based on latitude
#     if (row['LATITUDE'] >= row['Boundary+smoothed']) & (row['LATITUDE'] <= row['PF+smoothed']):
#         res = 'Zone1'
#     elif (row['LATITUDE'] >= row['PF+smoothed']) & (row['LATITUDE'] <= row['SAF+smoothed']):
#         res = 'Zone2'
#     elif (row['LATITUDE'] >= row['SAF+smoothed']) & (row['LATITUDE'] <= row['STF+smoothed']):
#         res = 'Zone3'
#     else:
#         res = 'Error'
#     result_array.append(res)
#
# df['CBL_zones'] = result_array
#
# df.to_excel(r'H:\Science\Datasets\Hydrographic\cbl_zones.xlsx')
df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\cbl_zones.xlsx')
df = df.loc[df['DELC14'] > -990]

results = pd.DataFrame()
zones = ['Zone1', 'Zone2','Zone3']
mean14C = []
std14C = []
meannit = []
stdnit = []
zone = []
for i in range(0, len(zones)):
    df1 = df.loc[df['CBL_zones'] == zones[i]]
    mean14C.append(np.mean(df1['DELC14']))
    std14C.append(np.std(df1['DELC14']))
    meannit.append(np.mean(df1['NITRAT']))
    stdnit.append(np.std(df1['NITRAT']))
    zone.append(zones[i])

results = pd.DataFrame({"zone": zone, "mean_14C": mean14C, "std14C":std14C, "mean_nitrate": meannit, "stdnitrate":stdnit})

plt.scatter(results['zone'], results['mean_14C'])
plt.scatter(results['zone'], results['mean_nitrate'])
plt.show()



















# """
# FIGURE SECTION
# """
#
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
# import matplotlib.gridspec as gridspec
# # from main_analysis import *
#
# # READ IN THE _ALLDATA FILE
# # df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_ALLDATA.xlsx')
# df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_ALLDATA100m.xlsx')
# print('ive loaded the data')
# # FILTER TO ONLY GRAB SURFACE SAMPLES
# df = df.loc[df['CTDPRS'] < 100] # ONLY GRAB SURFACE SAMPLES
#
# # WRITE TO A NEW FILE FOR FASTER PRODUCTION OF THIS CODE (insert to above later)
# # df.to_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_ALLDATA100m.xlsx')
#
# # CREATE SUBSETS OF DATA FOR SUBPLOTS 1, 2, and 3
# df_sub1 = df.loc[df['NITRAT'] > -990]
# df_sub1 = df_sub1[::100]
# df_sub2 = df.loc[df['DELC14'] > -990]
# df_sub2 = df_sub2[::10]
# # df_sub3 will be produced later.
#
# # ACC FRONT DATA
# acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
#
#
# # CREATE THE MAP
# fig = plt.figure(figsize=(12, 4))
# gs = gridspec.GridSpec(1, 3)
# gs.update(wspace=.4, hspace=0.1)
#
# """
# FIRST SUBPLOT: PLOT FRONTS AND PLOT NITRATE DATA
# """
# # Extract latitude, longitude, and NITRATE columns from HYDROGRAPHIC DATA
# xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
# m.drawcoastlines()
# m.shadedrelief()
# latitudes = df_sub1['LATITUDE']
# longitudes = df_sub1['LONGITUDE']
# nitrate = df_sub1['NITRAT']  # SST values (sea surface temperature)
# # Convert latitudes and longitudes to map coordinates
# x, y = m(longitudes.values, latitudes.values)
# # Plot the SST data as scatter points, color-coded by temperature
# m.scatter(x, y, c=nitrate, cmap='coolwarm', s=50, edgecolor='k', linewidth=0.5)
# cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)
# cbar.set_label('Nitrate')
#
# fronts = np.unique(acc_fronts['front_name'])
# fronts = ['PF','SAF','STF','Boundary']
# line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
#
# for i in range(0, len(fronts)):
#     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#     latitudes = this_one['latitude']
#     longitudes = this_one['longitude']
#     x, y = m(longitudes.values, latitudes.values)
#     m.plot(x, y, color='black', label=f'{fronts[i]}', linestyle=line_sys[i])
#
# """
# SECOND SUBPLOT: PLOT FRONTS AND PLOT DEL14C DATA
# """
# # Extract latitude, longitude, and NITRATE columns from HYDROGRAPHIC DATA
# xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
# m.drawcoastlines()
# m.shadedrelief()
# latitudes = df_sub2['LATITUDE']
# longitudes = df_sub2['LONGITUDE']
# nitrate = df_sub2['DELC14']
# # Convert latitudes and longitudes to map coordinates
# x, y = m(longitudes.values, latitudes.values)
# # Plot the SST data as scatter points, color-coded by temperature
# m.scatter(x, y, c=nitrate, cmap='coolwarm', s=50, edgecolor='k', linewidth=0.5)
# cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)
# cbar.set_label('DIC \u0394$^1$$^4$C (\u2030)')
#
# fronts = np.unique(acc_fronts['front_name'])
# fronts = ['PF','SAF','STF','Boundary']
# line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
#
# for i in range(0, len(fronts)):
#     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#     latitudes = this_one['latitude']
#     longitudes = this_one['longitude']
#     x, y = m(longitudes.values, latitudes.values)
#     m.plot(x, y, color='black', label=f'{fronts[i]}', linestyle=line_sys[i])
#
# """
# THIRD SUBPLOT: PLOT FRONTS AND PLOT DEL14C DATA
# """
# xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])
# m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
# m.drawcoastlines()
# m.shadedrelief()
#
# # """
# # COPIED AND PASTED THE MAP FROM THE BOTTOM OF MAIN_ANALYSIS.PY
# # THE BELOW CODE WORKS. I'm going to test plotting the glodap data above and then bring it into the plot below
# # """
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
# from main_analysis import locs1, chile, markers, colors, size1, locs2, nz
# line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
#
# # LOOP THROUGH FIGURES STYLES
#
#
# fronts = np.unique(acc_fronts['front_name'])
# fronts = ['PF','SAF','STF','Boundary']
# line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
#
# for i in range(0, len(fronts)):
#     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#     latitudes = this_one['latitude']
#     longitudes = this_one['longitude']
#     x, y = m(longitudes.values, latitudes.values)
#     m.plot(x, y, color='black', label=f'{fronts[i]}', linestyle=line_sys[i])
#
#     # PLOTTING CHILEAN SITES
# for i in range(0, len(locs1)):
#     slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
#     lat = slice['NewLat']
#     lat = lat[0]
#     lon = slice['new_Lon']
#     lon = lon[0]
#     x, y = m(lon, lat)
#     m.scatter(x, y, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')
#     print(locs1[i])
#
#     site_mean_100 = time_integrated_means.loc[time_integrated_means['Site'] == str(locs1[i])].reset_index(drop=True)
#     chile_lat = site_mean_100['y']
#     chile_lon = site_mean_100['x']
#     print(type(chile_lon))
#     z, a = m(list(chile_lon), list(chile_lat))
#
#     m.plot(z, a, color=colors[i])
#
#     # PLOTTING NZ SITES
# for i in range(0, len(locs2)):
#
#     slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
#     lat = slice['NewLat']
#     lat = lat[0]
#     lon = slice['NewLon']
#     lon = lon[0]
#     x, y = m(lon, lat)
#     # print(x, y)
#     m.scatter(x, y, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')
#
#     site_mean_100 = time_integrated_means.loc[time_integrated_means['Site'] == str(locs2[i])].reset_index(drop=True)
#     chile_lat = site_mean_100['y']
#     chile_lon = site_mean_100['x']
#     print(type(chile_lon))
#     z, a = m(list(chile_lon), list(chile_lat))
#     m.plot(z, a, color=colors[i])
#
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/glodap_overlay/test.png',
#             dpi=300, bbox_inches="tight")
# plt.close()