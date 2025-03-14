"""
Copy made of GLODAP_check_Nov29_2024.py
BUT ACC fronts edited to come from reviewer_polarfront_question.py including the freeman PF's instead.
In order to not have to change the script majorly, I'm going to rename the Freeman PF to simply PF. I will do these carefully
with comments to avoid confusion...

"""


# #
import pandas as pd
import numpy as np
from X_miller_curve_algorithm import ccgFilter
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt
from map_function import map1, map2, map3
#
"""
This file breaks if you clean the GLODAP data up inside the file. I'm not sure why. Making it in GLODAP_tidy, then reading it in, works.
"""
df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_submission/Data_Files/STEP1_GLODAP_C14.csv')
#acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')

# added on 12/3/25 to use Freemand and Lovenduski PF
acc_fronts = pd.read_csv('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/acc_w_freeman_FINAL.csv')

# remove ORSI PF
acc_fronts = acc_fronts.loc[acc_fronts['front_name'] != 'PF']

# now RENAME freeman PF to simply PF...
acc_fronts.loc[acc_fronts['front_name'] == 'Freeman_PF', 'front_name'] = 'PF'

"""
REMAIDER SHOULD REMAIN UNCHANGED EXCEPT FOR SAVE LOCATIONS
"""

#
# FILTER TO ONLY GRAB SURFACE SAMPLES
df = df.rename(columns={'G2expocode':'EXPOCODE', 'G2year':'DATE', 'G2pressure':'CTDPRS', 'G2nitrate':'NITRAT','G2c14':'DELC14','G2latitude':'LATITUDE','G2longitude':'LONGITUDE'})
df = df.loc[df['CTDPRS'] < 100] # ONLY GRAB SURFACE SAMPLES
df = df.loc[df['DELC14'] > -990]
df = df.loc[df['NITRAT'] > -990]
df = df.loc[df['DATE'] > 1979]
df = df.loc[df['LATITUDE'] <= -5]
print(f'{len(df)} is original length of data after inital filtering for time, depth, and latitude') #for later report


"""
In order to figure out where each point lies relative to the Southern Hemispheric frontal zones, I need to find the frontal zones
not only at the given longitudes from ORSI, but at the longitudes or my samples.
"""
# THIS BIT OF CODE WAS WRITTEN BY CHAT GPT
reference = pd.DataFrame()
reference['LONGITUDE'] = df['LONGITUDE']

# Iterate over each front
fronts = acc_fronts['front_name'].unique()
for front in fronts:
    # Extract latitude and longitude for the current front
    this_one = acc_fronts[acc_fronts['front_name'] == front]
    front_longitudes = this_one['longitude'].values
    front_latitudes = this_one['latitude'].values

    # Ensure the front data is sorted by longitude
    sorted_indices = np.argsort(front_longitudes)
    front_longitudes = front_longitudes[sorted_indices]
    front_latitudes = front_latitudes[sorted_indices]

    # Interpolate the front latitudes to match the longitudes of the data
    smoothed_latitudes = np.interp(reference['LONGITUDE'], front_longitudes, front_latitudes)

    # Add interpolated latitudes as a new column in the data
    reference[f'{front}_smoothed_LAT'] = smoothed_latitudes

    # Optional: Plot if required
    map2(reference['LONGITUDE'], smoothed_latitudes, f'{front}_smoothed_LAT')

# here is the dataframe of the smoothed fronts, on the sampled longitudes
reference.to_excel('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/GLODAP_smoothed_fronts_sample_lons_freemanPF.xlsx')
print(len(reference))

"""
NOW,
I WANT TO PUT THE DATA INTO BINS, OF FRONT, AND OCEAN ZONE
"""

results = []
for i in range(0, len(df)):
    row = df.iloc[i]
    sample_lat = row['LATITUDE']
    sample_lon = row['LONGITUDE']

    for j in range(0,len(reference)):
        # WE WANT TO COMPARE THE SAMPLE LAT, TO FRONTS AT SAMPLE LONGITUIDES
        ref_row = reference.iloc[j]
        ref_lon = ref_row['LONGITUDE']

        if sample_lon == ref_lon:
            abc = 1 # find a way to break to outer loop
            # print('YAY!')
            # print(sample_lon)
            # print(ref_lon)
            # print(sample_lat)

            # IF LONS MATCH, COMEPARE SAMPLE LAT, to FRONT LATS
            stf = ref_row['STF_smoothed_LAT']
            saf = ref_row['SAF_smoothed_LAT']
            pf = ref_row['PF_smoothed_LAT']
            boundary = ref_row['Boundary_smoothed_LAT']
            # print(f'STF IS {stf}')
            # print(f'SAF IS {saf}')
            # print(f'PF IS {pf}')
            # print(f'Bound IS {boundary}')

            if sample_lat >= stf: #above the subtropical front is the subtropical zone
                a = 'STZ'
            elif sample_lat <= boundary:
                a = 'SIZ'
            elif boundary < sample_lat < pf:
                a = 'ASZ'
            elif pf < sample_lat < saf:
                a = 'PFZ'
            elif saf < sample_lat < stf:
                a = 'SAZ'
            else:
                a= 'ERROR'
            results.append(a)
            # print(results)
            # print()
            break

# print(len(results))
# print(len(df))
df['Assigned_Zone'] = results

df.to_excel(r'C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/GLODAP_cbl_zones_freemanPF.xlsx')

"""
Check the assignments work via a map
"""

# assign ocean basin
df['Basin'] = 'Atlantic'
# start at the top of africa
df.loc[(df['LONGITUDE'] >= 21) & (df['LONGITUDE'] <= 120), 'Basin'] = 'Indian'
df.loc[(df['LONGITUDE'] >= 120), 'Basin'] = 'Pacific'
df.loc[(df['LONGITUDE'] >= -180) & (df['LONGITUDE'] <= -70), 'Basin'] = 'Pacific'

df.to_excel(r'C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/GLODAP_cbl_zones_sectors_assigned_freemanPF.xlsx')
print(len(df))

zones = ['STZ','SIZ','ASZ','PFZ','SAZ']
basins = ['Pacific','Indian','Atlantic']

for b in range(0, len(basins)):

    df2 = df.loc[df['Basin'] == basins[b]]

    for g in range(0, len(zones)):
        df3 = df2.loc[df2['Assigned_Zone'] == zones[g]]

        # ADD FIGURE TO CHECK
        plt.figure(figsize=(10, 10))
        ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
        ax.add_feature(cf.OCEAN)
        ax.add_feature(cf.LAND, edgecolor='black')
        ax.gridlines()

        fronts = np.unique(acc_fronts['front_name'])
        fronts = ['PF', 'SAF', 'STF', 'Boundary']
        line_sys = ['dotted', 'dashed', 'dashdot', 'solid']

        # ORSI FRONTS
        for p in range(len(fronts)):
            this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[p]]
            latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
            longitudes = this_one['longitude'].values

            ax.plot(
                longitudes,
                latitudes,
                transform=ccrs.PlateCarree(),  # Data is in lat/lon format
                linestyle=line_sys[p % len(line_sys)],  # Cycle through line styles
                label=fronts[p], color='black')

        # add the nitrate and 14C data
        cmap_reversed = plt.cm.get_cmap('coolwarm_r')
        latitudes_data = df3['LATITUDE'].values
        longitudes_data = df3['LONGITUDE'].values
        nitrate_data = df3['DELC14'].values
        sc = ax.scatter(
            longitudes_data,
            latitudes_data,
            c=nitrate_data,
            cmap=cmap_reversed, vmin=-150, vmax=150,
            transform=ccrs.PlateCarree())  # Data is in lat/lon format)
        # Add gridlines
        gridlines = ax.gridlines(draw_labels=True, linestyle='--', color='gray', alpha=0.7)

        # Customize gridlines
        gridlines.xlabels_top = False  # Don't show longitude labels at the top
        gridlines.ylabels_right = False  # Don't show latitude labels on the right
        gridlines.xlabel_style = {'size': 10, 'color': 'blue'}
        gridlines.ylabel_style = {'size': 10, 'color': 'blue'}

        cb = plt.colorbar(sc, ax=ax, orientation='vertical', pad=0.05, label='DIC \u0394$^1$$^4$C (\u2030)')
        plt.title(f'{zones[g]}_{basins[b]}')
        # plt.show()
        plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Images_and_Figures\GLODAP_FreemanPF/{zones[g]}_{basins[b]}.png', dpi=300, bbox_inches="tight")


"""
Compile the sectional averages
"""
# df = df.loc[df['CBL_zones'] != 'Error']

results = pd.DataFrame()

# atlantic data
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

zones = ['STZ','SAZ','PFZ','ASZ','SIZ']
for i in range(0, len(zones)):
    df1 = df.loc[(df['Assigned_Zone'] == zones[i]) & (df['Basin'] == 'Atlantic') ]
    mean14C.append(np.nanmean(df1['DELC14']))
    std14C.append(np.nanstd(df1['DELC14']))
    meannit.append(np.nanmean(df1['NITRAT']))
    stdnit.append(np.nanstd(df1['NITRAT']))
    zone.append(zones[i])

    df2 = df.loc[(df['Assigned_Zone'] == zones[i]) & (df['Basin'] == 'Pacific') ]
    mean14C_pac.append(np.nanmean(df2['DELC14']))
    std14C_pac.append(np.nanstd(df2['DELC14']))
    meannit_pac.append(np.nanmean(df2['NITRAT']))
    stdnit_pac.append(np.nanstd(df2['NITRAT']))

    df3 = df.loc[(df['Assigned_Zone'] == zones[i]) & (df['Basin'] == 'Indian') ]
    mean14C_ind.append(np.nanmean(df3['DELC14']))
    std14C_ind.append(np.nanstd(df3['DELC14']))
    meannit_ind.append(np.nanmean(df3['NITRAT']))
    stdnit_ind.append(np.nanstd(df3['NITRAT']))


results = pd.DataFrame({"zone": zone,
                        "mean_14C": mean14C, "std14C":std14C, "mean_nitrate": meannit, "stdnitrate":stdnit,
                        "mean_14C_pac": mean14C_pac, "std14C_pac":std14C_pac, "mean_nitrate_pac": meannit_pac, "stdnitrate_pac":stdnit_pac,
                        "mean_14C_ind": mean14C_ind, "std14C_ind":std14C_ind, "mean_nitrate_ind": meannit_ind, "stdnitrate_ind":stdnit_ind,
                        })
results.to_excel('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/GLODAP_RESULTS_FINAL_Feb12_25_FreemanPF.xlsx')

"""
DONT NEED THE FIGURE RIGHT NOW
"""

"""
FIGURE SECTION
"""
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt
from map_function import map1, map2, map3
from cmcrameri import cm


colors = getattr(cm, 'vanimo')(np.linspace(.8, .2, len(zones)))

# THIS SHEET HAS THE AVERAGE OF ORSI AND FREEMAN MANUALLY ADDED!
results = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/glodap_new_figure_read_in.xlsx', comment='#')

# Create a figure
fig = plt.figure(figsize=(10, 8))

# Define the 2x2 grid of axes
ax1 = fig.add_subplot(2, 2, 1, projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
ax2 = fig.add_subplot(2, 2, 2, projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
ax3 = fig.add_subplot(2, 2, 3)
ax4 = fig.add_subplot(2, 2, 4)

# First Subplot: Nitrate Map
ax1.add_feature(cf.OCEAN)
ax1.add_feature(cf.LAND, edgecolor='black')
# ax1.gridlines()
ax1.set_title("Nitrate")

# bring BACK IN THE ORSI PF and ORIGINAL DATA FOR FIGURE writing.
# I want to see how they shift the GLODAP data analysis
acc_fronts = pd.read_csv(r'C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/acc_w_freeman_FINAL.csv')
fronts = np.unique(acc_fronts['front_name'])
fronts = ['PF', 'SAF', 'STF', 'Boundary','Freeman_PF']
line_sys = ['solid', 'dashed', 'dashdot', 'dotted', 'solid']
color1 = ['black', 'black', 'black', 'black', 'black']
transpar = [1,1,1,1,0.5]

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
        label=fronts[i], color=color1[i], alpha=transpar[i])

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
# ax2.gridlines()
ax2.set_title("DIC \u0394$^1$$^4$C (\u2030)")

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
        label=fronts[i], color=color1[i], alpha=transpar[i])

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
ax4.scatter(results['zone'], results['mean_14C'], c=results['mean_14C'], cmap=cmap_reversed, s=blah, edgecolor='k', linewidth=0.5, vmin=-150, vmax=150, zorder=10, label='Atlantic Sector')

ax4.errorbar(results['zone'], results['mean_14C_pac'], yerr=results['std14C_pac'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
ax4.scatter(results['zone'], results['mean_14C_pac'], c=results['mean_14C_pac'], cmap=cmap_reversed, s=blah, edgecolor='k', linewidth=0.5, vmin=-150, vmax=150, zorder=10, marker='D', label='Pacific Sector')

ax4.errorbar(results['zone'], results['mean_14C_ind'], yerr=results['std14C_ind'], fmt='', ecolor='black', elinewidth=1, capsize=2, alpha=1, linestyle='', zorder=0)
ax4.scatter(results['zone'], results['mean_14C_ind'], c=results['mean_14C_ind'], cmap=cmap_reversed, s=blah, edgecolor='k', linewidth=0.5, vmin=-150, vmax=150, zorder=10, marker='s', label='Indian Sector')
ax4.set_ylabel('DIC \u0394$^1$$^4$C (\u2030)')
plt.legend()

# Display the plots
plt.tight_layout()
plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Images_and_Figures\GLODAP_FreemanPF/FIGURE_FINAL_Feb1_25_AVERAGEOFORSIANDFREEMAN.png', dpi=300, bbox_inches="tight")
