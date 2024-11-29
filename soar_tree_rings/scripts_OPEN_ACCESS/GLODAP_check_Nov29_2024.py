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

#
import pandas as pd
import numpy as np
from X_miller_curve_algorithm import ccgFilter
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
# from main_analysis import *


df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP1_reboot/STEP1_GLODAP_C14.csv')
acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')


# FILTER TO ONLY GRAB SURFACE SAMPLES
df = df.rename(columns={'G2expocode':'EXPOCODE', 'G2year':'DATE', 'G2pressure':'CTDPRS', 'G2nitrate':'NITRAT','G2c14':'DELC14','G2latitude':'LATITUDE','G2longitude':'LONGITUDE'})
df = df.loc[df['CTDPRS'] < 100] # ONLY GRAB SURFACE SAMPLES
df = df.loc[df['DELC14'] > -990]
df = df.loc[df['NITRAT'] > -990]
df = df.loc[df['DATE'] > 1979]


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
ax.add_feature(cf.BORDERS, linestyle=':')
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
ax.gridlines()
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_GLODAP_check_Nov29_2024/testmap.png', dpi=300, bbox_inches="tight")

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
Compile the sectional averages
"""
df = df.loc[df['CBL_zones'] != 'Error']

results = pd.DataFrame()
zones = np.unique(df['CBL_zones'])
zones = ['STZ','SAZ','PFZ','ASZ','SIZ']
# total data
mean14C = []
std14C = []
meannit = []
stdnit = []
zone = []

# pac data
mean14C_pac = []
std14C_pac = []
meannit_pac = []
stdnit_pac = []
zone_pac = []

# ind data
mean14C_ind = []
std14C_ind = []
meannit_ind = []
stdnit_ind = []
zone_ind = []


for i in range(0, len(zones)):
    df1 = df.loc[df['CBL_zones'] == zones[i]]
    mean14C.append(np.nanmean(df1['DELC14']))
    std14C.append(np.nanstd(df1['DELC14']))
    meannit.append(np.nanmean(df1['NITRAT']))
    stdnit.append(np.nanstd(df1['NITRAT']))
    zone.append(zones[i])

    df2 = df.loc[df['CBL_zones_sectored_CH'] == zones[i]]
    mean14C_pac.append(np.nanmean(df2['DELC14']))
    std14C_pac.append(np.nanstd(df2['DELC14']))
    meannit_pac.append(np.nanmean(df2['NITRAT']))
    stdnit_pac.append(np.nanstd(df2['NITRAT']))

    df3 = df.loc[df['CBL_zones_sectored_NZ'] == zones[i]]
    mean14C_ind.append(np.nanmean(df3['DELC14']))
    std14C_ind.append(np.nanstd(df3['DELC14']))
    meannit_ind.append(np.nanmean(df3['NITRAT']))
    stdnit_ind.append(np.nanstd(df3['NITRAT']))


results = pd.DataFrame({"zone": zone,
                        "mean_14C": mean14C, "std14C":std14C, "mean_nitrate": meannit, "stdnitrate":stdnit,
                        "mean_14C_pac": mean14C_pac, "std14C_pac":std14C_pac, "mean_nitrate_pac": meannit_pac, "stdnitrate_pac":stdnit_pac,
                        "mean_14C_ind": mean14C_ind, "std14C_ind":std14C_ind, "mean_nitrate_ind": meannit_ind, "stdnitrate_ind":stdnit_ind,
                        })
# results.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_GLODAP_check_Nov29_2024/glodap_goship_results_Nov29_24.xlsx')


"""
FIGURE SECTION
"""

# Create a figure
fig = plt.figure(figsize=(10, 8))

# Define the 2x2 grid of axes
ax1 = fig.add_subplot(2, 2, 1, projection=ccrs.Orthographic(central_longitude=0, central_latitude=-90))
ax2 = fig.add_subplot(2, 2, 2, projection=ccrs.Orthographic(central_longitude=0, central_latitude=-90))
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)

# First Subplot: Nitrate Map
ax1.add_feature(cf.OCEAN)
ax1.add_feature(cf.LAND, edgecolor='black')
ax1.gridlines()
ax1.set_title("Nitrate")

fronts = np.unique(acc_fronts['front_name'])
fronts = ['PF', 'SAF', 'STF', 'Boundary']
line_sys = ['dotted', 'dashed', 'dashdot', 'solid']

# Loop through each front and plot
for i in range(len(fronts)):
    this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
    latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
    longitudes = this_one['longitude'].values

    # Plot the data, making sure to specify the correct CRS for input data
    ax1.plot(
        longitudes,
        latitudes,
        transform=ccrs.PlateCarree(),  # Data is in lat/lon format
        linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
        label=fronts[i], color='black')

# add the nitrate and 14C data
dfn = df.loc[df['NITRAT'] > -999]
latitudes_data = dfn['LATITUDE'].values
longitudes_data = dfn['LONGITUDE'].values
nitrate_data = dfn['NITRAT'].values
sc = ax1.scatter(
    longitudes_data,
    latitudes_data,
    c=nitrate_data,
    cmap='coolwarm',
    transform=ccrs.PlateCarree())  # Data is in lat/lon format)
cb = plt.colorbar(sc, ax=ax1, orientation='vertical', pad=0.05, label='Nitrate (\u03BCM)')
# Show the plot


# 3rd subplot
ax2.add_feature(cf.OCEAN)
ax2.add_feature(cf.LAND, edgecolor='black')
ax2.gridlines()
ax2.set_title("DELC14")

fronts = np.unique(acc_fronts['front_name'])
fronts = ['PF', 'SAF', 'STF', 'Boundary']
line_sys = ['dotted', 'dashed', 'dashdot', 'solid']

# Loop through each front and plot
for i in range(len(fronts)):
    this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
    latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
    longitudes = this_one['longitude'].values

    # Plot the data, making sure to specify the correct CRS for input data
    ax2.plot(
        longitudes,
        latitudes,
        transform=ccrs.PlateCarree(),  # Data is in lat/lon format
        linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
        label=fronts[i], color='black')

cmap_reversed = plt.cm.get_cmap('coolwarm_r')
# add the nitrate and 14C data
dfn = df.loc[df['DELC14'] > -999]
latitudes_data = dfn['LATITUDE'].values
longitudes_data = dfn['LONGITUDE'].values
nitrate_data = dfn['DELC14'].values
sc = ax2.scatter(
    longitudes_data,
    latitudes_data,
    c=nitrate_data,
    cmap=cmap_reversed,
    transform=ccrs.PlateCarree())  # Data is in lat/lon format)

cb = plt.colorbar(sc, ax=ax2, orientation='vertical', pad=0.05, label='DIC \u0394$^1$$^4$C (\u2030)')
cb.set_ticks(np.linspace(-150, 100, 5))
# Show the plot


blah = 50
ax3.errorbar(results['zone'], results['mean_nitrate'], yerr=results['stdnitrate'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
ax3.scatter(results['zone'], results['mean_nitrate'], c=results['mean_nitrate'], cmap='coolwarm', s=blah, edgecolor='k', linewidth=0.5, vmin=0, vmax=32, zorder=10, marker='o')

ax3.errorbar(results['zone'], results['mean_nitrate_pac'], yerr=results['stdnitrate_pac'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
ax3.scatter(results['zone'], results['mean_nitrate_pac'], c=results['mean_nitrate_pac'], cmap='coolwarm', s=blah, edgecolor='k', linewidth=0.5, vmin=0, vmax=32, zorder=10, marker='D')

ax3.errorbar(results['zone'], results['mean_nitrate_ind'], yerr=results['stdnitrate_ind'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
ax3.scatter(results['zone'], results['mean_nitrate_ind'], c=results['mean_nitrate_ind'], cmap='coolwarm', s=blah, edgecolor='k', linewidth=0.5, vmin=0, vmax=32, zorder=10, marker='s')
ax3.set_ylabel('Nitrate (\u03BCM)')
ax3.legend()
# cbar = plt.colorbar(orientation='vertical', fraction=0.046, pad=0.04)


ax4.errorbar(results['zone'], results['mean_14C'], yerr=results['std14C'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
ax4.scatter(results['zone'], results['mean_14C'], c=results['mean_14C'], cmap=cmap_reversed, s=blah, edgecolor='k', linewidth=0.5, vmin=-150, vmax=150, zorder=10, label='Total')

ax4.errorbar(results['zone'], results['mean_14C_pac'], yerr=results['std14C_pac'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
ax4.scatter(results['zone'], results['mean_14C_pac'], c=results['mean_14C_pac'], cmap=cmap_reversed, s=blah, edgecolor='k', linewidth=0.5, vmin=-150, vmax=150, zorder=10, marker='D', label='Pacific Sector')

ax4.errorbar(results['zone'], results['mean_14C_ind'], yerr=results['std14C_ind'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
ax4.scatter(results['zone'], results['mean_14C_ind'], c=results['mean_14C_ind'], cmap=cmap_reversed, s=blah, edgecolor='k', linewidth=0.5, vmin=-150, vmax=150, zorder=10, marker='s', label='Indian Sector')
ax4.set_ylabel('DIC \u0394$^1$$^4$C (\u2030)')
plt.legend()

# Display the plots
plt.tight_layout()
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_GLODAP_check_Nov29_2024/bulkfigtest.png', dpi=300, bbox_inches="tight")
