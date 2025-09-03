"""
One of the flask oxalics recently broke
Before, we had flasks 3 and 4 which were deemed dubious because of bad values. We reran them because one broke, how do they look now
30 April 2025
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df = pd.read_excel('I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3561/flask_test.xlsx')
bar1 = df.loc[(df['R_number'] == '40696/1') & (df['DELTA14C'] > -700)]
bar2 = df.loc[(df['R_number'] == '40696/2') & (df['DELTA14C'] > -700)]
bar3 = df.loc[(df['R_number'] == '40696/3') & (df['DELTA14C'] > -700)]
bar4 = df.loc[(df['R_number'] == '40696/4') & (df['DELTA14C'] > -700)]

# Calculate mean and std for bar1 and bar2
mean1, std1 = bar1['DELTA14C'].mean(), bar1['DELTA14C'].std()
mean2, std2 = bar2['DELTA14C'].mean(), bar2['DELTA14C'].std()

fig = plt.figure(figsize=(8, 4))

plt.scatter(bar1['TP'], bar1['DELTA14C'], label='40696_1', alpha=0.1)
plt.scatter(bar2['TP'], bar2['DELTA14C'], label='40696_2', alpha=0.1)
plt.scatter(bar3['TP'], bar3['DELTA14C'], label='40696_3')
plt.scatter(bar4['TP'], bar4['DELTA14C'], label='40696_4')

# Add horizontal lines for 1-sigma range (mean ± std)
plt.axhline(mean1 + std1, color='gray', linestyle='-', alpha=0.6, label='40696_1 ±1σ')
plt.axhline(mean1 - std1, color='gray', linestyle='-', alpha=0.6)
plt.axhline(mean1 + std1+ std1, color='gray', linestyle='-', alpha=0.6, label='40696_1 ±2σ')
plt.axhline(mean1 - std1 - std1, color='gray', linestyle='-', alpha=0.6)

plt.ylim(30,50)
plt.xlabel('TW', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis

plt.legend()
plt.savefig(
    f'I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3561/ox_test.png', dpi=300, bbox_inches="tight")
plt.close()

