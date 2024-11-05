"""
UPDATES:

8/30/23
Adding a "better" hysplit plot for vizualization of the data around the ACC fronts

5/5/23
Since we decided to split the paper into two sections during our April meeting with Erik and Sarah, the paper
has become significantly simpler. All analyses/plots will be contained in one TRUTH file, which is this one.
For best future reference, the sheet will follow the format of the paper.

"""
# This is a test to see if my new commit works, on my new GNS PC. If this works, I think I'll be pretty much set up to continue working.
print('This is a test')

import numpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
from mpl_toolkits.basemap import Basemap
from X_my_functions import long_date_to_decimal_date
from matplotlib.patches import Polygon
from sklearn.linear_model import LinearRegression
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# read in the data from the previous .py files
df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference_to_sample_xvals2/samples_with_references10000.xlsx')
print(len(df))

df = df.loc[df['Site'] != 'Macquarie_Isl.'] # REMOVE IF WANT TO MAKE A CMP TO MQA COMPARISON PLOT LATER

df = df.sort_values(by=['DecimalDate'])
ref2 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference2/harmonized_dataset.xlsx')
ref1 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference1/reference1.xlsx')
bhdcgo = pd.read_excel(r'H:\Science\Datasets\CGOvBHD.xlsx')

# ensure all data are sliced for after 1980.
df = df.loc[df['DecimalDate'] > 1980].reset_index(drop=True)
ref2 = ref2.loc[ref2['Decimal_date'] > 1980].reset_index(drop=True)
ref1 = ref1.loc[ref1['Decimal_date'] > 1980].reset_index(drop=True)

# I DON"T WANT TO PRESENT MCQ as a TREE RING SITE!
df = df.loc[df['Site'] != 'MCQ']
# December 4, 2023: Removing Kapuni and RMB after notes from JT (or until we re-measure some of the cores)
df = df.loc[df['Site'] != 'Raul Marin Balmaceda']
df = df.loc[df['Site'] != 'near Kapuni school field, NZ']

print(len(df))

"""
FOR METHODS SECTION: DEVELOPMENT OF BACKGROUND REFERENCE: 
WE WANT TO SHOW THE DEVELOPMENT OF REFERENCE, WITH A MAP, AND PLOT OF THE DATA TOGETHER
"""

fig = plt.figure(figsize=(16, 4))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=.15, hspace=0.1)

# BHD MAP
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
maxlat = -40+20
minlat = -40-20
nz_max_lon = 180
nz_min_lon = 140
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='l')
# map.drawmapboundary(fill_color='lightgrey')
# map.fillcontinents(color='darkgrey')
# map.drawcoastlines(linewidth=0.1)
# map.drawmapboundary(fill_color='lightgrey')
# map.fillcontinents(color='darkgrey')
map.shadedrelief()
map.drawcoastlines(linewidth=0.1)
x, y = map(174.866, -41.4)  # BARING HEAD
x2, y2 = map(144.6883, -40.6822)
map.scatter(x, y, marker='o', edgecolor='black', facecolors='red')
map.scatter(x2, y2, marker='D', edgecolor='black', facecolors='blue')
plt.legend()
map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], linewidth=0.5)

xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# plt.text(1979, 322, '[B]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
# plt.text(1925, 322,  '[A]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
# plt.text(2035, 322,  '[C]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
plt.title('Background Reference')
plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
plt.xlabel('Year')
cgo = ref1.loc[ref1['#location'] == 'CGO']
bhd = ref1.loc[ref1['#location'] != 'CGO']

plt.plot(df['DecimalDate'], df['D14C_ref3t_mean'], zorder=10, label='CCGCRV Trend Reference', color='black')
plt.errorbar(cgo['Decimal_date'], cgo['D14C'], yerr=cgo['weightedstderr_D14C'], fmt='D',  elinewidth=1, capsize=2, label='Heidelberg Uni. Cape Grim Record', color='blue',  markersize = 2, alpha=0.75)
plt.errorbar(bhd['Decimal_date'], bhd['D14C'], yerr=bhd['weightedstderr_D14C'], fmt='o',  elinewidth=1, capsize=2, label='RRL/NIWA Wellington Record', color='red',  markersize =2, alpha=0.75)
plt.legend()

xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])

x = bhdcgo['Date']
x = long_date_to_decimal_date(x)
bhdcgo['Date'] = x
c = stats.ttest_rel(bhdcgo['BHD_D14C'], bhdcgo['CGO_D14C'])
plt.errorbar(bhdcgo['Date'], bhdcgo['BHD_D14C'], yerr=bhdcgo['standard deviation1'], fmt='o',  elinewidth=1, capsize=2, label='Baring Head measured by RRL/NIWA', color='green',  markersize = 4)
plt.errorbar(bhdcgo['Date'], bhdcgo['CGO_D14C'], yerr=bhdcgo['standard deviation2'], fmt='o',  elinewidth=1, capsize=2, label='Cape Grim measured by RRL/NIWA', color='purple',  markersize = 4)
plt.title('Site Intercomparison')
plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
plt.xlabel('Year')
plt.legend()
plt.locator_params(axis='x', nbins=4)
plt.xlim(2017, 2019)
# plt.close()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/NewFig1.png',
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
    elif current_row['Site'] == 'Eastbourne 1, NZ':
        lat_array.append(-41.2923)
        lon_array.append(174.8971)  # change Chilean Longitudes to degrees East.
    elif current_row['Site'] == 'Eastbourne 2, NZ':
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

Update: The above section is not valid because we are only including Tree Rings and not NEU and MCQ data any more. 
"""

# mtarray = []
# mtarray2 = []
# for i in range(0, len(df)):
#     df_row = df.iloc[i]
#
#     if pd.isna(df_row['D14C_1']) is True:
#         mtarray.append(df_row['D14C'])
#         mtarray2.append(df_row['D14Cerr'])
#     else:
#         mtarray.append(df_row['D14C_1'])
#         mtarray2.append(df_row['weightedstderr_D14C_1'])
#
# df['D14C_1'] = mtarray
# df['weightedstderr_D14C_1'] = mtarray2
# df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/test.xlsx')
# ?
# renaming columns as a workaround for removing the above code block
df = df.rename(columns={'∆14C':'D14C_1'})
df = df.rename(columns = {'∆14Cerr':'weightedstderr_D14C_1'})


"""
How is the data when viewed relative to reference 2 and reference 3? 
"""
# The difference between the data, and REFERENCE 2, the harmonized reference (WEIGHTED RESIDUAL)
quaderr = np.sqrt(df['weightedstderr_D14C_1']**2 + df['D14C_ref2t_std']**2)

df['r2_diff_trend'] = df['D14C_1'] - df['D14C_ref2t_mean']
df['r2_diff_trend_errprop'] = np.sqrt(df['weightedstderr_D14C_1'] ** 2 + df['D14C_ref2t_std'] ** 2)

# The difference between the data, and REFERENCE 1, BHD with CGO in the gaps (WEIGHTED RESIDUAL)
df['r3_diff_trend'] = df['D14C_1'] - df['D14C_ref3t_mean']
df['r3_diff_trend_errprop'] = np.sqrt(df['weightedstderr_D14C_1'] ** 2 + df['D14C_ref3t_std'] ** 2)

# And the difference between the two differences...
df['deltadelta'] = df['r2_diff_trend'] - df['r3_diff_trend']

df['deltadelta_err'] = np.sqrt(df['r2_diff_trend_errprop'] ** 2 + df['r3_diff_trend_errprop'] ** 2)
df_2 = df  # renaming for import into second analytical file

# see DiscEqn 9
D_ocean = -150
D_err = 30

df['testrat'] = (df['D14C_1'] - D_ocean) / (df['D14C_ref3t_mean'] - D_ocean)


testrat_e1 = np.sqrt(df['D14C_1']**2 + D_err**2)
testrat_e2 = np.sqrt(df['D14C_ref3t_mean']**2 + D_err**2)

step1 = ((testrat_e1)/ (df['D14C_1'] - D_ocean))**2
step2 = ((testrat_e2)/ (df['D14C_ref3t_mean'] - D_ocean))**2
step3 = (df['D14C_1'] - D_ocean) / (df['D14C_ref3t_mean'] - D_ocean) *  np.sqrt(step1 + step2)
df['testrat_err'] = step3

# df['testrat_err'] = df['testrat'] * [np.sqrt(testrat_e1**2 / (df['D14C'] - D_ocean)) +  np.sqrt( testrat_e2**2 /(df['D14C_ref3t_mean'] - D_ocean))]

df = df.loc[df['Site'] != 'NMY']

# trying out removing the one hihg outlier in Kapuni
# df = df.loc[df['r3_diff_trend'] <= 10]

df = df.sort_values(by=['Site','DecimalDate'])
df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/final_results.xlsx')



"""
Lets test the difference between the two sites
"""
df_testing = df.loc[(df['DecimalDate'] >1987) & (df['DecimalDate'] <1994)]
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
p_resultsss.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/p_results.xlsx')


"""
12/12/2023
Need to make the new plot to compare CMP and MCQ before I remove mcquarie island for the tree-ring plots. 
Even though the MCQ figure will be last
"""
fig = plt.figure(figsize=(12, 12))
sites = np.unique(df['Site'])
for m in range(0, len(sites)):
    thisonee = df.loc[df['Site'] == sites[i]]
    plt.plot(thisonee['DecimalDate'], thisonee['r3_diff_trend'])

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/cmp_mcq.png',
            dpi=300, bbox_inches="tight")




"""
AT THIS POINT I WRITE THAT REF 1 will be USED FROM NOW ON!
At a high-level, how does the raw data look? This will be the first plot to go into our paper...
"""

# SORT VALUES BY LATITUDE SO THEY APPEAR IN ORDER ON THE PLOTS LATER
df = df.sort_values(by=['NewLat', 'DecimalDate'], ascending=False).reset_index(drop=True)

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
    plt.errorbar(slice['DecimalDate'], slice['r3_diff_trend'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

plt.text(1981.5, 14, '[B]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
plt.text(1976.5-20, 14, '[A]', horizontalalignment='center', verticalalignment='center', fontsize=14, fontweight="bold")
plt.ylim(-15, 15)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.xticks([], [])
plt.xlim(1980, 2020)
plt.axhline(0, color='black')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.xlabel('Year of Growth')


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
    plt.errorbar(slice['DecimalDate'], slice['r3_diff_trend'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')


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
map.shadedrelief()

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

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/newmap.png',
            dpi=300, bbox_inches="tight")
plt.close()

results_array = pd.DataFrame({"Site": site_array, "Region": region_array, "Lat": lat_array, "Mean": mean_array, "Std": std_array, "F_B": testrat_arr, "F_B_error": testrat_err_arr})
results_array.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/summary_means.xlsx')

nz1 =  results_array.loc[results_array['Region'] == 'NZ']
nz1_x = nz1['Lat']
nz1_x = np.array(nz1_x)
nz1_y = nz1['Mean']
nz1_y = np.array(nz1_y)

ch1 =  results_array.loc[results_array['Region'] == 'Chile']
ch1_x = ch1['Lat']
ch1_x = np.array(ch1_x)
ch1_y = ch1['Mean']
ch1_y = np.array(ch1_y)

# regress the data
slope, intercept, rvalue, pvalue, stderr = stats.linregress(ch1_x, ch1_y)
sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(nz1_x, nz1_y)
#
# I just want the line to go across the plot for easier vizualization...
# ch1_x = np.append(ch1_x, -60)
# ch1_x = np.append(ch1_x, -35)
# nz1_x = np.append(nz1_x, -60)
# nz1_x = np.append(nz1_x, -35)
#
# ax5.plot(ch_x, slope*ch_x+intercept, color='gray')
# ax6.plot(nz_x, sslope*nz_x+sintercept, color='gray')
#
print("ChileMEANS: y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2))
print("NZMEANS: y=%.3fx+%.3f\R$^2$=%.3f"%(sslope, sintercept,srvalue**2))

# what is the CHILE_MEAN_regresiion without Monte Tarn?
ch2 =  results_array.loc[(results_array['Region'] == 'Chile') & (results_array['Site'] != 'Monte Tarn, Punta Arenas, CH')]
ch2_x = ch2['Lat']
ch2_x = np.array(ch2_x)
ch2_y = ch2['Mean']
ch2_y = np.array(ch2_y)
slope, intercept, rvalue, pvalue, stderr = stats.linregress(ch2_x, ch2_y)
print("ChileMEANS_NOTARN: y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2))

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
    # plt.plot(ch1_x, slope*ch1_x+intercept, color='gray', alpha=0.05)
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
    # plt.plot(nz1_x, sslope*nz1_x+sintercept, color='gray', alpha=0.05)
#
plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.xlabel('Latitude (N)')
plt.text(-60+3.5, 7, '[B] New Zealand', horizontalalignment='center', verticalalignment='center', fontweight="bold")

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/MainFig2.5.png',
            dpi=300, bbox_inches="tight")
plt.close()


"""
Compare the two navarino's
"""



maxlat = -54
minlat = -56
chile_max_lon = -66
chile_min_lon = -70
res = 'h'
x = 5
fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=1, hspace=0.35)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=chile_min_lon, urcrnrlon=chile_max_lon, resolution=res)
# map.drawmapboundary(fill_color='lightgrey')
# map.fillcontinents(color='darkgrey')
# map.drawcoastlines(linewidth=0.1)


x, y = map(-68.32, -54.92472)
map.scatter(x, y,  marker='o', color='lightgreen', s=60, edgecolor='black',label="Puerto Navarino")

x2, y2 = map(-67.43917, -54.92639)
map.scatter(x2, y2,  marker='D', color='purple', s=60, edgecolor='black',label="Baja Rosales")

x3, y3 = map(-68.3030, -54.8019)
map.scatter(x3, y3,  marker='o', color='goldenrod', s=60, edgecolor='black', label='Ushuaia, Argentina')
# plt.text(x3, y3+0.15, 'Ushuaia', fontsize=14, fontweight="bold")
plt.legend()

map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], linewidth=0.5)
map.shadedrelief()
# map.drawcoastlines()
map.drawparallels(np.arange(-90, 90, 0.5), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 1), labels=[1, 1, 0, 1], linewidth=0.5)


xtr_subsplot = fig.add_subplot(gs[2:4, 0:4])
slice1 = chile.loc[chile['Site'] == 'Puerto Navarino, Isla Navarino, CH'].reset_index(drop=True)  # grab the first data to plot, based on location
pn = np.mean(slice1['r3_diff_trend'])
std = np.std(slice1['r3_diff_trend'])
print(f'PN mean is {pn}, std is {std}')

plt.errorbar(slice1['DecimalDate'], slice1['r3_diff_trend'], slice1['r3_diff_trend_errprop'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"-54.9N; Puerto Navarino, Isla Navarino; n={len(slice1)}", ls='none', fmt='o', color='lightgreen', ecolor='#4393c3', markeredgecolor='black')

slice2 = chile.loc[chile['Site'] == 'Baja Rosales, Isla Navarino, CH'].reset_index(drop=True)  # grab the first data to plot, based on location
pn = np.mean(slice2['r3_diff_trend'])
std = np.std(slice2['r3_diff_trend'])
print(f'BR mean is {pn}, std is {std}')
plt.errorbar(slice2['DecimalDate'], slice2['r3_diff_trend'], slice2['r3_diff_trend_errprop'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"-54.9N; Baja Rosales, Isla Navarino; n={len(slice2)}", ls='none', fmt='D', color='purple', ecolor='#2166ac', markeredgecolor='black')


print('')
print('Is there a difference between Puerto Navarino and Baja Rosales? Null Hypothesis says: theres no difference!')
c = stats.ttest_ind(slice1['r3_diff_trend'], slice2['r3_diff_trend'])
print(c)
print('the datas p-value is 0.07 or 7%')


plt.ylim(-10, 10)
plt.xlim(1980, 2020)
plt.axhline(0, color='black')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')

# plt.show()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/Navarino.png',
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

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/RaulMarin.png',
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

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/MonteTarn.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
At the NIWA meeting on May 25, they discussed doing 5 year averages of the data to smooth inconsistent sampling rates
"""
labels = []
num_labels=[]
for i in range(0, len(df)):
    row = df.iloc[i]
    dd = row['DecimalDate']
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
five_year_means.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/five_year_means.xlsx')

# From the above code, we have 5-year averages for each site. But now we want the WHOLE temporal average
# What do we use to index, since the groupby.mean removes the sites, since they're strings? We can use the unique
# latitudes from each site.
full_temporal_means = df.groupby('Lat').mean('r3_diff_trend').reset_index()
full_temporal_means.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/full_temporal_5_year_means.xlsx')

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
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/MainFig2.5_w_bkgd_averages.png',
            dpi=300, bbox_inches="tight")
plt.close()


#
# """
# Plotting the main figures against the LandFrac
# """
# # IMPORT LANDFRAC DATA FROM HYSPLIT WORK
# landfrac = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/landfracresults_edited.xlsx').reset_index(drop=True)
# times = [0, -4, -8, -12, -16, -20]
# timelabel = ['zero','four','eight','twelve','sixteen','twenty']
#
#
# for m in range(0, len(times)):
#     landfrac_slice = landfrac.loc[landfrac['timestep'] == int(times[m])]
#
#     fig = plt.figure(figsize=(8, 8))
#     gs = gridspec.GridSpec(4, 4)
#     gs.update(wspace=1, hspace=0.35)
#
#     xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])
#     plt.title('Chile')
#     chile1 = results_array.loc[results_array['Region'] == 'Chile']
#     for i in range(0, len(chile1)):
#         slice = chile1.loc[chile1['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
#         landfrac_slice2 = landfrac_slice.loc[landfrac_slice['location'] == str(locs1[i])]
#         plt.errorbar(landfrac_slice2['LandFrac'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(slice['Site'])}", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
#
#     plt.xlim(0, 1)
#     plt.xticks([], [])
#     plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
#
#     xtr_subsplot = fig.add_subplot(gs[2:4, 0:4])
#     plt.title('New Zealand')
#     chile1 = results_array.loc[results_array['Region'] == 'NZ']
#     for i in range(0, len(chile1)):
#         slice = chile1.loc[chile1['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
#         landfrac_slice3 = landfrac_slice.loc[landfrac_slice['location'] == str(locs2[i])]
#         label = slice['Site']
#         plt.errorbar(landfrac_slice3['LandFrac'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=label, ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
#     plt.xlabel(f'Fraction of trajectory over land, {timelabel[m]} hours')
#     plt.xlim(0, 1)
#     plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/MainFig2_wLandFRac_{timelabel[m]}.png',
#                 dpi=300, bbox_inches="tight")
#     plt.close()
#
# #
# """
# Trying the LandFrac Plot another way
# """
# easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/easy_access2 - Copy.xlsx')
# landfrac = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/landfracresults_edited.xlsx').reset_index(drop=True)
#
# fig = plt.figure(figsize=(8, 8))
# gs = gridspec.GridSpec(4, 4)
# gs.update(wspace=1, hspace=0.35)
#
# xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])
# plt.title('Chile')
# chile1 = results_array.loc[results_array['Region'] == 'Chile']
# for i in range(0, len(chile1)):
#     slice = chile1.loc[chile1['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
#     landfrac_slice2 = landfrac.loc[landfrac['location'] == str(locs1[i])]  # match the site with the Chilean data
#
#     x = landfrac_slice2['timestep']
#     y = landfrac_slice2['LandFrac']
#     plt.scatter(x,y, marker=markers[i], color=colors[i])
#
#
# xtr_subsplot = fig.add_subplot(gs[2:4, 0:4])
# plt.title('New Zealand')
# chile1 = results_array.loc[results_array['Region'] == 'NZ']
# for i in range(0, len(chile1)):
#     slice = chile1.loc[chile1['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
#     landfrac_slice2 = landfrac.loc[landfrac['location'] == str(locs2[i])]  # match the site with the Chilean data
#
#     x = landfrac_slice2['timestep']
#     y = landfrac_slice2['LandFrac']
#     plt.scatter(x,y, marker=markers[i], color=colors[i])
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/MainFig2_wLandFRac_NEW.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#

"""
T-test to see what is significantly different from the background
"""
df_testing = df.loc[(df['DecimalDate'] >1987) & (df['DecimalDate'] <1994)]


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
p_resultsss.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/p_results.xlsx')


"""
Jocelyn wants me to change the figures a bit, so I'm trying to that here...
Feb 22, 2024

Need to reload some of the data from the g
"""

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference_to_sample_xvals2/samples_with_references10000.xlsx')
df = df.loc[df['Site'] != 'Macquarie_Isl.'] # REMOVE IF WANT TO MAKE A CMP TO MQA COMPARISON PLOT LATER

df = df.sort_values(by=['DecimalDate'])
ref2 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference2/harmonized_dataset.xlsx')
ref1 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference1/reference1.xlsx')
bhdcgo = pd.read_excel(r'H:\Science\Datasets\CGOvBHD.xlsx')

# ensure all data are sliced for after 1980.
df = df.loc[df['DecimalDate'] > 1980].reset_index(drop=True)
ref2 = ref2.loc[ref2['Decimal_date'] > 1980].reset_index(drop=True)
ref1 = ref1.loc[ref1['Decimal_date'] > 1980].reset_index(drop=True)

# I DON"T WANT TO PRESENT MCQ as a TREE RING SITE!
df = df.loc[df['Site'] != 'MCQ']
# December 4, 2023: Removing Kapuni and RMB after notes from JT (or until we re-measure some of the cores)
df = df.loc[df['Site'] != 'Raul Marin Balmaceda']
df = df.loc[df['Site'] != 'near Kapuni school field, NZ']

# set some parameters
maxlat = -30
minlat = -60
nz_max_lon = 185
nz_min_lon = 155
chile_max_lon = -55
chile_min_lon = -85
res = 'l'
c1, c2, c3, c4, c5, c6, c7, c8 = '#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac'
colors = [c1, c2, c3, c4, c5, c6, c7, c8]
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D']
size1 = 8


# Create a figure
fig = plt.figure(figsize=(10, 10))

# Create a GridSpec with 3 rows and 2 columns
gs = gridspec.GridSpec(3, 2)

# Add subplots to the GridSpec
ax1 = fig.add_subplot(gs[0, 0])
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=chile_min_lon, urcrnrlon=chile_max_lon, resolution=res)
# map.drawmapboundary(fill_color='lightgrey')
# map.fillcontinents(color='darkgrey')
# map.drawcoastlines(linewidth=0.1)
map.shadedrelief()
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




ax2 = fig.add_subplot(gs[0, 1])
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution=res)
# map.drawmapboundary(fill_color='lightgrey')
# map.fillcontinents(color='darkgrey')
# map.drawcoastlines(linewidth=0.1)
map.shadedrelief()

for i in range(0, len(locs2)):

    slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    lat = slice['NewLat']
    lat = lat[0]
    lon = slice['NewLon']
    lon = lon[0]
    x, y = map(lon, lat)
    # print(x, y)
    ax2.scatter(x, y, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')
map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], linewidth=0.5)


ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(df['DecimalDate'], df['D14C_ref3t_mean'], zorder=10, label='CCGCRV Trend Reference', color='black')
for i in range(0, len(locs1)):
    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    ax3.errorbar(slice['DecimalDate'], slice['D14C_1'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=.3, ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor=colors[i])
ax3.set_xticks([], [])
ax3.set_ylim(0, 300)
ax3.set_xlim(1980, 2020)
ax3.set_ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)')
ax3.legend()

ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(df['DecimalDate'], df['D14C_ref3t_mean'], zorder=10, label='Southern Hemisphere Background', color='black')
for i in range(0, len(locs2)):
    slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    plt.errorbar(slice['DecimalDate'], slice['D14C_1'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=.3, ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor=colors[i])
ax4.set_xticks([], [])
ax4.set_yticks([], [])
ax4.set_ylim(0, 300)
ax4.set_xlim(1980, 2020)


ax5 = fig.add_subplot(gs[2, 0])
for i in range(0, len(locs1)):
    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    # print(slice)
    latitude = slice['NewLat']
    latitude = latitude[0]
    latitude = round(latitude, 1)
    ax5.errorbar(slice['DecimalDate'], slice['r3_diff_trend'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

ax5.set_ylim(-15, 15)
ax5.set_xlim(1980, 2020)
ax5.axhline(0, color='black')
ax5.set_ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
ax5.set_xlabel('Year of Growth')


ax6 = fig.add_subplot(gs[2, 1])
for i in range(0, len(locs2)):
    slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    latitude = slice['NewLat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    ax6.errorbar(slice['DecimalDate'], slice['r3_diff_trend'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

ax6.set_ylim(-15, 15)
ax6.set_xlim(1980, 2020)
ax6.axhline(0, color='black')
ax6.set_xlabel('Year of Growth')
ax6.set_yticks([], [])


# EB asked for an inset histogram to help vizualize the data...
inset_ax5 = inset_axes(ax5, width="25%", height="25%", loc='upper right')
# Create a histogram
counts, bins, patches = inset_ax5.hist(chile['r3_diff_trend'], bins=10, edgecolor='black', color='gray')
for count, bin_start, bin_end in zip(counts, bins[:-1], bins[1:]):
    print(f"Bin range: {bin_start:.2f} to {bin_end:.2f}, Count: {count}")
inset_ax5.set(xlim=(-10, 10))
print('space')
inset_ax6 = inset_axes(ax6, width="25%", height="25%", loc='upper right')
# Create a histogram
counts, bins, patches = inset_ax6.hist(nz['r3_diff_trend'], bins=10, edgecolor='black', color='gray')
for count, bin_start, bin_end in zip(counts, bins[:-1], bins[1:]):
    print(f"Bin range: {bin_start:.2f} to {bin_end:.2f}, Count: {count}")
inset_ax5.set(xlim=(-10, 10))

# plot trends
ch_x = chile['DecimalDate']
ch_x = np.array(ch_x)
ch_y = chile['r3_diff_trend']
ch_y = np.array(ch_y)

nz_x = nz['DecimalDate']
nz_x = np.array(nz_x)
nz_y = nz['r3_diff_trend']
nz_y = np.array(nz_y)

# regress the data
slope, intercept, rvalue, pvalue, stderr = stats.linregress(ch_x, ch_y)
sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(nz_x, nz_y)

# I just want the line to go across the plot for easier vizualization...
ch_x = np.append(ch_x, 1980)
ch_x = np.append(ch_x, 2020)
nz_x = np.append(nz_x, 1980)
nz_x = np.append(nz_x, 2020)

ax5.plot(ch_x, slope*ch_x+intercept, color='gray')
ax6.plot(nz_x, sslope*nz_x+sintercept, color='gray')

print("Chile: y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2))
print("NZ: y=%.3fx+%.3f\R$^2$=%.3f"%(sslope, sintercept,srvalue**2))


plt.tight_layout()
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/newfigJT.png',
            dpi=300, bbox_inches="tight")
plt.close()

ch_greater = chile.loc[chile['r3_diff_trend'] > 0]
ch_greater = len(ch_greater)/len(chile)
ch_less = 1-ch_greater
print('Chile, min, max, average, percent above zero, percent below zero')
print(min(chile['r3_diff_trend']))
print(max(chile['r3_diff_trend']))
print(np.mean(chile['r3_diff_trend']))
print(np.std(chile['r3_diff_trend']))
print(ch_greater)
print(ch_less)



print()
nz_greater = nz.loc[nz['r3_diff_trend'] > 0]
nz_greater = len(nz_greater)/len(nz)
nz_less = 1-nz_greater
print('NZ, min, max, average, percent above zero, percent below zero')
print(min(nz['r3_diff_trend']))
print(max(nz['r3_diff_trend']))
print(np.mean(nz['r3_diff_trend']))
print(np.std(nz['r3_diff_trend']))
print(nz_greater)
print(nz_less)


