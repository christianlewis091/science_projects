"""
Updated: 29 November 2022

This file does the following:
1. This file loops through the dataset and calculates the P-values of each latitude with the other latitudes.
2. The output data has been transferred to the file here:
file:///C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/PVALUES.pdf

3. Calculate the slopes of changing data for the results section.
    Creates plots Plot10_NZ_band1.png and Plot10_CH_band1.png

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from soar_analysis3 import *
from soar_analysis4 import *
from scipy import stats

for i in range(0, len(locs1)):  # locs1-3 from SOAR analysis3.
    current_loc = locs1[i]
    current_data = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)

    other_locs = [s for s in locs1 if s != (locs1[i])]

    for k in range(0, len(other_locs)):
        next_loc = other_locs[k]
        next_data = chile.loc[chile['Site'] == str(next_loc)].reset_index(drop=True)

        x = stats.ttest_ind(next_data['r2_diff_trend'], current_data['r2_diff_trend'])

        label1, label2 = next_data['NewLat'], current_data['NewLat']
        label1, label2 = label1[0], label2[0]
        print(f"Independent t-test results for Chile Lat_{str(label1)}_{str(label2)} is {x}")

for i in range(0, len(locs2)):  # locs1-3 from SOAR analysis3.
    current_loc = locs2[i]
    current_data = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)
    other_locs = [s for s in locs2 if s != (locs2[i])]

    for k in range(0, len(other_locs)):
        next_loc = other_locs[k]
        next_data = nz.loc[nz['Site'] == str(next_loc)].reset_index(drop=True)

        x = stats.ttest_ind(next_data['r2_diff_trend'], current_data['r2_diff_trend'])

        label1, label2 = next_data['NewLat'], current_data['NewLat']
        label1, label2 = label1[0], label2[0]
        print(f"Independent t-test results for NZ Lat_{str(label1)}_{str(label2)} is {x}")

print('Here are the results that correspond to Figure 4.')
print(stats.ttest_ind(means_ch1['r2_diff_trend'], means_ch2['r2_diff_trend']))
print(stats.ttest_ind(means_ch1['r2_diff_trend'], means_ch3['r2_diff_trend']))
print(stats.ttest_ind(means_ch2['r2_diff_trend'], means_ch3['r2_diff_trend']))

print(stats.ttest_ind(means_nz1['r2_diff_trend'], means_nz2['r2_diff_trend']))
print(stats.ttest_ind(means_nz1['r2_diff_trend'], means_nz3['r2_diff_trend']))
print(stats.ttest_ind(means_nz2['r2_diff_trend'], means_nz3['r2_diff_trend']))

"""
I want to re-do the p-value testing at each site, in the block above, but break it up in time.
"""
# chile.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/test.xlsx')
# make a list of all the unique time bands in the Chile dataset
dts = np.unique(chile['Time_Bands'])
lengths = []

time_array = []
p_array = []
lat1_array = []
lat2_array = []
time_array_minyear = []
for t in range(0, len(dts)):
    current_time = dts[t]
    current_timedata = chile.loc[chile['Time_Bands'] == dts[t]].reset_index(drop=True)
    locs = np.unique(current_timedata['Site'])
    if len(locs) > 1:
        for i in range(0, len(locs)):  # locs1-3 from SOAR analysis3.
            current_loc = locs[i]
            current_data = current_timedata.loc[current_timedata['Site'] == str(locs[i])].reset_index(drop=True)

            other_locs = [s for s in locs if s != (locs[i])]
            for k in range(0, len(other_locs)):
                next_loc = other_locs[k]
                next_data = current_timedata.loc[current_timedata['Site'] == str(next_loc)].reset_index(drop=True)
                x = stats.ttest_ind(next_data['r2_diff_trend'], current_data['r2_diff_trend'])

                label1 = next_data['NewLat'].reset_index(drop=True)
                label2 = current_data['NewLat'].reset_index(drop=True)
                label1 = label1[0]
                label2 = label2[0]

                # print(f"Independent t-test results for Chile Lat_{str(label1)}_{str(label2)} is {x}, time is {current_time}")
                time_array.append(current_time)
                p_array.append(x[1])
                lat1_array.append(label1)
                lat2_array.append(label2)

                time_int = str(current_time)
                time_int = time_int[9:13]
                time_array_minyear.append(time_int)

time_dependent_results = pd.DataFrame({"Time": time_array, "Lat 1": lat1_array, "Lat 2": lat2_array, "P-value": p_array,
                                       "Time Min Year": time_array_minyear}).dropna(subset="P-value")
time_dependent_results_ch = time_dependent_results.loc[time_dependent_results['P-value'] <= 0.01].reset_index(drop=True)

"""Now repeat for NZ """

dts = np.unique(nz['Time_Bands'])
lengths = []
#
time_array = []
p_array = []
lat1_array = []
lat2_array = []
time_array_minyear = []
for t in range(0, len(dts)):
    current_time = dts[t]
    current_timedata = nz.loc[nz['Time_Bands'] == dts[t]].reset_index(drop=True)
    locs = np.unique(current_timedata['Site'])
    if len(locs) > 1:
        for i in range(0, len(locs)):  # locs1-3 from SOAR analysis3.
            current_loc = locs[i]
            current_data = current_timedata.loc[current_timedata['Site'] == str(locs[i])].reset_index(drop=True)

            other_locs = [s for s in locs if s != (locs[i])]
            for k in range(0, len(other_locs)):
                next_loc = other_locs[k]
                next_data = current_timedata.loc[current_timedata['Site'] == str(next_loc)].reset_index(drop=True)
                x = stats.ttest_ind(next_data['r2_diff_trend'], current_data['r2_diff_trend'])

                label1 = next_data['NewLat'].reset_index(drop=True)
                label2 = current_data['NewLat'].reset_index(drop=True)
                label1 = label1[0]
                label2 = label2[0]

                # print(f"Independent t-test results for Chile Lat_{str(label1)}_{str(label2)} is {x}, time is {current_time}")
                time_array.append(current_time)
                p_array.append(x[1])
                lat1_array.append(label1)
                lat2_array.append(label2)

                time_int = str(current_time)
                time_int = time_int[9:13]
                time_array_minyear.append(int(time_int))

time_dependent_results = pd.DataFrame({"Time": time_array, "Lat 1": lat1_array, "Lat 2": lat2_array, "P-value": p_array,
                                       "Time Min Year": time_array_minyear}).dropna(subset="P-value")
time_dependent_results_nz = time_dependent_results.loc[time_dependent_results['P-value'] <= 0.01].reset_index(drop=True)

# since duplicates exist when different parts of the result matrix overlap (i.e., Lat 45 versus 52, and then later, 52 vs 45), I can use a nifty way to remove them by adding up the latitudes and
# removing duplicates based on the sum of those latitudes
results_dataframe = pd.DataFrame()
times = np.unique(time_dependent_results_nz['Time Min Year'])
for i in range(0, len(times)):
    curtime = times[i]
    current_block = time_dependent_results_nz.loc[time_dependent_results_nz['Time Min Year'] == curtime]

    current_block['Dup_label'] = current_block['Lat 1'] + current_block['Lat 2']
    current_block = current_block.drop_duplicates(subset='Dup_label', keep='first')
    results_dataframe = pd.concat([current_block, results_dataframe])

time_dependent_results_nz = results_dataframe

results_dataframe = pd.DataFrame()
times = np.unique(time_dependent_results_ch['Time Min Year'])
for i in range(0, len(times)):
    curtime = times[i]
    current_block = time_dependent_results_ch.loc[time_dependent_results_ch['Time Min Year'] == curtime]

    current_block['Dup_label'] = current_block['Lat 1'] + current_block['Lat 2']
    current_block = current_block.drop_duplicates(subset='Dup_label', keep='first')
    results_dataframe = pd.concat([current_block, results_dataframe])

time_dependent_results_ch = results_dataframe

time_dependent_results_nz.to_excel(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/time_dependent_pvalues_nz.xlsx')
time_dependent_results_ch.to_excel(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/time_dependent_pvalues_ch.xlsx')

"""
Calculate average latitudinal gradients

"""
"""Chile"""
avs = []
stds = []
lats_arr = []
for i in range(0, len(locs1)):  # locs1-3 from SOAR analysis3.
    current_loc = locs1[i]
    current_data = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)
    avs.append(np.average(current_data['r2_diff_trend']))
    stds.append(np.std(current_data['r2_diff_trend']))
    lats = current_data['NewLat'].reset_index(drop=True)
    lats_arr.append(lats[0])
#
# print(avs)
# print(lats_arr)
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html
res = stats.linregress(lats_arr, avs)
# print(res)
mx = np.float64(lats_arr) * res[0]
b = res[1]

plt.plot(lats_arr, avs, 'o', label='original data')
plt.plot(lats_arr, (mx + b), 'r', label='fitted line')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.title('Latitudinal Gradient (Zonal Means); Chile')
plt.text(-55, 2, 'R2 = 0.549', fontsize=12)
plt.text(-55, 1, 'm = 0.225', fontsize=12)
plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Plot8.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""NZ """

avs = []
stds = []
lats_arr = []
for i in range(0, len(locs2)):  # locs1-3 from SOAR analysis3.
    current_loc = locs2[i]
    current_data = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)
    avs.append(np.average(current_data['r2_diff_trend']))
    stds.append(np.std(current_data['r2_diff_trend']))
    lats = current_data['NewLat'].reset_index(drop=True)
    lats_arr.append(lats[0])

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html
res = stats.linregress(lats_arr, avs)
mx = np.float64(lats_arr) * res[0]
b = res[1]

plt.plot(lats_arr, avs, 'o', label='original data')
plt.plot(lats_arr, (mx + b), 'r', label='fitted line')
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.title('Latitudinal Gradient (Zonal Means); NZ')
plt.text(-55, 1, 'R2 = =0.741', fontsize=12)
plt.text(-55, 0, 'm = 0.251', fontsize=12)
plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Plot9.png',
            dpi=300, bbox_inches="tight")
plt.close()
# plt.show()


"""
Quickly trying to find the slopes on either side of the peak DD14C on Figure 4. This will appear in the results section.
"""
# First I want to write a few lines that can identify the date at which DD14C is max in CH and NZ 38-45S.
means_ch1 = means_ch1.loc[means_ch1['Decimal_date'] > 1984]  # remove the uptick pre1985
print(means_ch1.to_markdown())
print(means_nz1.to_markdown())


def slope_check(df, max_date, name):

    before = df.loc[df['Decimal_date'] <= (max_date + 1)]
    after = df.loc[df['Decimal_date'] >= (max_date - 1)]

    res1 = stats.linregress(before['Decimal_date'], before['r2_diff_trend'])
    res2 = stats.linregress(after['Decimal_date'], after['r2_diff_trend'])
    mx1 = np.float64(before['Decimal_date']) * res1[0]
    mx2 = np.float64(after['Decimal_date']) * res2[0]
    b1 = res1[1]
    b2 = res2[1]


    plt.plot(before['Decimal_date'], before['r2_diff_trend'], 'o', label='original data')
    plt.plot(after['Decimal_date'], after['r2_diff_trend'], 'o', label='original data')
    plt.plot(before['Decimal_date'], (mx1 + b1), 'r', label='fitted line')
    plt.plot(after['Decimal_date'], (mx2 + b2), 'r', label='fitted line')
    plt.title(str(name))
    plt.text(min(before['Decimal_date']), max(after['r2_diff_trend']), 'R2 before= {}'.format(str(res1[2])), fontsize=12)
    plt.text(min(before['Decimal_date']), max(after['r2_diff_trend']) - 0.5, 'm = {}'.format(str(res1[0])), fontsize=12)

    plt.text(min(before['Decimal_date']), max(after['r2_diff_trend']) - 1, 'R2 after = {}'.format(str(res2[2])), fontsize=12)
    plt.text(min(before['Decimal_date']), max(after['r2_diff_trend']) - 1.5, 'm after= {}'.format(str(res2[0])), fontsize=12)

    # plt.legend()
    plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Plot10_{}.png'.format(name),
                dpi=300, bbox_inches="tight")
    plt.close()


# Chile max r2_diff_trend is 6.68416 in 2002
# For NZ, max r2_diff_trend is  1.8781 in 2006.53
x = slope_check(means_ch1, 2002.000, 'chile_band1')
x = slope_check(means_ch2, min(means_ch2['Decimal_date']), 'chile_band2')
x = slope_check(means_ch3, min(means_ch3['Decimal_date']), 'ch_band3')
x = slope_check(means_nz1, min(means_nz1['Decimal_date']), 'nz_band1')
x = slope_check(means_nz2, min(means_nz2['Decimal_date']), 'nz_band2')
x = slope_check(means_nz3, min(means_nz3['Decimal_date']), 'nz_band3')

print(means_ch1)

slopes_nz, slopes_ch = [0.104, -0.009, 0.126], [0.054, 0.083]

print(f"Average and std of slopes NZ is {np.average(slopes_nz)} +/- {np.std(slopes_nz)}")
print(f"Average and std of slopes NZ is {np.average(slopes_ch)} +/- {np.std(slopes_ch)}")