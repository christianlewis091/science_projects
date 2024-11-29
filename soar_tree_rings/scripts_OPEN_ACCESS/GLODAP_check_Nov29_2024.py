"""
28-09-23
We previously made a cool map showing the differences in 14C and nitrate along the different fronts.
Lets try to quantify it a little bit more. To do this, I'm going to comment out the section that makes the map until later,
to speed up the code.
I wrote a file called CBL_zones which labels each datapoint (within the boundaries of the fronts) which I will call later into the plot

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
#
import pandas as pd
import numpy as np
from X_miller_curve_algorithm import ccgFilter
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
# from main_analysis import *


df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP1_reboot/STEP1_GLODAP_C14.csv')
acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')


# FILTER TO ONLY GRAB SURFACE SAMPLES
df = df.rename(columns={'G2expocode':'EXPOCODE', 'G2year':'DATE', 'G2pressure':'CTDPRS', 'G2nitrate':'NITRAT','G2c14':'DELC14','G2latitude':'LATITUDE','G2longitude':'LONGITUDE'})


"""
I'll need to smooth the acc fronts to the lat/lons where there is data in order to do the differeceing.
"""
# the smoothing will output latitude data wherever it sees longitude data on X
datas = pd.DataFrame({'x': df['LONGITUDE'], 'y': df['LATITUDE']}).sort_values(by=['x'], ascending=True).reset_index(drop=True)

n = 3 # set the amount of times the code will iterate (set to 10,000 once everything is final)
cutoff = 667  # FFT filter cutoff

# Do this for each front
fronts = np.unique(acc_fronts['front_name'])
fronts = ['PF','SAF','STF','Boundary']
line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']

# Create a Cartopy plot
projection = ccrs.PlateCarree()
fig, ax = plt.subplots(figsize=(10, 6), subplot_kw={'projection': projection})

# Add features like coastlines and borders
ax.coastlines(resolution='110m')
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())  # Set global extent

# Iterate over each front to create and plot the smoothed data
for i in range(len(fronts)):
    this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
    latitudes = this_one['latitude'].reset_index(drop=True)
    longitudes = this_one['longitude'].reset_index(drop=True)
    yerr = latitudes * 0.01

    # Dynamically name a variable
    smoothed = ccgFilter(longitudes, latitudes, cutoff).getSmoothValue(datas['x'])
    df[f'{fronts[i]}+smoothed'] = smoothed

    # Test it by showing in a plot
    ax.plot(
        datas['x'], smoothed,
        transform=ccrs.Geodetic(),  # Specify the CRS of the data
        color='black',
        label=f'{fronts[i]}',
        linestyle=line_sys[i]
    )

# Add legend and show the plot
ax.legend(loc='upper left')
plt.show()

#
# I need to make sure that the northernmost front isn't calculating everyting in the northern
# hemispehre so I index only to include everything souht of 5S.

df = df.loc[df['LATITUDE'] <= -5]
cruise_names = np.unique(df['EXPOCODE'].astype(str))
cruise_names = pd.DataFrame({"EXPOCODES": cruise_names})
print(min(df['DATE']))
print(max(df['DATE']))
cruise_names.to_excel(r'H:\Science\Datasets\Hydrographic\names.xlsx')
# subset data so that I only see data where the latitude of the pont is lower than STF
# columns_to_dropna = ['Boundary+smoothed', 'PF+smoothed','SAF+smoothed','STF+smoothed']
# df = df.dropna(subset=columns_to_dropna, inplace=True)

# loop through the DF and assign a "SURFACE FRONT" to each point based on its lat and lon...
result_array = []
results_array_sectors1 = []
results_array_sectors2 = []
for j in range(0, len(df)):
    row = df.iloc[j]
    # print(row['LATITUDE'])
    # print(row['Boundary+smoothed'])
    # print(row['PF+smoothed'])
    # print(row['SAF+smoothed'])
    # print(row['STF+smoothed'])

    # assign label based on latitude
    if (row['LATITUDE'] >= row['STF+smoothed']):
        res = 'STZ'
    elif (row['LATITUDE'] >= row['Boundary+smoothed']) & (row['LATITUDE'] <= row['PF+smoothed']):
        res = 'ASZ'
    elif (row['LATITUDE'] >= row['PF+smoothed']) & (row['LATITUDE'] <= row['SAF+smoothed']):
        res = 'PFZ'
    elif (row['LATITUDE'] >= row['SAF+smoothed']) & (row['LATITUDE'] <= row['STF+smoothed']):
        res = 'SAZ'
    elif (row['LATITUDE'] <= row['Boundary+smoothed']):
        res = 'SIZ'
    else:
        res = 'Error'

    # assign label based on latitude and longitude (PACIFIC SIDE FOR CHILEAN DATA)
    if (row['LATITUDE'] >= row['STF+smoothed']) & (-150 <= row['LONGITUDE'] <= -90):
        res2 = 'STZ'
    elif (row['LATITUDE'] >= row['Boundary+smoothed']) & (row['LATITUDE'] <= row['PF+smoothed']) & (-150 <= row['LONGITUDE'] <= -90):
        res2 = 'ASZ'
    elif (row['LATITUDE'] >= row['PF+smoothed']) & (row['LATITUDE'] <= row['SAF+smoothed']) & (-150 <= row['LONGITUDE'] <= -90):
        res2 = 'PFZ'
    elif (row['LATITUDE'] >= row['SAF+smoothed']) & (row['LATITUDE'] <= row['STF+smoothed']) & (-150 <= row['LONGITUDE'] <= -90):
        res2 = 'SAZ'
    elif (row['LATITUDE'] <= row['Boundary+smoothed']):
        res2 = 'SIZ'
    else:
        res2 = 'Error'
    # INDIAN SIDE FOR NZ ORIGIN
    if (row['LATITUDE'] >= row['STF+smoothed']) & (60 <= row['LONGITUDE'] <= 120):
        res3 = 'STZ'
    elif (row['LATITUDE'] >= row['Boundary+smoothed']) & (row['LATITUDE'] <= row['PF+smoothed']) & (60 <= row['LONGITUDE'] <= 120):
        res3 = 'ASZ'
    elif (row['LATITUDE'] >= row['PF+smoothed']) & (row['LATITUDE'] <= row['SAF+smoothed']) & (60 <= row['LONGITUDE'] <= 120):
        res3 = 'PFZ'
    elif (row['LATITUDE'] >= row['SAF+smoothed']) & (row['LATITUDE'] <= row['STF+smoothed']) & (60 <= row['LONGITUDE'] <= 120):
        res3 = 'SAZ'
    elif (row['LATITUDE'] <= row['Boundary+smoothed']):
        res3 = 'SIZ'
    else:
        res3 = 'Error'

    # append the total zone
    result_array.append(res)
    # append the Pac zone
    results_array_sectors1.append(res2)
    # append the indian zone
    results_array_sectors2.append(res3)
df['CBL_zones'] = result_array
df['CBL_zones_sectored_CH'] = results_array_sectors1
df['CBL_zones_sectored_NZ'] = results_array_sectors2
df.to_excel(r'H:\Science\Datasets\Hydrographic\cbl_zones.xlsx')


"""
FIGURE SECTION
"""
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt

df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\cbl_zones.xlsx')
acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')

df = df.loc[df['CTDPRS'] < 100] # ONLY GRAB SURFACE SAMPLES

# CREATE SUBSETS OF DATA FOR SUBPLOTS 1, 2, and 3
# df_sub1 = df.loc[df['NITRAT'] > -990]
# df_sub1 = df_sub1[::10]
# df_sub2 = df.loc[df['DELC14'] > -990]
# df_sub2 = df_sub2[::10]
# df_sub3 will be produced later.


import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import numpy as np

# Create figure and map projection
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.Orthographic(central_longitude=0, central_latitude=-90))

# Add land and coastlines for context
ax.add_feature(cf.LAND, edgecolor='black')
ax.coastlines()

# Ensure fronts are unique
fronts = np.unique(acc_fronts['front_name'])
fronts = ['PF', 'SAF', 'STF', 'Boundary']
line_sys = ['dotted', 'dashed', 'dashdot', 'solid']

# Loop through each front and plot
for i in range(len(fronts)):
    this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
    latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
    longitudes = this_one['longitude'].values

    # Plot the data, making sure to specify the correct CRS for input data
    ax.plot(
        longitudes,
        latitudes,
        transform=ccrs.PlateCarree(),  # Data is in lat/lon format
        linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
        label=fronts[i]
    )

# add the nitrate and 14C data
dfn = df.loc[df['NITRAT'] > -999]
latitudes_data = dfn['LATITUDE'].values
longitudes_data = dfn['LONGITUDE'].values
nitrate_data = dfn['NITRAT'].values
sc = ax.scatter(
    longitudes_data,
    latitudes_data,
    c=nitrate_data,
    cmap='coolwarm',
    transform=ccrs.PlateCarree())  # Data is in lat/lon format)
cb = plt.colorbar(sc, ax=ax, orientation='vertical', pad=0.05, label='NITRAT')
# Show the plot

plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_GLODAP_check_Nov29_2024/nitrate.png', dpi=300, bbox_inches="tight")

plt.close()


# Create figure and map projection
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.Orthographic(central_longitude=0, central_latitude=-90))

# Add land and coastlines for context
ax.add_feature(cf.LAND, edgecolor='black')
ax.coastlines()

# Ensure fronts are unique
fronts = np.unique(acc_fronts['front_name'])
fronts = ['PF', 'SAF', 'STF', 'Boundary']
line_sys = ['dotted', 'dashed', 'dashdot', 'solid']

# Loop through each front and plot
for i in range(len(fronts)):
    this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
    latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
    longitudes = this_one['longitude'].values

    # Plot the data, making sure to specify the correct CRS for input data
    ax.plot(
        longitudes,
        latitudes,
        transform=ccrs.PlateCarree(),  # Data is in lat/lon format
        linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
        label=fronts[i]
    )

# add the nitrate and 14C data
cmap_reversed = plt.cm.get_cmap('coolwarm_r')
dfn = df.loc[df['DELC14'] > -999]
latitudes_data = dfn['LATITUDE'].values
longitudes_data = dfn['LONGITUDE'].values
nitrate_data = dfn['DELC14'].values
sc = ax.scatter(
    longitudes_data,
    latitudes_data,
    c=nitrate_data,
    cmap=cmap_reversed,
    transform=ccrs.PlateCarree())  # Data is in lat/lon format)
cb = plt.colorbar(sc, ax=ax, orientation='vertical', pad=0.05, label='DELC14')
# Show the plot
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_GLODAP_check_Nov29_2024/C14.png', dpi=300, bbox_inches="tight")
plt.close()


# # # set colorbar boundaries
# #
# #
# # """
# # FIRST SUBPLOT: PLOT FRONTS AND PLOT NITRATE DATA
# # """
# # # Extract latitude, longitude, and NITRATE columns from HYDROGRAPHIC DATA
# xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
# m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
# m.drawcoastlines()
# m.shadedrelief()
# latitudes = df_sub1['LATITUDE']
# longitudes = df_sub1['LONGITUDE']
# nitrate = df_sub1['NITRAT']
# # # Convert latitudes and longitudes to map coordinates
# x, y = m(longitudes.values, latitudes.values)
# # Plot the SST data as scatter points, color-coded by temperature
# plt.title('Nitrate (\u03BCM)')
# m.scatter(x, y, c=nitrate, cmap='coolwarm', s=50, edgecolor='k', linewidth=0.5, vmin=0, vmax=32)
# cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)
# # cbar.set_label('Nitrate')
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
# # """
# # SECOND SUBPLOT: PLOT FRONTS AND PLOT DEL14C DATA
# # """
# # #flip colormap
# cmap_reversed = plt.cm.get_cmap('coolwarm_r')
# # Extract latitude, longitude, and NITRATE columns from HYDROGRAPHIC DATA
# xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
# plt.title('DIC \u0394$^1$$^4$C (\u2030)')
# m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
# m.drawcoastlines()
# m.shadedrelief()
# latitudes = df_sub2['LATITUDE']
# longitudes = df_sub2['LONGITUDE']
# nitrate = df_sub2['DELC14']
# # Convert latitudes and longitudes to map coordinates
# x, y = m(longitudes.values, latitudes.values)
# # Plot the SST data as scatter points, color-coded by temperature
# m.scatter(x, y, c=nitrate, cmap=cmap_reversed, s=50, edgecolor='k', linewidth=0.5, vmin=-150, vmax=150)
# cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)
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
# results.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/glodap_overlay/glodap_goship_results.xlsx')
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
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/glodap_overlay/GLODAP_data_final.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#










