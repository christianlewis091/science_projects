import pandas as pd
import numpy as np
import warnings
import xlsxwriter
from datetime import date
warnings.simplefilter(action='ignore')
import plotly.express as px
import matplotlib.pyplot as plt
today = date.today()

"""
We are working on an AMS data quality paper that was originally started by Albert Zondervan, who is not at uOttawa.
Jocelyn wants to rerun the scripts that created the plots, and numbers for the data quality paper; however, we
are concerned that many data in the record should have quality flags, and currently do not. This script's goal is to
help me identify and flag those data.


September 12, 2023
I'm splitting the document into different "steps" that I can use as the flags to help identify where flags came in. 


September 8, 2023:
Initialization of this file. Creating the folders where the data will be stored:

Location of Original Data
H:\Science\Datasets\Alberts_dataquality

Location of Output
# C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output

Flags we will enter are as follows:
in general, where X can be any flag in that column:
A column 1 flag "X.." indicates the measurement is BAD and should not be used anymore, a "hard" flag
A column 2 flag ".X." is a soft flag. The measurement needs some looking at before further use
A column 3 flag "..X" is informational

# X can be any of the following, the following are previously used flags:
# "..T" = Test sample
# "A.." = Analytical problem
# "N.." = Sampling problem for Airs
# ".F." = Contains fossil fuel pollution
# "..D" = Data has been updated since publication
# "..P" = Data is preliminary and needs to be checked

PHASES OF THIS FILE: 
><>><>><>><>><>><>><>><>
PHASE 1: IDENTIFY INNOCUOUS JOB NOTES
><>><>><>><>><>><>><>><>
Label all jobNOTES that are NOT BAD, by filtering and labeling things that are clearly innocuous, such 
as, things that are only digits, or, the things listed below.  
Phase 1 adds "filtering flags" to the data based on what's written in the job notes
# 1 == HAD NO DATA IN JOB NOTES
# 2 == ONLY ONE CHARACTER
# 3 == CONTAINS THE WORD TEST
# 4 == ONLY CONTAINS NUMBERS
# 5 == DESCRIBES X/Y (1 of 2, 3 of 6, etc)
# 6 == DESCRIBES ANYTHING COMTAINING ONLY EA "XYZ"
# 7 == DESCRIBES A "COMMON DEPEAT" (i.e., "skip acid etch", or "notify client

Adding a soft flag to anything that contains test. 

><>><>><>><>><>><>><>><>
PHASE 2: MANUALLY CHECK REST OF JOB NOTES
><>><>><>><>><>><>><>><>
There are of course heaps of job notes that don't fit into the strict labeling categories I've made in phase 1, 
although phase 1 did capture 75% of the notes, 25% remain and need manual checking. I went through these and added 
some labels that I thought were appropriate at the time. This can be found on this sheet: 

'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/manual_checks.csv'

By mergeing it back to the data from phase 1 and re-labeling for cleaner data, we can have a full, better dataset
I am flagging anything that says "Discuss" with a soft flag, and anything with "Remove" with a hard flag

><>><>><>><>><>><>><>><>
PHASE 3: Plot the data to look for outliers (THE ROUGH IN) 
><>><>><>><>><>><>><>><>

><>><>><>><>><>><>><>><>
PHASE 4: Plot the data to look for outliers (zooming into each "known") 
><>><>><>><>><>><>><>><>



"""
#
# # IMPORT THE DATA FILE
# df = pd.read_csv(r'H:\Science\Datasets\Alberts_dataquality\simplified RLIMS dataset.csv')
#
# # INITIAlZE A COLUMN FOR ME TO ADD THINGS TO FILTER ON LATER
# df['CBL_Filtering_Category'] = -999

"""
><>><>><>><>><>><>><>><>
PHASE 1: IDENTIFY INNOCUOUS JOB NOTES
><>><>><>><>><>><>><>><>
"""
# # See documentation above for details on 1-7 labeling scheme
# # Checking for "must contain -999" because if it doesn't it's already been labeled
# df.loc[(df['jobNOTES'] == 'Missing[]') & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 1
# df.loc[(df['jobNOTES'].str.len() == 1) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 2
# df.loc[(df['jobNOTES'].str.isdigit()) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 4
#
# # Label anything containing "test"
# tests = ['TEST','test','Test']
# for i in range(len(tests)):
#     df.loc[(df['jobNOTES'].str.contains(tests[i], na=False)) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 3
#
# # HOW MANY OF THE JOB NOTES ARE SUCH AS: 1 OF 2, 3 of 6
# for i in range(0, 10):
#     for k in range(0, 10):
#         df.loc[(df['CBL_Filtering_Category'] == -999) & (df['jobNOTES'] == f'{i} of {k}'), 'CBL_Filtering_Category'] = 5
#         df.loc[(df['CBL_Filtering_Category'] == -999) & (df['jobNOTES'] == f'Split {i} of {k}'), 'CBL_Filtering_Category'] = 5
#         df.loc[(df['CBL_Filtering_Category'] == -999) & (df['jobNOTES'] == f'split {i} of {k}'), 'CBL_Filtering_Category'] = 5
#
# # HOW MANY NOTES ARE ONLY EA NUMBERS? # TODO THIS LINE TAKES THE LONGEST! (UNCOMMENT WHEN CODE IS READY
# for x in range(0,10):
#     for y in range(0, 10):
#         for z in range(0, 10):
#             df.loc[(df['jobNOTES'].str.contains(f'EA {x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
#             df.loc[(df['jobNOTES'].str.contains(f'EA # {x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
#             df.loc[(df['jobNOTES'].str.contains(f'EA{x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
#             df.loc[(df['jobNOTES'].str.contains(f'EA #{x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
#             df.loc[(df['jobNOTES'].str.contains(f'for EA{x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
#
# # MANY OF THE JOB NOTES ARE SOMETHING I CAN CALL "COMMON REPEATS", and are things I don't think we need to worry too much about
# common_repeats = pd.read_excel(r'H:\Science\Datasets\Alberts_dataquality\common_repeats.xlsx').astype(str)
# repeats = common_repeats['REPEAT']
# for i in range(0, len(repeats)):
#     x = str(repeats[i])
#     df.loc[(df['jobNOTES'] == x) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 7
#
#
# # REPLACE THE NUMBERS WITH ACTUAL LABELS THAT ARE MORE DESCRIPTIVE. FOR SOME REASON COULDN'T ADD THESE AT FIRST,
# # PANDAS BUG?
#
# df = df.replace({'CBL_Filtering_Category': {1: 'PHASE1_EmptyJobNotes',
#                                             2: 'PHASE1_1-Char',
#                                             3: 'PHASE1_Contains_TEST',
#                                             4: 'PHASE1_Only_Digits',
#                                             5: 'PHASE1_X_of_Y',
#                                             6: 'PHASE1_EA_XYZ',
#                                             7: 'PHASE1_Common_Repeats'}})
#
# # add a soft flag to those that contain test
# df.loc[df['CBL_Filtering_Category'] == 'PHASE1_Contains_TEST', 'flag'] = '.X.'
#
# df.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_1_{today}.csv')
# length_remaining = df.loc[df['CBL_Filtering_Category'] == -999]
# phase1_frac_captured = (len(length_remaining)/ len(df))*100

"""
><>><>><>><>><>><>><>><>
PHASE 2: MANUALLY CHECK REST OF JOB NOTES
><>><>><>><>><>><>><>><>
"""

# # READ IN MANUAL CHECKS/ REREAD IN DF AND SETUP FOR A MERGE WITH THOSE MANUAL CHECKS
# df = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_1_{today}.csv')
# manual_checks = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/manual_checks.csv')
#
# # isolate all those that needed manual checks (-999s), and drop the column
# df_dropped = df.loc[df['CBL_Filtering_Category'] == str(-999)].drop(columns=['CBL_Filtering_Category'])
# df_keep = df.loc[df['CBL_Filtering_Category'] != str(-999)]
#
# # now I can merge those two on their TP values
# df_dropped = df_dropped.merge(manual_checks)
# df_dropped.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE2_manually_checked.csv')
#
# # now concatonate the files completely together
# df_combined = pd.concat([df_dropped, df_keep])
#
# df_combined = df_combined.replace({'CBL_Filtering_Category': {'13C_soft_filter': 'PHASE2_13C_soft_filter',
#                                                               'Discuss': 'PHASE2_needs_discussion',
#                                                               'OK': 'PHASE2_OK',
#                                                               'Remove': 'PHASE2_Remove',
#                                                               'soft_filter': 'PHASE2_softfilter',
#                                                               }})
# # add a soft flag to those that say discuss
# df_combined.loc[df_combined['CBL_Filtering_Category'] == 'PHASE2_needs_discussion', 'flag'] = '.X.'
# df_combined.loc[df_combined['CBL_Filtering_Category'] == 'PHASE2_Remove', 'flag'] = 'X..'
#
# print(np.unique(df_combined['CBL_Filtering_Category'].astype(str)))
#
# df_combined.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_2_{today}.csv')

"""
><>><>><>><>><>><>><>><>
PHASE 3: Roughly check for outliers with plotly, and remove
><>><>><>><>><>><>><>><>
"""
# # TODO Check this section, no "test" samples exist in knowns? The plots don't change...
# df_combined = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_2_{today}.csv')
# # ONLY LOOK AT KNOWNS
# knowns = ['CBOr','GB','CBAi','CBIn','UNSt']
#
# # Code for MPL
# x = df_combined.loc[df_combined['AMScategID'].isin(knowns)]
# x.set_index('TP', inplace=True)
# x['RTS'] = x['RTS'].astype(float)
#
# fig = plt.figure(figsize=(20, 20))
# x.groupby('sampleDESC')['RTS'].plot(legend=True)
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.savefig(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/figures/roughplot.png')
#
# # Code for PLTLY
# x = df_combined.loc[df_combined['AMScategID'].isin(knowns)]
# fig = px.scatter(x, x="TP", y="RTS", color="sampleDESC",
#                  labels={
#                      "TP": "TP (Wheel Number)",
#                      "RTS": "Ratio to standard",
#                      "sampleDESC": "Sample Description"
#                  },
#                  title="Manually Specified Labels")
# fig.write_html(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/figures/LOCATE_OUTLIERS.html')
#
#
# # REPEAT CODE FROM ABOVE, removing all things with "test"
# df_combined = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_2_{today}.csv')
# df_combined = df_combined.loc[df_combined['CBL_Filtering_Category'] != 3]
#
# # Code for MPL
# x = df_combined.loc[df_combined['AMScategID'].isin(knowns)]
# x.set_index('TP', inplace=True)
# x['RTS'] = x['RTS'].astype(float)
#
# fig = plt.figure(figsize=(20, 20))
# x.groupby('sampleDESC')['RTS'].plot(legend=True)
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.savefig(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/figures/roughplot_notest.png')
#
# # Code for PLTLY
# x = df_combined.loc[df_combined['AMScategID'].isin(knowns)]
# fig = px.scatter(x, x="TP", y="RTS", color="sampleDESC",
#                  labels={
#                      "TP": "TP (Wheel Number)",
#                      "RTS": "Ratio to standard",
#                      "sampleDESC": "Sample Description"
#                  },
#                  title="Manually Specified Labels")
# fig.write_html(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/figures/LOCATE_OUTLIERS_notest.html')

"""
There's a few points that look in definite need of removal from the line Plotly line plots created above:
Here are their TP's:

NBS Oxalic, 62379, 63982
Travertine, 67815, 67816
Kauri, 64942
"""

# df_combined = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_2_{today}.csv')
#
# TPs_to_remove = [62379,63982, 67815, 67816, 64942]
# for i in range(0, len(TPs_to_remove)):
#     df_combined.loc[df_combined['TP'] == TPs_to_remove[i], 'CBL_Filtering_Category'] = 'PHASE3_PLOTLYoutlier'
#     df_combined.loc[df_combined['flag'] == TPs_to_remove[i], 'CBL_Filtering_Category'] = 'X..'
#
# print(np.unique(df_combined['CBL_Filtering_Category'].astype(str)))
#
# df_combined.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_3_{today}.csv')


"""
><>><>><>><>><>><>><>><>
PHASE 4: Look for more data to flag by making individual plots of the "knowns" and running statistics
><>><>><>><>><>><>><>><>
"""
# read in the file from previous phase and isolate only the knowns
df_p4 = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_3_{today}.csv')

# CHANGE SOME DESCRIPTIONS IF THEY'RE CAUSING ISSUES
df_p4.loc[df_p4['sampleDESC'] == 'Aliquot of SIL "Old Leucine" standard decanted into vial, used as a standard in EA combustion runs', 'sampleDESC'] = 'OLD_Leucine'
df_p4.loc[df_p4['sampleDESC'] == 'GAS-37257\x1d', 'sampleDESC'] = 'Gas-37257_noslash'
df_p4.loc[df_p4['sampleDESC'] == 'GAS-38265\x1d', 'sampleDESC'] = 'Gas-38265_noslash'
df_p4.loc[df_p4['sampleDESC'] == 'GAS-38921\x1d', 'sampleDESC'] = 'Gas-38921_noslash'
df_p4.loc[df_p4['sampleDESC'] == 'GAS35868\x1d', 'sampleDESC'] = 'Gas-35868_noslash'
df_p4.loc[df_p4['sampleDESC'] == 'Kapuni bubbled NaOH 0.01"ID tubing 30s 20140123', 'sampleDESC'] = 'Kapuni_bubbled'

# replace all the R numbers from backslashes to underscores:
fin_array = []
for i in range(0, len(df_p4)):
    row = df_p4.iloc[i]
    R = row['R']
    new_r = R.replace('/', '_')
    fin_array.append(new_r)
df_p4['New_R'] = fin_array


# Im interested in the knowns only, primaries, and secondaries
knowns = ['CBOr','GB','CBAi','CBIn','UNSt','GB','OX1','OX1_SM']
print(np.unique(df_p4['AMScategID']))
# only looking at the "knowns" (see above)
df_p4 = df_p4.loc[df_p4['AMScategID'].isin(knowns)]
# list of unique R's in the known range
knowns_rs = np.unique(df_p4['New_R'])



def stats_and_plots(r_number):
    this_one = df_p4.loc[df_p4['New_R'] == r_number].reset_index(drop=True).sort_values(by=['TW'])
    desc = this_one['sampleDESC']

    # The raw data
    x = this_one['TW'].astype(float)
    y = this_one['RTS'].astype(float)
    yerrr = this_one['RTSerr'].astype(float)

    # stats
    avs = np.mean(y)
    sigma1 = np.std(y)
    sigma2 = sigma1*2
    sigma3 = sigma1*3

    # setup figure dimensions
    fig = plt.figure(figsize=(10, 10))
    scaling_fac = 6
    plt.ylim(avs-(sigma1*scaling_fac), avs+(sigma1*scaling_fac))
    plt.title(f'{knowns_rs[i]}_{desc[0]}')
    plt.xlabel('TW')
    plt.ylabel('Ratio to Standard')

    plt.fill_between(x, avs-sigma1, avs+sigma1, color='brown', alpha=0.1)
    plt.fill_between(x, avs-sigma2, avs+sigma2, color='brown', alpha=0.05)
    plt.fill_between(x, avs-sigma3, avs+sigma3,  color='brown', alpha=0.025)
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.axhline(avs, linestyle='-', color='black',alpha=0.5)
    plt.errorbar(x, y, yerr=yerrr, fmt="o",capsize=2)
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/figures/stat_plots/{today}_{r_number}_{desc[0]}.png')

list1 = ['41347_13',
         '41347_12',
         '41347_3',
         '41347_2',
         '40699_1',
         '40430_3',
         '40430_2',
         '40430_1',
         '40142_7',
         '40142_3',
         '40142_2',
         '40142_1',
         '40113_1',
         '29855_1',
         '26294_2',
         '26294_1',
         '26281_1',
         '24779_1']

for i in range(0,len(list1)):
    stats_and_plots(str(list1[i]))

# TODO it seems like the output from this list is small. Are there some R numbers not being captured when we look in
# TODO the list of "knowns?"
























