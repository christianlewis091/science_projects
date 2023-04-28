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
# print(len(df['deltadelta']))
# print(max(df['deltadelta']))
#
#
# print(np.average(df['deltadelta']))
# print(np.std(df['deltadelta']))

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
gs.update(wspace=1, hspace=.6)

site_array = []
lat_array = []
stat_array = []
mean_array = []
std_array = []
xtr_subsplot = fig.add_subplot(gs[0:2, 2:6])
for i in range(0, len(locs1)):

    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    latitude = slice['NewLat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    x = stats.ttest_rel(slice['r2_diff_trend'], slice['r3_diff_trend'])
    stat_array.append(x[1])
    mean_array.append(np.nanmean(slice['r2_diff_trend']))
    std_array.append(np.nanstd(slice['r2_diff_trend']))
    lat_array.append(latitude)
    site_array.append(str(locs1[i]))
    plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N, {str(locs1[i])}", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

plt.ylim(-15, 15)
plt.xticks([], [])
plt.xlim(1980, 2020)
plt.axhline(0, color='black')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - SHB1]')


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
    plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N, {str(locs2[i])}", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
plt.ylim(-15, 15)
plt.xlim(1980, 2020)
plt.axhline(0, color='black')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - SHB1]')

# NOW DRAW THE MAPS
# SET MAP BOUNDARIES
maxlat = -30
minlat = -60
nz_max_lon = 180
nz_min_lon = 160
chile_max_lon = -60
chile_min_lon = -80
res = 'l'

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
    map.scatter(x, y, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution=res)
map.drawmapboundary(fill_color='lightgrey')
map.fillcontinents(color='darkgrey')
map.drawcoastlines(linewidth=0.1)

for i in range(0, len(locs1)):

    slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    lat = slice['NewLat']
    lat = lat[0]
    lon = slice['NewLon']
    lon = lon[0]
    x, y = map(lon, lat)
    map.scatter(x, y)

plt.show()



results_array = pd.DataFrame({"Site": site_array, "Lat": lat_array, "Mean": mean_array, "Std": std_array, "Paired T-test p-value": stat_array})
# results_array.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/site_ttest.xlsx')
















































df_2 = df  # renaming for import into second analytical file











































"""
Break up the data by general latitude bands 
"""
# you can easily see the different latitude bands where the data falls in the 3D plot, see 3d3.png, or you can recreate
# it below and actually play around with moving the plot. I determined where to draw the bands based on this visual cue

b1 = df.loc[(df['NewLat'] > - 40) & (df['NewLat'] <= - 39)]
b2 = df.loc[(df['NewLat'] > - 42) & (df['NewLat'] < - 40)]
b3 = df.loc[(df['NewLat'] > - 44.25) & (df['NewLat'] < - 43)]
b4 = df.loc[(df['NewLat'] > - 47) & (df['NewLat'] < - 46)]
b5 = df.loc[(df['NewLat'] > - 48) & (df['NewLat'] < - 47)]
b6 = df.loc[(df['NewLat'] > - 53) & (df['NewLat'] < - 52)]
b7 = df.loc[(df['NewLat'] > - 54) & (df['NewLat'] < - 53)]
b8 = df.loc[(df['NewLat'] > - 55.5) & (df['NewLat'] < - 54)]
b9 = df.loc[(df['NewLat'] > - 60) & (df['NewLat'] < -55.5)]
b10 = df.loc[(df['NewLat'] > - 75) & (df['NewLat'] < -60)]

# See Plot 2 for the data based on the indexing above
# now we find the summary data based on each
# (This loop finds the mean and standard deviation of the b1-b9 above, and links it to a lat lon
datas = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10]
lats = [-40, -42, -44, -47, -48, -53, -54, -55, -60, -75] # The MAX LAT
mean_array_ref2 = []
std_error_array_ref2 = []
mean_array_ref3 = []
std_error_array_ref3 = []
stdev1 = []
stdev2 = []
for i in range(0, len(datas)):
    data = datas[i]  # grab first dataset
    mean1 = np.mean(data['r2_diff_trend'])
    mean2 = np.mean(data['r3_diff_trend'])
    stdevr1 = (np.std(data['r2_diff_trend']))
    stdevr2 = (np.std(data['r3_diff_trend']))
    mean_array_ref2.append(mean1)
    mean_array_ref3.append(mean2)
    stdev1.append(stdevr1)
    stdev2.append(stdevr2)



























