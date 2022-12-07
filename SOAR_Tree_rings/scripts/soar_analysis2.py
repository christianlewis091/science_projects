"""
Updated: 29 November 2022

This file does the following:
1. Breaks up the data based on certain latitudinal bands defined in analysis1.py.
2. Calculates broad data for each latitudinal band, for different time intervals.
3. Creates plot 4.

This entire file will be left as is, but has been pretty much overruled by the files that produce
plot 7, a better version of plot 4.
"""

import pandas as pd
import numpy as np
from soar_analysis1 import df_2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

"""
This file will continue where SOAR_analysis1.py left off, but will index based on longitude, and decades.
"""

chile = df_2.loc[df_2['Country'] == 0]
nz = df_2.loc[df_2['Country'] == 1]
ant = df_2.loc[df_2['Country'] == 2]

def analysis1(df, year):
    df = df.loc[(df['Decimal_date'] < year) & (df['Decimal_date'] >= (year - 10))]
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
    lats = [-40, -42, -44, -47, -48, -53, -54, -55, -60, -75]  # The MAX LAT
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
    results['Year'] = year
    return results


chileresults = pd.DataFrame()
nzresults = pd.DataFrame()
antresults = pd.DataFrame()
years = [1990, 2000, 2010, 2020]
for year in years:
    chile_an = analysis1(chile, year)
    nz_an = analysis1(nz, year)
    ant_an = analysis1(ant, year)

    chileresults = pd.concat([chileresults, chile_an])
    nzresults = pd.concat([nzresults, nz_an])
    antresults = pd.concat([antresults, ant_an])


chileresults = chileresults.dropna(subset="Mean_r2")
nzresults = nzresults.dropna(subset="Mean_r2")
antresults  = antresults .dropna(subset="Mean_r2")

# with pd.ExcelWriter(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/soar_time_series.xlsx') as writer:
#
#     # use to_excel function and specify the sheet_name and index
#     # to store the dataframe in specified sheet
#     chileresults.to_excel(writer, sheet_name="Chile", index=False)
#     nzresults.to_excel(writer, sheet_name="NewZealand", index=False)
#     antresults.to_excel(writer, sheet_name="Antarctica", index=False)



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
a1, a2, a3, a4, a5, a6 = '#d73027', '#fee090', '#abd9e9', '#4575b4', '#41b6c4', '#ffffcc'
# c1, c2, c3 = '#ece2f0', '#a6bddb', '#1c9099'
# d1, d2 = '#ef8a62', '#67a9cf'
# size1 = 10
ch1 = 'red'
ch2 = a3
ch3 = 'black'
alph = .9
alph2 = 0.5


sp1 = chileresults.loc[chileresults['Year'] == 1990]
sp2 = chileresults.loc[chileresults['Year'] == 2000]
sp3 = chileresults.loc[chileresults['Year'] == 2010]
sp4 = chileresults.loc[chileresults['Year'] == 2020]

fig = plt.figure(4, figsize=(12, 4))
gs = gridspec.GridSpec(2, 6)
gs.update(wspace=.35, hspace=.25)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.title('Chile')

plt.errorbar(sp1['Lat'], sp1['Mean_r2'], sp1['stdev_r2'], fmt='o', color=a1, ecolor=a1, elinewidth=1, capsize=2, alpha=alph, label='1980 - 1990')
plt.plot(sp1['Lat'], sp1['Mean_r2'], color=a1)
plt.errorbar(sp1['Lat'], sp1['Mean_r3'], sp1['stdev_r3'], fmt='o', color=a1, ecolor=a1, elinewidth=1, capsize=2, alpha=alph2, label='1980 - 1990')
plt.plot(sp1['Lat'], sp1['Mean_r3'], color=a1)

plt.errorbar(sp2['Lat'], sp2['Mean_r2'], sp2['stdev_r2'], fmt='D', color=a2, ecolor=a2, elinewidth=1, capsize=2, alpha=alph, label='1990 - 2000')
plt.plot(sp2['Lat'], sp2['Mean_r2'], color=a2)
plt.errorbar(sp2['Lat'], sp2['Mean_r3'], sp2['stdev_r3'], fmt='D', color=a2, ecolor=a2, elinewidth=1, capsize=2, alpha=alph2, label='1990 - 2000')
plt.plot(sp2['Lat'], sp2['Mean_r3'], color=a2)

plt.errorbar(sp3['Lat'], sp3['Mean_r2'], sp3['stdev_r2'], fmt='X', color=a3, ecolor=a3, elinewidth=1, capsize=2, alpha=alph, label='2000 - 2010')
plt.plot(sp3['Lat'], sp3['Mean_r2'], color=a3)
plt.errorbar(sp3['Lat'], sp3['Mean_r3'], sp3['stdev_r3'], fmt='X', color=a3, ecolor=a3, elinewidth=1, capsize=2, alpha=alph2, label='2000 - 2010')
plt.plot(sp3['Lat'], sp3['Mean_r3'], color=a3)

plt.errorbar(sp4['Lat'], sp4['Mean_r2'], sp4['stdev_r2'], fmt='^', color=a4, ecolor=a4, elinewidth=1, capsize=2, alpha=alph, label='2010 - 2020')
plt.plot(sp4['Lat'], sp4['Mean_r2'], color=a4)
plt.errorbar(sp4['Lat'], sp4['Mean_r3'], sp4['stdev_r3'], fmt='^', color=a4, ecolor=a4, elinewidth=1, capsize=2, alpha=alph2, label='2010 - 2020')
plt.plot(sp4['Lat'], sp4['Mean_r3'], color=a4)
plt.ylim(-12, 8)
plt.xlim(-60, -35)
plt.ylabel('Difference from Reference', fontsize=14)  # label the y axis
plt.xlabel('Latitude (N)', fontsize=14)  # label the y axis


xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.title('New Zealand')
sp1 = nzresults.loc[nzresults['Year'] == 1990]
plt.errorbar(sp1['Lat'], sp1['Mean_r2'], sp1['stdev_r2'], fmt='o', color=a1, ecolor=a1, elinewidth=1, capsize=2, alpha=alph, label='1980 - 1990')
plt.plot(sp1['Lat'], sp1['Mean_r2'], color=a1)
plt.errorbar(sp1['Lat'], sp1['Mean_r3'], sp1['stdev_r3'], fmt='o', color=a1, ecolor=a1, elinewidth=1, capsize=2, alpha=alph2, label='1980 - 1990')
plt.plot(sp1['Lat'], sp1['Mean_r3'], color=a1)

sp2 = nzresults.loc[nzresults['Year'] == 2000]
plt.errorbar(sp2['Lat'], sp2['Mean_r2'], sp2['stdev_r2'], fmt='D', color=a2, ecolor=a2, elinewidth=1, capsize=2, alpha=alph, label='1990 - 2000')
plt.plot(sp2['Lat'], sp2['Mean_r2'], color=a2)
plt.errorbar(sp2['Lat'], sp2['Mean_r3'], sp2['stdev_r3'], fmt='D', color=a2, ecolor=a2, elinewidth=1, capsize=2, alpha=alph2, label='1990 - 2000')
plt.plot(sp2['Lat'], sp2['Mean_r3'], color=a2)

sp3 = nzresults.loc[nzresults['Year'] == 2010]
plt.errorbar(sp3['Lat'], sp3['Mean_r2'], sp3['stdev_r2'], fmt='X', color=a3, ecolor=a3, elinewidth=1, capsize=2, alpha=alph, label='2000 - 2010')
plt.plot(sp3['Lat'], sp3['Mean_r2'], color=a3)
plt.errorbar(sp3['Lat'], sp3['Mean_r3'], sp3['stdev_r3'], fmt='X', color=a3, ecolor=a3, elinewidth=1, capsize=2, alpha=alph2, label='2000 - 2010')
plt.plot(sp3['Lat'], sp3['Mean_r3'], color=a3)

sp4 = nzresults.loc[nzresults['Year'] == 2020]
plt.errorbar(sp4['Lat'], sp4['Mean_r2'], sp4['stdev_r2'], fmt='^', color=a4, ecolor=a4, elinewidth=1, capsize=2, alpha=alph, label='2010 - 2020')
plt.plot(sp4['Lat'], sp4['Mean_r2'], color=a4)
plt.errorbar(sp4['Lat'], sp4['Mean_r3'], sp4['stdev_r3'], fmt='^', color=a4, ecolor=a4, elinewidth=1, capsize=2, alpha=alph2, label='2010 - 2020')
plt.plot(sp4['Lat'], sp4['Mean_r3'], color=a4)
plt.ylim(-12, 8)
plt.xlim(-60, -35)
plt.xlabel('Latitude (N)', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:2, 4:6])
plt.title('Antarctica')
sp1 = antresults.loc[antresults['Year'] == 1990]
plt.errorbar(sp1['Lat'], sp1['Mean_r2'], sp1['stdev_r2'], fmt='o', color=a1, ecolor=a1, elinewidth=1, capsize=2, alpha=alph, label='1980 - 1990')
plt.plot(sp1['Lat'], sp1['Mean_r2'], color=a1)
plt.errorbar(sp1['Lat'], sp1['Mean_r3'], sp1['stdev_r3'], fmt='o', color=a1, ecolor=a1, elinewidth=1, capsize=2, alpha=alph2, label='1980 - 1990')
plt.plot(sp1['Lat'], sp1['Mean_r3'], color=a1)

sp2 = antresults.loc[antresults['Year'] == 2000]
plt.errorbar(sp1['Lat'], sp1['Mean_r2'], sp1['stdev_r2'], fmt='D', color=a2, ecolor=a2, elinewidth=1, capsize=2, alpha=alph, label='1990 - 2000')
plt.plot(sp2['Lat'], sp2['Mean_r2'], color=a2)
plt.errorbar(sp1['Lat'], sp1['Mean_r3'], sp1['stdev_r3'], fmt='D', color=a2, ecolor=a2, elinewidth=1, capsize=2, alpha=alph2, label='1990 - 2000')
plt.plot(sp2['Lat'], sp2['Mean_r3'], color=a2)

sp3 = antresults.loc[antresults['Year'] == 2010]
plt.errorbar(sp3['Lat'], sp3['Mean_r2'], sp3['stdev_r2'], fmt='X', color=a3, ecolor=a3, elinewidth=1, capsize=2, alpha=alph, label='2000 - 2010')
plt.plot(sp3['Lat'], sp3['Mean_r2'], color=a3)
plt.errorbar(sp3['Lat'], sp3['Mean_r3'], sp3['stdev_r3'], fmt='X', color=a3, ecolor=a3, elinewidth=1, capsize=2, alpha=alph2, label='2000 - 2010')
plt.plot(sp3['Lat'], sp3['Mean_r3'], color=a3)

sp4 = antresults.loc[antresults['Year'] == 2020]
plt.errorbar(sp4['Lat'], sp4['Mean_r2'], sp4['stdev_r2'], fmt='^', color=a4, ecolor=a4, elinewidth=1, capsize=2, alpha=alph, label='2010 - 2020')
plt.plot(sp4['Lat'], sp4['Mean_r2'], color=a4)
plt.errorbar(sp4['Lat'], sp4['Mean_r3'], sp4['stdev_r3'], fmt='^', color=a4, ecolor=a4, elinewidth=1, capsize=2, alpha=alph2, label='2010 - 2020')
plt.plot(sp4['Lat'], sp4['Mean_r2'], color=a4)
plt.ylim(-12, 8)
plt.xlim(-76, -70)
plt.xlabel('Latitude (N)', fontsize=14)  # label the y axis
plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot4.png',
            dpi=300, bbox_inches="tight")
plt.close()




"""
Some extra misc. calc's for the paper: What are the sizes of the errors relative to each other? R2 v R3, and the time-
averaged means
"""
r2_error = np.average(df_2['r2_diff_trend_errprop'])
r2_std = np.std(df_2['r2_diff_trend_errprop'])

r3_error = np.average(df_2['r3_diff_trend_errprop'])
r3_std = np.std(df_2['r3_diff_trend_errprop'])

# print(r2_error)
# print(r2_std)
#
# print(r3_error)
# print(r3_std)
#
# print()
# print()

# time averaged means
timeseries_err_ch = np.average(chileresults['stdev_r2'])
timeseries_std_ch = np.std(chileresults['stdev_r2'])

timeseries_err_nz = np.average(nzresults['stdev_r2'])
timeseries_std_nz = np.std(nzresults['stdev_r2'])

timeseries_err_ant = np.average(antresults['stdev_r2'])
timeseries_std_ant = np.std(antresults['stdev_r2'])

# printlist = [timeseries_err_ch, timeseries_std_ch, timeseries_err_nz, timeseries_std_nz, timeseries_err_ant, timeseries_std_ant]
# for item in printlist:
#     print(item)



