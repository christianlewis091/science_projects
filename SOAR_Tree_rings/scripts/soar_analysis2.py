import pandas as pd
import numpy as np
from soar_analysis1 import df_2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

"""
This file will continue where SOAR_analysis1.py left off, but will index based on longitude, and decades.
"""
print(df_2.columns)
chile = df_2.loc[df_2['Country'] == 0]
nz = df_2.loc[df_2['Country'] == 1]
ant = df_2.loc[df_2['Country'] == 2]


def analysis1(df):
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

    results = pd.DataFrame(
        {"Lat": lats, "Mean_r2": mean_array_ref2, "Mean_r3": mean_array_ref3, "stdev_r2": stdev1, "stdev_r3": stdev2})
    return results

chile_an = analysis1(chile)
nz_an = analysis1(nz)
ant_an = analysis1(ant)



"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
PLOTTING FUNCTIONS
"""
# https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3
# Skyblue to distant mountain green
a1, a2, a3, a4, a5, a6 = '#253494', '#7fcdbb', '#2c7fb8', '#c7e9b4', '#41b6c4', '#ffffcc'
c1, c2, c3 = '#ece2f0', '#a6bddb', '#1c9099'
d1, d2 = '#ef8a62', '#67a9cf'
size1 = 10
ch1 = 'red'
ch2 = a3
ch3 = 'black'
alph = .9

fig = plt.figure()

plt.errorbar(chile_an['Lat'], chile_an['Mean_r2'], chile_an['stdev_r2'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha=1, label='Chile_R2')
plt.errorbar(chile_an['Lat'], chile_an['Mean_r3'], chile_an['stdev_r3'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha=.5, label='Chile_R3')

plt.errorbar(nz_an['Lat'], nz_an['Mean_r2'], nz_an['stdev_r2'], fmt='D', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha=1, label='NZ_R2')
plt.errorbar(nz_an['Lat'], nz_an['Mean_r3'], nz_an['stdev_r3'], fmt='D', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha=0.5, label='NZ_R3')

plt.errorbar(ant_an['Lat'], ant_an['Mean_r2'], ant_an['stdev_r2'], fmt='X', color=ch3, ecolor=ch3, elinewidth=1, capsize=2, alpha=1, label='ANT_R2')
plt.errorbar(ant_an['Lat'], ant_an['Mean_r3'], ant_an['stdev_r3'], fmt='X', color=ch3, ecolor=ch3, elinewidth=1, capsize=2, alpha=.5, label='ANT_R3')
plt.legend()
plt.ylabel('Difference From Reference', fontsize=14)  # label the y axis
plt.xlabel('Latitude', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot4.png',
            dpi=300, bbox_inches="tight")
plt.close()





# fig = plt.figure(4, figsize=(12, 4))
# gs = gridspec.GridSpec(2, 6)
# gs.update(wspace=.35, hspace=.25)
#
# xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
# plt.title('Chilean Sampling Sites')
# plt.errorbar(chile_an['Lat'], chile_an['Mean_r2'], chile_an['stdev_r2'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha=alph, label='R2')
# plt.errorbar(chile_an['Lat'], chile_an['Mean_r3'], chile_an['stdev_r3'], fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha=alph, label='R2')
#
#
# plt.xlabel('Latitude', fontsize=14)  # label the y axis
#
#
# xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
# plt.title('NZ Sampling Sites')
# plt.errorbar(nz_an['Lat'], nz_an['Mean_r2'], nz_an['stdev_r2'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha=alph, label='R2')
# plt.errorbar(nz_an['Lat'], nz_an['Mean_r3'], nz_an['stdev_r3'], fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha=alph, label='R2')
# plt.xlabel('Latitude', fontsize=14)  # label the y axis
#
#
# xtr_subsplot = fig.add_subplot(gs[0:2, 4:6])
# plt.title('Antarctic Sampling Sites (Neumayer Station)')
# plt.errorbar(ant_an['Lat'], ant_an['Mean_r2'], ant_an['stdev_r2'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha=alph, label='R2')
# plt.errorbar(ant_an['Lat'], ant_an['Mean_r3'], ant_an['stdev_r3'], fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha=alph, label='R2')
# plt.xlabel('Latitude', fontsize=14)  # label the y axis

# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot4.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
