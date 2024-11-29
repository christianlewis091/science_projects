"""
THIS FILE CONTAINS ERRORS.
USE GLODAP_check_nov29_2024.py

"""


# """
# 28-09-23
# We previously made a cool map showing the differences in 14C and nitrate along the different fronts.
# Lets try to quantify it a little bit more. To do this, I'm going to comment out the section that makes the map until later,
# to speed up the code.
# I wrote a file called CBL_zones which labels each datapoint (within the boundaries of the fronts) which I will call later into the plot
#
# 22-09-2023
# From my last meeting with Erik and Sara, we saw that Campbell island's HYSPLIT back-trajectory goes into the
# most southerly region of the polar front. We asked, can we quantify/qualify this a little bit better?
# To do so, I can overlay GLODAP data on top of the ORSI 1995 fronts, and I can overlay the 14C data, to compare upwellings
#
# Luckily, I had already been working on a compilation of GLODAP and GO-SHIP data for my '14C-Water Mass Project',
# so I already have a file of the webscraped data from the python file called "water_mass_dataset_creator.py".
#
# In the first subplot, I want to plot nitrate to show upwelling, so I've created a dataset called _ALLDATA where I have not
# filtered for only those which contain 14C.
#
# I WILL filter for only those that contain 14C for the second subplot.
#
# The third will be hyplsit data
# """
#
# """
# QUANTIFICATION SECTION
# """
# #
# import pandas as pd
# import numpy as np
# from X_miller_curve_algorithm import ccgFilter
# import matplotlib.pyplot as plt
# # from mpl_toolkits.basemap import Basemap
# import matplotlib.gridspec as gridspec
# # from X_my_functions import monte_carlo_randomization_trend
# # from main_analysis import *
# #
# # df = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP2_assign_masses/STEP2_WATER_MASSES_ASSIGNED.xlsx')
# df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP1_reboot/STEP1_GLODAP_C14.csv')
# acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
# # df = df[['G2expocode', 'G2cruise', 'G2station', 'G2region', 'G2cast', 'G2year', 'G2month', 'G2day', 'G2hour', 'G2minute', 'G2latitude', 'G2longitude','G2pressure','G2temperature','G2salinity', 'G2salinityf', 'G2nitrate','G2salinityqc','G2c14', 'G2c14f', 'G2c14err','G2sigma0']]
#
# """
# I'll need to smooth the acc fronts to the lat/lons where there is data in order to do the differeceing.
# """
# # the smoothing will output latitude data wherever it sees longitude data on X
# datas = pd.DataFrame({'x': df['G2longitude'], 'y': df['G2latitude']}).sort_values(by=['x'], ascending=True).reset_index(drop=True)
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
#
#     # # test it by showing in a plot / works so i'm removing this
#     # x, y = m(datas['x'], smoothed)
#     # m.plot(x, y, color='black', label=f'{fronts[i]}', linestyle=line_sys[i])
#
# # df.to_excel(r'H:\Science\Datasets\Hydrographic\test.xlsx')
# # df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\test.xlsx')
#
# # I need to make sure that the northernmost front isn't calculating everyting in the northern
# # hemispehre so I index only to include everything souht of 5S.
#
# df = df.loc[df['G2latitude'] <= -5]
# cruise_names = np.unique(df['G2expocode'].astype(str))
# cruise_names = pd.DataFrame({'G2expocode': cruise_names})
# print(min(df['G2year']))
# print(max(df['G2year']))
#
# cruise_names.to_excel(r'H:\Science\Datasets\Hydrographic\names.xlsx')
# # subset data so that I only see data where the latitude of the pont is lower than STF
# # columns_to_dropna = ['Boundary+smoothed', 'PF+smoothed','SAF+smoothed','STF+smoothed']
# # df = df.dropna(subset=columns_to_dropna, inplace=True)
#
# df = df.rename(columns={'G2pressure':'CTDPRS', 'G2nitrate':'NITRAT','G2c14':'DELC14','G2latitude':'LATITUDE','G2longitude':'LONGITUDE'})
#
# # loop through the DF and assign a "SURFACE FRONT" to each point based on its lat and lon...
# result_array = []
# results_array_sectors1 = []
# results_array_sectors2 = []
# for j in range(0, len(df)):
#     row = df.iloc[j]
#     # print(row['LATITUDE'])
#     # print(row['Boundary+smoothed'])
#     # print(row['PF+smoothed'])
#     # print(row['SAF+smoothed'])
#     # print(row['STF+smoothed'])
#
#     # assign label based on latitude
#     if (row['LATITUDE'] >= row['STF+smoothed']):
#         res = 'STZ'
#     elif (row['LATITUDE'] >= row['Boundary+smoothed']) & (row['LATITUDE'] <= row['PF+smoothed']):
#         res = 'ASZ'
#     elif (row['LATITUDE'] >= row['PF+smoothed']) & (row['LATITUDE'] <= row['SAF+smoothed']):
#         res = 'PFZ'
#     elif (row['LATITUDE'] >= row['SAF+smoothed']) & (row['LATITUDE'] <= row['STF+smoothed']):
#         res = 'SAZ'
#     elif (row['LATITUDE'] <= row['Boundary+smoothed']):
#         res = 'SIZ'
#     else:
#         res = 'Error'
#
#     # assign label based on latitude and longitude (PACIFIC SIDE FOR CHILEAN DATA)
#     if (row['LATITUDE'] >= row['STF+smoothed']) & (-150 <= row['LONGITUDE'] <= -90):
#         res2 = 'STZ'
#     elif (row['LATITUDE'] >= row['Boundary+smoothed']) & (row['LATITUDE'] <= row['PF+smoothed']) & (-150 <= row['LONGITUDE'] <= -90):
#         res2 = 'ASZ'
#     elif (row['LATITUDE'] >= row['PF+smoothed']) & (row['LATITUDE'] <= row['SAF+smoothed']) & (-150 <= row['LONGITUDE'] <= -90):
#         res2 = 'PFZ'
#     elif (row['LATITUDE'] >= row['SAF+smoothed']) & (row['LATITUDE'] <= row['STF+smoothed']) & (-150 <= row['LONGITUDE'] <= -90):
#         res2 = 'SAZ'
#     elif (row['LATITUDE'] <= row['Boundary+smoothed']):
#         res2 = 'SIZ'
#     else:
#         res2 = 'Error'
#     # INDIAN SIDE FOR NZ ORIGIN
#     if (row['LATITUDE'] >= row['STF+smoothed']) & (60 <= row['LONGITUDE'] <= 120):
#         res3 = 'STZ'
#     elif (row['LATITUDE'] >= row['Boundary+smoothed']) & (row['LATITUDE'] <= row['PF+smoothed']) & (60 <= row['LONGITUDE'] <= 120):
#         res3 = 'ASZ'
#     elif (row['LATITUDE'] >= row['PF+smoothed']) & (row['LATITUDE'] <= row['SAF+smoothed']) & (60 <= row['LONGITUDE'] <= 120):
#         res3 = 'PFZ'
#     elif (row['LATITUDE'] >= row['SAF+smoothed']) & (row['LATITUDE'] <= row['STF+smoothed']) & (60 <= row['LONGITUDE'] <= 120):
#         res3 = 'SAZ'
#     elif (row['LATITUDE'] <= row['Boundary+smoothed']):
#         res3 = 'SIZ'
#     else:
#         res3 = 'Error'
#
#     # append the total zone
#     result_array.append(res)
#     # append the Pac zone
#     results_array_sectors1.append(res2)
#     # append the indian zone
#     results_array_sectors2.append(res3)
# df['CBL_zones'] = result_array
# df['CBL_zones_sectored_CH'] = results_array_sectors1
# df['CBL_zones_sectored_NZ'] = results_array_sectors2
# df.to_excel(r'H:\Science\Datasets\Hydrographic\cbl_zones.xlsx')
#
#
# """
# FIGURE SECTION
# """
#
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
#
# import matplotlib.gridspec as gridspec
# # from main_analysis import *
#
# # # READ IN THE _ALLDATA FILE
# # df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_ALLDATA.xlsx')
# # df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_ALLDATA100m.xlsx')
# # data read in above
#
# # FILTER TO ONLY GRAB SURFACE SAMPLES
#
#
#
# df = df.loc[df['CTDPRS'] < 100] # ONLY GRAB SURFACE SAMPLES
# # df = df.loc[df['G2year'] > 1979] # ONLY GRAB SURFACE SAMPLES
# # WRITE TO A NEW FILE FOR FASTER PRODUCTION OF THIS CODE (insert to above later)
# # df.to_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_ALLDATA100m.xlsx')
#
# # CREATE SUBSETS OF DATA FOR SUBPLOTS 1, 2, and 3
# df_sub1 = df.loc[df['NITRAT'] > -990]
# df_sub2 = df.loc[df['DELC14'] > -990]
# # df_sub3 will be produced later.
#
# # ACC FRONT DATA
# acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
# #
# #
# # # CREATE THE MAP
#
# fig = plt.figure(figsize=(12, 8))
# gs = gridspec.GridSpec(4, 4)
# gs.update(wspace=.55, hspace=0.1)
# # # set colorbar boundaries
# #
# #
# # """
# # FIRST SUBPLOT: PLOT FRONTS AND PLOT NITRATE DATA
# # """
# # # Extract latitude, longitude, and NITRATE columns from HYDROGRAPHIC DATA
# xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
# # m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
# # m.drawcoastlines()
# # m.shadedrelief()
# # latitudes = df_sub1['LATITUDE']
# # longitudes = df_sub1['LONGITUDE']
# # nitrate = df_sub1['NITRAT']
# # # # Convert latitudes and longitudes to map coordinates
# # x, y = m(longitudes.values, latitudes.values)
# # # Plot the SST data as scatter points, color-coded by temperature
# # plt.title('Nitrate (\u03BCM)')
# # m.scatter(x, y, c=nitrate, cmap='coolwarm', s=50, edgecolor='k', linewidth=0.5, vmin=0, vmax=32)
# # cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)
# # # cbar.set_label('Nitrate')
# #
# # fronts = np.unique(acc_fronts['front_name'])
# # fronts = ['PF','SAF','STF','Boundary']
# # line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
# #
# # for i in range(0, len(fronts)):
# #     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
# #     latitudes = this_one['latitude']
# #     longitudes = this_one['longitude']
# #     x, y = m(longitudes.values, latitudes.values)
# #     m.plot(x, y, color='black', label=f'{fronts[i]}', linestyle=line_sys[i])
# #
# # # """
# # # SECOND SUBPLOT: PLOT FRONTS AND PLOT DEL14C DATA
# # # """
# # # #flip colormap
# cmap_reversed = plt.cm.get_cmap('coolwarm_r')
# # # Extract latitude, longitude, and NITRATE columns from HYDROGRAPHIC DATA
# xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
# # plt.title('DIC \u0394$^1$$^4$C (\u2030)')
# # m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
# # m.drawcoastlines()
# # m.shadedrelief()
# # latitudes = df_sub2['LATITUDE']
# # longitudes = df_sub2['LONGITUDE']
# # nitrate = df_sub2['DELC14']
# # # Convert latitudes and longitudes to map coordinates
# # x, y = m(longitudes.values, latitudes.values)
# # # Plot the SST data as scatter points, color-coded by temperature
# # m.scatter(x, y, c=nitrate, cmap=cmap_reversed, s=50, edgecolor='k', linewidth=0.5, vmin=-150, vmax=150)
# # cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)
#
#
# # fronts = np.unique(acc_fronts['front_name'])
# # fronts = ['PF','SAF','STF','Boundary']
# # line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
# #
# # for i in range(0, len(fronts)):
# #     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
# #     latitudes = this_one['latitude']
# #     longitudes = this_one['longitude']
# #     x, y = m(longitudes.values, latitudes.values)
# #     m.plot(x, y, color='black', label=f'{fronts[i]}', linestyle=line_sys[i])
#
# df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\cbl_zones.xlsx')
# df = df.loc[df['CBL_zones'] != 'Error']
# df = df.loc[df['DELC14'] > -990]
# df = df.loc[df['NITRAT'] > -990]
#
# results = pd.DataFrame()
# zones = np.unique(df['CBL_zones'])
# zones = ['STZ','SAZ','PFZ','ASZ','SIZ']
# # total data
# mean14C = []
# std14C = []
# meannit = []
# stdnit = []
# zone = []
#
# # pac data
# mean14C_pac = []
# std14C_pac = []
# meannit_pac = []
# stdnit_pac = []
# zone_pac = []
#
# # ind data
# mean14C_ind = []
# std14C_ind = []
# meannit_ind = []
# stdnit_ind = []
# zone_ind = []
#
#
# for i in range(0, len(zones)):
#     df1 = df.loc[df['CBL_zones'] == zones[i]]
#     mean14C.append(np.nanmean(df1['DELC14']))
#     std14C.append(np.nanstd(df1['DELC14']))
#     meannit.append(np.nanmean(df1['NITRAT']))
#     stdnit.append(np.nanstd(df1['NITRAT']))
#     zone.append(zones[i])
#
#     df2 = df.loc[df['CBL_zones_sectored_CH'] == zones[i]]
#     mean14C_pac.append(np.nanmean(df2['DELC14']))
#     std14C_pac.append(np.nanstd(df2['DELC14']))
#     meannit_pac.append(np.nanmean(df2['NITRAT']))
#     stdnit_pac.append(np.nanstd(df2['NITRAT']))
#
#     df3 = df.loc[df['CBL_zones_sectored_NZ'] == zones[i]]
#     mean14C_ind.append(np.nanmean(df3['DELC14']))
#     std14C_ind.append(np.nanstd(df3['DELC14']))
#     meannit_ind.append(np.nanmean(df3['NITRAT']))
#     stdnit_ind.append(np.nanstd(df3['NITRAT']))
#
#
# results = pd.DataFrame({"zone": zone,
#                         "mean_14C": mean14C, "std14C":std14C, "mean_nitrate": meannit, "stdnitrate":stdnit,
#                         "mean_14C_pac": mean14C_pac, "std14C_pac":std14C_pac, "mean_nitrate_pac": meannit_pac, "stdnitrate_pac":stdnit_pac,
#                         "mean_14C_ind": mean14C_ind, "std14C_ind":std14C_ind, "mean_nitrate_ind": meannit_ind, "stdnitrate_ind":stdnit_ind,
#                         })
# results.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/glodap_overlay/glodap_goship_results_Nov29_2024.xlsx')
# xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
# # plt.errorbar(results['zone'], results['mean_nitrate'], yerr=results['stdnitrate'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha=1)
#
# blah = 50
# results_tot = results.loc[(results['zone'] == 'STZ') | (results['zone'] == 'SAZ') | (results['zone'] == 'PFZ') | (results['zone'] == 'ASZ') |(results['zone'] == 'SIZ')]
# results_pac = results.loc[(results['zone'] == 'STZ') | (results['zone'] == 'SAZ') | (results['zone'] == 'PFZ') | (results['zone'] == 'ASZ') |(results['zone'] == 'SIZ')]
#
# plt.errorbar(results['zone'], results['mean_nitrate'], yerr=results['stdnitrate'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
# plt.scatter(results['zone'], results['mean_nitrate'], c=results['mean_nitrate'], cmap='coolwarm', s=blah, edgecolor='k', linewidth=0.5, vmin=0, vmax=32, zorder=10, marker='o')
#
# plt.errorbar(results['zone'], results['mean_nitrate_pac'], yerr=results['stdnitrate_pac'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
# plt.scatter(results['zone'], results['mean_nitrate_pac'], c=results['mean_nitrate_pac'], cmap='coolwarm', s=blah, edgecolor='k', linewidth=0.5, vmin=0, vmax=32, zorder=10, marker='D')
#
# plt.errorbar(results['zone'], results['mean_nitrate_ind'], yerr=results['stdnitrate_ind'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
# plt.scatter(results['zone'], results['mean_nitrate_ind'], c=results['mean_nitrate_ind'], cmap='coolwarm', s=blah, edgecolor='k', linewidth=0.5, vmin=0, vmax=32, zorder=10, marker='s')
# plt.ylabel('Nitrate (\u03BCM)')
# # cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)
#
# xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
# plt.errorbar(results['zone'], results['mean_14C'], yerr=results['std14C'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
# plt.scatter(results['zone'], results['mean_14C'], c=results['mean_14C'], cmap=cmap_reversed, s=blah, edgecolor='k', linewidth=0.5, vmin=-150, vmax=150, zorder=10, label='Total')
#
# plt.errorbar(results['zone'], results['mean_14C_pac'], yerr=results['std14C_pac'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
# plt.scatter(results['zone'], results['mean_14C_pac'], c=results['mean_14C_pac'], cmap=cmap_reversed, s=blah, edgecolor='k', linewidth=0.5, vmin=-150, vmax=150, zorder=10, marker='D', label='Pacific Sector')
#
# plt.errorbar(results['zone'], results['mean_14C_ind'], yerr=results['std14C_ind'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
# plt.scatter(results['zone'], results['mean_14C_ind'], c=results['mean_14C_ind'], cmap=cmap_reversed, s=blah, edgecolor='k', linewidth=0.5, vmin=-150, vmax=150, zorder=10, marker='s', label='Indian Sector')
# plt.ylabel('DIC \u0394$^1$$^4$C (\u2030)')
# # cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)
# plt.legend()
#
# # add labels
# # plt.text(-3, 95, '[B]', horizontalalignment='center', verticalalignment='center', fontsize=12)
# # plt.text(0, 95, '[D]', horizontalalignment='center', verticalalignment='center', fontsize=12)
# # plt.text(-3, 492, '[A]', horizontalalignment='center', verticalalignment='center', fontsize=12)
# # plt.text(0, 492, '[C]', horizontalalignment='center', verticalalignment='center', fontsize=12)
# # plt.text(3, 492, '[E]', horizontalalignment='center', verticalalignment='center', fontsize=12)
#
#
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/glodap_overlay/GLODAP_data_final_NoV29_2024.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
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
#
