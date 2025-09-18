
"""
Sept 15 2024,
We changed a few things. Editing step 7

We are working on an AMS data quality paper that was originally started by Albert Zondervan, who is not at uOttawa.
Jocelyn wants to rerun the scripts that created the plots, and numbers for the data quality paper; however, we
are concerned that many data in the record should have quality flags, and currently do not. This script's goal is to
help me identify and flag those data.

June 7, 2024
Pickng this project back up full steam ahead. Re-running script along with writng more notes in my methods doc.
I'm writing the script to follow a workflow in the associated power point Draft1_progress.pptx.


January 8, 2024
Re-exporting the full RLIMS dataset to run the script and will keep updating here. 

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
import pandas as pd
import numpy as np
import warnings
import os
from datetime import date
warnings.simplefilter(action='ignore')
import plotly.express as px
import matplotlib.pyplot as plt
today = date.today()

# """
# IMPORT THE DATA FILE
# """
# # # this file contains all of RLIMS as downloaded from one of our most recent wheels (today is 21/12/2023; Dec 21),
# df = pd.read_csv(r'H:\Science\Datasets\Alberts_dataquality\FINAL_WORKING_DATASET.csv').dropna(subset='TP')
# df = df.dropna(subset='RTS_corrected')
# print(f'The original length of the dataframe is {len(df)}')
#
# #
# """
# I'm having trouble with the flagging, so I need to be able to generate continuous status reports as I flag. I don't
# want to keep repeating the code, so I'll write a function to do it.
# """
def flagging_status_check(comment):
    # find the unique quality flags and their occurances, put it into a dataframe
    unique_values_A = df['Quality Flag'].value_counts()
    qfs = pd.DataFrame(unique_values_A)

    unique_values_B = df['Keep_Remove'].value_counts()
    krs = pd.DataFrame(unique_values_B)

    unique_values_C = df['Comment'].value_counts()
    comms = pd.DataFrame(unique_values_C)

    removes = df.loc[df['Keep_Remove'] == 'Remove']

    with pd.ExcelWriter(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/{comment}.xlsx', engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name='Whole Dataframe')
        removes.to_excel(writer, sheet_name='Set For Removal')
        qfs.to_excel(writer, sheet_name='Quality Flags')
        krs.to_excel(writer, sheet_name='Keep Remove Counts')
        comms.to_excel(writer, sheet_name='Comments')

# """
# Output initial description file for this dataframe
# """
# # initalize this category
# df['Keep_Remove'] = 'NYC' # not yet categorized
# df['Comment'] = 'NAN'
# flagging_status_check('01_Initial_State')
#
# #
# """
# Label those that have been manually checked for removal
# In June 2024, I had already manually selected loads for removal. Those TP's are here below...
# """
# # put all those that have already been manually checked as labeled for REMOVAL
# for_removal = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/Manually_checked_data.xlsx')
# df.loc[df['TP'].isin(for_removal['TP']), 'Keep_Remove'] = 'Remove'
# df.loc[df['TP'].isin(for_removal['TP']), 'Comment'] = 'Manually checked in previous iteration of screening work. Labelled for removal here'
# flagging_status_check('02_Manual_Checks_Removed')
#
# #
# """
# Set all the hard flags for removal
# """
# hards = ['A..','N..','X..','P..','O..','E..','T..','x..']
# df.loc[df['Quality Flag'].isin(hards), 'Keep_Remove'] = 'Remove'
# df.loc[df['Quality Flag'].isin(hards), 'Comment'] = 'Hard Flag Found. Set for removal'
# flagging_status_check('03_Hard_flags_removed')
#
# """
# I've already gone through and manaully screened for all the middle "soft" flags that need to be categorized,
# and these were removed in step 01 (manual checks), I can label the remaining for keeping
# """
# softs = ['.X.','.A.','.S.','.T.','.O.','.Q.','.D.','.E.','.F.','.C.']
# df.loc[(df['Quality Flag'].isin(softs)) & (df['Keep_Remove'] == 'NYC'), 'Keep_Remove'] = 'Keep'
# df.loc[(df['Quality Flag'].isin(softs)) & (df['Keep_Remove'] == 'Keep'), 'Comment'] = 'Soft flag; but not seen as required for removal. Set to "keep"'
# # flagging_status_check('04_soft_flags_removed')
#
# """
# Set all 'informational' flags to keep if they're not already labelled for removal
# """
# infs = ['..D','..X','..T','..S']
# df.loc[(df['Quality Flag'].isin(infs)) & (df['Keep_Remove'] == 'NYC'), 'Keep_Remove'] = 'Keep'
# df.loc[(df['Quality Flag'].isin(infs)) & (df['Keep_Remove'] == 'Keep'), 'Comment'] = 'Informational Flags set for keep if not already labelled for removal'
# # flagging_status_check('05_informational_flags')
#
# """
# Weird quality flags need to be manaully checked. But I checked them and they look fine according to job notes.
# """
# odd = ['X.S','A.S','O.D','.FD']
# df.loc[(df['Quality Flag'].isin(odd)) & (df['Keep_Remove'] == 'NYC'), 'Keep_Remove'] = 'Keep'
# df.loc[(df['Quality Flag'].isin(odd)) & (df['Keep_Remove'] == 'Keep'), 'Comment'] = 'Odd quality Flag, but set for keeping at this point'
# # flagging_status_check('06_odd_flags')
#
# # whats left are the NON flagged data that need to be checked for flags requried, but first I need to fix a few of the flags
# df = df.replace({'Quality Flag': {'.....': '...'}})
# #
# """
# # Flag all samples that contain the word "test" in job notes
# """
# df = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Paper_1_output\06_odd_flags.xlsx", sheet_name='Whole Dataframe')
# tests = ['TEST','test','Test']
# for i in range(len(tests)):
#     df.loc[(df['Job::Job notes'].str.contains(tests[i], na=False)) & (df['Keep_Remove'] == 'NYC') & (df['Quality Flag'] == '...'), 'Keep_Remove'] = 'Keep' # edited from Remove to Keep on Sept 15 2025
#     df.loc[(df['Job::Job notes'].str.contains(tests[i], na=False)) & (df['Keep_Remove'] == 'Keep') & (df['Quality Flag'] == '..T'), 'Keep_Remove'] = 'Keep' # edited from Remove to Keep on Sept 15 2025
#     df.loc[(df['Job::Job notes'].str.contains(tests[i], na=False)) & (df['Keep_Remove'] == 'Remove'), 'Comment'] = 'Removed because the keyword test was found in job notes, quality flag should be added!'
# flagging_status_check('07_test_found')

"""
On June 21, 2024, I received an email with these “test” jobs manually checked by Jocelyn, but there were only 590 rows with the “test” keyword comment. Where are the rest? I'm going to check the difference 
"""
# import pandas as pd
#
# df1 = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Paper_1_output\07_test_found.xlsx")
# df1 = df1.loc[df1['Comment'] == 'Removed because the keyword test was found in job notes, quality flag should be added!']
# df2 = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Paper_1_output\Final_RLIMS_IMPORT_toshare.xlsx")
# df2 = df2.loc[df2['Comment'] == 'Removed because the keyword test was found in job notes, quality flag should be added!']
# diff = df1[~df1["TP"].isin(df2["TP"])]
# diff.to_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Paper_1_output\diff_test.xlsx")

# """
# Merge Jocelyn's Manual Comments with my dataframe
# """
#
# jct = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Paper_1_output\Final_RLIMS_IMPORT_toshare.xlsx")
# print(np.unique(jct['Should a new flag be added? ']))
# df = df.merge(jct[['TP', 'JCT','Manual Check Comment','Should a new flag be added? ']], on='TP', how='left')
# # change keep-remove status based on Jocleny's suggsted flagging
# df.loc[(df['Should a new flag be added? '] == 'X..'), 'Keep_Remove'] = 'Remove'
# df.loc[(df['Should a new flag be added? '] == 'X..'), 'Comment'] = 'Removed beacuse of Jocelyns manual check'
# flagging_status_check('07_and_a_half_JCT_manualcheck')
#
# """
# First, I want to make sure there are no werid values or other strings in FM column. I'm having a lot of trouble
# with random '?' characters...
# """
# mask = df.applymap(lambda x: x == '?')
#
# # Step 3: Identify and retrieve the cells with '?'
# rows, cols = mask.any(axis=1), mask.any(axis=0)
# positions = [(row, col) for row in mask.index for col in mask.columns if mask.at[row, col]]
#
# # print("Positions of '?':", positions)
# df.loc[mask.any(axis=1), 'Keep_Remove'] = 'Remove'
# df.loc[mask.any(axis=1), 'Comment'] = 'Annoying ? character is breaking my code'
# flagging_status_check('08_questionmark_found_removed')
#
# """
# Set rest of positions not yet characterized to keep
# """
# df.loc[(df['Keep_Remove'] == 'NYC'), 'Keep_Remove'] = 'Keep'
# flagging_status_check('09_NYC_changed_to_keep')
#
# """
# Remove where there is no FM data
# """
# df.loc[(df['F_corrected_normed'] == ''), 'Comment'] = 'Removed because absence of FM data'
# df.loc[(df['F_corrected_normed'] == ''), 'Keep_Remove'] = 'Remove'
#
# df.loc[(df['F_corrected_normed_error'] == ''), 'Comment'] = 'Removed because absence of FM data'
# df.loc[(df['F_corrected_normed_error'] == ''), 'Keep_Remove'] = 'Remove'
#
# # editing some flags in the above excel sheet on October 14, 2024 based on some extra analysis
# # This chunk used to be in Data_quality_paper3.py but has now been moved
# df.loc[(df['Job::R'] == '40142/1_CELL_ST') & (df['TP'] > 63764) & (df['TP'] < 65183), 'Keep_Remove'] = 'Remove'
# df.loc[(df['Job::R'] == '40142/1_CELL_ST') & (df['TP'] > 63764) & (df['TP'] < 65183), 'Comment'] = 'editing some flags in the above excel sheet on October 14, 2024 based on some extra analysis'
# # length123 = df.loc[(df['Job::R'] == '40142/1_CELL_ST') & (df['Keep_Remove'] == 'Keep')]
# flagging_status_check('10_FM_dropna')
df = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/10_FM_dropna.xlsx')

"""
SPLITTING DATAFRAME INTO KEEP AND REMOVE, WILL MERGE BACK LATER. FLAGGING BASED ON STATISTUCS
We're going to create a 4-panel plot. FM over time, and residual (left top and bottom),
Then FM over time and residual after 3-sigma flag removes.

"""
df_keep = df.loc[df['Keep_Remove'] == 'Keep']
df_rem = df.loc[df['Keep_Remove'] == 'Remove']

df_keep['F_corrected_normed'] = df_keep['F_corrected_normed'].astype(float)
df_keep['F_corrected_normed_error'] = df_keep['F_corrected_normed_error'].astype(float)

# how many different R numbers are there in the dataset?
df_keep['Job::R'] = df['Job::R'].replace('/', '_', regex=True)#
rs = df_keep['Job::R'].value_counts()

# Filter to get only those with 10 or more counts
rs = rs[rs >= 10]
rs = pd.DataFrame(rs)
rs.to_excel(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/Rs_more_than_10.xlsx')
rs = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/Rs_more_than_10.xlsx')
rs = rs['Job::R']

# Initialize an empty list to collect all the outlier TPs
outlier_TPs = []

# set output for plotly file later
outdir = r"C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/plotly_manual_flag"

# TODO continue here making the figure
# TODO If >3 sigma, add it to a growing list, and then I can just set all those TP's to remove later.
# Now we'll loop, calculate the mean of each R, and set a flag for data where the value is > 3 sigma
for i in range(0, len(rs)):

    # Initialize Figure
    # Create 2x2 grid of subplots
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    plt.subplots_adjust(wspace=0.4, hspace=0.3)
    # Access each subplot
    ax1 = axes[0, 0]  # top left
    ax2 = axes[0, 1]  # top right
    ax3 = axes[1, 0]  # bottom left
    ax4 = axes[1, 1]  # bottom right

    # get the data with this R value
    this_R_set = df_keep.loc[(df_keep['Job::R'] == rs[i])].reset_index(drop=True)
    descrip = this_R_set['Samples::Sample Description']
    descrip = descrip.replace('-', '_', regex=True)#
    descrip = descrip.replace(':', '_', regex=True)#
    descrip=descrip[0]
    ax1.errorbar(this_R_set['TP'], this_R_set['F_corrected_normed'], yerr=this_R_set['F_corrected_normed_error'], marker='o', linestyle='', color='black', alpha=0.5)

    # find the average for the R number
    data = this_R_set['F_corrected_normed'].astype(float) # data needed to be forced to float)
    unc = this_R_set['F_corrected_normed_error'].astype(float)
    average = np.mean(data)
    sig1 = np.std(data)
    ax1.axhline(average, color='k', linestyle='--', linewidth=1)               # mean
    ax1.axhline(average + 3*sig1, color='r', linestyle=':', linewidth=1)       # +3 sigma
    ax1.axhline(average - 3*sig1, color='r', linestyle=':', linewidth=1)       # -3 sigma

    # calculate the residual for this one
    this_R_set['residual'] = (this_R_set['F_corrected_normed'] - average)/this_R_set['F_corrected_normed_error']

    # find outliers (more than 3 sigma from mean)
    mask = ((data - unc) > (average + 3*sig1)) | ((data+unc) < (average - 3*sig1))

    # collect the TPs from those rows
    outlier_TPs.extend(this_R_set.loc[mask, 'TP'].tolist())

    ax3.scatter(this_R_set['TP'], this_R_set['residual'], color='black', alpha=0.5)

    # print(outlier_TPs)
    ax1.set_title(f'Before Statistical Flagging')
    ax3.set_xlabel('TP Number')
    ax1.set_ylabel('F_corrected_normed')
    ax3.set_ylabel('Residual')

    """
    make right side 2 plots after the removal of the data
    """

    # make a second subset of this TP number, where those TP's that were highlighted as outliers are removed
    this_R_set2 = this_R_set.loc[~this_R_set['TP'].isin(outlier_TPs)].reset_index(drop=True)

    # find the average for the R number
    data2 = this_R_set2['F_corrected_normed'].astype(float) # data needed to be forced to float)
    unc2 = this_R_set2['F_corrected_normed_error'].astype(float)
    average2 = np.mean(data2)
    sig1_2 = np.std(data2) # 1-sigma for this secondary subset after outliers are removed
    ax2.axhline(average, color='k', linestyle='--', linewidth=1)               # mean
    ax2.axhline(average + 3*sig1_2, color='r', linestyle=':', linewidth=1)       # +3 sigma
    ax2.axhline(average - 3*sig1_2, color='r', linestyle=':', linewidth=1)       # -3 sigma

    # calculate the residual for this one
    this_R_set2['residual'] = (this_R_set2['F_corrected_normed'] - average2)/this_R_set2['F_corrected_normed_error']
    ax2.errorbar(this_R_set2['TP'], this_R_set2['F_corrected_normed'], yerr=this_R_set2['F_corrected_normed_error'], marker='o', linestyle='', color='black', alpha=0.5)
    ax4.scatter(this_R_set2['TP'], this_R_set2['residual'], color='black', alpha=0.5)

    # print(outlier_TPs)
    ax2.set_title(f'After Statistical Flagging')
    ax4.set_xlabel('TP Number')
    ax2.set_ylabel('F_corrected_normed')
    ax4.set_ylabel('Residual')

    # strike line through residuals
    ax3.axhline(0, color='k', linestyle='--', linewidth=1)               # mean
    ax4.axhline(0, color='k', linestyle='--', linewidth=1)               # mean


    # Add subplot labels
    ax1.text(-0.1, 1.05, "A", transform=ax1.transAxes,
             fontsize=14, fontweight="bold", va="top", ha="right")
    ax2.text(-0.1, 1.05, "B", transform=ax2.transAxes,
             fontsize=14, fontweight="bold", va="top", ha="right")
    ax3.text(-0.1, 1.05, "C", transform=ax3.transAxes,
             fontsize=14, fontweight="bold", va="top", ha="right")
    ax4.text(-0.1, 1.05, "D", transform=ax4.transAxes,
             fontsize=14, fontweight="bold", va="top", ha="right")

    plt.savefig((f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/3_sigma_flag/{rs[i]}.png'))
    # TODO CHANGE KEEP/REMOVES AND COMMENTS FOR THOSE IN TP_OUTLIER LIST GENERATED IN LOOP ABOVE
    # TODO CHECK ALL PLOTS FOR MORE MANUAL POINTS TO REMOVE (14047_2 (MADE IT THROUGH FILTER BECAUSE OF LARGE ERROR BARS)) AND 24779_1

    plt.close()

    # use plotly created now for next manual filtering step (see later)
    fig = px.scatter(this_R_set2, x="TP", y="F_corrected_normed", error_y="F_corrected_normed_error", hover_data=["TP"],title=f"R = {rs[i]}")
    outfile = os.path.join(outdir, f"{rs[i]}.html")
    # Save as interactive HTML
    fig.write_html(outfile)

"""
So, to create the plots above, we created new dataframes called DF_keep and DF_remove, but we dno't need to recombine
them or anything, we just needed to create a list of new TP's to flag.
"""
df.loc[(df['TP'].isin(outlier_TPs)), 'Comment'] = 'Caught in 3-sigma statistical flag, see plot. Sept 18, 2025 CBL'
df.loc[(df['TP'].isin(outlier_TPs)), 'Keep_Remove'] = 'Remove'
flagging_status_check('11_3_sigma_drop')

"""
Even after the plots and 3 sigma flag, I still quickly find outlier that need removal and flagging. 
For instance 14047_2 has one that has huge errors so it's not excluded, but its so obviously bad. 
We can use plotlys created above to quickly hover over and find where these points are...
"""
# 24779 is sucrose where loads just dont have data!!!!
manual_remove_tps = [67815,  # 14047_2
# TODO keep checking plotly for manual removals!



                     ]







#
    # # the maximum allowed value is the average + 3 sigma, min is average - 3 sigma
    # max_allowed = average+(3*sig1)
    # min_allowed = average-(3*sig1)
    #
    # # where do outliers exist?
    # # where is the measured value - the 1-sigma, still higher than allowed max?
    # df_keep.loc[((df_keep['Job::R'] == rs[i]) &
    #              ((df_keep['F_corrected_normed']-df_keep['F_corrected_normed_error']) > max_allowed)),
    #             'Keep_Remove'] = 'Remove'
    # df_keep.loc[((df_keep['Job::R'] == rs[i]) &
    #              ((df_keep['F_corrected_normed']-df_keep['F_corrected_normed_error']) > max_allowed)),
    #             'Comment'] = 'Removed because the value greater than 3-sigma including error'
#
#     # where is the measured value - the 1+sigma, still lower than allowed max?
#     df_keep.loc[((df_keep['Job::R'] == rs[i]) &
#                  ((df_keep['F_corrected_normed']+df_keep['F_corrected_normed_error']) < min_allowed)),
#                 'Keep_Remove'] = 'Remove'
#     df_keep.loc[((df_keep['Job::R'] == rs[i]) &
#                  ((df_keep['F_corrected_normed']+df_keep['F_corrected_normed_error']) < min_allowed)),
#                 'Comment'] = 'Removed because the value less than 3-sigma including error'
# #
# # where were REMOVES and COMMENTS added in the Keep DF from the 3-sigma change?
# high_removes = df_keep.loc[df_keep['Comment'] == 'Removed because the value greater than 3-sigma including error']
# low_removes = df_keep.loc[df_keep['Comment'] == 'Removed because the value less than 3-sigma including error']
#
# # move these comments and KEEP/REMOVES over to the main DF
# df.loc[(df['TP'].isin(high_removes['TP'])), 'Keep_Remove'] = 'Remove'
# df.loc[(df['TP'].isin(high_removes['TP'])), 'Comment'] = 'Removed because the value greater than 3-sigma including error'
#
# df.loc[(df['TP'].isin(low_removes['TP'])), 'Keep_Remove'] = 'Remove'
# df.loc[(df['TP'].isin(low_removes['TP'])), 'Comment'] = 'Removed because the value less than 3-sigma including error'
#
# # here, the final DF is written to the drive. !
# flagging_status_check('11_3_sigma_drop')
#
# """
# LETS MANUALLY LOOK AT EVERYTHING SET FOR REMOVAL AND CHECK WE HAVEN"T FLAGGED ANYTHING WE ACTUALLY THINK IS OK
# """
#
# checks = df.loc[df['Keep_Remove'] == 'Remove']
# checks.to_excel((r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/Double_Check.xlsx'))
#
# """
# I can reimport everything from here so the script doesnt have to run all over again...
# """
# import pandas as pd
#
# df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/11_3_sigma_drop.xlsx', sheet_name= 'Whole Dataframe')
# print(len(df))
#
# # I manually looked at every line and decided where flags needs to be added or not. double check moved to H drive in case of computer failure.
# checks = pd.read_excel((r'H:/Science/Papers/In Prep Work/2023_Zondervan_DataQuality/Moved to IDrive/Double_check.xlsx'))
#
# # there were many cases in which flags need to be added.
# # here is the final list of where flags need to be added. This searches for 1) where the quality flag was empty and 2) where the NEW quality flag is NOT empty.
# final_import_to_rlims = checks.loc[(checks['Quality Flag'] == '...') & (checks['Should a new flag be added? '] != -999)]
# # print(len(final_import_to_rlims))
# final_import_to_rlims.to_excel((r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/Final_RLIMS_IMPORT.xlsx'))
#
# # here is the file that Jocelyn has manually checked.
# checks_final = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/Final_RLIMS_IMPORT_toshare.xlsx', sheet_name= 'SelectColumns')
#
# JTs_comments = np.unique(checks_final['JCT'].astype(str))
# # print(JTs_comments)
#
# comments_to_keep = ['AMS is fine' 'Also Waikato tests',
#                     'Checked RLIMS - no problem' ,
#                     'Good result',
#                     'I think these are fine, it was a problem with 13C not AMS',
#                     "I think this is fine - one of Mr Potato Chips' samples",
#                     'I think this one is fine' "Just didn't get a 13C" 'LG1 not RG20',
#                     'Mr Potato Chips' ,
#                     'No flag needed',
#                     'No flag needed - this was a test that demonstrated that doing single combustions gives different results than splitting a large combustion and this is how we do things now',
#                     'Notes show it is fine',
#                     'Ok but different treatment than usual',
#                     'Probably ok - these are where we changed the amount of CuO in combustion tubes',
#                     'RPO complexities' 'Repeat - this one is ok',
#                     'Result agrees for both measurements of this sample',
#                     'Result is fine',
#                     'ST was repeated - no problem',
#                     'These were sent to ANU (SSAMS) to make sure we can run our samples there',
#                     'These were submitted as graphite, and are tests freom Waikato',
#                     'This sample was run 3 times and this is one of the good repeats',
#                     'ok - early tests of RG20',
#                     'this is a second calams analysis of the same wheel',
#                     'JCT Either EA or sealed tube is fine - whichever is more convenient._x000B_For Waikato/GNS intercomparison test wheel - larger batch may be combusted and split for graphitization_x000B_']
#
#
# # the next three lines takes all TP's with Jocelyns comments above (which make the data seem fine) and changes the Keep Remove to Keep
# # TODO these lines take TP numbers where JCT checked it and was happy, and changes Keep_Remove to Keep. However, the manual check notes, or the flag,
# # TODO or the rest of the information gets lost. This needs to be done a bit cleaner...
# # TODO additionally, this process can likely be re-written to be smoother in a second go-around (if I'm re-doing this stuff)
# TPs_for_keeping = checks_final.loc[checks_final['JCT'].isin(comments_to_keep)]
# TPs_for_keeping = TPs_for_keeping['TP']
# df.loc[df['TP'].isin(TPs_for_keeping), 'Keep_Remove'] = 'Keep'
# print(len(df))
#
# flagging_status_check('12_second_manual_check')

# NOTICED THAT THERE ARE STILL SOME ISSUES TO BE RESOLVED HERE...

