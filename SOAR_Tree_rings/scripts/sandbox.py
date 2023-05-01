import numpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from X_my_functions import plotfunc_line, plotfunc_scat, plotfunc_2line, plotfunc_error
import matplotlib.gridspec as gridspec
from scipy import stats
from mpl_toolkits.basemap import Basemap

# read in the data from the previous .py files
df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/samples_with_references10000.xlsx')
ref2 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/harmonized_dataset.xlsx')
ref3 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/reference3.xlsx')

# ensure all data are sliced for after 1980.
df = df.loc[df['Decimal_date'] > 1980].reset_index(drop=True)
ref2 = ref2.loc[ref2['Decimal_date'] > 1980].reset_index(drop=True)
ref3 = ref3.loc[ref3['Decimal_date'] > 1980].reset_index(drop=True)


""" 
The following code block adds lats and lons to certain cites that were missing data (NMY, MCQ)
Need to add a flag for the "Chile" versus "NZ" datasets
Also, all the Lon data are not systematically E or W...
This block of code cleans up all the messiness in the lats and lons, and gives us flags to index later based on country
"""

neumayer_lat = -70.6666
neumayer_lon = -8.2667  # E
mcq_lat = -54.6208
mcq_lon = 158.8556  # E

lat_array = []
lon_array = []
for i in range(0, len(df)):
    current_row = df.iloc[i]
    if current_row['Site'] == 'NMY':
        lat_array.append(neumayer_lat)
        lon_array.append(neumayer_lon)
    elif current_row['Site'] == 'MCQ':
        lat_array.append(mcq_lat)
        lon_array.append(mcq_lon)
    elif current_row['Site'] == '23 Nikau St, Eastbourne, NZ':
        lat_array.append(-41.2923)
        lon_array.append(174.8971)  # change Chilean Longitudes to degrees East.
    elif current_row['Site'] == '19 Nikau St, Eastbourne, NZ':
        lat_array.append(-41.2923)
        lon_array.append(174.8971)  # change Chilean Longitudes to degrees East.
    else:
        lat_array.append(current_row['Lat'])
        lon_array.append(current_row['Lon'])
df['NewLat'] = lat_array
df['NewLon'] = lon_array


df['Country'] = -999  # Chile = 0, NZ = 1, NMY = 2
country_array = []
for i in range(0, len(df)):
    current_row = df.iloc[i]
    if current_row['NewLon'] > 90:
        country_array.append(1)
    elif 50 < current_row['NewLon'] < 90:
        country_array.append(0)
    elif current_row['NewLon'] < 0:
        country_array.append(2)
    else:
        print(current_row)
df['Country'] = country_array


df = df.drop_duplicates().reset_index(drop=True)

"""
Currently, the data has two types of "sample D14C values". There is the 1) Original D14C values, and "corrected" D14C values
which are called D14C_1. These corrected values only exist for NEU and MCQ datasets, and will be used in reference to 
the harmonized dataset, where the reference also has a correction applied. However, in the dataframe, the SOAR data cells
wrt D14C_1 are completely empty (because no corrected data exists), and this may complicate the otherwise simple script. 
Therefore, I'm going to tell python, wherever D14C_1 is NaN, put in the data from D14C. 
"""

mtarray = []
mtarray2 = []
for i in range(0, len(df)):
    df_row = df.iloc[i]

    if pd.isna(df_row['D14C_1']) is True:
        mtarray.append(df_row['D14C'])
        mtarray2.append(df_row['D14Cerr'])
    else:
        mtarray.append(df_row['D14C_1'])
        mtarray2.append(df_row['weightedstderr_D14C_1'])

df['D14C_1'] = mtarray
df['weightedstderr_D14C_1'] = mtarray2
# df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/test.xlsx')
# Checked, it works!


"""
How is the data when viewed relative to reference 2 and reference 3? 
"""
# The difference between the CORRECTED samples, and REFERENCE 2, the harmonized reference (WEIGHTED RESIDUAL)
quaderr = np.sqrt(df['weightedstderr_D14C_1']**2 + df['D14C_ref2t_std']**2)

df['r2_diff_trend'] = df['D14C_1'] - df['D14C_ref2t_mean']
df['r2_diff_trend_errprop'] = np.sqrt(df['weightedstderr_D14C_1'] ** 2 + df['D14C_ref2t_std'] ** 2)

# The difference between the raw samples, and REFERENCE 3, BHD with CGO in the gaps (WEIGHTED RESIDUAL)
df['r3_diff_trend'] = df['D14C'] - df['D14C_ref3t_mean']
df['r3_diff_trend_errprop'] = np.sqrt(df['D14Cerr'] ** 2 + df['D14C_ref3t_std'] ** 2)

# And the difference between the two differences...
df['deltadelta'] = df['r2_diff_trend'] - df['r3_diff_trend']

df['deltadelta_err'] = np.sqrt(df['r2_diff_trend_errprop'] ** 2 + df['r3_diff_trend_errprop'] ** 2)
df_2 = df  # renaming for import into second analytical file
# df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/testing.xlsx')


"""
At a high-level, how does the raw data look? This will be the first plot to go into our paper...

"""

# SORT VALUES BY LATITUDE SO THEY APPEAR IN ORDER ON THE PLOTS LATER
df = df.sort_values(by=['NewLat', 'Decimal_date'], ascending=False).reset_index(drop=True)

# first we'll extract the data by country flags that we've added above
chile = df.loc[df['Country'] == 0].reset_index(drop=True)
chile['new_Lon'] = chile['Lon'] * -1

nz = df.loc[df['Country'] == 1].reset_index(drop=True)

# GETS "LOCS", LOCATIONS, WHILE PRESERVING LATITUDES IN PREVIOUSLY SORTED ORDER
# u, indices = np.unique(a, return_index=True) # https://numpy.org/doc/stable/reference/generated/numpy.unique.html
u1, locs1 = np.unique(chile['Site'], return_index=True)
temp = pd.DataFrame({"ind": u1, "locs":locs1}).sort_values(by=['locs'], ascending=True).reset_index(drop=True)
locs1 = temp['ind']
u2, locs2 = np.unique(nz['Site'], return_index=True)
temp2 = pd.DataFrame({"ind": u2, "locs":locs2}).sort_values(by=['locs'], ascending=True).reset_index(drop=True)
locs2 = temp2['ind']


# PREPARE THE FIGURE
# SELECT COLORS WE"LL USE FOR THE PAPER:
c1, c2, c3, c4, c5, c6, c7, c8 = '#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac'
colors = [c1, c2, c3, c4, c5, c6, c7, c8]
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D']
size1 = 8

fig = plt.figure(figsize=(12, 12))
gs = gridspec.GridSpec(4, 6)
gs.update(wspace=1, hspace=0.1)

site_array = []
lat_array = []
stat_array = []
mean_array = []
std_array = []
region_array = []
xtr_subsplot = fig.add_subplot(gs[0:2, 2:6])

# Hard coding it to get rid of a bug - a few sites aren't appearing for some reason..
for i in range(0, len(locs1)):
    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    print(slice)
    latitude = slice['NewLat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    x = stats.ttest_rel(slice['r2_diff_trend'], slice['r3_diff_trend'])
    stat_array.append(x[1])
    mean_array.append(np.nanmean(slice['r2_diff_trend']))
    std_array.append(np.nanstd(slice['r2_diff_trend']))
    lat_array.append(latitude)
    site_array.append(str(locs1[i]))
    region_array.append("Chile")
    plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

plt.text(1981.5, 14, '[B]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
plt.text(1976.5-20, 14, '[A]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
plt.ylim(-15, 15)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.xticks([], [])
plt.xlim(1980, 2020)
plt.axhline(0, color='black')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')


xtr_subsplot = fig.add_subplot(gs[2:4, 2:6])
for i in range(0, len(locs2)):
    slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    latitude = slice['NewLat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    x = stats.ttest_rel(slice['r2_diff_trend'], slice['r3_diff_trend'])
    stat_array.append(x[1])
    mean_array.append(np.nanmean(slice['r2_diff_trend']))
    std_array.append(np.nanstd(slice['r2_diff_trend']))
    lat_array.append(latitude)
    site_array.append(str(locs2[i]))
    region_array.append("NZ")
    plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

plt.ylim(-15, 15)
plt.text(1981.5, 14, '[D]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
plt.text(1976.5-20, 14, '[C]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
plt.xlim(1980, 2020)
plt.axhline(0, color='black')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.xlabel('Year of Growth')

# NOW DRAW THE MAPS
# SET MAP BOUNDARIES
maxlat = -30
minlat = -60
nz_max_lon = 185
nz_min_lon = 155
chile_max_lon = -55
chile_min_lon = -85
res = 'l'


"""
ADD THE MAPS TO THE PLOT
"""

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=chile_min_lon, urcrnrlon=chile_max_lon, resolution=res)
map.drawmapboundary(fill_color='lightgrey')
map.fillcontinents(color='darkgrey')
map.drawcoastlines(linewidth=0.1)
for i in range(0, len(locs1)):

    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    lat = slice['NewLat']
    lat = lat[0]
    lon = slice['new_Lon']
    lon = lon[0]
    x, y = map(lon, lat)
    print(x, y)
    map.scatter(x, y, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')
plt.legend()
map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], linewidth=0.5)

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution=res)
map.drawmapboundary(fill_color='lightgrey')
map.fillcontinents(color='darkgrey')
map.drawcoastlines(linewidth=0.1)


for i in range(0, len(locs2)):

    slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    lat = slice['NewLat']
    lat = lat[0]
    lon = slice['NewLon']
    lon = lon[0]
    x, y = map(lon, lat)
    print(x, y)
    map.scatter(x, y, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')
map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], linewidth=0.5)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/newmap.png',
            dpi=300, bbox_inches="tight")
plt.close()

results_array = pd.DataFrame({"Site": site_array, "Region": region_array, "Lat": lat_array, "Mean": mean_array, "Std": std_array, "Paired T-test p-value": stat_array})
# results_array.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/site_ttest.xlsx')


"""
Averaged across time, what does the data look like via latitude
"""

fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=1, hspace=0.5)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])

slice = results_array.loc[results_array['Region'] == 'Chile']
plt.errorbar(slice['Lat'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label="Chile", ls='none', fmt='o', color='black', ecolor='black', markeredgecolor='black')
plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.xticks([], [])
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.text(-60+2, 7, '[A] Chile', horizontalalignment='center', verticalalignment='center', fontweight="bold")

xtr_subsplot = fig.add_subplot(gs[2:4, 0:4])

slice = results_array.loc[results_array['Region'] == 'NZ']
plt.errorbar(slice['Lat'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label="New Zealand", ls='none', fmt='o', color='black', ecolor='black', markeredgecolor='black')
plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.xlabel('Latitude \u00B0N')
plt.text(-60+3, 7, '[B] New Zealand', horizontalalignment='center', fontweight="bold")


plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/MainFig2.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
Trying to get the symbols to match first figure
"""

fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=1, hspace=0.25)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])
chile = results_array.loc[results_array['Region'] == 'Chile']
for i in range(0, len(chile)):
    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    plt.errorbar(slice['Lat'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(slice['Site'])}", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.xticks([], [])
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.text(-60+2, 7, '[A] Chile', horizontalalignment='center', verticalalignment='center', fontweight="bold")

xtr_subsplot = fig.add_subplot(gs[2:4, 0:4])
chile = results_array.loc[results_array['Region'] == 'NZ']
for i in range(0, len(chile)):
    slice = chile.loc[chile['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    label = slice['Site']
    plt.errorbar(slice['Lat'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=label, ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.text(-60+3.5, 7, '[B] New Zealand', horizontalalignment='center', verticalalignment='center', fontweight="bold")

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/MainFig2.5.png',
            dpi=300, bbox_inches="tight")
plt.close()

