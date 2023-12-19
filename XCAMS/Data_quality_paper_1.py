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
Phase 4 outliers/labels overwrite those from phase 3.
400 flags added to the data

"""

# IMPORT THE DATA FILE
df = pd.read_csv(r'H:\Science\Datasets\Alberts_dataquality\simplified RLIMS dataset.csv')
length_check = df
# INITIAlZE A COLUMN FOR ME TO ADD THINGS TO FILTER ON LATER
df['CBL_Filtering_Category'] = -999

"""
><>><>><>><>><>><>><>><>
PHASE 1: IDENTIFY INNOCUOUS JOB NOTES
><>><>><>><>><>><>><>><>
"""
# See documentation above for details on 1-7 labeling scheme
# Checking for "must contain -999" because if it doesn't it's already been labeled
df.loc[(df['jobNOTES'] == 'Missing[]') & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 1
df.loc[(df['jobNOTES'].str.len() == 1) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 2
df.loc[(df['jobNOTES'].str.isdigit()) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 4

# Label anything containing "test"
tests = ['TEST','test','Test']
for i in range(len(tests)):
    df.loc[(df['jobNOTES'].str.contains(tests[i], na=False)) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 3
df.loc[(df['AMScategID'] == 'Test'), 'CBL_Filtering_Category'] = 3

# HOW MANY OF THE JOB NOTES ARE SUCH AS: 1 OF 2, 3 of 6
for i in range(0, 10):
    for k in range(0, 10):
        df.loc[(df['CBL_Filtering_Category'] == -999) & (df['jobNOTES'] == f'{i} of {k}'), 'CBL_Filtering_Category'] = 5
        df.loc[(df['CBL_Filtering_Category'] == -999) & (df['jobNOTES'] == f'Split {i} of {k}'), 'CBL_Filtering_Category'] = 5
        df.loc[(df['CBL_Filtering_Category'] == -999) & (df['jobNOTES'] == f'split {i} of {k}'), 'CBL_Filtering_Category'] = 5

# HOW MANY NOTES ARE ONLY EA NUMBERS? # TODO THIS LINE TAKES THE LONGEST! (UNCOMMENT WHEN CODE IS READY
for x in range(0,10):
    for y in range(0, 10):
        for z in range(0, 10):
            df.loc[(df['jobNOTES'].str.contains(f'EA {x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
            df.loc[(df['jobNOTES'].str.contains(f'EA # {x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
            df.loc[(df['jobNOTES'].str.contains(f'EA{x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
            df.loc[(df['jobNOTES'].str.contains(f'EA #{x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
            df.loc[(df['jobNOTES'].str.contains(f'for EA{x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6

# MANY OF THE JOB NOTES ARE SOMETHING I CAN CALL "COMMON REPEATS", and are things I don't think we need to worry too much about
common_repeats = pd.read_excel(r'H:\Science\Datasets\Alberts_dataquality\common_repeats.xlsx').astype(str)
repeats = common_repeats['REPEAT']
for i in range(0, len(repeats)):
    x = str(repeats[i])
    df.loc[(df['jobNOTES'] == x) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 7


# REPLACE THE NUMBERS WITH ACTUAL LABELS THAT ARE MORE DESCRIPTIVE. FOR SOME REASON COULDN'T ADD THESE AT FIRST,
# PANDAS BUG?
df = df.replace({'CBL_Filtering_Category': {1: 'PHASE1_EmptyJobNotes',
                                            2: 'PHASE1_1-Char',
                                            3: 'PHASE1_Contains_TEST',
                                            4: 'PHASE1_Only_Digits',
                                            5: 'PHASE1_X_of_Y',
                                            6: 'PHASE1_EA_XYZ',
                                            7: 'PHASE1_Common_Repeats'}})

# add a soft flag to those that contain test
df.loc[df['CBL_Filtering_Category'] == 'PHASE1_Contains_TEST', 'flag'] = '.X.'

df.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_1.csv')
length_remaining = df.loc[df['CBL_Filtering_Category'] == -999]
phase1_frac_captured = (len(length_remaining)/ len(df))*100

# GENERATE REPORT PART1
print(f"The initial lenght of the data was {len(length_check)}, and now after phase 1 it is {len(df)}")
print(f"The amount of data that has been categorized is {len(df) - len(length_remaining)}, and the amount left the categorize is {len(length_remaining)}")

"""
><>><>><>><>><>><>><>><>
PHASE 2: MANUALLY CHECK REST OF JOB NOTES
><>><>><>><>><>><>><>><>
"""

# # READ IN MANUAL CHECKS/ REREAD IN DF AND SETUP FOR A MERGE WITH THOSE MANUAL CHECKS
df = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_1.csv')
manual_checks = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/manual_checks.csv')

# isolate all those that needed manual checks (-999s), and drop the column
df_dropped = df.loc[df['CBL_Filtering_Category'] == str(-999)].drop(columns=['CBL_Filtering_Category'])
df_keep = df.loc[df['CBL_Filtering_Category'] != str(-999)]

# now I can merge those two on their TP values
# THE TWO FILES WERE THE SAME LENGTH, BUT AFTER MERGEING, BECAME 6 VALUES LONGER...
print(len(df_dropped))
print(len(manual_checks))
df_dropped = df_dropped.merge(manual_checks)
df_dropped.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE2_manually_checked.csv')
print(len(df_dropped))
# WHY???
# duplicate_series = df_dropped.duplicated(subset=['TP'])
# duplicate_rows = df_dropped[duplicate_series]
# print("Duplicate Rows:")
# print(duplicate_rows)
# duplicate_rows.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/test2.csv')

# now concatonate the files completely together
df_combined = pd.concat([df_dropped, df_keep])

df_combined = df_combined.replace({'CBL_Filtering_Category': {'13C_soft_filter': 'PHASE2_13C_soft_filter',
                                                              'Discuss': 'PHASE2_needs_discussion',
                                                              'OK': 'PHASE2_OK',
                                                              'Remove': 'PHASE2_Remove',
                                                              'soft_filter': 'PHASE2_softfilter',
                                                              }})
# add a soft flag to those that say discuss
df_combined.loc[df_combined['CBL_Filtering_Category'] == 'PHASE2_needs_discussion', 'flag'] = '.X.'
df_combined.loc[df_combined['CBL_Filtering_Category'] == 'PHASE2_Remove', 'flag'] = 'X..'

print(np.unique(df_combined['CBL_Filtering_Category'].astype(str)))

df_combined.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_2.csv')

"""
><>><>><>><>><>><>><>><>
PHASE 3: Roughly check for outliers with plotly, and remove
><>><>><>><>><>><>><>><>
"""
# # TODO Check this section, no "test" samples exist in knowns? The plots don't change...
df_combined = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_2.csv')
# ONLY LOOK AT KNOWNS
knowns = ['CBOr','GB','CBAi','CBIn','UNSt']

# Code for MPL
x = df_combined.loc[df_combined['AMScategID'].isin(knowns)]
x.set_index('TP', inplace=True)
x['RTS'] = x['RTS'].astype(float)

fig = plt.figure(figsize=(20, 20))
x.groupby('sampleDESC')['RTS'].plot(legend=True)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/figures/roughplot.png')

# Code for PLTLY
x = df_combined.loc[df_combined['AMScategID'].isin(knowns)]
fig = px.scatter(x, x="TP", y="RTS", color="sampleDESC",
                 labels={
                     "TP": "TP (Wheel Number)",
                     "RTS": "Ratio to standard",
                     "sampleDESC": "Sample Description"
                 },
                 title="Manually Specified Labels")
fig.write_html(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/figures/LOCATE_OUTLIERS.html')


# REPEAT CODE FROM ABOVE, removing all things with "test"
df_combined = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_2.csv')
df_combined = df_combined.loc[df_combined['CBL_Filtering_Category'] != 3]

# Code for MPL
x = df_combined.loc[df_combined['AMScategID'].isin(knowns)]
x.set_index('TP', inplace=True)
x['RTS'] = x['RTS'].astype(float)

fig = plt.figure(figsize=(20, 20))
x.groupby('sampleDESC')['RTS'].plot(legend=True)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/figures/roughplot_notest.png')

# Code for PLTLY
x = df_combined.loc[df_combined['AMScategID'].isin(knowns)]
fig = px.scatter(x, x="TP", y="RTS", color="sampleDESC",
                 labels={
                     "TP": "TP (Wheel Number)",
                     "RTS": "Ratio to standard",
                     "sampleDESC": "Sample Description"
                 },
                 title="Manually Specified Labels")
fig.write_html(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/figures/LOCATE_OUTLIERS_notest.html')

"""
There's a few points that look in definite need of removal from the line Plotly line plots created above:
Here are their TP's:

NBS Oxalic, 62379, 63982
Travertine, 67815, 67816
Kauri, 64942
"""

df_combined = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_2.csv')

TPs_to_remove = [62379,63982, 67815, 67816, 64942]
for i in range(0, len(TPs_to_remove)):
    df_combined.loc[df_combined['TP'] == TPs_to_remove[i], 'CBL_Filtering_Category'] = 'PHASE3_PLOTLYoutlier'
    df_combined.loc[df_combined['flag'] == TPs_to_remove[i], 'CBL_Filtering_Category'] = 'X..'

df_combined.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_3.csv')


"""
><>><>><>><>><>><>><>><>
PHASE 4: Look for more data to flag by making individual plots of the "knowns" and running statistics
><>><>><>><>><>><>><>><>
"""
#
# read in the file from previous phase and isolate only the knowns
df_p4 = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_3.csv')
df_p4 = df_p4.loc[df_p4['RTS'] != 'Missing[]']

# CHANGE SOME DESCRIPTIONS IF THEY'RE CAUSING ISSUES
df_p4.loc[df_p4['sampleDESC'] == 'Aliquot of SIL "Old Leucine" standard decanted into vial, used as a standard in EA combustion runs', 'sampleDESC'] = 'OLD_Leucine'
df_p4.loc[df_p4['sampleDESC'] == 'GAS-37257\x1d', 'sampleDESC'] = 'Gas-37257_noslash'
df_p4.loc[df_p4['sampleDESC'] == 'GAS-38265\x1d', 'sampleDESC'] = 'Gas-38265_noslash'
df_p4.loc[df_p4['sampleDESC'] == 'GAS-38921\x1d', 'sampleDESC'] = 'Gas-38921_noslash'
df_p4.loc[df_p4['sampleDESC'] == 'GAS35868\x1d', 'sampleDESC'] = 'Gas-35868_noslash'
df_p4.loc[df_p4['sampleDESC'] == 'Kapuni bubbled NaOH 0.01"ID tubing 30s 20140123', 'sampleDESC'] = 'Kapuni_bubbled'

df_p4.loc[df_p4['sampleDESC'] == 'FIRI-C: turbidite', 'sampleDESC'] = 'firi_c_turbidite'
df_p4.loc[df_p4['sampleDESC'] == 'FIRI-D: wood', 'sampleDESC'] = 'firi_d_wood'
df_p4.loc[df_p4['sampleDESC'] == 'FIRI-E: humic acid', 'sampleDESC'] = 'firi_e_humicacid'
df_p4.loc[df_p4['sampleDESC'] == 'FIRI-F: wood', 'sampleDESC'] = 'firi_f_wood'
df_p4.loc[df_p4['sampleDESC'] == 'FIRI-G: Barley mash', 'sampleDESC'] = 'firi_g_barley_mash'
df_p4.loc[df_p4['sampleDESC'] == 'FIRI-H: wood', 'sampleDESC'] = 'firi_h_wood'
df_p4.loc[df_p4['sampleDESC'] == 'FIRI-I: cellulose', 'sampleDESC'] = 'firi_I_cellulose'
df_p4.loc[df_p4['sampleDESC'] == 'IAEA-C1: Carrara Marble', 'sampleDESC'] = 'iaea_c1_marble'
df_p4.loc[df_p4['sampleDESC'] == 'IAEA-C1: Carrara Marble WATER LINE', 'sampleDESC'] = 'iaea_c1_marble_waterline'
df_p4.loc[df_p4['sampleDESC'] == 'IAEA-C1: Carrara Marble WATER LINE COMBINED', 'sampleDESC'] = 'iaea_c1_marble_waterlinecombined'
df_p4.loc[df_p4['sampleDESC'] == 'IAEA-C2: Freshwater Travertine', 'sampleDESC'] = 'iaea_c2_travertine'

df_p4.loc[df_p4['sampleDESC'] == 'TIRI H: Ellanmore Whole Peat', 'sampleDESC'] = 'tiri_h_peat'
df_p4.loc[df_p4['sampleDESC'] == 'TIRI I: Caerwys Quarry Travertine', 'sampleDESC'] = 'tiri_t_quarry_travertine'
df_p4.loc[df_p4['sampleDESC'] == 'TIRI J: Buiston Crannog Palisade - Wood', 'sampleDESC'] = 'tiri_j_wood'
df_p4.loc[df_p4['sampleDESC'] == 'TIRI K: Turbidite Carbonate (Mainly Coccolith Calcite)', 'sampleDESC'] = 'tiri_k_carbonate'
df_p4.loc[df_p4['sampleDESC'] == 'TIRI L: Whalebone', 'sampleDESC'] = 'tiri_l_whalebone'

# replace all the R numbers from backslashes to underscores:
fin_array = []
for i in range(0, len(df_p4)):
    row = df_p4.iloc[i]
    R = row['R']
    new_r = R.replace('/', '_')
    fin_array.append(new_r)
df_p4['New_R'] = fin_array

# I ONLY WANT TO EDIT/LOOK AT DATA WHO ARE IN THE "KNOWNS"
# LETS CREATE A UNIQUE LIST OF R NUMBERS FOR THE KNOWNS
knowns = ['CBOr','GB','CBAi','CBIn','UNSt','GB','OX1','OX1_SM']
sub_list = df_p4.loc[df_p4['AMScategID'].isin(knowns)]
knowns_Rs = np.unique(sub_list['New_R'])

df_p4['CBL_stat_flags'] = -999
for i in range(0, len(knowns_Rs)):
    # where-ever the data is 3-sigma greater than the mean,
    subset = df_p4.loc[df_p4['New_R'] == knowns_Rs[i]].reset_index(drop=True)

    if len(subset) > 3:
        x = subset['TW'].astype(float)
        y = subset['RTS'].astype(float)
        yerr = subset['RTSerr'].astype(float)
        mean1 = np.mean(y)
        one_sig = np.std(y)
        two_sig = 2*one_sig
        three_sig = 3*one_sig
        desc = subset['sampleDESC']

        tests = df_p4.loc[(df_p4['New_R'] == knowns_Rs[i]) & (df_p4['CBL_Filtering_Category'] == 'PHASE1_Contains_TEST')].sort_values(by=['TW'])

        # FLAG ANNYTHING THAT IS GREATER THAN 3 SIGMA
        df_p4.loc[(df_p4['New_R'] == knowns_Rs[i]) & (df_p4['RTS'].astype(float) > (mean1+three_sig)).astype(float), 'flag'] = 'X..'
        df_p4.loc[(df_p4['New_R'] == knowns_Rs[i]) & (df_p4['RTS'].astype(float) < (mean1-three_sig)).astype(float), 'flag'] = 'X..'
        df_p4.loc[(df_p4['New_R'] == knowns_Rs[i]) & (df_p4['RTS'].astype(float) > (mean1+three_sig)).astype(float), 'CBL_Filtering_Category'] = 'Phase4_3_sigma_out'
        df_p4.loc[(df_p4['New_R'] == knowns_Rs[i]) & (df_p4['RTS'].astype(float) < (mean1-three_sig)).astype(float), 'CBL_Filtering_Category'] = 'Phase4_3_sigma_out'

        flagged = df_p4.loc[(df_p4['New_R'] == knowns_Rs[i]) & (df_p4['CBL_Filtering_Category'] == 'Phase4_3_sigma_out')].sort_values(by=['TW'])
        not_flagged = df_p4.loc[(df_p4['New_R'] == knowns_Rs[i]) & (df_p4['CBL_Filtering_Category'] != 'Phase4_3_sigma_out')].sort_values(by=['TW'])

        fig = plt.figure(figsize=(10, 8))
        scaling_fac = 6
        plt.ylim(mean1-(one_sig*scaling_fac), mean1+(one_sig*scaling_fac))
        plt.xlabel('TW')
        plt.ylabel('Ratio to Standard')
        plt.title(f'{knowns_Rs[i]}_{desc[0]}')
        plt.axhline(mean1, color='black')
        plt.fill_between(not_flagged['TW'], mean1-three_sig, mean1+three_sig, alpha=0.1)
        plt.fill_between(not_flagged['TW'], mean1-two_sig, mean1+two_sig, alpha=0.15)
        plt.fill_between(not_flagged['TW'], mean1-one_sig, mean1+one_sig, alpha=0.2)

        plt.errorbar(flagged['TW'].astype(float), flagged['RTS'].astype(float), yerr=flagged['RTSerr'].astype(float), color='red', capsize=2, fmt='o', label='3-\u03C3 flag')
        plt.errorbar(not_flagged['TW'].astype(float), not_flagged['RTS'].astype(float), yerr=not_flagged['RTSerr'].astype(float), color='blue', capsize=2, fmt='o', label='No flag')
        plt.errorbar(tests['TW'].astype(float), tests['RTS'].astype(float), yerr=tests['RTSerr'].astype(float), color='yellow', capsize=2, fmt='o', label='Job Notes = Test')
        plt.legend()
        plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/figures/stat_plots/{knowns_Rs[i]}_{desc[0]}.png', dpi=300, bbox_inches="tight")
df_p4.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_4.csv')
print(len(df_p4))
print(np.unique(df_p4['CBL_Filtering_Category'].astype(str)))


# """
# I'm now returning to this project a few months later (12/18/2023)
# I can see in Phase3.csv, that all of the data are labeled, however, i cant find if I've removed any of the data yet for
# the plots that are created in the segment just above. I can check that by just looking at the lenght of the files
# from the original file to the phase3 file.
# """
df = pd.read_csv(r'H:\Science\Datasets\Alberts_dataquality\simplified RLIMS dataset.csv')
df_p1 = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_1.csv')
df_p2 = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_2.csv')
df_p3 = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_3.csv')
df_p4 = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_4.csv')

print(len(df))
print(len(df_p1))
print(len(df_p2))
print(len(df_p3))
print(len(df_p4))






