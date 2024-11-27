"""
Jocelyn would like the answers to the following questions.

Is there a pattern in recent dropoffs in currents and isotope ratios, leading to fractionation, and issues forcing us to use Mode 1 vs Mode 5.
How do we deal with small samples with respect to new concerns such as describes above?
See Jacob's data/recent wheels, and cathy's recent wheels.

Is there actual overcorrection in the data, or is within the error, and it's actually no problem?
If we "pretend" correct Kauri and Firi-D from recent wheels, do they look OK?

How will the foram test wheel look? This wheel is designed to understand if we're able to run some small samples for a student with small foram samples.

This will start by the handover between KS and CBL, started with the Excel sheet in the following file directory:
I:\C14Data\Graphite\RCM10\XCAMS\TW3532 analysis.xlsx

The first thing I'd like to do is forge a pathway to import XCAMS runlogs into python, without having to copy and paste manually. This will make things easier, and simpler to reconstruct later on.
"""

import glob
import numpy as np
import pandas as pd
import os
from xcams.RLIMS_eqns_as_funcs import f_normed_corrected

"""
I'm going to record my notes and thought process alongside the code in these triple apostrophe comments. 

First, I'm going to go back into CALAMS and look at LUC1, TW3536. 
Do I see any obvious problem? 
The first thong to note about TW3536 is that the primary standards don't look to hot. One has 0.996, another 0.997, and 1.002.
We've done better. 

But, the real problem was the "overcorrection" of small oxalics (cathy's secondary oxalics for RPO). 
In order for me to check this, and compare it (most easily) to all other smalls, I need to run the CALAMS eqn inside python
1. Has Kilho done this, and can I take an eqn from his excel sheet? 
1.1 I can't simply calculate RTS in python without dealing with the calibration curve. 
1.2 I don't know what to make of Kilho's sheet, there is no notes or documentation, just numbers everywhere. 
1.3 What IS potentially useful is simply the wheels he has analyzed. 

I must go back and correct all important small wheels in CALAMS Mode 5; then I can go back and anaylze them by mergeing their 
raw data (.out file) with their RTS data (from CALAMS)

Below is a list of the wheels I need to start with: 
TW3536 (LUC1)
TW3532 (RCM5)
TW3524 (RCM4)
TW3514 (RCM3)
TW3509 (RCM2)
TW3504 (RCM1)

I am manually dragging the .csv files (which get read into RLIMS) into a new folder for this analysis -> 
#'C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis\selected_data'

Below, I am going to aggregate all these excel sheets (the out files) for easier viewing, 
I'm also going to aggregate the .csv files
"""

"""
The .out files
"""
# Define the path and file extension
directory_path = r"C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis\selected_data\*.out"

files = glob.glob(directory_path, recursive=True)

df = pd.DataFrame()
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
        df = pd.concat([df, data], ignore_index=True)

        print(f"Total rows in the combined DataFrame: {len(df)}")

df.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\November_2024_fractionation_analysis\output\dot_out_data.xlsx')

"""
the .csv files
!!! MANUALLY ADD COLUMN HEADERS FIRST!!!
"""
# Define the path and file extension
directory_path = r"C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis\selected_data\*.csv"

files = glob.glob(directory_path, recursive=True)

df = pd.DataFrame()
# Iterate through each file and open it
for file_path in files:
    with open(file_path, 'r') as file:
        data = pd.read_csv(file)

        # Add only the filename as a new column
        data['Filename'] = os.path.basename(file_path)

        # Append to the main DataFrame
        df = pd.concat([df, data], ignore_index=True)

        print(f"Total rows in the combined DataFrame: {len(df)}")

df.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\November_2024_fractionation_analysis\output\dot_csv_data.xlsx')


"""
12/11/24
We need to see if the final values are overcorrected (including the MCC and DCC's). For this reason, I could plot the raw data, 
but I need to plot RLIMS corrected data. Rather than reimporting and exporting over and over, I can run the equations here.
 
r"C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis shows the RLIMS eqns in an easy to understand format. 
These eqns are coded into function in C:/Users/clewis/IdeaProjects/GNS/xcams/RLIMS_eqns_as_func.py

I have confirmed with a past air wheel that the equations work. 
"""

# import functions from other script
from RLIMS_eqns_as_funcs import *

"""
I also need the MCC values right off the bat, and need to know what sample's what. Let me import those from RLIMS. 
"""
df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\November_2024_fractionation_analysis\selected_data\rlims_output.xlsx')

"""
I've found out a little bit in my investigations so far, which include the figures below, output to this project's folder.
1. There is a strange pattern where larger samples have larger blanks, from RCM10. This is odd. 
2. I'm going to calculate MCC the UC Irvine way MCC
"""
# # start with LUC1 TW3536
# df.loc[(df['TW'] == 3536), 'UCI_MCC'] = 50
# df.loc[(df['TW'] == 3536), 'UCI_MCC_err'] = 1
# df.loc[(df['TW'] == 3536), 'UCI_DCC'] = 2
# df.loc[(df['TW'] == 3536), 'UCI_DCC_err'] = 1
#
# df.loc[(df['TW'] == 3504), 'UCI_MCC'] = 50
# df.loc[(df['TW'] == 3504), 'UCI_MCC_err'] = 1
# df.loc[(df['TW'] == 3504), 'UCI_DCC'] = 2
# df.loc[(df['TW'] == 3504), 'UCI_DCC_err'] = 1
#
# df.loc[(df['TW'] == 3509), 'UCI_MCC'] = 50
# df.loc[(df['TW'] == 3509), 'UCI_MCC_err'] = 1
# df.loc[(df['TW'] == 3509), 'UCI_DCC'] = 2
# df.loc[(df['TW'] == 3509), 'UCI_DCC_err'] = 1
#
# df.loc[(df['TW'] == 3514), 'UCI_MCC'] = 50
# df.loc[(df['TW'] == 3514), 'UCI_MCC_err'] = 1
# df.loc[(df['TW'] == 3514), 'UCI_DCC'] = 2
# df.loc[(df['TW'] == 3514), 'UCI_DCC_err'] = 1
#
# df.loc[(df['TW'] == 3524), 'UCI_MCC'] = 50
# df.loc[(df['TW'] == 3524), 'UCI_MCC_err'] = 1
# df.loc[(df['TW'] == 3524), 'UCI_DCC'] = 2
# df.loc[(df['TW'] == 3524), 'UCI_DCC_err'] = 1
#
# df.loc[(df['TW'] == 3524), 'UCI_MCC'] = 50
# df.loc[(df['TW'] == 3524), 'UCI_MCC_err'] = 1
# df.loc[(df['TW'] == 3524), 'UCI_DCC'] = 2
# df.loc[(df['TW'] == 3524), 'UCI_DCC_err'] = 1
#
# df.loc[df['Job::AMS Category'] =='Primary Standard OxI', 'UCI_MCC'] = 0
# df.loc[df['Job::AMS Category'] =='Primary Standard OxI', 'UCI_DCC'] = 0
# df.loc[df['Job::AMS Category'] =='Primary Standard OxI', 'UCI_MCC_err'] = 0
# df.loc[df['Job::AMS Category'] =='Primary Standard OxI', 'UCI_DCC_err'] = 0
#
# # THIS IS THE NEW MCC
# df['M_uci'] =  df['UCI_MCC']/(1000*df['wtgraph'])
# df['M_uci_err'] =  df['M_uci']*(df['UCI_MCC_err']/df['UCI_MCC'])
#
# # THIS IS THE NEW DCC
# df['D_uci'] = (df['UCI_DCC']/1000)*(1/df['wtgraph'] - 1/0.75) # 0.75 is primary ox weight estimate
# df['D_uci_err'] = df['D_uci']*(df['UCI_DCC_err']/df['UCI_DCC'])
#
# # recalculate the RLIMS eqns:
# df['RTS_CORR_CBL'] = rts_corrected(df['Ratio to standard'], df['M_uci'], df['D_uci'], 0)
# df['RTS_CORR_ERR_CBL'] = rts_corr_error(df['Ratio to standard'], df['Ratio to standard error'],
#                                        df['M_uci'], df['M_uci_err'],
#                                        df['D_uci'], df['D_uci_err'],
#                                        0,0)
# df['FM_CORR_CBL'] = f_normed_corrected(df['RTS_CORR_CBL'], 0.9878)
# df['FM_CORR_ERR_CBL'] = f_corr_norm_err(df['RTS_CORR_CBL'], df['RTS_CORR_ERR_CBL'], df['Wheel To Wheel Error'])

"""
Now, I can re-plot those oxalics of various sizes to see if any of them changed...
"""
#
# import matplotlib.pyplot as plt
# from matplotlib.ticker import ScalarFormatter
# import seaborn as sns
#
# # Create a figure with two horizontal subplots
# fig, ax = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns
#
# # PARAMETERIZE THE FIGURES
# ax[0].set_xscale('log')  # Logarithmic scale for x-axis
# ax[0].axhline(y=1, label='OX-1 Concensus (RTS, raw)', color='red' ,alpha=0.5)
#
# ax[1].set_xscale('log')  # Logarithmic scale for x-axis
# ax[1].axhline(y=1.04, label='OX-1 Concensus (FM, corrected data)', color='red' ,alpha=0.5)
#
# ax[0].grid(True, which="both", ls="--")
# ax[1].grid(True, which="both", ls="--")
#
# ax[0].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
# ax[1].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
# ax[0].set_xlim(.05, 1.2)
# ax[1].set_xlim(.05, 1.2)
#
#
# ax[0].set_title('OX-I analysis RTS Space')
# ax[1].set_title('OX-I analysis RECALC FM')
#
# ax[0].set_xlabel('Sample size (mg C)')
# ax[1].set_xlabel('Sample size (mg C)')
# ax[0].set_ylabel('Ratio to standard')
# ax[1].set_ylabel('Fraction Modern')
#
# # NOW WE CAN POPULATE IT WITH DATA
# # load up primary oxalics
# primary_ox = df.loc[df['Job::AMS Category'] =='Primary Standard OxI']
# second_nbs_ox = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'NBS Oxalic I')]
# second_flask_ox = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'OxI CO2 flask')]
#
# ax[0].errorbar(primary_ox['wtgraph'], primary_ox['Ratio to standard'], yerr=primary_ox['Ratio to standard error'], marker='o', linestyle='', label='Primary OX-1')
# ax[0].errorbar(second_nbs_ox['wtgraph'], second_nbs_ox['Ratio to standard'], yerr=second_nbs_ox['Ratio to standard error'], marker='o', linestyle='', label='NBS OX Secondaries')
# ax[0].errorbar(second_flask_ox['wtgraph'], second_flask_ox['Ratio to standard'], yerr=second_flask_ox['Ratio to standard error'], marker='o', linestyle='', label='Flask OX Secondaries')
#
# ax[1].errorbar(primary_ox['wtgraph'], primary_ox['FM_CORR_CBL'], yerr=primary_ox['FM_CORR_ERR_CBL'], marker='o', linestyle='', label='Primary OX-1')
# ax[1].errorbar(second_nbs_ox['wtgraph'], second_nbs_ox['FM_CORR_CBL'], yerr=second_nbs_ox['FM_CORR_ERR_CBL'], marker='o', linestyle='', label='NBS OX Secondaries')
# ax[1].errorbar(second_flask_ox['wtgraph'], second_flask_ox['FM_CORR_CBL'], yerr=second_flask_ox['FM_CORR_ERR_CBL'], marker='o', linestyle='', label='Flask OX Secondaries')
# ax[1].legend()
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/Figure5.png', dpi=300, bbox_inches="tight")
# plt.close()

"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
FIGURES BELOW
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""


"""
From RLIMS, I was able to output all the things I created tools to calculate (RLIMS eqns), but its fine. Those tools may be helpful later. 
It also means I likely didn't need to join the .csv files above, because I can also export that data, which was uploaded into RLIMS. 
None of this matters - just trying to keep the workflow clean. 

The first thing I'd like to check now is, what is the spread of oxalics (primary and non-primary) along the size spectrum? 
How do they differ in raw and corrected space? 
"""
# import matplotlib.pyplot as plt
# from matplotlib.ticker import ScalarFormatter
# import seaborn as sns
#
# # Create a figure with two horizontal subplots
# fig, ax = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns
#
# # PARAMETERIZE THE FIGURES
# ax[0].set_xscale('log')  # Logarithmic scale for x-axis
# ax[0].axhline(y=1, label='OX-1 Concensus (RTS, raw)', color='red' ,alpha=0.5)
#
# ax[1].set_xscale('log')  # Logarithmic scale for x-axis
# ax[1].axhline(y=1.04, label='OX-1 Concensus (FM, corrected data)', color='red' ,alpha=0.5)
#
# ax[0].grid(True, which="both", ls="--")
# ax[1].grid(True, which="both", ls="--")
#
# ax[0].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
# ax[1].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
# ax[0].set_xlim(.05, 1.2)
# ax[1].set_xlim(.05, 1.2)
#
#
# ax[0].set_title('OX-I analysis RTS Space')
# ax[1].set_title('OX-I analysis FM Space')
#
# ax[0].set_xlabel('Sample size (mg C)')
# ax[1].set_xlabel('Sample size (mg C)')
# ax[0].set_ylabel('Ratio to standard')
# ax[1].set_ylabel('Fraction Modern')
#
# # NOW WE CAN POPULATE IT WITH DATA
# # load up primary oxalics
# primary_ox = df.loc[df['Job::AMS Category'] =='Primary Standard OxI']
# second_nbs_ox = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'NBS Oxalic I')]
# second_flask_ox = df.loc[(df['Job::AMS Category'] !='Primary Standard OxI') & (df['Samples::Sample Description'] == 'OxI CO2 flask')]
#
# ax[0].errorbar(primary_ox['wtgraph'], primary_ox['Ratio to standard'], yerr=primary_ox['Ratio to standard error'], marker='o', linestyle='', label='Primary OX-1')
# ax[0].errorbar(second_nbs_ox['wtgraph'], second_nbs_ox['Ratio to standard'], yerr=second_nbs_ox['Ratio to standard error'], marker='o', linestyle='', label='NBS OX Secondaries')
# ax[0].errorbar(second_flask_ox['wtgraph'], second_flask_ox['Ratio to standard'], yerr=second_flask_ox['Ratio to standard error'], marker='o', linestyle='', label='Flask OX Secondaries')
#
# ax[1].errorbar(primary_ox['wtgraph'], primary_ox['F_corrected_normed'], yerr=primary_ox['F_corrected_normed_error'], marker='o', linestyle='', label='Primary OX-1')
# ax[1].errorbar(second_nbs_ox['wtgraph'], second_nbs_ox['F_corrected_normed'], yerr=second_nbs_ox['F_corrected_normed_error'], marker='o', linestyle='', label='NBS OX Secondaries')
# ax[1].errorbar(second_flask_ox['wtgraph'], second_flask_ox['F_corrected_normed'], yerr=second_flask_ox['F_corrected_normed_error'], marker='o', linestyle='', label='Flask OX Secondaries')
# ax[1].legend()
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/Figure1.png', dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# Analyze if DCC is appropriate
# """
# df['color'] = 'blue'
# df.loc[(df['TW'] == 3504), 'color'] = 'b'
# df.loc[(df['TW'] == 3509), 'color'] = 'g'
# df.loc[(df['TW'] == 3514), 'color'] = 'r'
# df.loc[(df['TW'] == 3524), 'color'] = 'c'
# df.loc[(df['TW'] == 3536), 'color'] = 'm'
# df.loc[(df['TW'] == 3532), 'color'] = 'y'
# df.loc[(df['TW'] == 3536), 'color'] = 'k'
#
# # Create a figure and a set of subplots
# fig, ax = plt.subplots()
#
# # Set the x and y scales to logarithmic
# ax.set_xscale('log')
# ax.set_yscale('log')
#
# # Set the limits for x and y axes
# ax.set_xlim(0.001, 10)
# ax.set_ylim(0.0001, 1)
#
# # Add labels to the axes
# ax.set_xlabel('Sample Size (mg)')
# ax.set_ylabel('Ratio to OX-1')
# ax.xaxis.set_major_formatter(ScalarFormatter())
# ax.yaxis.set_major_formatter(ScalarFormatter())
# ax.xaxis.get_major_formatter().set_scientific(False)
# ax.yaxis.get_major_formatter().set_scientific(False)
# # Add a grid for better readability
# ax.grid(True, which="both", ls="--")
#
# # add the diagonal lines
# x = [0.001, 10]
# y1 = [0.2, .00002]
# y2 = [0.3, .00003]
# y3 = [0.4, .00004]
# y4 = [0.5, .00005]
# y5 = [0.6, .00006]
# y6 = [0.8, .00008]
# y7 = [1, .0001]
# y8 = [2, .0002]
# y9 = [5, .0005]
# ys = [y1, y2, y3, y4, y5, y6, y7, y8, y9]
# labels = ['0.2','0.3','0.4','0.5','0.6','0.8','1','2','5']
# for i in range(0, len(ys)):
#     plt.plot(x, ys[i], color='black')
#
# kapuni = df.loc[df['Samples::Sample Description'] == 'Kapuni CO2 cylinder']
# marble = df.loc[df['Samples::Sample Description'] == 'IAEA-C1: Carrara Marble']
# Kauri = df.loc[df['Samples::Sample Description'] == 'Kauri Renton Road ']
#
# ax.scatter(kapuni['wtgraph'], kapuni['Ratio to standard'], label=f'Kapuni', marker='o', zorder=3, color=kapuni['color'], edgecolor='black')
# ax.scatter(marble['wtgraph'], marble['Ratio to standard'], label=f'marble', marker='X', zorder=3, color=marble['color'], edgecolor='black')
# ax.scatter(Kauri['wtgraph'], Kauri['Ratio to standard'], label=f'Kauri', marker='D', zorder=3, color=Kauri['color'], edgecolor='black')
# plt.title('')
# # Place the legend on the sidebar
# ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=10)
#
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/Figure3_MCC.png', dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# Individual MCC plots per wheel
# """
# tws = np.unique(df['TW'])
# for j in range(0, len(tws)):
#     subdf = df.loc[df['TW'] == tws[j]]
#     # Create a figure and a set of subplots
#     fig, ax = plt.subplots()
#
#     # Set the x and y scales to logarithmic
#     ax.set_xscale('log')
#     ax.set_yscale('log')
#
#     # Set the limits for x and y axes
#     ax.set_xlim(0.001, 10)
#     ax.set_ylim(0.0001, 1)
#
#     # Add labels to the axes
#     ax.set_xlabel('Sample Size (mg)')
#     ax.set_ylabel('Ratio to OX-1')
#     ax.xaxis.set_major_formatter(ScalarFormatter())
#     ax.yaxis.set_major_formatter(ScalarFormatter())
#     ax.xaxis.get_major_formatter().set_scientific(False)
#     ax.yaxis.get_major_formatter().set_scientific(False)
#     # Add a grid for better readability
#     ax.grid(True, which="both", ls="--")
#
#     # add the diagonal lines
#     x = [0.001, 10]
#     y1 = [0.2, .00002]
#     y2 = [0.3, .00003]
#     y3 = [0.4, .00004]
#     y4 = [0.5, .00005]
#     y5 = [0.6, .00006]
#     y6 = [0.8, .00008]
#     y7 = [1, .0001]
#     y8 = [2, .0002]
#     y9 = [5, .0005]
#     ys = [y1, y2, y3, y4, y5, y6, y7, y8, y9]
#     labels = ['0.2','0.3','0.4','0.5','0.6','0.8','1','2','5']
#     for i in range(0, len(ys)):
#         plt.plot(x, ys[i], color='black')
#
#     kapuni = subdf.loc[subdf['Samples::Sample Description'] == 'Kapuni CO2 cylinder']
#     marble = subdf.loc[subdf['Samples::Sample Description'] == 'IAEA-C1: Carrara Marble']
#     Kauri = subdf.loc[subdf['Samples::Sample Description'] == 'Kauri Renton Road ']
#
#     if len(kapuni) >0:
#         ax.scatter(kapuni['wtgraph'], kapuni['Ratio to standard'], label=f'Kapuni', marker='o', zorder=3, color=kapuni['color'], edgecolor='black')
#
#     if len(marble)>0:
#         ax.scatter(marble['wtgraph'], marble['Ratio to standard'], label=f'marble', marker='X', zorder=3, color=marble['color'], edgecolor='black')
#
#     if len(Kauri)>0:
#         ax.scatter(Kauri['wtgraph'], Kauri['Ratio to standard'], label=f'Kauri', marker='D', zorder=3, color=Kauri['color'], edgecolor='black')
#     plt.title(f'TW{tws[j]}')
#     # Place the legend on the sidebar
#     ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., fontsize=10)
#
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis/output/Figure3_MCC_{tws[j]}.png', dpi=300, bbox_inches="tight")
#     plt.close()
#










