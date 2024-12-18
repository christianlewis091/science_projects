"""
Updated: April 28, 2023
I want to change the plots, now that I'm getting serious about preparing this work for the Radiocarbon Journal. I'm
going to rewrite the plot so that Plot6.png is side-by-side the map.

Updated: 29 November 2022

This file does the following:
1. It uses a for loop to iterate through all the different sites in the three dataset groups (Chile, NZ, antarctica)
and runs a paired t-test to compare the use of Reference 2 from Reference 3. The results get output to here:
results_array.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/site_ttest.xlsx')

2. It also makes Plot 6!
3. It also makes Plot 6.5, used to compare Campbell Island and MCQ, which was intended to validate Campbell Island.

"""


import pandas as pd
import numpy as np
from soar_analysis1 import df_2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats

# site_array = []
# for i in range(0, len(df_2)):
#     current_row = df_2.iloc[i]
#     if str(current_row['#location']) == 'nan':
#         site_array.append(current_row['Site'])
#     elif str(current_row['Site']) == 'nan':
#         site_array.append(current_row['#location'])
# df_2['SiteNew'] = site_array
df_2 = df_2.sort_values(by=['NewLat', 'Decimal_date'], ascending=False).reset_index(drop=True)
locs = np.unique(df_2['Site'])

chile = df_2.loc[df_2['Country'] == 0].reset_index(drop=True)
nz = df_2.loc[df_2['Country'] == 1].reset_index(drop=True)
ant = df_2.loc[df_2['Country'] == 2].reset_index(drop=True)

chile_experiment = chile
# chile.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/blahblah.xlsx')
"""
The following code block just allows me to preserve the original index order of the data after indexing by Country
"""
# u, indices = np.unique(a, return_index=True) # https://numpy.org/doc/stable/reference/generated/numpy.unique.html
u1, locs1 = np.unique(chile['Site'], return_index=True)
temp = pd.DataFrame({"ind": u1, "locs":locs1}).sort_values(by=['locs'], ascending=True).reset_index(drop=True)
locs1 = temp['ind']

u2, locs2 = np.unique(nz['Site'], return_index=True)
temp2 = pd.DataFrame({"ind": u2, "locs":locs2}).sort_values(by=['locs'], ascending=True).reset_index(drop=True)
locs2 = temp2['ind']

u3, locs3 = np.unique(ant['Site'], return_index=True)
temp3 = pd.DataFrame({"ind": u3, "locs":locs3}).sort_values(by=['locs'], ascending=True).reset_index(drop=True)
locs3 = temp3['ind']


a1, a2, a3, a4, a5, a6, a7, a8 = '#d73027', '#f46d43', '#fdae61', '#fee090', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4'
c1, c2, c3 = '#ece2f0', '#a6bddb', '#1c9099'
d1, d2 = '#ef8a62', '#67a9cf'
colors = [a1, a2, a3, a4, a5, a6, a7, a8]
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D']

fig = plt.figure(figsize=(12, 12))
gs = gridspec.GridSpec(6, 3)
gs.update(wspace=.35, hspace=.6)
xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])


site_array = []
lat_array = []
result_array = []
for i in range(0, len(locs1)):

    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    latitude = slice['NewLat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    x = stats.ttest_rel(slice['r2_diff_trend'], slice['r3_diff_trend'])
    result_array.append(x[1])
    lat_array.append(latitude)
    site_array.append(str(locs1[i]))

    col = colors[i]
    mark = markers[i]


    plt.plot(slice['Decimal_date'], slice['r2_diff_trend'], color=col)
    plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], fmt=mark, elinewidth=1, capsize=2, alpha=1, color=col, label=f"{str(latitude)} N, {str(locs1[i])}")
plt.ylim(-10, 10)
plt.xlim(1980, 2020)
plt.title('Chile')
plt.text(1983, (0.9*10), '[A]', fontsize=12)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.axhline(0, color='black')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - SHB1]')


xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
for i in range(0, len(locs2)):
    col = colors[i]
    mark = markers[i]
    slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location

    latitude = slice['NewLat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    x = stats.ttest_rel(slice['r2_diff_trend'], slice['r3_diff_trend'])
    result_array.append(x[1])
    lat_array.append(latitude)
    site_array.append(str(locs2[i]))

    plt.plot(slice['Decimal_date'], slice['r2_diff_trend'], color=col)
    plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], fmt=mark, elinewidth=1, capsize=2, alpha=1, color=col, label=f"{str(latitude)} N, {str(locs2[i])}")
plt.ylim(-15, 15)
plt.xlim(1980, 2020)
plt.text(1983, (0.9*15), '[B]', fontsize=12)
plt.title('New Zealand')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.axhline(0, color='black')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - SHB1]')

xtr_subsplot = fig.add_subplot(gs[4:6, 0:2])

for i in range(0, len(locs3)):
    col = colors[i]
    mark = markers[i]
    slice = ant.loc[ant['Site'] == str(locs3[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    latitude = slice['NewLat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    x = stats.ttest_rel(slice['r2_diff_trend'], slice['r3_diff_trend'])
    result_array.append(x[1])
    lat_array.append(latitude)
    site_array.append(str(locs3[i]))

    plt.plot(slice['Decimal_date'], slice['r2_diff_trend'], color='#4575b4')
    plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], fmt=mark, elinewidth=1, capsize=2, alpha=1, color='#4575b4', label=f"{str(latitude)} N, {str(locs3[i])}")
plt.ylim(-25, 15)
plt.xlim(1980, 2020)
plt.text(1983, (0.9*15), '[C]', fontsize=12)
plt.title('Antarctic')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - SHB1]')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.axhline(0, color='black')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot6.png',
            dpi=300, bbox_inches="tight")
# plt.show()
plt.close()


results_array = pd.DataFrame({"Site": site_array, "Lat": lat_array, "Paired T-test p-value": result_array})
results_array.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/site_ttest.xlsx')


"""an extra plot"""
a1, a3, a5, a8 ='#d73027', '#fdae61', '#1c9099', '#4575b4' # testing
fig = plt.figure()
campbell = nz.loc[nz['Site'] == str(locs2[6])].reset_index(drop=True)
mcq = nz.loc[nz['Site'] == str(locs2[7])].reset_index(drop=True)
plt.plot(campbell['Decimal_date'], campbell['r2_diff_trend'], color=a1)
plt.errorbar(campbell['Decimal_date'], campbell['r2_diff_trend'], campbell['r2_diff_trend_errprop'], fmt='o', elinewidth=1, capsize=2, alpha=1, color=a1, label=f"-52.5 N N, {str(locs2[6])}")
plt.plot(mcq['Decimal_date'], mcq['r2_diff_trend'], color=a5)
plt.errorbar(mcq['Decimal_date'], mcq['r2_diff_trend'], mcq['r2_diff_trend_errprop'], fmt='x', elinewidth=1, capsize=2, alpha=1, color=a5, label=f"-54.6 N N, {str(locs2[7])}")
plt.axhline(0, color='black')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - SHB1]')
plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot6_point5.png',
            dpi=300, bbox_inches="tight")
plt.close()
print(locs1)



"""another extra plot
Hi Jocelyn,
I’m moving this to a smaller group as the discussion bends away from the specifics of MQA and more broadly to SH D14C.
Do you have a plot of the difference between Campbell and Chile D14C over time, with Heidelberg MQA thrown on for good measure?
Maybe even better, if you provide the data as a file I could plot DRP, MQA and also Chile and Campbell tree values.
It would be interesting to see how they line up relative to one another.
Re intercomparibility, apologies if you shown this already, but could you or Christian share your analysis re INSTAAR minus Heidelberg?
Thanks,
John

"""

# Grab the raw data again
df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/complete_samples.xlsx')



campbell = df.loc[df['Site'] == 'World\'s Loneliest Tree, Camp Cove, Campbell island']
chile1 = df.loc[df['Site'] == 'Bahia San Pedro, Chile']
chile2 = df.loc[df['Site'] == 'Baja Rosales, Isla Navarino']
chile3 = df.loc[df['Site'] == 'Puerto Navarino, Isla Navarino']
chile4 = df.loc[df['Site'] == 'Raul Marin Balmaceda']
chile5 = df.loc[df['Site'] == 'Seno Skyring']
mcq = df.loc[df['Site'] == 'MCQ']

c1, c2, c3 = '#d73027', '#fdae61', '#1c9099'
markers = ['o','v','8','s','p','+','x','D']


fig, axs = plt.subplots(2, sharex=True, figsize=(8, 8))
fig.subplots_adjust(hspace=0.25)

# plot the raw data first
axs[0].set_title('Measurements')
axs[1].set_title('Measurements subtracted from Southern Hemisphere Background (Baring Head)')
axs[0].scatter(campbell['Decimal_date'], campbell['D14C'], marker = 'o', label='Cambell Island', color=c1)
axs[0].scatter(chile2['Decimal_date'], chile2['D14C'], marker = 'D', label='Baja Rosales, Isla Navarino', color=c2)
axs[0].scatter(mcq['Decimal_date'], mcq['D14C'], marker = 's', label='Macquarie Island', color=c3)
axs[0].set_xlim(1980, 2022)
axs[0].set_ylim(0, 300)


campbell = nz.loc[nz['Site'] == str(locs2[6])].reset_index(drop=True)
mcq = nz.loc[nz['Site'] == str(locs2[7])].reset_index(drop=True)
chile1 = chile.loc[chile['Site'] == str(locs1[7])].reset_index(drop=True)

axs[1].plot(campbell['Decimal_date'], campbell['r2_diff_trend'], color=c1)
axs[1].errorbar(campbell['Decimal_date'], campbell['r2_diff_trend'], campbell['r2_diff_trend_errprop'], fmt='o', elinewidth=1, capsize=2, alpha=1, color=c1, label=f"-52.5 N N, {str(locs2[6])}")

axs[1].plot(chile1['Decimal_date'], chile1['r2_diff_trend'], color=c2)
axs[1].errorbar(chile1['Decimal_date'], chile1['r2_diff_trend'], chile1['r2_diff_trend_errprop'], fmt='D', elinewidth=1, capsize=2, alpha=1, color=c2, label=f"-54.6 N N, {str(locs2[7])}")

axs[1].plot(mcq['Decimal_date'], mcq['r2_diff_trend'], color=c3)
axs[1].errorbar(mcq['Decimal_date'], mcq['r2_diff_trend'], mcq['r2_diff_trend_errprop'], fmt='s', elinewidth=1, capsize=2, alpha=1, color=c3, label=f"-54.6 N N, {str(locs2[7])}")

axs[0].set_ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)')
axs[0].legend()
axs[1].set_ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - SHB1]')
axs[1].set_xlabel('Year')
axs[1].axhline(0, color='black', alpha=0.5)
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot_forJohn.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
Re-drawing plot 6 so that it's side-by-side the map. 
"""



fig = plt.figure(figsize=(12, 12))
gs = gridspec.GridSpec(4, 6)
gs.update(wspace=1, hspace=.6)



# first plot
xtr_subsplot = fig.add_subplot(gs[0:2, 2:6])
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
for i in range(0, len(locs1)):

    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    latitude = slice['NewLat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    x = stats.ttest_rel(slice['r2_diff_trend'], slice['r3_diff_trend'])
    result_array.append(x[1])
    lat_array.append(latitude)
    site_array.append(str(locs1[i]))

    col = colors[i]
    mark = markers[i]


    plt.plot(slice['Decimal_date'], slice['r2_diff_trend'], color=col)
    plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], fmt=mark, elinewidth=1, capsize=2, alpha=1, color=col, label=f"{str(latitude)} N, {str(locs1[i])}")
plt.ylim(-10, 10)
plt.xlim(1980, 2020)
plt.title('Chile')
plt.text(1983, (0.9*10), '[A]', fontsize=12)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.axhline(0, color='black')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - SHB1]')

# second plot
xtr_subsplot = fig.add_subplot(gs[2:4, 2:6])
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')


from PLOT_sampling_sites_map import *

# first map
xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=chile_min_lon, urcrnrlon=chile_max_lon, resolution=res)
# parameters to make the plot more beautiful
map.drawcoastlines(linewidth=0.5)
map.drawmapboundary(fill_color=fillcol, linewidth=0.5)
map.fillcontinents(color=land, lake_color=lakes)
map.drawcountries(linewidth=0.5)
map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], fontsize=12, linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], fontsize=12, linewidth=0.5)
chile_lat = chile['Lat']
chile_lon = chile['new_Lon']
z, a = map(chile_lon, chile_lat)
map.scatter(z, a, marker='D',color=c2, s = size1)


# second map
xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution=res)
# parameters to make the plot more beautiful
map.drawcoastlines(linewidth=0.5)
map.drawmapboundary(fill_color=fillcol, linewidth=0.5)
map.fillcontinents(color=land, lake_color=lakes)
map.drawcountries()
map.drawparallels(np.arange(-90, 90, 10), labels=[False, False, False, False], fontsize=12, linewidth=0.5)
map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], fontsize=12, linewidth=0.5)
nz_lat = nz['Lat']
nz_lon = nz['Lon']
x, y = map(nz_lon, nz_lat)
map.scatter(x, y, marker='D',color=c2, s= size1)



# fig = plt.figure(figsize=(12, 12))
# gs = gridspec.GridSpec(6, 3)
# gs.update(wspace=.35, hspace=.6)
# xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
#
#
# site_array = []
# lat_array = []
# result_array = []
# for i in range(0, len(locs1)):
#
#     slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
#     latitude = slice['NewLat']
#     latitude = latitude[0]
#     latitude = round(latitude, 1)
#
#     x = stats.ttest_rel(slice['r2_diff_trend'], slice['r3_diff_trend'])
#     result_array.append(x[1])
#     lat_array.append(latitude)
#     site_array.append(str(locs1[i]))
#
#     col = colors[i]
#     mark = markers[i]
#
#
#     plt.plot(slice['Decimal_date'], slice['r2_diff_trend'], color=col)
#     plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], fmt=mark, elinewidth=1, capsize=2, alpha=1, color=col, label=f"{str(latitude)} N, {str(locs1[i])}")
# plt.ylim(-10, 10)
# plt.xlim(1980, 2020)
# plt.title('Chile')
# plt.text(1983, (0.9*10), '[A]', fontsize=12)
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.axhline(0, color='black')
# plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - SHB1]')
#
#
# xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
# for i in range(0, len(locs2)):
#     col = colors[i]
#     mark = markers[i]
#     slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
#
#     latitude = slice['NewLat']
#     latitude = latitude[0]
#     latitude = round(latitude, 1)
#
#     x = stats.ttest_rel(slice['r2_diff_trend'], slice['r3_diff_trend'])
#     result_array.append(x[1])
#     lat_array.append(latitude)
#     site_array.append(str(locs2[i]))
#
#     plt.plot(slice['Decimal_date'], slice['r2_diff_trend'], color=col)
#     plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], fmt=mark, elinewidth=1, capsize=2, alpha=1, color=col, label=f"{str(latitude)} N, {str(locs2[i])}")
# plt.ylim(-15, 15)
# plt.xlim(1980, 2020)
# plt.text(1983, (0.9*15), '[B]', fontsize=12)
# plt.title('New Zealand')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.axhline(0, color='black')
# plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - SHB1]')
# xtr_subsplot = fig.add_subplot(gs[4:6, 0:2])
#
# for i in range(0, len(locs3)):
#     col = colors[i]
#     mark = markers[i]
#     slice = ant.loc[ant['Site'] == str(locs3[i])].reset_index(drop=True)  # grab the first data to plot, based on location
#     latitude = slice['NewLat']
#     latitude = latitude[0]
#     latitude = round(latitude, 1)
#
#     x = stats.ttest_rel(slice['r2_diff_trend'], slice['r3_diff_trend'])
#     result_array.append(x[1])
#     lat_array.append(latitude)
#     site_array.append(str(locs3[i]))
#
#     plt.plot(slice['Decimal_date'], slice['r2_diff_trend'], color='#4575b4')
#     plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], fmt=mark, elinewidth=1, capsize=2, alpha=1, color='#4575b4', label=f"{str(latitude)} N, {str(locs3[i])}")
# plt.ylim(-25, 15)
# plt.xlim(1980, 2020)
# plt.text(1983, (0.9*15), '[C]', fontsize=12)
# plt.title('Antarctic')
# plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - SHB1]')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.axhline(0, color='black')
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot6.png',
#             dpi=300, bbox_inches="tight")
# # plt.show()
# plt.close()
#

