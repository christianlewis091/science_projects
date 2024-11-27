"""
For the original context of why this exists, and what progress was made so far, see "...fractinoation_analysis_V0" and
C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/summary.docx

This is my second attempt at understanding this problem, with a bit more data on hand.
"""

import glob
import numpy as np
import pandas as pd
import os
from xcams.RLIMS_eqns_as_funcs import f_normed_corrected

# create a tidy file of the XCAMS runlog data
"""
The .out files
"""
# Define the path and file extension
directory_path = r"C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis\selected_data\*.out"

files = glob.glob(directory_path, recursive=True)

df_out = pd.DataFrame()
# df = pd.DataFrame(columns=['timestamp','run','(block)','position','TP#','(stnd)','14Ccnts','(cnts)','Tdetect','BeacGen','BeacROI','LTF','(%DT)','13Ccurr','(13Ccurr_stdev)','(13Ctime)','12Ccurr','(12Ctime)','12CLEcurr','(12CLEtime)','(CathCurr)','(MPAtime)','(MPAcnts)','(MPAtime)','(MPAcnts)','(MPAtime)','(MPAcnts)'])
# Iterate through each file and open it
for file_path in files:
    with open(file_path, 'r') as file:
        # Skip the first three lines
        for _ in range(3):
            next(file)

        # Read the rest of the file
        data = pd.read_csv(file, sep='\t', engine='python')

        # Add only the filename as a new column
        data['Filename'] = os.path.basename(file_path)

        # Append to the main DataFrame
        df_out = pd.concat([df_out, data], ignore_index=True)

        # print(f"Total rows in the combined DataFrame: {len(df_out)}")

df_out.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\November_2024_fractionation_analysis\output\dot_out_data.xlsx')

# read in the data from RLIMS
df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\November_2024_fractionation_analysis\selected_data\rlims_output.xlsx')

#21/11/24 I need to add TW3542



"""
A broad look at all the oxalics, in all the wheels that we've uploaded...
"""

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import seaborn as sns

# Create a figure with two horizontal subplots
fig, ax = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns

# PARAMETERIZE THE FIGURES
ax[0].set_xscale('log')  # Logarithmic scale for x-axis
ax[0].axhline(y=1, label='OX-1 Concensus (RTS, raw)', color='red' ,alpha=0.5)

ax[1].set_xscale('log')  # Logarithmic scale for x-axis
ax[1].axhline(y=1.04, label='OX-1 Concensus (FM, corrected data)', color='red' ,alpha=0.5)

ax[0].grid(True, which="both", ls="--")
ax[1].grid(True, which="both", ls="--")

ax[0].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
ax[1].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
ax[0].set_xlim(.05, 1.2)
ax[1].set_xlim(.05, 1.2)


ax[0].set_title('OX-I analysis RTS Space')
ax[1].set_title('OX-I analysis FM Space')

ax[0].set_xlabel('Sample size (mg C)')
ax[1].set_xlabel('Sample size (mg C)')
ax[0].set_ylabel('Ratio to standard')
ax[1].set_ylabel('Fraction Modern')

# NOW WE CAN POPULATE IT WITH DATA
# load up primary oxalics
primary_ox = df.loc[df['Job::AMS Category'] =='Primary Standard OxI']
second_nbs_ox = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'NBS Oxalic I')]
second_flask_ox = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'OxI CO2 flask')]

ax[0].errorbar(primary_ox['wtgraph'], primary_ox['Ratio to standard'], yerr=primary_ox['Ratio to standard error'], marker='o', linestyle='', label='Primary OX-1')
ax[0].errorbar(second_nbs_ox['wtgraph'], second_nbs_ox['Ratio to standard'], yerr=second_nbs_ox['Ratio to standard error'], marker='o', linestyle='', label='NBS OX Secondaries')
ax[0].errorbar(second_flask_ox['wtgraph'], second_flask_ox['Ratio to standard'], yerr=second_flask_ox['Ratio to standard error'], marker='o', linestyle='', label='Flask OX Secondaries')

ax[1].errorbar(primary_ox['wtgraph'], primary_ox['F_corrected_normed'], yerr=primary_ox['F_corrected_normed_error'], marker='o', linestyle='', label='Primary OX-1')
ax[1].errorbar(second_nbs_ox['wtgraph'], second_nbs_ox['F_corrected_normed'], yerr=second_nbs_ox['F_corrected_normed_error'], marker='o', linestyle='', label='NBS OX Secondaries')
ax[1].errorbar(second_flask_ox['wtgraph'], second_flask_ox['F_corrected_normed'], yerr=second_flask_ox['F_corrected_normed_error'], marker='o', linestyle='', label='Flask OX Secondaries')
ax[1].legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/Figure0.png', dpi=300, bbox_inches="tight")
plt.close()

"""
Figure 1
"""

# Create a figure with two horizontal subplots
fig, ax = plt.subplots(1, 3, figsize=(18, 6))  # 1 row, 3 columns

# PARAMETERIZE THE FIGURES
ax[0].set_xscale('log')  # Logarithmic scale for x-axis
ax[0].axhline(y=1, label='OX-1 Concensus (RTS, raw)', color='red' ,alpha=0.5)

ax[1].set_xscale('log')  # Logarithmic scale for x-axis
ax[1].axhline(y=1.04, label='OX-1 Concensus (FM, corrected data)', color='red' ,alpha=0.5)

ax[2].set_xscale('log')  # Logarithmic scale for x-axis
ax[2].axhline(y=.5693424810176299, label='FIRI-D Concensus (FM, corrected data)', color='red' ,alpha=0.5)

ax[0].grid(True, which="both", ls="--")
ax[1].grid(True, which="both", ls="--")
ax[2].grid(True, which="both", ls="--")

ax[0].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
ax[1].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
ax[2].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
ax[0].set_xlim(.05, 1.2)
ax[1].set_xlim(.05, 1.2)
ax[2].set_xlim(.05, 1.2)

ax[0].set_title('OX-I analysis RTS Space')
ax[1].set_title('OX-I analysis FM Space')
ax[2].set_title('FIRI-D analysis FM Space')

ax[0].set_xlabel('Sample size (mg C)')
ax[1].set_xlabel('Sample size (mg C)')
ax[2].set_xlabel('Sample size (mg C)')
ax[0].set_ylabel('Ratio to standard')
ax[1].set_ylabel('Fraction Modern')
ax[2].set_ylabel('Fraction Modern')

# NOW WE CAN POPULATE IT WITH DATA
# load up primary oxalics

primary_ox = df.loc[df['Job::AMS Category'] =='Primary Standard OxI']
# print(np.unique(primary_ox['Job::AMS Category'])) # confirm no mixups
second_nbs_ox = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'NBS Oxalic I')]
mode1_ox = df.loc[(df['Mode'] ==1) & (df['Samples::Sample Description'] == 'NBS Oxalic I')]
firid = df.loc[df['Samples::Sample Description'] =='FIRI-D: wood']

# highlight those where MCC or DCC is inserted
second_nbs_ox_corr = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'NBS Oxalic I') & (df['MCC'] > 0)]
mode1_ox_corr = df.loc[(df['Mode'] ==1) & (df['Samples::Sample Description'] == 'NBS Oxalic I') & (df['MCC'] > 0)]
firid_corr = df.loc[(df['Samples::Sample Description'] =='FIRI-D: wood') & (df['MCC'] > 0)]

# highlight TW3542
primary_ox_3542 = df.loc[(df['Job::AMS Category'] =='Primary Standard OxI') & (df['TW'] == 3542)]
second_nbs_ox_3542 = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'NBS Oxalic I') & (df['TW'] == 3542)]
firid_3542 = df.loc[(df['Samples::Sample Description'] =='FIRI-D: wood') & (df['TW'] == 3542)]

# highlight TW3531
primary_ox_3532_1 = df.loc[(df['Job::AMS Category'] =='Primary Standard OxI') & (df['TW'] == 3532.1)]
second_nbs_ox_3532_1 = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'NBS Oxalic I') & (df['TW'] == 3532.1)]
firid_3532_1 = df.loc[(df['Samples::Sample Description'] =='FIRI-D: wood') & (df['TW'] == 3532.1)]



ax[0].errorbar(primary_ox['wtgraph'], primary_ox['Ratio to standard'], yerr=primary_ox['Ratio to standard error'], marker='o', linestyle='', label='Primary OX-1', markerfacecolor='gray', markeredgecolor='black', alpha=0.2, ecolor='black')
ax[0].errorbar(second_nbs_ox['wtgraph'], second_nbs_ox['Ratio to standard'], yerr=second_nbs_ox['Ratio to standard error'], marker='o', linestyle='', label='NBS OX-1 secondaries', markerfacecolor='gray', markeredgecolor='black', alpha=1, ecolor='black')
ax[0].errorbar(mode1_ox['wtgraph'], mode1_ox['Ratio to standard'], yerr=mode1_ox['Ratio to standard error'], marker='D', linestyle='', label='Mode 1 NBS OX-1 secondaries', markerfacecolor='cadetblue', markeredgecolor='black', alpha=1, ecolor='black')

ax[1].errorbar(primary_ox['wtgraph'], primary_ox['F_corrected_normed'], yerr=primary_ox['F_corrected_normed_error'], marker='o', linestyle='', label='Primary OX-1', markerfacecolor='gray', markeredgecolor='black', alpha=0.2, ecolor='black')
ax[1].errorbar(second_nbs_ox['wtgraph'], second_nbs_ox['F_corrected_normed'], yerr=second_nbs_ox['F_corrected_normed_error'], marker='o', linestyle='', label='NBS OX-1 secondaries', markerfacecolor='gray', markeredgecolor='black', alpha=1, ecolor='black')
ax[1].errorbar(mode1_ox['wtgraph'], mode1_ox['F_corrected_normed'], yerr=mode1_ox['F_corrected_normed_error'], marker='D', linestyle='', label='Mode 1 NBS OX-1 secondaries', markerfacecolor='cadetblue', markeredgecolor='black', alpha=1, ecolor='black')

# overlay those that are corrected with MCC
ax[1].errorbar(second_nbs_ox_corr['wtgraph'], second_nbs_ox_corr['F_corrected_normed'], yerr=second_nbs_ox_corr['F_corrected_normed_error'], marker='o', linestyle='', label='NBS OX-1 secondaries, corrected', markerfacecolor='yellow', markeredgecolor='black', alpha=1, ecolor='black', zorder=5)
ax[1].errorbar(mode1_ox_corr['wtgraph'], mode1_ox_corr['F_corrected_normed'], yerr=mode1_ox_corr['F_corrected_normed_error'], marker='D', linestyle='', label='Mode 1 NBS OX-1 secondaries, corrected', markerfacecolor='yellow', markeredgecolor='black', alpha=1, ecolor='black', zorder=5)

# overlay TW3542
ax[1].errorbar(primary_ox_3542['wtgraph'], primary_ox_3542['F_corrected_normed'], yerr=primary_ox_3542['F_corrected_normed_error'], marker='o', linestyle='', label='Primary OX-1 3542', markerfacecolor='dodgerblue', markeredgecolor='black', alpha=0.2, ecolor='black')
ax[1].errorbar(second_nbs_ox_3542['wtgraph'], second_nbs_ox_3542['F_corrected_normed'], yerr=second_nbs_ox_3542['F_corrected_normed_error'], marker='o', linestyle='', label='NBS OX-1 secondaries 3542', markerfacecolor='dodgerblue', markeredgecolor='black', alpha=1, ecolor='black')

# overlay T3532_1
ax[1].errorbar(primary_ox_3532_1['wtgraph'], primary_ox_3532_1['F_corrected_normed'], yerr=primary_ox_3532_1['F_corrected_normed_error'], marker='o', linestyle='', label='Primary OX-1 3532_1', markerfacecolor='red', markeredgecolor='black', alpha=0.2, ecolor='black')
ax[1].errorbar(second_nbs_ox_3532_1['wtgraph'], second_nbs_ox_3532_1['F_corrected_normed'], yerr=second_nbs_ox_3532_1['F_corrected_normed_error'], marker='o', linestyle='', label='NBS OX-1 secondaries 3532_1', markerfacecolor='red', markeredgecolor='black', alpha=1, ecolor='black')


ax[2].errorbar(firid['wtgraph'], firid['F_corrected_normed'], yerr=firid['F_corrected_normed_error'], marker='o', linestyle='', label='FIRI-D', markerfacecolor='gray', markeredgecolor='black', alpha=1, ecolor='black')
ax[2].errorbar(firid_corr['wtgraph'], firid_corr['F_corrected_normed'], yerr=firid_corr['F_corrected_normed_error'], marker='o', linestyle='', label='FIRI-D w/ MCC', markerfacecolor='yellow', markeredgecolor='black', alpha=1, ecolor='black')
ax[2].errorbar(firid_3542['wtgraph'], firid_3542['F_corrected_normed'], yerr=firid_3542['F_corrected_normed_error'], marker='o', linestyle='', label='FIRI-D 3542', markerfacecolor='dodgerblue', markeredgecolor='black', alpha=1, ecolor='black',zorder=5)
ax[2].errorbar(firid_3532_1['wtgraph'], firid_3532_1['F_corrected_normed'], yerr=firid_3532_1['F_corrected_normed_error'], marker='o', linestyle='', label='FIRI-D 3532_1', markerfacecolor='red', markeredgecolor='black', alpha=1, ecolor='black',zorder=5)

ax[1].legend(fontsize=8)
ax[2].legend(fontsize=8)
plt.show()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/Figure1_w3542.png', dpi=300, bbox_inches="tight")
plt.close()

# plt.scatter(firid_3542['wtgraph'], firid_3542['F_corrected_normed'])
# plt.show()

"""
What can i learn about the secondary NBS oxalics from their ratios? 
"""
#
# # prepare for merge
df_ex = df[['TP','wtgraph','Job::AMS Category','Samples::Sample Description']].rename(columns={'TP':'TP#'})
#
# # create new merged dataframe for each subtype, primaries and NBS secondaries
df_out_2 = pd.merge(df_out, df_ex, on='TP#')
# df_out_2.to_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/test.xlsx')

primary_ox = df_out_2.loc[df_out_2['Job::AMS Category'] =='Primary Standard OxI']
second_nbs_ox = df_out_2.loc[(df_out_2['Job::AMS Category'] !='Primary Standard OxI') & (df_out_2['Samples::Sample Description'] == 'NBS Oxalic I')]

tps_p = np.unique(primary_ox['TP#'])
tps_n = np.unique(second_nbs_ox['TP#'])

fig, ax = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 3 columns

for i in range(0, len(tps_p)):
    # find the TPs in the dot_out data
    tp_i = df_out_2.loc[df_out_2['TP#'] == tps_p[i]].reset_index(drop=True)
    # print(np.unique(tp_i['Job::AMS Category']))
    tp_i['thirteen_twelve'] = tp_i['13Ccurr']/tp_i['12Ccurr']
    sc = ax[0].scatter(tp_i['run'], tp_i['thirteen_twelve'], c=tp_i['wtgraph'], cmap='viridis', vmin=0.05, vmax=1)

for i in range(0, len(tps_n)):
    # find the TPs in the dot_out data
    tp_i = df_out_2.loc[df_out_2['TP#'] == tps_n[i]].reset_index(drop=True)
    # print(np.unique(tp_i['Job::AMS Category']))
    tp_i['thirteen_twelve'] = tp_i['13Ccurr']/tp_i['12Ccurr']
    sc = ax[1].scatter(tp_i['run'], tp_i['thirteen_twelve'], c=tp_i['wtgraph'], cmap='viridis', vmin=0.05, vmax=1)

ax[0].set_ylim(0.0106, 0.0113)
ax[1].set_ylim(0.0106, 0.0113)
ax[0].set_title('Primary OX-1, 13Curr/12current')
ax[1].set_title('Secondary NBS, 13Curr/12current')
fig.colorbar(sc, ax=ax, label='wtgraph')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/Figure2.png', dpi=300, bbox_inches="tight")
plt.close()
#
"""
Now I'd like to zoom in and find the secondaries that have these low 13C/12C current anomalies
"""

for i in range(0, len(tps_n)):
    # Find the TPs in the dot_out data
    tp_i = df_out_2.loc[df_out_2['TP#'] == tps_n[i]].reset_index(drop=True)
    # Calculate the 13Ccurr / 12Ccurr ratio
    tp_i['thirteen_twelve'] = tp_i['13Ccurr'] / tp_i['12Ccurr']

    # Scatter plot with color map
    plt.scatter(tp_i['run'], tp_i['thirteen_twelve'])
    plt.ylim(0.0106, 0.0113)
    plt.title(f'{tps_n[i]}')  # Title in red

    # Save each figure as a separate PNG file
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/fold/Figure2_{i}.png', dpi=300, bbox_inches="tight")
    plt.close()


"""
Problematic samples are listed in array below. These samples have low 13/12. Are these the ones that are way off in Figure1? 
"""

tp_checks = [88288,88229,88230,88231, 88232,88233,88234,88235, 88236, 88237, 88271, 88272]

# Create a figure with two horizontal subplots
fig, ax = plt.subplots(1, 3, figsize=(18, 6))  # 1 row, 3 columns

# PARAMETERIZE THE FIGURES
ax[0].set_xscale('log')  # Logarithmic scale for x-axis
ax[0].axhline(y=1, label='OX-1 Concensus (RTS, raw)', color='red' ,alpha=0.5)

ax[1].set_xscale('log')  # Logarithmic scale for x-axis
ax[1].axhline(y=1.04, label='OX-1 Concensus (FM, corrected data)', color='red' ,alpha=0.5)

ax[2].set_xscale('log')  # Logarithmic scale for x-axis
ax[2].axhline(y=.5693424810176299, label='FIRI-D Concensus (FM, corrected data)', color='red' ,alpha=0.5)

ax[0].grid(True, which="both", ls="--")
ax[1].grid(True, which="both", ls="--")
ax[2].grid(True, which="both", ls="--")

ax[0].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
ax[1].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
ax[2].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
ax[0].set_xlim(.05, 1.2)
ax[1].set_xlim(.05, 1.2)
ax[2].set_xlim(.05, 1.2)

ax[0].set_title('OX-I analysis RTS Space')
ax[1].set_title('OX-I analysis FM Space')
ax[2].set_title('FIRI-D analysis FM Space')

ax[0].set_xlabel('Sample size (mg C)')
ax[1].set_xlabel('Sample size (mg C)')
ax[2].set_xlabel('Sample size (mg C)')
ax[0].set_ylabel('Ratio to standard')
ax[1].set_ylabel('Fraction Modern')
ax[2].set_ylabel('Fraction Modern')

# NOW WE CAN POPULATE IT WITH DATA
# load up primary oxalics

primary_ox = df.loc[df['Job::AMS Category'] =='Primary Standard OxI']
# print(np.unique(primary_ox['Job::AMS Category'])) # confirm no mixups
second_nbs_ox = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'NBS Oxalic I')]
mode1_ox = df.loc[(df['Mode'] ==1) & (df['Samples::Sample Description'] == 'NBS Oxalic I')]
firid = df.loc[df['Samples::Sample Description'] =='FIRI-D: wood']

# highlight those where MCC or DCC is inserted
second_nbs_ox_corr = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'NBS Oxalic I') & (df['MCC'] > 0)]
mode1_ox_corr = df.loc[(df['Mode'] ==1) & (df['Samples::Sample Description'] == 'NBS Oxalic I') & (df['MCC'] > 0)]
firid_corr = df.loc[(df['Samples::Sample Description'] =='FIRI-D: wood') & (df['MCC'] > 0)]

# highlight problematic samples with low 13/12 Current!
trubs = df.loc[df['TP'].isin(tp_checks)]
# trubs.to_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/problem_samples.xlsx')

ax[0].errorbar(primary_ox['wtgraph'], primary_ox['Ratio to standard'], yerr=primary_ox['Ratio to standard error'], marker='o', linestyle='', label='Primary OX-1', markerfacecolor='gray', markeredgecolor='black', alpha=0.2, ecolor='black')
ax[0].errorbar(second_nbs_ox['wtgraph'], second_nbs_ox['Ratio to standard'], yerr=second_nbs_ox['Ratio to standard error'], marker='o', linestyle='', label='NBS OX-1 secondaries', markerfacecolor='gray', markeredgecolor='black', alpha=1, ecolor='black')
ax[0].errorbar(mode1_ox['wtgraph'], mode1_ox['Ratio to standard'], yerr=mode1_ox['Ratio to standard error'], marker='D', linestyle='', label='Mode 1 NBS OX-1 secondaries', markerfacecolor='cadetblue', markeredgecolor='black', alpha=1, ecolor='black')

ax[1].errorbar(primary_ox['wtgraph'], primary_ox['F_corrected_normed'], yerr=primary_ox['F_corrected_normed_error'], marker='o', linestyle='', label='Primary OX-1', markerfacecolor='gray', markeredgecolor='black', alpha=0.2, ecolor='black')
ax[1].errorbar(second_nbs_ox['wtgraph'], second_nbs_ox['F_corrected_normed'], yerr=second_nbs_ox['F_corrected_normed_error'], marker='o', linestyle='', label='NBS OX-1 secondaries', markerfacecolor='gray', markeredgecolor='black', alpha=1, ecolor='black')
ax[1].errorbar(mode1_ox['wtgraph'], mode1_ox['F_corrected_normed'], yerr=mode1_ox['F_corrected_normed_error'], marker='D', linestyle='', label='Mode 1 NBS OX-1 secondaries', markerfacecolor='cadetblue', markeredgecolor='black', alpha=1, ecolor='black')
ax[1].errorbar(trubs['wtgraph'], trubs['F_corrected_normed'], yerr=trubs['F_corrected_normed_error'], marker='o', linestyle='', label='NBS OX-1 secondaries BAD!', markerfacecolor='red', markeredgecolor='black', alpha=1, ecolor='black')

# overlay those that are corrected with MCC
ax[1].errorbar(second_nbs_ox_corr['wtgraph'], second_nbs_ox_corr['F_corrected_normed'], yerr=second_nbs_ox_corr['F_corrected_normed_error'], marker='o', linestyle='', label='NBS OX-1 secondaries, corrected', markerfacecolor='yellow', markeredgecolor='black', alpha=1, ecolor='black', zorder=5)
ax[1].errorbar(mode1_ox_corr['wtgraph'], mode1_ox_corr['F_corrected_normed'], yerr=mode1_ox_corr['F_corrected_normed_error'], marker='D', linestyle='', label='Mode 1 NBS OX-1 secondaries, corrected', markerfacecolor='yellow', markeredgecolor='black', alpha=1, ecolor='black', zorder=5)

ax[2].errorbar(firid['wtgraph'], firid['F_corrected_normed'], yerr=firid['F_corrected_normed_error'], marker='o', linestyle='', label='FIRI-D', markerfacecolor='gray', markeredgecolor='black', alpha=1, ecolor='black')
ax[2].errorbar(firid_corr['wtgraph'], firid_corr['F_corrected_normed'], yerr=firid_corr['F_corrected_normed_error'], marker='o', linestyle='', label='FIRI-D w/ MCC', markerfacecolor='yellow', markeredgecolor='black', alpha=1, ecolor='black')

ax[1].legend(fontsize=8)
ax[2].legend(fontsize=8)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/Figure5.png', dpi=300, bbox_inches="tight")
plt.close()

"""
The TP’s highlighted above ,and in red on the plot, are all from TW3514. 
These TPs are NOT the smallest, and most overcorrected as I’d hoped. These problematic ones that I was looking for are in RED. 
There must be something else driving the problem for the other ones. Now, I’ll approach from the other side. Let me find out what the TP’s of those are, and look at their currents. 
By plotting in plotly, I can easily find these TPs.
"""

import plotly.graph_objects as go

# Create the figure
fig = go.Figure()

# Scatter plot with error bars
fig.add_trace(go.Scatter(
    x=second_nbs_ox['wtgraph'],
    y=second_nbs_ox['F_corrected_normed'],
    error_y=dict(type='data', array=second_nbs_ox['F_corrected_normed_error'], color='black'),
    mode='markers',
    marker=dict(color='gray', line=dict(color='black', width=1)),
    name='NBS OX-1 secondaries',
    text=second_nbs_ox['TP'],  # Add TP data for hover
    opacity=1
))

# Set axis limits and labels
fig.update_xaxes(title_text="wtgraph", range=[0.05, 1.2])
fig.update_yaxes(title_text="F_corrected_normed")

# Set plot title and layout
fig.update_layout(
    title="NBS OX-1 Secondaries with Error Bars",
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True),
    template="plotly_white"
)

# Save the plot as an HTML file
fig.write_html("C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/Figure6.html")

# Optionally display the plot
# fig.show()

"""
Trying to understand what's going on with the data that's too high, and the data that's too low. 
"""

tp_2high = [88942, 88943, 88944, 88946, 88272, 88271, 88945]
tp_2low = [89202, 89374, 89373,89375, 89371, 89384, 89200, 89199, 89370]

trubs_2h = df.loc[(df['TP'].isin(tp_2high))]
trubs_2l = df.loc[(df['TP'].isin(tp_2low))]
trubs_2h.to_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/trubs2h.xlsx')
trubs_2l.to_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/trubs2l.xlsx')

plt.scatter(second_nbs_ox['wtgraph'],
            (1/second_nbs_ox['C12C13 ratio']),
            marker='o',
            linestyle='',
            label='All other NBS OX-1 secondaries',
            facecolor='gray',  # Use facecolor instead of markerfacecolor
            edgecolor='black',
            alpha=1)

plt.scatter(trubs_2h['wtgraph'],
            (1/trubs_2h['C12C13 ratio']),
            marker='o',
            linestyle='',
            label='Too high NBS secondaries',
            facecolor='red',  # Use facecolor instead of markerfacecolor
            edgecolor='black',
            alpha=1)

plt.scatter(trubs_2l['wtgraph'],
            (1/trubs_2l['C12C13 ratio']),
            marker='o',
            linestyle='',
            label='Too low NBS secondaries',
            facecolor='blue',  # Use facecolor instead of markerfacecolor
            edgecolor='black',
            alpha=1)

plt.ylabel('13/12 Ratio')
plt.xlabel('wtgraph')
plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/Figure7.png', dpi=300, bbox_inches="tight")

























# import matplotlib.animation as animation
#
# # Set up figure and axis
# fig, ax = plt.subplots()
# ax.set_ylim(0.0106, 0.0113)
# scatter = None  # Placeholder for scatter plot
#
# # Create an update function for animation
# tp_flag_list = []
# def update(i):
#     global scatter
#     ax.clear()  # Clear the axis to update with each new frame
#     tp_i = df_out_2.loc[df_out_2['TP#'] == tps_n[i]].reset_index(drop=True)
#     print(np.unique(tp_i['Job::AMS Category']))  # Debugging output
#
#     # Calculate ratio and create scatter plot for this frame
#     tp_i['thirteen_twelve'] = tp_i['13Ccurr'] / tp_i['12Ccurr']
#     scatter = ax.scatter(tp_i['run'], tp_i['thirteen_twelve'], c=tp_i['wtgraph'], cmap='viridis', vmin=0.05, vmax=1)
#     ax.axhline(y=np.mean(tp_i['thirteen_twelve']), label='OX-1 Concensus (FM, corrected data)', color='red' ,alpha=0.5)
#     ax.set_title(f"TP# {tps_n[i]}")  # Set title to indicate the current frame
#     ax.set_ylim(0.0106, 0.0113)
#
#     if np.mean(tp_i['thirteen_twelve']) <= .01095:
#         tp_flag_list.append(tps_n[i])
#         ax.set_title(f"TP# {tps_n[i]}", color='red')  # Set title to indicate the current frame
#
# # Initialize and save the animation
# ani = animation.FuncAnimation(fig, update, frames=range(len(tps_n)), repeat=False)
# ani.save('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/Figure3_animation.gif',
#          dpi=300, writer='imagemagick')
# plt.close()
#









































# """
# Plot with the flagged low data on the side
# """
# fig, ax = plt.subplots(1, 3, figsize=(18, 6))  # 1 row, 3 columns
#
# for i in range(0, len(tps_p)):
#     # find the TPs in the dot_out data
#     tp_i = df_out_2.loc[df_out_2['TP#'] == tps_p[i]].reset_index(drop=True)
#     print(np.unique(tp_i['Job::AMS Category']))
#     tp_i['thirteen_twelve'] = tp_i['13Ccurr']/tp_i['12Ccurr']
#     sc = ax[0].scatter(tp_i['run'], tp_i['thirteen_twelve'], c=tp_i['wtgraph'], cmap='viridis', vmin=0.05, vmax=1)
#
# for i in range(0, len(tps_n)):
#     # find the TPs in the dot_out data
#     tp_i = df_out_2.loc[df_out_2['TP#'] == tps_n[i]].reset_index(drop=True)
#     print(np.unique(tp_i['Job::AMS Category']))
#     tp_i['thirteen_twelve'] = tp_i['13Ccurr']/tp_i['12Ccurr']
#     sc = ax[1].scatter(tp_i['run'], tp_i['thirteen_twelve'], c=tp_i['wtgraph'], cmap='viridis', vmin=0.05, vmax=1)
#
# for i in range(0, len(tp_flag_list)):
#     # find the TPs in the dot_out data
#     tp_i = df_out_2.loc[df_out_2['TP#'] == tp_flag_list[i]].reset_index(drop=True)
#     print(np.unique(tp_i['Job::AMS Category']))
#     tp_i['thirteen_twelve'] = tp_i['13Ccurr']/tp_i['12Ccurr']
#     sc = ax[2].scatter(tp_i['run'], tp_i['thirteen_twelve'], c=tp_i['wtgraph'], cmap='viridis', vmin=0.05, vmax=1)
#
# ax[0].set_ylim(0.0106, 0.0113)
# ax[1].set_ylim(0.0106, 0.0113)
# ax[2].set_ylim(0.0106, 0.0113)
# ax[0].set_title('Primary OX-1, 13Curr/12current')
# ax[1].set_title('Secondary NBS, 13Curr/12current')
# ax[2].set_title('LOW Secondary NBS, 13Curr/12current')
# fig.colorbar(sc, ax=ax, label='wtgraph')
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/V1_output/Figure4.png', dpi=300, bbox_inches="tight")
# plt.close()
# #
#
















