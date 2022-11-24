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
# print(locs1)
# print(locs2)
# print(locs3)



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
results_array.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/testttest.xlsx')

















