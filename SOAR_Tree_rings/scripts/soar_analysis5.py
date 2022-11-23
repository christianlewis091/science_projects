import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from soar_analysis4 import *
from soar_analysis3 import *
from scipy import stats

for i in range(0, len(locs1)):  #locs1-3 from SOAR analysis3.
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

print()
print()

for i in range(0, len(locs2)):  #locs1-3 from SOAR analysis3.
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


#
print('Here are the results that correspond to Figure 4.')
print(stats.ttest_ind(means_ch1['r2_diff_trend'], means_ch2['r2_diff_trend']))
print(stats.ttest_ind(means_ch1['r2_diff_trend'], means_ch3['r2_diff_trend']))
print(stats.ttest_ind(means_ch2['r2_diff_trend'], means_ch3['r2_diff_trend']))

print(stats.ttest_ind(means_nz1['r2_diff_trend'], means_nz2['r2_diff_trend']))
print(stats.ttest_ind(means_nz1['r2_diff_trend'], means_nz3['r2_diff_trend']))
print(stats.ttest_ind(means_nz2['r2_diff_trend'], means_nz3['r2_diff_trend']))
#
#
#
