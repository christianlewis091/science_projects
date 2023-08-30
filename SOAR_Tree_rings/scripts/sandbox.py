"""
UPDATES:
8/30/23
Adding a "better" hysplit plot for vizualization of the data around the ACC fronts

5/5/23
Since we decided to split the paper into two sections during our April meeting with Erik and Sarah, the paper
has become significantly simpler. All analyses/plots will be contained in one TRUTH file, which is this one.
For best future reference, the sheet will follow the format of the paper.
"""

import numpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
from mpl_toolkits.basemap import Basemap
from X_my_functions import long_date_to_decimal_date
from sklearn.linear_model import LinearRegression

# read in the data from the previous .py files
df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/samples_with_references10000.xlsx')
ref2 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/harmonized_dataset.xlsx')
ref1 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/reference3.xlsx')
bhdcgo = pd.read_excel(r'H:\Science\Datasets\CGOvBHD.xlsx')
# ensure all data are sliced for after 1980.
df = df.loc[df['Decimal_date'] > 1980].reset_index(drop=True)
ref2 = ref2.loc[ref2['Decimal_date'] > 1980].reset_index(drop=True)
ref1 = ref1.loc[ref1['Decimal_date'] > 1980].reset_index(drop=True)

# I DON"T WANT TO PRESENT MCQ as a TREE RING SITE!
df = df.loc[df['Site'] != 'MCQ']

"""
FOR METHODS SECTION: DEVELOPMENT OF BACKGROUND REFERENCE: 
WE WANT TO SHOW THE DEVELOPMENT OF REFERENCE, WITH A MAP, AND PLOT OF THE DATA TOGETHER
"""

fig = plt.figure(figsize=(16, 4))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=.25, hspace=0.1)

# BHD MAP
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
maxlat = -40+20
minlat = -40-20
nz_max_lon = 180
nz_min_lon = 140
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='l')
map.drawmapboundary(fill_color='lightgrey')
map.fillcontinents(color='darkgrey')
map.drawcoastlines(linewidth=0.1)
x, y = map(174.866, -41.4)  # BARING HEAD
x2, y2 = map(144.6883, -40.6822)
map.scatter(x, y, marker='o', edgecolor='black', facecolors='black')
map.scatter(x2, y2, marker='D', edgecolor='black', facecolors='gray')
plt.legend()
map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], linewidth=0.5)


xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
plt.text(1979, 322, '[B]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
plt.text(1925, 322,  '[A]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
plt.text(2035, 322,  '[C]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
plt.title('Background Reference')
plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
plt.xlabel('Year')
cgo = ref1.loc[ref1['#location'] == 'CGO']
bhd = ref1.loc[ref1['#location'] != 'CGO']
plt.plot(df['Decimal_date'], df['D14C_ref3t_mean'], zorder=10, label='CCGCRV Trend Reference', color='black')
plt.errorbar(cgo['Decimal_date'], cgo['D14C'], yerr=cgo['weightedstderr_D14C'], fmt='D',  elinewidth=1, capsize=2, label='Heidelberg Uni. Cape Grim Record', color='dimgray',  markersize = 2, alpha=0.75)
plt.errorbar(bhd['Decimal_date'], bhd['D14C'], yerr=bhd['weightedstderr_D14C'], fmt='o',  elinewidth=1, capsize=2, label='RRL/NIWA Wellington Record', color='darkgray',  markersize =2, alpha=0.75)
plt.legend()

xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])

x = bhdcgo['Date']
x = long_date_to_decimal_date(x)
bhdcgo['Date'] = x
c = stats.ttest_rel(bhdcgo['BHD_D14C'], bhdcgo['CGO_D14C'])
plt.errorbar(bhdcgo['Date'], bhdcgo['BHD_D14C'], yerr=bhdcgo['standard deviation1'], fmt='o',  elinewidth=1, capsize=2, label='Baring Head measured by RRL/NIWA', color='black',  markersize = 4)
plt.errorbar(bhdcgo['Date'], bhdcgo['CGO_D14C'], yerr=bhdcgo['standard deviation2'], fmt='o',  elinewidth=1, capsize=2, label='Cape Grim measured by RRL/NIWA', color='gray',  markersize = 4)
plt.title('Site Intercomparison')
plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
plt.xlabel('Year')
plt.legend()
plt.locator_params(axis='x', nbins=4)
plt.xlim(2017, 2019)
# plt.close()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/NewFig1.png',
            dpi=300, bbox_inches="tight")
plt.close()


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
        x = 1
        # print(current_row)
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
df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/test.xlsx')
# ?


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

# see DiscEqn 9
D_ocean = -150
D_err = 30

df['testrat'] = (df['D14C'] - D_ocean) / (df['D14C_ref3t_mean'] - D_ocean)

testrat_e1 = np.sqrt(df['D14C']**2 + D_err**2)
testrat_e2 = np.sqrt(df['D14C_ref3t_mean']**2 + D_err**2)

step1 = ((testrat_e1)/ (df['D14C'] - D_ocean))**2
step2 = ((testrat_e2)/ (df['D14C_ref3t_mean'] - D_ocean))**2
step3 = (df['D14C'] - D_ocean) / (df['D14C_ref3t_mean'] - D_ocean) *  np.sqrt(step1 + step2)
df['testrat_err'] = step3

# df['testrat_err'] = df['testrat'] * [np.sqrt(testrat_e1**2 / (df['D14C'] - D_ocean)) +  np.sqrt( testrat_e2**2 /(df['D14C_ref3t_mean'] - D_ocean))]

df = df.loc[df['Site'] != 'NMY']
df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/final_results.xlsx')


"""
Lets test the difference between the two sites
"""
df_testing = df.loc[(df['Decimal_date'] >1987) & (df['Decimal_date'] <1994)]
#df_testing.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/achecks.xlsx')

stat=[]
pval=[]
site=[]
blahs = np.unique(df_testing['Site'])

for i in range(0, len(blahs)):
    blah_data = df_testing.loc[df_testing['Site'] == blahs[i]]
    if len(blah_data) > 1:
        a = blah_data['r2_diff_trend'].dropna()
        b = blah_data['r3_diff_trend'].dropna()
        x = stats.ttest_ind(a,b)
        stat.append(x[0])
        pval.append(x[1])
        site.append(blahs[i])
p_resultsss = pd.DataFrame({"Site": site, "Stat": stat, "P-value": pval})
# print(p_resultsss)
p_resultsss.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/p_results.xlsx')

"""
AT THIS POINT I WRITE THAT REF 1 will be USED FROM NOW ON!

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
testrat_arr = []
testrat_err_arr = []
xtr_subsplot = fig.add_subplot(gs[0:2, 2:6])

for i in range(0, len(locs1)):
    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    # print(slice)
    latitude = slice['NewLat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    x = stats.ttest_rel(slice['r2_diff_trend'], slice['r3_diff_trend'])
    stat_array.append(x[1])
    mean_array.append(np.nanmean(slice['r3_diff_trend']))
    std_array.append(np.nanstd(slice['r3_diff_trend']))
    testrat_arr.append(np.nanmean(slice['testrat']))
    testrat_err_arr.append(np.nanmean(slice['testrat_err']))
    lat_array.append(latitude)
    site_array.append(str(locs1[i]))
    region_array.append("Chile")
    # Errorbars removed after meeting with JT ap[ril 23
    # plt.errorbar(slice['Decimal_date'], slice['r3_diff_trend'], slice['r3_diff_trend_errprop'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
    plt.errorbar(slice['Decimal_date'], slice['r3_diff_trend'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

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
    mean_array.append(np.nanmean(slice['r3_diff_trend']))
    std_array.append(np.nanstd(slice['r3_diff_trend']))
    testrat_arr.append(np.nanmean(slice['testrat']))
    testrat_err_arr.append(np.nanmean(slice['testrat_err']))
    lat_array.append(latitude)
    site_array.append(str(locs2[i]))
    region_array.append("NZ")
    # Removed errorbars May 23 after meeting with JT
    # plt.errorbar(slice['Decimal_date'], slice['r3_diff_trend'], slice['r3_diff_trend_errprop'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
    plt.errorbar(slice['Decimal_date'], slice['r3_diff_trend'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')


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
    # print(x, y)
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
    # print(x, y)
    map.scatter(x, y, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')
map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], linewidth=0.5)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/newmap.png',
            dpi=300, bbox_inches="tight")
plt.close()

results_array = pd.DataFrame({"Site": site_array, "Region": region_array, "Lat": lat_array, "Mean": mean_array, "Std": std_array, "F_B": testrat_arr, "F_B_error": testrat_err_arr})
results_array.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/site_ttest.xlsx')


"""
PLOTTING THE AVERAGES> Trying to get the symbols to match first figure
"""

fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=1, hspace=0.25)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])
chile1 = results_array.loc[results_array['Region'] == 'Chile']
for i in range(0, len(chile1)):
    slice = chile1.loc[chile1['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    plt.errorbar(slice['Lat'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(slice['Site'])}", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.xticks([], [])
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.text(-60+2, 7, '[A] Chile', horizontalalignment='center', verticalalignment='center', fontweight="bold")

xtr_subsplot = fig.add_subplot(gs[2:4, 0:4])
chile1 = results_array.loc[results_array['Region'] == 'NZ']
for i in range(0, len(chile1)):
    slice = chile1.loc[chile1['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    label = slice['Site']
    plt.errorbar(slice['Lat'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=label, ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.xlabel('Latitude (N)')
plt.text(-60+3.5, 7, '[B] New Zealand', horizontalalignment='center', verticalalignment='center', fontweight="bold")

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/MainFig2.5.png',
            dpi=300, bbox_inches="tight")
plt.close()


"""
Compare the two navarino's
"""



maxlat = -54
minlat = -56
chile_max_lon = -66
chile_min_lon = -70
res = 'i'
x = 5
fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=1, hspace=0.35)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=chile_min_lon, urcrnrlon=chile_max_lon, resolution=res)
map.drawmapboundary(fill_color='lightgrey')
map.fillcontinents(color='darkgrey')
map.drawcoastlines(linewidth=0.1)


x, y = map(-68.32, -54.92472)
map.scatter(x, y,  marker='X', color='#4393c3', s=60, edgecolor='black',label="Puerto Navarino")

x2, y2 = map(-67.43917, -54.92639)
map.scatter(x2, y2,  marker='D', color='#2166ac', s=60, edgecolor='black',label="Baja Rosales")

x3, y3 = map(-68.3030, -54.8019)
map.scatter(x3, y3,  marker='o', color='goldenrod', s=60, edgecolor='black', label='Ushuaia, Argentina')
# plt.text(x3, y3+0.15, 'Ushuaia', fontsize=14, fontweight="bold")
plt.legend()

map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], linewidth=0.5)
# map.shadedrelief()
# map.drawcoastlines()
map.drawparallels(np.arange(-90, 90, 0.5), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 1), labels=[1, 1, 0, 1], linewidth=0.5)


xtr_subsplot = fig.add_subplot(gs[2:4, 0:4])
slice1 = chile.loc[chile['Site'] == 'Puerto Navarino, Isla Navarino'].reset_index(drop=True)  # grab the first data to plot, based on location

plt.errorbar(slice1['Decimal_date'], slice1['r3_diff_trend'], slice1['r3_diff_trend_errprop'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"-54.9N; Puerto Navarino, Isla Navarino; n={len(slice1)}", ls='none', fmt='X', color='#4393c3', ecolor='#4393c3', markeredgecolor='black')

slice2 = chile.loc[chile['Site'] == 'Baja Rosales, Isla Navarino'].reset_index(drop=True)  # grab the first data to plot, based on location

plt.errorbar(slice2['Decimal_date'], slice2['r3_diff_trend'], slice2['r3_diff_trend_errprop'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"-54.9N; Baja Rosales, Isla Navarino; n={len(slice2)}", ls='none', fmt='D', color='#2166ac', ecolor='#2166ac', markeredgecolor='black')

c = stats.ttest_ind(slice1['r3_diff_trend'], slice2['r3_diff_trend'])
print(c)



plt.ylim(-10, 10)
plt.xlim(1980, 2020)
plt.axhline(0, color='black')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.text(1982, 11, '[B]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
plt.text(1982, 34,  '[A]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")

# plt.show()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Navarino.png',
            dpi=300, bbox_inches="tight")
plt.close()


"""
I'm working on the results section and want to plot the Chile average data with a linear regression and fill-between the 1-sigma. I want to do this if I also remove the two driving sites. 
"""
# c1, c2, c3, c4, c5, c6, c7, c8 = '#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac'
# colors = [c1, c2, c3, c4, c5, c6, c7, c8]
# markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D']
maxlat = -42
minlat = -46
nz_max_lon = 185
nz_min_lon = 155
chile_max_lon = -72
chile_min_lon = -75
res = 'i'
x = 5
fig = plt.figure()

map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=chile_min_lon, urcrnrlon=chile_max_lon, resolution=res)

x, y = map(-72.94694, -43.79)
map.scatter(x, y,  marker='^', color='#d6604d', s=180, edgecolor='black', alpha=1)

map.drawparallels(np.arange(-90, 90, 1), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 1), labels=[1, 1, 0, 1], linewidth=0.5)
map.shadedrelief()
map.drawcoastlines()
map.drawparallels(np.arange(-90, 90, 1), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 1), labels=[1, 1, 0, 1], linewidth=0.5)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/RaulMarin.png',
            dpi=300, bbox_inches="tight")
plt.close()


maxlat = -53.7+2
minlat = -53.7-2
nz_max_lon = -70.97+2
nz_min_lon = -70.97-2
chile_max_lon = -70.97+2
chile_min_lon = -70.97-2
res = 'i'
x = 5
fig = plt.figure()

map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=chile_min_lon, urcrnrlon=chile_max_lon, resolution=res)

x, y = map(-70.97, -53.7)
map.scatter(x, y,  marker='*', color='#4393c3', s=180, edgecolor='black', alpha=1)

map.drawparallels(np.arange(-90, 90, 1), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 1), labels=[1, 1, 0, 1], linewidth=0.5)
map.shadedrelief()
map.drawcoastlines()
map.drawparallels(np.arange(-90, 90, 1), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 1), labels=[1, 1, 0, 1], linewidth=0.5)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/MonteTarn.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
At the NIWA meeting on May 25, they discussed doing 5 year averages of the data to smooth inconsistent sampling rates
"""
labels = []
num_labels=[]
for i in range(0, len(df)):
    row = df.iloc[i]
    dd = row['Decimal_date']
    site = str(row['Site'])
    if 1980 < dd <= 1985:
        labels.append(f'Interval1_{site}')
    elif 1985 < dd <= 1990:
        labels.append(f'Interval2_{site}')
    elif 1990 < dd <= 1995:
        labels.append(f'Interval3_{site}')
    elif 1995 < dd <= 2000:
        labels.append(f'Interval4_{site}')
    elif 2000 < dd <= 2005:
        labels.append(f'Interval5_{site}')
    elif 2005 < dd <= 2010:
        labels.append(f'Interval6_{site}')
    elif 2010 < dd <= 2015:
        labels.append(f'Interval7_{site}')
    elif 2015 < dd <= 2021:
        labels.append(f'Interval7_{site}')
    else:
        labels.append('Error')

df['Interval_labels'] = labels
five_year_means = df.groupby('Interval_labels').mean('r3_diff_trend').reset_index()
five_year_means.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/five_year_means.xlsx')

# From the above code, we have 5-year averages for each site. But now we want the WHOLE temporal average
# What do we use to index, since the groupby.mean removes the sites, since they're strings? We can use the unique
# latitudes from each site.
full_temporal_means = df.groupby('Lat').mean('r3_diff_trend').reset_index()
full_temporal_means.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/full_temporal_5_year_means.xlsx')

# and now we'll re-make plot Main2.5

"""
PLOTTING THE AVERAGES> Trying to get the symbols to match first figure
"""

fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=1, hspace=0.25)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])
chile1 = results_array.loc[results_array['Region'] == 'Chile']
chile2 = full_temporal_means.loc[full_temporal_means['Country'] == 0]
nz2 = full_temporal_means.loc[full_temporal_means['Country'] == 1]
for i in range(0, len(chile1)):
    slice = chile1.loc[chile1['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    plt.errorbar(slice['Lat'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(slice['Site'])}", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

plt.scatter(chile2['Lat'], chile2['r3_diff_trend'], color='black', s=100, alpha=0.5)
plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.xticks([], [])
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.text(-60+2, 7, '[A] Chile', horizontalalignment='center', verticalalignment='center', fontweight="bold")

xtr_subsplot = fig.add_subplot(gs[2:4, 0:4])
chile1 = results_array.loc[results_array['Region'] == 'NZ']
for i in range(0, len(chile1)):
    slice = chile1.loc[chile1['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    label = slice['Site']
    plt.errorbar(slice['Lat'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=label, ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
plt.scatter(nz2['Lat'], nz2['r3_diff_trend'], color='black', s=100, alpha=0.5)
plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.xlabel('Latitude (N)')
plt.text(-60+3.5, 7, '[B] New Zealand', horizontalalignment='center', verticalalignment='center', fontweight="bold")
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/MainFig2.5_w_bkgd_averages.png',
            dpi=300, bbox_inches="tight")
plt.close()



"""
Plotting the main figures against the LandFrac
"""
# IMPORT LANDFRAC DATA FROM HYSPLIT WORK
landfrac = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data//landfracresults_edited.xlsx').reset_index(drop=True)
times = [0, -4, -8, -12, -16, -20]
timelabel = ['zero','four','eight','twelve','sixteen','twenty']


for m in range(0, len(times)):
    landfrac_slice = landfrac.loc[landfrac['timestep'] == int(times[m])]


    fig = plt.figure(figsize=(8, 8))
    gs = gridspec.GridSpec(4, 4)
    gs.update(wspace=1, hspace=0.35)

    xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])
    plt.title('Chile')
    chile1 = results_array.loc[results_array['Region'] == 'Chile']
    for i in range(0, len(chile1)):
        slice = chile1.loc[chile1['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
        landfrac_slice2 = landfrac_slice.loc[landfrac_slice['location'] == str(locs1[i])]
        plt.errorbar(landfrac_slice2['LandFrac'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(slice['Site'])}", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

    plt.xlim(0, 1)
    plt.xticks([], [])
    plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')

    xtr_subsplot = fig.add_subplot(gs[2:4, 0:4])
    plt.title('New Zealand')
    chile1 = results_array.loc[results_array['Region'] == 'NZ']
    for i in range(0, len(chile1)):
        slice = chile1.loc[chile1['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
        landfrac_slice3 = landfrac_slice.loc[landfrac_slice['location'] == str(locs2[i])]
        label = slice['Site']
        plt.errorbar(landfrac_slice3['LandFrac'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=label, ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
    plt.xlabel(f'Fraction of trajectory over land, {timelabel[m]} hours')
    plt.xlim(0, 1)
    plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/MainFig2_wLandFRac_{timelabel[m]}.png',
                dpi=300, bbox_inches="tight")
    plt.close()

#

"""
MAPP OF ACC FRONTS
"""
# LOAD HYSPLOT DATA
easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/easy_access2 - Copy.xlsx')

# ADDING PROPER SITE NAMES FOR THE FOLLOWING LOOP TO READ
year = ['2005_2006', '2010_2011','2015_2016','2020_2021']

# LOAD ACC FRONTS DATA
acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
fronts = np.unique(acc_fronts['front_name'])

for k in range(0, len(year)):
    means_dataframe_100 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_{year[k]}.xlsx')
    # ADDING PROPER SITE NAMES FOR THE FOLLOWING LOOP TO READ
    means_dataframe_100 = means_dataframe_100.merge(easy_access)
    # SEE hysplit_make_plots_GNS.py
    timemin = -(6*24)
    means_dataframe_100 = means_dataframe_100.loc[means_dataframe_100['timestep'] > timemin]
    # fronts = ['PF','SAF','STF']
    map = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
    map.drawmapboundary(fill_color='lightgrey')
    map.fillcontinents(color='darkgrey')
    map.drawcoastlines(linewidth=0.1)
    #
    # PLOTTING THE ACC FRONTS
    for i in range(0, len(fronts)):
        this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]

        chile_lat = this_one['latitude']
        chile_lon = this_one['longitude']
        print(type(chile_lon))
        z, a = map(list(chile_lon), list(chile_lat))

        map.plot(z, a, color='black', label=f'{fronts[i]}')

    # PLOTTING CHILEAN SITES
    for i in range(0, len(locs1)):
        slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
        lat = slice['NewLat']
        lat = lat[0]
        lon = slice['new_Lon']
        lon = lon[0]
        x, y = map(lon, lat)
        map.scatter(x, y, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')
        print(locs1[i])

        site_mean_100 = means_dataframe_100.loc[means_dataframe_100['Site'] == str(locs1[i])].reset_index(drop=True)
        chile_lat = site_mean_100['y']
        chile_lon = site_mean_100['x']
        print(type(chile_lon))
        z, a = map(list(chile_lon), list(chile_lat))

        map.plot(z, a, color=colors[i])

    # PLOTTING NZ SITES
    for i in range(0, len(locs2)):

        slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
        lat = slice['NewLat']
        lat = lat[0]
        lon = slice['NewLon']
        lon = lon[0]
        x, y = map(lon, lat)
        # print(x, y)
        map.scatter(x, y, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')


        site_mean_100 = means_dataframe_100.loc[means_dataframe_100['Site'] == str(locs2[i])].reset_index(drop=True)
        chile_lat = site_mean_100['y']
        chile_lon = site_mean_100['x']
        print(type(chile_lon))
        z, a = map(list(chile_lon), list(chile_lat))
        map.plot(z, a, color=colors[i])

    map.drawparallels(np.arange(-90, 90, 10), labels=[False, False, False, False], fontsize=7, linewidth=0.5)
    map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/ACC_map_{year[k]}.png',
                dpi=300, bbox_inches="tight")
    plt.close()

#
#
#







# from mpl_toolkits.basemap import Basemap
# import numpy as np
# import matplotlib.pyplot as plt
#
# acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
# fronts = np.unique(acc_fronts['front_name'])
#
# # lon_0, lat_0 are the center point of the projection.
# # resolution = 'l' means use low resolution coastlines.
# m = Basemap(projection='ortho',lon_0=-105,lat_0=-90,resolution='l')
# m.drawcoastlines()
# m.fillcontinents(color='coral',lake_color='aqua')
#
# for i in range(0, len(fronts)):
#     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#     xs = this_one['latitude']
#     ys = this_one['longitude']
#
#     z, a = map(ys, xs)
#
#     map.scatter(z, a, label=f'{fronts[i]}')
#
#
# m.drawmapboundary(fill_color='aqua')
# plt.title("Full Disk Orthographic Projection")
# plt.show()





