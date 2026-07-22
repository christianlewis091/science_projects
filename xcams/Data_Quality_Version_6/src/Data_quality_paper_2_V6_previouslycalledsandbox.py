"""
IMPORT STATEMENT
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
# from inorganics_troublehsooting import solved_it_list
import seaborn as sns

"""
May 25, 2026
Another big edit: We're going to add data from 2024 to present, so not cut ourselves short of data that we have/data that's been accumulating as we've been 
trying to get the paper done. This was dealt with by creating a new version (V6), and incorporating data in the early section of Data_Quality)_paper_1_v6.py


Met with JCT on April 2, 2026, and found some more large feedback that will require restructuting the code.
Good news is the pieces are all in place so it should be straightforward and more elegent.
What needs to be changes? sigma_bw needs to be calcualted according to groups FIRST (airs, inorganics, water, etc).
Then, that sigma_bw can be applied when calculating mean FM and D14C values that are reported for each secondary.
Before, I was calculating a sigma_bw for each standard. But you can't do this for unknowns. THat's why we need one per pretreatment group.

How are we going to achieve this?
I'll try to make a descriptive outline here before I get straight into coding.

## STEP 0.
 - A bit more of data cleaning:
 - In the past I've been working with a larger excel sheet. Now, I'll just locate the R's I'm interested in (secondaries, stds, blanks,
   and remove the rest.
 - There will be some inclusion of preamble from previous versions of this code
 - A lot of this workflow depends on data being in the groups listed above. So the first thing
   is to add a column that we can locate on, saying which group each R is in.
   ## our groups are: air_r = ['40430/1','40430/2'];
                   inor_r = ['41347/2','41347/3'];
                   water_r = ['41347/12','41347/13'];
                   organic_r = ['24889/4','24889/5','24889/7','24889/9'];
                   rpo = ['24889/14']

## STEP 1.1: CALCULATE CHI2 FOR EACH GROUP (chi2 requires RTS, weighted mean, and RTS_err)
 - calculate weighted mean in RTS space using eqn from _2. Use groupby for cleanliness
 - now calculate chi2 reduced

## STEP 1.2: CALCULATE SIGMA_BW FOR GROUPS
 - assign collection date for each group using the secondaries.xlsx file and take careful notes about
   how we're lucky all secondaries have the same collection date...otherwise this would be more
   complicated (sigma_bw is grouped from different R's, so if different R's had different collection dates,
   it would be difficult to convert sigma_bw to per mil based on those collection dates

 - calculate sigma_bw using RTS and chi2 from above.
 - output n, chi2 reduced, and sigma_bw to an excel file.

 # STEP 2: CALCULATE SUMMARY STATISTICS AND MAKE PLOTS FOR ALL SECONDARY STANDARDS AND BLANKS
 # STEP 2.1 HOUSEKEEPING
 - At the end of this step, we want sigma_ams (easy), chi2_reduced, FM, and D14C for each secondary standard and blank
 - In order to set ourselves up for success, we need to associate a few extra bits of information with each R number
 - - Associate the sigma_bw that we calculated above based on group (use .loc function that we do in _1 script)
 - - Associate collection dates based on groups (again we're lucky its the same for every group type)

 # STEP 2.2: INDEX BASED ON PRETREATMENTS
 - - Then, we've been asked to index/seperate a lot of the organics based on pre-treatment. This will be a chunk of messy code

 # STEP 2.3: CALCULATE SUMMARY STATS
 - - Then we can run our loop from _2 to calculate summary statistics and make plots
 - - - Lets still use RTS for chi2 reduced, with the undestanding that chi2_red > 1 is dealt with with sigma_bw which is included in FM error (the following step)
 - - - The plots are in FM, so we'll need to convert to FM (see _2 for that bit of code)

 # STEP 2.4 OUTPUT DATA
 - Simply calculate D14C after the loop has found wmean of FM. We don't need to calc D14C in the loop
 - ouput data with n, chi2_red, FM, FM_err (using new sig_bw) and D14C

#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&
Some more comments on the metadata:
Its been messy to add new versions of the code/restructure it and draw from previous folders,
So I'll do my best to update the directories so they're clean/all in one space.

The files we'll need for this to run smoothly are:
1. "12_manual_plotly_drop": the last iteration of data cleaning/checking from the _1 script.
   This lives here: C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/12_manual_plotly_drop.xlsx

2. "Secondaries.xlsx":
    An old version lived here: "C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_paper_2_2025_output\seconds.xlsx"
    Now it lives: "C:/Users\clewis\IdeaProjects\GNS/xcams\seconds_April3_2026.xlsx" because its a mistake to create loads of new folders
    for the percieved sake of tidiness

#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&#!(*$^%&
What functions will we need for this to be done most cleanly?
 - weighted mean calculation
 - chi2 reduced calculation
 - conversion to per mil
 - conversion to D14C
 
These will be based on prevoius versions of the code and will be put at the top. I'll try to use them as much as possible
to keep everything tidy. 
"""
# FUNCTIONS
# calculate delta14C from FM
def calc_delta_14C(FM, FM_err, colldate):
    # delta_14C = ((FM*np.exp((1950-colldate)/8267))-1)*1000 # my written version
    delta_14C =  1000*(FM*np.exp((1950-colldate)/8267)-1)
    delta_14C_err = 1000*(FM_err*np.exp((1950-colldate)/8267))
    return delta_14C, delta_14C_err

# convert ratio to standard to per mil, for instance for sigma_bw calculation
def rts_to_permille_for_errors(rts, colldate):
    rts_to_FM  = (np.sqrt(rts**2)/0.95)*0.98780499
    FM_to_permille = 1000*(rts_to_FM*np.exp((1950-colldate)/8267))
    return FM_to_permille



def weighted_mean(rts_corrected, rts_corrected_error):
    wmean_num = np.sum(rts_corrected/rts_corrected_error**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    wmean_dem = np.sum(1/rts_corrected_error**2)
    wmean = wmean_num / wmean_dem
    return wmean

# DONT COMBINE THE FOLLOWING FUNCTIONS ALL INTO ONE!
# residual is calculate per row, (will be appended for each row to plot on a figure)
# chi2 is caluclated per R number, and also per group
# sigma_bw is calculated only for each main group.
def residual(rts_corrected, wm, rts_corrected_error):
    residual = (rts_corrected - wm) / rts_corrected_error
    return residual

def calc_chi2_red(rts_corrected, wm, rts_corrected_error):
    chi2_red_num = np.sum((rts_corrected-wm)**2/rts_corrected_error**2)
    chi2_red_denom = len(rts_corrected)-1 # subtract number of groups in degrees of freedom calc.

    chi2_red = chi2_red_num/chi2_red_denom


    return chi2_red

def calculate_sigma_bw(chi2_red_input, rts_corrected_error):
    if chi2_red_input < 1:
        sigbw = 0

    else:
        term2 = np.sqrt(chi2_red_input - 1)
        term1 = np.nanmean(rts_corrected_error)
        sigbw = term1*term2

    return sigbw

def check_firi_length(df, comment):
    checks = ['24889/4', '24889/6']
    subdf_lencheck = df.loc[df['Job::R'].isin(checks)]
    print(f'FIRI LENGTH CHECK = {len(subdf_lencheck)}, {comment}')

"""
###########
###########
###########
###########
## STEP 0.
 - A bit more of data cleaning:
 - In the past I've been working with a larger excel sheet. Now, I'll just locate the R's I'm interested in (secondaries, stds, blanks,
   and remove the rest.
 - There will be some inclusion of preamble from previous versions of this code
 - A lot of this workflow depends on data being in the groups listed above. So the first thing
   is to add a column that we can locate on, saying which group each R is in.
   ## our groups are: air_r = ['40430/1','40430/2', '40430/5];
                   inor_r = ['41347/2','41347/3'];
                   water_r = ['41347/12','41347/13'];
                   organic_r = ['24889/4','24889/5','24889/7','24889/9'];
                   rpo = ['24889/14']
"""
#
# # READ IN THE DATASETS THAT WE'LL BE USING HERE!
df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_1_V6_output\13_manual_drop.xlsx", sheet_name= 'Whole Dataframe')
print(f"Initial Read in: Is TP = 89255 present at this stage? {'Yes' if (df['TP'] == 89255).any() else 'No'}") # debugging a future script...why do future air materials come out differnt due to past data? 

df = df.dropna(subset='TP') # this gets rid of empty rows that were exported (i think) due to EA combustion run number
print(f"DropNA: Is TP = 89255 present at this stage? {'Yes' if (df['TP'] == 89255).any() else 'No'}")

df_rs = np.unique(df['Job::R'])
# check_firi_length(df, 'after import of 12_manual_plotly_Drop')

seconds = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\seconds_April3_2026.xlsx", sheet_name='new', comment='#')

"""
The bit of code below compares the R numbers in the exported file to that of the "secondaries" file which lists our target R numbers. 
The reason there turns out to be two additional R's in the exported file is beacuse when I search to export 14047/1 for instance, it 
includes things that begin like that, so it also grabs 14047/13, and similary 26281/10 is grabbed when I search for 26281/1. 
"""
# sec_rs = np.unique(seconds['Job::R'])


# # Convert to sets
# df_set = set(df_rs)
# sec_set = set(sec_rs)

# # Differences
# only_in_df = df_set - sec_set
# only_in_seconds = sec_set - df_set

# print("Only in df:")
# print(sorted(only_in_df))

# print("\nOnly in seconds:")
# print(sorted(only_in_seconds))

"""
End of check section above
"""

# CREATE A LIST OF R NUMBERS BASED ON THOSE IN SECONDARIES FILE, THESE ARE WHAT WE KEEP
rs_of_secondaries_and_blanks = np.unique(seconds['Job::R'])
# print(rs_of_secondaries_and_blanks)

# WE ONLY WANT TO KEEP/ANALYZE THOSE DATA IN R NUMBERS USED FOR SECONDARIES AND BLANKS!
# print(f"Full datset from _1 script has length {len(df)}")
df = df.loc[df['Job::R'].isin(rs_of_secondaries_and_blanks)]
# print(f"Subset only including data from secondaries and blanks R numbers has length {len(df)}. This differs slightly from original import. See explanation in script.")
df.to_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/secondaries_subset.xlsx")
print(f"Filtered for secondaries: Is TP = 89255 present at this stage? {'Yes' if (df['TP'] == 89255).any() else 'No'}")

"""
We have to be doubly sure that the blanks are indeed getting 45% error. 
In the end, we'll be calculating standard error, but for now, lets set the F_corrected_normed_error for blanks to 45%
"""
# df['err45'] = df['F_corrected_normed']*0.45
# blank_rs = ['40430/6','40142/2','40142/1','14047/1','14047/11']
# mask = df['Job::R'].isin(blank_rs)
# df.loc[mask, 'F_corrected_normed_error'] = df.loc[mask, 'err45']
# df['blank_error_check'] = df['F_corrected_normed_error']/df['F_corrected_normed'] # should be 0.45 for blanks...

"""
Code above was a mistake, the MCC should have 45% error/uncertainty on the MCC, not the measured blank value...
"""


# """
# Some more debugging toward the end of analysis: why is 41347/3 have way high chi2? 
# There were some wheels with hihg blanks and a previously small (in old small range). Lets remove these
# April 8, 2026
# It seems there is just way excess variability as post TP = 860000 for the carbonates. 
# 83620, 87986, and 88174 are all related to wheels where blanks were high, and one categorized as previuosly small. 
# 86089, 87469 87932 and 88133 are after a large sampling gap where variability suddely increases. 
# More detail: 
# 83620: an old small of 0.2 in 2022. 
# 87986: There was a problem with this wheel includnig low counts and bad calibration
# 88174: "Carbonate blank looks high, similar value to TW3507" 
# 87469 - 88133: Data after this period is just so highly variable...why? Doesn't represent long-term dataset of paper. Remove. 
# 86089 doesnt look great but there is no problem with it so we'll keep it in!

# See Inorganics Troubleshooting! Lots of investigatino and debugging
# In the end I think the water line blank is masking variability of LAA performance on water line 

# IN THE END WE SHOULDN"T REMOVE ANYTHING BECAUSE THERE IS NO GROUNDS TOO! WE CAN"T FIND ANY REASON!

# """

"""
here we can decide to add a size filter or not. 
By comparing these two datasets which include or excluide this line, we find it only affects some blanks, the rest are unaffected. 
Because large blanks are more representative of what we're after in this paper; we'll continue WITH the size filter for writing. 
You may have to re-write them by re-running the script with the line commented and not commented, potentially after more changes are made. 
"C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output\statistics_including_size_filter.xlsx"
"C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output\statistics_no_size_filter.xlsx"

May 25, 2026
Since we're now including data up to the present, this includes a lot of RCM 10 data. 
The RCM10 data is going to be removed in the size filter, and initial tests would be removed by the Hard Flag. 
I'll do a special script to discuss RCM10 tests later, where I'll filter on "graphite Line"
"""
# after I expanded the time of the work, from 2012 to 2024, we actually got LESS BHDamb2013. This is because many were 
# quality flagged in the meantime due to some tank pressure issues. However the chi2 got worse rather than better, so i'm testing keeping them in.
# df.loc[(df['Job::R'] == '40430/1') & (df['TW'] >= 3500) & (df['Quality Flag'] == 'A..'), 'Keep_Remove'] = 'Keep'


# print(f"Length before size filter is {len(df)}")
df = df.loc[df['wtgraph'] > 0.2]
print(f"Size filter: Is TP = 89255 present at this stage? {'Yes' if (df['TP'] == 89255).any() else 'No'}")
# print(f"Length after size filter is {len(df)}")
# check_firi_length(df, 'after size filter')

# print()
# print(f"Length before I say - remove those selected for removal in _1! is {len(df)}")
df.to_excel("C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/data_checks_along_the_way/pre_keepremove.xlsx")
df = df.loc[df['Keep_Remove'] == 'Keep']
print(f"Keep Remove: Is TP = 89255 present at this stage? {'Yes' if (df['TP'] == 89255).any() else 'No'}")
# check_firi_length(df, 'after keep remove')
# print(f"Length after I say - remove those selected for removal in _1! is {len(df)}")


"""
Text from Data Quality Paper 2 2025:
I need to parse between the different types of FIRI pretreatments from albert's TABLES.xlsx and see if I can find the same difference
after getting rid of flagged data.
FIRI-D is cellulose pretreated.
FIRI-E is AAA
FIRI-I is AAA
TIRL-L only has 2 measurements in RLIMS so lets forget about this.
I'm going to EDIT the R numbers for those names which may have EA and ST to look at these differences. This will be shown below. "EA Combustion::Run Numner"
After spending a bunch of July 4, 2024 on this: I just have to manually go through and check the pre-treatments for all FIRIs that were in Alberts sheet

New notes:
Contrasting to above, we'll be changing things from here, see more notes as we go below.
The first change to the block below which will happen on excel, is that FIRI-F's will be manually added to the FIRI_edited excel sheet
FIRI_F'schanged to FIRI'D's later

/////

THE CHUNK THAT WAS BELOW HAS BEEN MOVED TO A CLEANER INITIAL FILE IN THE 0.PY SECTION!
"""

# """
# Last bit of STEP 0: we need to associate each R number with its final group
# """

df = df.merge(seconds[['Job::R', 'Collection Date', 'Group','Merge Comment','Reference for Collection Date','Expected FM']], on='Job::R', how='left')
print(f"First Merge: Is TP = 89255 present at this stage? {'Yes' if (df['TP'] == 89255).any() else 'No'}")
# print()
# print(f"Lets make sure we haven't lost any data after mergeing with seconds: Length after merge: {len(df)}")
# print()

df.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/data_checks_along_the_way/mergecheck2.xlsx') # output to recheck

# Quick housekeeping/troubleshooting check before any math is done
# Try converting to numeric and see if anything fails
pd.to_numeric(df['RTS_corrected_error'], errors='raise')
pd.to_numeric(df['RTS_corrected'], errors='raise')
pd.to_numeric(df['Collection Date'], errors='raise')

# TODO see lines below
# # # trying to remove 1 to understand why carbonates secondaries went bad...
# df = df.loc[df['TW']!= 3397] # a big clump of data with some data holes exist for this wheel on LAC CARB, is this the problem?



# """
#         .      .      .      .      .      .
#    .       🚀        .      .       🌍      .
#         .      .   ⭐    .      .       .

# ======= ENTERING NEXT ANALYSIS PHASE ==========

#    .      .      .      .      .      .
#         🌑     .      .      .     🛰️
#    .      .      .      .      .      .
# """

# """
# ## STEP 1.1: CALCULATE CHI2 FOR EACH GROUP (chi2 requires RTS, weighted mean (from each R NUMBER, and RTS_err)
#  - calculate weighted mean in RTS space using eqn from _2 FOR EACH R NUMBER. Use groupby for cleanliness
#  - now calculate chi2 reduced

# ## STEP 1.2: CALCULATE SIGMA_BW FOR GROUPS
#  - assign collection date for each group using the secondaries.xlsx file and take careful notes about
#    how we're lucky all secondaries have the same collection date...otherwise this would be more
#    complicated (sigma_bw is grouped from different R's, so if different R's had different collection dates,
#    it would be difficult to convert sigma_bw to per mil based on those collection dates

#  - calculate sigma_bw using RTS and chi2 from above.
#  - output n, chi2 reduced, and sigma_bw to an excel file.
# """

# CHAT GPT AIDED BIT OF CODE TO CALCULATE WMEAN
# Calculate Weighted mean. One for each R number
# we can also calculate residuals here. One for every ROW!
df['wmean'] = df.groupby('Job::R')['RTS_corrected'].transform(lambda x: weighted_mean(df.loc[x.index, 'RTS_corrected'], df.loc[x.index, 'RTS_corrected_error']))
df['residual'] = residual(df['RTS_corrected'],df['wmean'],df['RTS_corrected_error'])

# this is a good time to output data that will be used to plot the air data
# we want to see the before and after flask oxalic normalization, so the data needs to be before filtering for flasks, 
# and before the between wheel error is incorporated
df.to_excel(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/for_air_plot.xlsx")
print(f"For air plot: Is TP = 89255 present at this stage? {'Yes' if (df['TP'] == 89255).any() else 'No'}")

# print()
# print(f"Length after wmean - groupby: {len(df)}")
# print()
df.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/data_checks_along_the_way/step1_groupbycheck.xlsx') # output to recheck

# NOW CALCULATE CHI2 REDUCED
# HAD TROUBLE HERE SO DOING IT MANUALLY TO TROUBLESHOOT
# Set list of R numbers for each group, then create new dataframes for each group
air_r = ['40430/1','40430/2','40430/5']
inor_r = ['41347/2','41347/3']
water_r = ['41347/12','41347/13']
organic_r = ['24889/4','24889/5','24889/7','24889/9']
rpo_r = ['24889/14']
bone_r = ['26281/1']

air_materials = df.loc[(df['Job::R'].isin(air_r)) & (df['AMS Timetable From Results::Standard Prep Type'] == 'FLASK')].copy()
air_materials.to_excel(rf'I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\script_testing/air_materials_dataqualitypaper.xlsx')
print()
print(f"AirMaterialsforCV (DATAFRAME): Is TP = 89255 present at this stage? {'Yes' if (df['TP'] == 89255).any() else 'No'}")
print(f"AirMaterialsforCV (AIR MATERIAL subdf): Is TP = 89255 present at this stage? {'Yes' if (air_materials['TP'] == 89255).any() else 'No'}")
print()

inorganic_materials = df.loc[(df['Job::R'].isin(inor_r))].copy()
water_materials = df.loc[(df['Job::R'].isin(water_r))].copy()
organic_materials = df.loc[(df['Job::R'].isin(organic_r))].copy()
rpo_materials = df.loc[(df['Job::R'].isin(rpo_r))].copy()
bone_materials = df.loc[(df['Job::R'].isin(bone_r))].copy()

datasets = [air_materials, inorganic_materials, water_materials, organic_materials, rpo_materials, bone_materials]
names = ['Air', 'Inorganic', 'Water', 'Organic','RPO', 'Bone']
k = [3,2,2,4,1,1]

# SET SOME ARRAYS TO FILL WITH DATA!
length = []
desc_arr = []
chi2_red_arr = []
sigbw_arr = []
sigbw_percent_arr = []
sig_bw_pm_arr = []

for i in range(0, len(datasets)):

    df2 = datasets[i]  # access first subset

    length.append(len(df2))  # append length of data
    desc_arr.append(names[i]) # append description of data
    k_i = k[i] # edit denominator of chi2 to be n-k, where k is the number of materials. 

    """
    Calculate chi2 reduced
    """
    chi2_red_num = np.sum((df2['RTS_corrected']-df2['wmean'])**2/df2['RTS_corrected_error']**2)
    chi2_red_denom = len(df2)-k_i # subtract number of groups in degrees of freedom calc.
    chi2_red = chi2_red_num/chi2_red_denom
    # print(chi2_red)
    chi2_red_arr.append(chi2_red)

    """
    calculate sigma_bw striaght up (This is the turnbull 2015 method) (if this doesn't work, its beacuse the sqrt function went negative because chi2 was less than 1)
    See Eqn at bottom of page 1 of scan file:///I:/C14Data/Data%20Quality%20Paper/CBL_V3/Data_Quality_Eqns_CBL_JCT.pdf
    """
    if chi2_red < 1:
        # according to the eqn, if chi2 is less than 1, you'd be taking sqrt of negative number which doesn't work. So if less than 1, set to 0.
        sigbw = 0
        # print('I found a zero!')

    else:
        term2 = np.sqrt(chi2_red - 1)
        # term1 = np.nanmean(df2['RTS_corrected_error'])/(df2['wmean'].iloc[0]); this is wrong, see notes right below!
        # There has been some confusion lately about the term above (in my own head)
        # here is where we are normalizing by RTS (in the manuscript this lands as Eqn 5.)
        # In earlier version, I had this listed as term1 = np.nanmean(df2['RTS_corrected_error'])/np.nanmean(df2['RTS_corrected']) 
        # Then, I thought it was wrong/thoght I caught a bug when I was updating the eqns in the manuscript. Why are we using the nanmean instead of the weighted mean???
        # So then, I switched to weighted mean (the RTSb bar)
        # BUT now I believe these are both wrong...
        # For a given df2 in the loop, there are a few values each with different set values (for instance for airs, there is BHDamb, BHDspike, BHDspike2025)
        # In reality, the first one was almost right but there shouldn't be the nanmean before the RTS_corrected. It shouid be nanmean of (RTS_err/RTS)
        term1 = np.nanmean(df2['RTS_corrected_error']/df2['RTS_corrected']) 

        sigbw = term1*term2

    sigbw_arr.append(sigbw) 

    sigbw_percent_arr.append(sigbw*100) # convert to percent, which is used in RLIMS, which we can use later for FM calc so its consistent with RLIMS

    colldate1 = df2['Collection Date'].iloc[0]
    sig_bw_pm_arr.append(rts_to_permille_for_errors(sigbw, colldate1))

    """
    Draw a nice plot with residuals and FM's (we're not using D14C because the collection dates for FIRI are too difficult to pin down)...
    """

    # Residuals on the bottom
    rs_here = np.unique(df2['Job::R'])
    markers = ['o','D','X','s']
    colors = ['blue','green','red','black']

    for j in range(0,len(rs_here)):
        this_r = df2.loc[(df2['Job::R'] == rs_here[j])]

        plt.scatter(this_r['TP'], this_r['residual'], color=colors[j], linestyle='', marker=markers[j], label=f'{rs_here[j]}')
        plt.axhline(y=0, color='black')
    plt.legend()

    plt.tight_layout()
    plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/mpl_output/{i}.png",
                dpi=300, bbox_inches="tight")
    plt.close()

output_grouped = pd.DataFrame({
    'Group': desc_arr,
    'Data Length (n)': length,
    'Chi2 Reduced': chi2_red_arr,
    'sigmabw_rts': sigbw_arr,
    'sigmabw_rts_percent': sigbw_percent_arr,
    'sigmabw_pm': sig_bw_pm_arr,
})


# """
#         .      .      .      .      .      .
#    .       🚀        .      .       🌍      .
#         .      .   ⭐    .      .       .

# ======= ENTERING NEXT ANALYSIS PHASE ==========

#    .      .      .      .      .      .
#         🌑     .      .      .     🛰️
#    .      .      .      .      .      .
# """

# """
#  # STEP 2: CALCULATE SUMMARY STATISTICS AND MAKE PLOTS FOR ALL SECONDARY STANDARDS AND BLANKS
#  # STEP 2.1 HOUSEKEEPING
#  - At the end of this step, we want sigma_ams (easy), chi2_reduced, FM, and D14C for each secondary standard and blank
#  - In order to set ourselves up for success, we need to associate a few extra bits of information with each R number
#  - - Associate the sigma_bw that we calculated above based on group (use .loc function that we do in _1 script)
#  - - Associate collection dates based on groups (again we're lucky its the same for every group type)

#  # STEP 2.2: INDEX BASED ON PRETREATMENTS
#  - - Then, we've been asked to index/seperate a lot of the organics based on pre-treatment. This will be a chunk of messy code

#  # STEP 2.3: CALCULATE SUMMARY STATS
#  - - Then we can run our loop from _2 to calculate summary statistics and make plots
#  - - - Lets still use RTS for chi2 reduced, with the undestanding that chi2_red > 1 is dealt with with sigma_bw which is included in FM error (the following step)
#  - - - The plots are in FM, so we'll need to convert to FM (see _2 for that bit of code)

#  # STEP 2.4 OUTPUT DATA
#  - Simply calculate D14C after the loop has found wmean of FM. We don't need to calc D14C in the loop
#  - ouput data with n, chi2_red, FM, FM_err (using new sig_bw) and D14C

# """

# First thing to do is merge the sigma_BW (the wheel to wheel error essentially) onto the main dataframe.
# We can do this like above
# IMPORTANT! Air secondaries are calculated based on flask ONLY but wtw error is mapped on ALL! Flask only reindexed later for individual secondaries
df = df.merge(output_grouped[['sigmabw_rts','sigmabw_pm','sigmabw_rts_percent','Group']], on='Group', how='left')

# One important thing to note:
# At this point, the blanks and Travertine were not included in the grouped calculation of sigbw.
# We know the Travertine is bad, so we don't want it in there.
# Blanks are highly variable and don't repreesnt our secondaries
# However, now that we've calulated sigma_bw for each pretreatment, we can probably go ahread and add it onto these,
# - for calculations coming up. We'll need it for conversion to FM and D14C errors.
# - Why not just leave the travertine out completely? We want to be able to discuss data before and after travertine incorporation, show how it was variable

# grab values and map onto the travertines...
# NO WTW errors needed for blanks!
grab_inorganic = df.loc[df["Group"] == "Inorganic", ["sigmabw_rts", "sigmabw_pm","sigmabw_rts_percent"]].iloc[0]
df.loc[df["Job::R"] == "14047/2", ["sigmabw_rts", "sigmabw_pm","sigmabw_rts_percent"]] = grab_inorganic.values

grab_water = df.loc[df["Group"] == "Water", ["sigmabw_rts", "sigmabw_pm","sigmabw_rts_percent"]].iloc[0]
df.loc[df["Job::R"] == "14047/12", ["sigmabw_rts", "sigmabw_pm","sigmabw_rts_percent"]] = grab_water.values

# recalculate the total uncertainty for each individual row/measurement, based on its sigma_AMS and newly calculated sigma_bw.
df['F_corrected_normed_error_NEW, with sigbw_RTS_percent'] = (np.sqrt(df['RTS_corrected_error']**2 + (df['sigmabw_rts_percent']*0.01*df['RTS_corrected'])**2)/0.95)*0.98780499

# use newly appended sigma_bw to calculate new FM errors for later residual plot
# some groups have sigmabw as 0 becuse chi2 were >1, see output from module above. Others have 0 beacuse they don't have WTW error applied. These include blanks, and things in "tuning" or "removed" categories
df["sigmabw_rts"] = df["sigmabw_rts"].fillna(0) # dupliactes line later but I left that later one cuz it was added first and don't want to break the code

# HOW DIFFERENT IS FM_err WITH NEW SIGMA_BW versus PREVIOUS WTW ERROR?
df['FM_err_new_sigbw'] = (np.sqrt(df['RTS_corrected_error']**2 + (df['sigmabw_rts_percent']*.01*df['RTS_corrected'])**2)/0.95)*0.98780499
df['diff_err'] = df['F_corrected_normed_error'] - df['FM_err_new_sigbw'] # calculate the percent change with the new FM_err_new_sigmba.
df['diff_err_percent'] = ((df['F_corrected_normed_error'] - df['FM_err_new_sigbw'])/df['F_corrected_normed_error'])*100 # calculate the percent change with the new FM_err_new_sigmba.

df.to_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/data_checks_along_the_way/sigbw_merge_calc_check.xlsx")


# print()
# print(f"Lets make sure we haven't lost any data: Length after mergeing big gruop sigma_bws: {len(df)}")
# print()

# print(df.columns)
dfprint = df[['Job::R','Group', 'F_corrected_normed', 'F_corrected_normed_error', 'DELTA14C',
              'DELTA14C_Error', 'Reference for Collection Date', 'Expected FM', 'wmean', 'residual', 'sigmabw_rts', 'sigmabw_pm']]

dfprint.to_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/data_checks_along_the_way/sigma_bw_merged_to_df.xlsx")
# having some problems with downstream calculations probably related to this mapping above


"""
 # STEP 2.2: INDEX BASED ON PRETREATMENTS
 - - Then, we've been asked to index/seperate a lot of the organics based on pre-treatment. This will be a chunk of messy code

# I'm taking this from Data_Quality_Paper_2_2026_v1.py
"""

kapuni = df.loc[(df['Job::R'] == '40699/1')].copy()

airdeadCO2 = df.loc[(df['Job::R'] == '40430/3')].copy()
bhdamb_flask = df.loc[(df['Job::R'] == '40430/1') & (df['AMS Timetable From Results::Standard Prep Type'] == 'FLASK')].copy()
bhdspike_flask = df.loc[(df['Job::R'] == '40430/2') & (df['AMS Timetable From Results::Standard Prep Type'] == 'FLASK')].copy()
bhdspike_flask2025 = df.loc[(df['Job::R'] == '40430/5') & (df['AMS Timetable From Results::Standard Prep Type'] == 'FLASK')].copy()
# for simplicity, lets just remove non-OX-flask prepared Airs frmo the databased because its confusing to find them later!
df = df.drop(df[(df['Job::R'] == '40430/1') & (df['AMS Timetable From Results::Standard Prep Type'] != 'FLASK')].index)
df = df.drop(df[(df['Job::R'] == '40430/2') & (df['AMS Timetable From Results::Standard Prep Type'] != 'FLASK')].index)

carr_marb_carb = df.loc[(df['Job::R'] == '14047/1')].copy()
travertine_carb = df.loc[(df['Job::R'] == '14047/2')].copy()
lac1carb = df.loc[(df['Job::R'] == '41347/2')].copy()
laa1carb = df.loc[(df['Job::R'] == '41347/3')].copy()

# what about that wheel with 4 in the same wheel? What's going on there?

firi_l = df.loc[(df['Job::R'] == '26281/1')].copy()

carr_marb_water = df.loc[(df['Job::R'] == '14047/11')].copy()
travertine_water = df.loc[(df['Job::R'] == '14047/12')].copy()
lac1water = df.loc[(df['Job::R'] == '41347/12')].copy()
laa1water = df.loc[(df['Job::R'] == '41347/13')].copy()

# now i have a better way of assigning the AAA, Cellulose, ST, and EA...
df['EA_ST'] = ''
df['AAA_CELL'] = ''
df.loc[(df['EA Combustion::Run Number'].notna()), 'EA_ST'] = 'EA' #wherever you find an EA run number, it means it was EA.
df.loc[(df['EA Combustion::Run Number'].isna()), 'EA_ST'] = 'ST' #wherever you don't, it was sealed tube
df.loc[(df['Cellulose Extraction Completed::Start Operator'].notna()), 'AAA_CELL'] = 'CELL' #use operator process start as proxy
df.loc[(df['AAA Processes::End Operator'].notna()), 'AAA_CELL'] = 'AAA' #use operator process start as proxy
df.loc[((df['AAA Processes::End Operator'].notna()) & (df['Cellulose Extraction Completed::Start Operator'].notna())), 'AAA_CELL'] = 'BOTH' 

# this should be probably be elsewhere...
df.loc[(df['Should a new flag be added? '] == 'X..'), 'Keep_Remove'] = 'Remove'

kauri_all = df.loc[((df['Job::R'] == '40142/1') | (df['Job::R'] == '40142/2'))].copy()
kauri_aaa = df.loc[(df['Job::R'] == '40142/2')].copy()
kauri_cell = df.loc[(df['Job::R'] == '40142/1')].copy().reset_index()


kauri_aaa_ea = df.loc[((df['Job::R'] == '40142/2') & (df['EA_ST'] =='EA'))].copy()
kauri_aaa_st = df.loc[((df['Job::R'] == '40142/2') & (df['EA_ST']== 'ST'))].copy()
kauri_cell_ea = df.loc[((df['Job::R'] == '40142/1') & (df['EA_ST'] =='EA'))].copy()
kauri_cell_st = df.loc[((df['Job::R'] == '40142/1') & (df['EA_ST'] == 'ST'))].copy()

# we're setting the FIRI-F R numbers to go into the FIRI D category too....
# will be simplest to first set all FIRI-F's to FIRI D...the line below accomplishes that
df.loc[(df['Job::R'] == '24889/6'),'Job::R'] = '24889/4'

firi_d_all = df.loc[(df['Job::R'] == '24889/4')].copy()
firi_d_aaa_ea = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA')].copy()
firi_d_aaa_st = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] == 'ST')].copy()
firi_d_cell_ea = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='CELL') & (df['EA_ST'] =='EA')].copy()
firi_d_cell_st = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='CELL') & (df['EA_ST'] == 'ST')].copy()
firi_d_cell = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='CELL')].copy()
firi_d_aaa = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA')].copy()

firi_d_rpo = df.loc[(df['Job::R'] == '24889/14')].copy()

# FIRI E HAS NO PRETREATMENT!!! JUST GRAPHITE
firi_e = df.loc[(df['Job::R'] == '24889/5')].copy()

firi_g_all = df.loc[(df['Job::R'] == '24889/7')].copy()
firi_g_aaa_ea = df.loc[(df['Job::R'] == '24889/7') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA')].copy()
firi_g_aaa_st = df.loc[(df['Job::R'] == '24889/7') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] == 'ST')].copy()


# JOCELYN SAID THAT WE SHOULD REMOVE ANY FIRI-I THAT HAVE PRETREATMENT. HOWEVER, THEY ALL ARE EITHER CELLULOSE OR AAA. SHE SPECIFICALLY SAID TO GET RID OF AAA, SO WE"LL JST KEEP CELLULOSE
# firi_i_aaa_ea = df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA')].copy()
# firi_i_cell_ea = df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA')].copy()
# firi_i_aaa = df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='AAA')].copy()
firi_i_nopretreat = df.loc[((df['Job::R'] == '24889/9')) & (df['AAA_CELL'] =='')].copy()

datasets = [kapuni,
            airdeadCO2, bhdamb_flask, bhdspike_flask, bhdspike_flask2025, 
            carr_marb_carb, travertine_carb, lac1carb, laa1carb,
            carr_marb_water, travertine_water, lac1water, laa1water,
            firi_l,
            kauri_all,
            kauri_aaa, kauri_cell,
            kauri_aaa_ea, kauri_aaa_st,
            kauri_cell_ea, kauri_cell_st,
            firi_d_all, firi_d_aaa_ea, firi_d_aaa_st, firi_d_cell_ea, firi_d_cell_st, firi_d_cell, firi_d_aaa,
            firi_d_rpo,
            firi_e,
            firi_g_all, firi_g_aaa_ea, firi_g_aaa_st,
            firi_i_nopretreat]


names = ['KAPUNI',
         'AIRDEADCO2','BHDAMB_FLASK','BHDSPIKE_FLASK', 'BHDSPIKE_FLASK2025',
         'CARR_MARB_CARB','TRAV_CARB','LAC1_CARB','LAA1_CARB',
         'CARR_MARB_WATER','TRAV_WATER','LAC1_WATER','LAA1_WATER',
         'FIRI_L',
         'KAURI_ALL',
         'KAURI_AAA','KAURI_CELL',
         'KAURI_AAA_EA','KAURI_AAA_ST',
         'KAURI_CELL_EA','KAURI_CELL_ST',
         'FIRI_D_ALL', 'FIRI_D_AAA_EA','FIRI_D_AAA_ST','FIRI_D_CELL_EA','FIRI_D_CELL_ST', 'FIRI_D_CELL','FIRI_D_AAA',
         'FIRI_D_RPO',
         'FIRI_E',
         'FIRI_G_ALL','FIRI_G_AAA_EA','FIRI_G_AAA_ST',
         'FIRI_I_nopretreatment']

"""
lets loop through the R numbers and get means and stats assigned to each value in the database...
The loop will compare R numbers from the 'seconds.xlsx' with the R numbers from the dataframe
"""

# set output for plotly file later
outdir = r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/plotly_check"

# set inital value for wmean so i can calc residual later
df['wmean_subsets'] = -999

# dataset descriptors
group_name = []
R_num = []
desc_arr = []
length = []

# calculated statistics
wmean_arr = []

# summary statistics for each individual group
chi2_red_arr = []  # will contain: individual material chi2 result
fm_arr = []        # will contain: weighted mean from RTS converted to FM; ### F_corrected_normed = (wmean/0.95)*0.98780499
stderr_arr = []    # will contain: standard error of the FM' standard_err = np.std(subset1['F_corrected_normed'], ddof=1) / np.sqrt(len(subset1['F_corrected_normed']))
stdev_arr=[]       # will contain: standard deviation; np.std(subset1['F_corrected_normed'])
coll_date_arr = [] # will contain: collection date, transferred from manually filled in sheet with secondary standards information
d14C_arr = []      # will contain: converted d14C
d14C_err_arr = []  # will contain: conveted d14C error

# stuff based on the pooled statistics
CV_r_arr = []          # sigma_bw from above
CV_percent_arr = []
CV_permil_arr = []
sigma_r_arr = []       # sigma_r corresponds to eqn 7 on the manuscript; the CVr (previously called sigma_bw) multiplied by the weighted mean
sigma_r_permil_arr = []

total_unc_min_arr = [] # these two will hold the data which answers: what is our repeatability that we can expect on an individual measuremnet? For that, we apply the total uncertaity calculatino using new sigma_bw
                   #    for all rows, and look at the max and min, which we'll report in the table. 
total_unc_max_arr = []
total_unc_min_permil_arr = []
total_unc_max_permil_arr = []
av_prec_arr = []

for i in range(0, len(datasets)):

    # Create figure and 2 vertical subplots
    fig, axs = plt.subplots(2, 1, figsize=(6, 8), sharex=True)  # 3 rows, 1 column

    # holdover from previous version
    df2 = datasets[i]

    # print(f'Length of df {names[i]} is {len(df2)}')
    title_i = df2['Job::R'].iloc[0]
    R_num.append(df2['Job::R'].iloc[0]) # append R number, description, group name
    desc_arr.append(names[i])
    group_name.append(df2['Group'].iloc[0])
    length.append(len(df2))
    colldate1 = df2['Collection Date'].iloc[0]

    # map the max and min expected uncerainties for indiviudual measurements onto the final table. 
    total_unc_min = np.min(df2['F_corrected_normed_error_NEW, with sigbw_RTS_percent'])
    total_unc_max = np.max(df2['F_corrected_normed_error_NEW, with sigbw_RTS_percent'])
    # append to the arrays
    total_unc_min_arr.append(total_unc_min)
    total_unc_max_arr.append(total_unc_max)

    # what is the average precision? 
    avprec = np.nanmean(df2['F_corrected_normed_error_NEW, with sigbw_RTS_percent'])

    total_unc_min_per_mil = rts_to_permille_for_errors(total_unc_min, colldate1)
    total_unc_max_per_mil = rts_to_permille_for_errors(total_unc_max, colldate1)
    avprec_per_mil = rts_to_permille_for_errors(avprec, colldate1)

    total_unc_min_permil_arr.append(total_unc_min_per_mil)
    total_unc_max_permil_arr.append(total_unc_max_per_mil)
    av_prec_arr.append(avprec_per_mil)

    CV_r = df2['sigmabw_rts'].iloc[0]
    CV_r_arr.append(CV_r)

    CV_percent = df2['sigmabw_rts_percent'].iloc[0]
    CV_percent_arr.append(CV_percent)

    CV_permil = df2['sigmabw_pm'].iloc[0]
    CV_permil_arr.append(CV_permil)

    """
    The weighted mean comes from Albert's original version of the paper. I've copied his formula here which comes from
    #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    We need to recalculate wmean since we're dealing with subsets now, especially for the many permutations or organic pretreatment subsets
    """
    # renaming as holdover from previous version
    subset1 = df2

    wmean_num = np.sum(subset1['RTS_corrected']/subset1['RTS_corrected_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    wmean_dem = np.sum(1/subset1['RTS_corrected_error']**2)
    wmean = wmean_num / wmean_dem
    wmean_arr.append(wmean)
    # print(f'{names[i]}, {wmean}')

    sigma_r = wmean*CV_r
    sigma_r_arr.append(sigma_r)

    sigma_r_permil_arr.append(rts_to_permille_for_errors(sigma_r, colldate1))

    """
    Calculate residual: again, while we've already done this in previous section, we're re-doing it relative to wmean of subset for pretreatment permutations
    """
    subset1['residual'] = ( subset1['RTS_corrected'] - wmean ) / subset1['RTS_corrected_error']

    """
    Calculate chi2 reduced for subset
    """
    # calc chi2
    chi2_red_num = np.sum((subset1['RTS_corrected']-wmean)**2/subset1['RTS_corrected_error']**2)
    chi2_red_denom = len(subset1)-1 # subtract number of groups in degrees of freedom calc.
    chi2_red = chi2_red_num/chi2_red_denom
    chi2_red_arr.append(chi2_red)

    """
    Conversion to Fraction modern
    RLIMS EQN: If(IsEmpty(rts_stds_av) = False; (RTS_corrected / (Standard Specific Activity Constant * rts_stds_av)) *( ((1 + delta13C_stds_av/ 1000) / (1 + delta13C_In_Calculation / 1000)) ^Normalization_exp_factor )* Standard 13C Value Constant;"")
    # The last term is the 13C value constant, a go-between for conventions - its so confusing
    """

    term1 = np.nanmean(subset1['RTS_corrected_error']) # why is it written like this? Legacy. From Data Qualiyt Paper_2 2026 v1.py

    subset1["sigmabw_rts_percent"] = subset1["sigmabw_rts_percent"].fillna(0) # This line is important. For blanks, and Kapuni (tuning), no WTW error is applied. But if there is no data there, the rest of the calcualtions won't run. So we just need to set it to 0.
    sigbw_rts_percent = (subset1['sigmabw_rts_percent'].iloc[0])

    F_corrected_normed = (wmean/0.95)*0.98780499 #wmean converted to FM
    fm_arr.append(F_corrected_normed)

    F_corrected_normed_error = (np.sqrt(term1**2 + (sigbw_rts_percent*0.01*wmean)**2)/0.95)*0.98780499
    
    """
    May 20, 2025, making an edit to the FM corrected values. 
    In the past I've calculated it as: 
    F_corrected_normed_error = (np.sqrt(term1**2 + (sigbw_rts_percent*0.01*wmean)**2)/0.95)*0.98780499
    This figuration incorporates the sigbw_rts_percent that we've worked so hard to calculate. 
    But actually JCT thinks we should be reporting the standard error.
    Perhaps I've been thinking about it slightly wrong; 
    I've been wanting to use sigma_bw in the final calculation of our uncertainty. However, 
    it's perhaps better thought of as a marker of how much uncertainty needs to be added to each 
    measurement in real life (as they're coming off of XCAMS); and the calculation as I've had it before
    isn't the best for summarized long-term data sets. 
    I've kept the original commented out below, and added in the numpy standard error calculation here: 
    standard error of the mean:sem = np.std(data, ddof=1) / np.sqrt(len(data))
    """


    stddev = np.std(subset1['F_corrected_normed'])
    stdev_arr.append(stddev)
    # we deicded to use STANDARD ERROR, but were keeping this in the output for now...

    standard_err = np.std(subset1['F_corrected_normed'], ddof=1) / np.sqrt(len(subset1['F_corrected_normed']))
    # F_corrected_normed_error = (np.sqrt(term1**2 + (sigbw_rts_percent*0.01*wmean)**2)/0.95)*0.98780499 

    stderr_arr.append(standard_err)
    

    """
    Conversion to D14C
    """
    colldate1 = subset1['Collection Date'].iloc[0]
    coll_date_arr.append(colldate1)
    delta_14C =  1000*(F_corrected_normed*np.exp((1950-colldate1)/8267)-1)
    delta_14C_err = 1000*(standard_err*np.exp((1950-colldate1)/8267))
    d14C_arr.append(delta_14C)
    d14C_err_arr.append(delta_14C_err)

    """
    Draw a nice plot with residuals and FM's (we're not using D14C because the collection dates for FIRI are too difficult to pin down)...
    """

    # Residuals on the bottom
    axs[1].scatter(subset1['TP'], subset1['residual'], color='black', linestyle='')
    axs[1].axhline(y=0, color='black')

    # Second subplot
    subset1['F_corrected_normed'] = pd.to_numeric(subset1['F_corrected_normed'], errors="coerce")
    subset1['F_corrected_normed_error'] = pd.to_numeric(subset1['F_corrected_normed_error'], errors="coerce")
    subset1['TP'] = pd.to_numeric(subset1['TP'], errors="coerce")
    axs[0].axhline(y=F_corrected_normed, color='black') # see above, I convert wmean to FM space
    concval = subset1['Expected FM'].iloc[0]
    axs[0].axhline(y=concval, color='red', alpha=0.5)

    axs[0].errorbar(subset1['TP'], subset1['F_corrected_normed'], yerr=subset1['F_corrected_normed_error'], color='black', linestyle='', label = f'{names[i]}', marker='o')
    axs[0].legend()
    axs[1].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
    axs[0].set_ylabel('Fraction Modern')

    stats_text = (
        f"$n$ = {len(df2)}\n"
        f"$\\chi^2 red$ = {chi2_red:.2f}\n"
        f"wmean = {F_corrected_normed:.4f}"
    )

    axs[0].text(
        0.05, 0.95,                # position (relative axes coords)
        stats_text,
        transform=axs[0].transAxes,
        fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
    )
    axs[0].set_title(title_i)
    plt.tight_layout()


    plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output\mpl_output/{i}.png", dpi=300, bbox_inches="tight")
    plt.close()

    """
    Some quick plotly to faster identify outliers to remove
    """

#     import plotly.graph_objects as go

#     fig_plotly = go.Figure()

#     fig_plotly.add_trace(go.Scatter(x=subset1['TP'],y=subset1['residual'],mode='markers', marker=dict(size=8), text=subset1['TP'], hovertemplate=
#                 '<b>TP:</b> %{x}<br>' +
#                 '<b>Residual:</b> %{y:.2f}<br>' +
#                 '<extra></extra>')
#     )
#     # Zero line
#     fig_plotly.add_hline(
#         y=0,
#         line_color='black'
#     )
#     fig_plotly.update_layout(
#         title=title_i,
#         xaxis_title='TP',
#         yaxis_title='Residual',
#         height=500,
#         width=800
#     )
#     fig_plotly.show()


output_R_specific = pd.DataFrame({
                        'Group': group_name,
                        'Job::R': R_num,
                        'Description': desc_arr,
                        'n': length,

                        'wmean': wmean_arr,

                        'chi2red': chi2_red_arr,
                        'Fraction Modern': fm_arr,
                        'Standard Error':stderr_arr,
                        'Standard Deviation (dont for main unc!)': stdev_arr,
                        'Collection Date': coll_date_arr,
                        'D14C': d14C_arr,
                        'D14C_err': d14C_err_arr,

                        'CV_r': CV_r_arr,
                        'CV_r_percent': CV_percent_arr,
                        'CV_permil': CV_permil_arr,
                        'sigma_r': sigma_r_arr,
                        'sigma_r_permil': sigma_r_permil_arr,
                        'total_unc_min': total_unc_min_arr,
                        'total_unc_min_permil': total_unc_min_permil_arr,
                        'tot_unc_max': total_unc_max_arr,
                        'total_unc_max_permil': total_unc_max_permil_arr,
                        'Average precision for ind cathode': av_prec_arr,
                        })

# print(av_prec_arr)

# NOW RUN SOME T-TESTS BEFORE OUTPUTTING THE RESULTS!
results_lines = []

# EA versus ST shown via FIRI-D's
t1, p1 = stats.ttest_ind(firi_d_cell_ea['F_corrected_normed'], firi_d_cell_st['F_corrected_normed'])
results_lines.append(
    f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_D_CELL_EA and FIRI_D_CELL_ST. Results p > 0.05 shows there is no observable difference")

# EA versus ST shown via FIRI-G's
t1, p1 = stats.ttest_ind(firi_g_aaa_ea['F_corrected_normed'], firi_g_aaa_st['F_corrected_normed'])
results_lines.append(
    f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_G_CELL_EA and FIRI_G_CELL_ST. Results p  > 0.05 shows there is no observable difference")

results_lines.append('#The results above show that there is no observable difference between EA and ST for organic pretreatments. Since thats settled, we can recombined all and do t-tests with the AAA and Cell main groupings'
                     )

# CELL vs AAA using FIRI D
t1, p1 = stats.ttest_ind(firi_d_cell['F_corrected_normed'], firi_d_aaa['F_corrected_normed'])
results_lines.append(
    f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_D_CELL and FIRI_D_AAA.")

# # CELL vs AAA using FIRI I
# t1, p1 = stats.ttest_ind(firi_i_aaa['F_corrected_normed'], firi_i_cell['F_corrected_normed'])
# results_lines.append(
#     f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_I_CELL and FIRI_I_AAA. Results <0.05 shows there is no observable difference")

results_df = pd.DataFrame({"T-test Results": results_lines})

output_dir = (rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/Final_results_V6_edit4.xlsx")

df_columns_cleaned = df[[
      'RTS_corrected', 'RTS_corrected_error',
      'MCC',
      'F_corrected_normed', 'F_corrected_normed_error','F_corrected_normed_error_NEW, with sigbw_RTS_percent', 
      'DELTA14C',
      'DELTA14C_Error',
      'wtgraph',
      'TP', 'TW', 'Quality Flag',
      'Job::R', 'Samples::Sample Description',
      'EA_ST', 'AAA_CELL', 'Collection Date', 'Group', 'Merge Comment',
      'Reference for Collection Date', 'Expected FM', 'wmean', 'residual',
      'sigmabw_rts','sigmabw_pm','sigmabw_rts_percent','Group','Date Run']]

# Write to Excel
with pd.ExcelWriter(output_dir, engine="openpyxl", mode="w") as writer:
    df_columns_cleaned.to_excel(writer, sheet_name="Clean Dataset", index=False)
    output_grouped.to_excel(writer, sheet_name="Group Statistics", index=False)
    output_R_specific.to_excel(writer, sheet_name="Secondaries Statistics", index=False)
    results_df.to_excel(writer, sheet_name="T-test results", index=False)

print(f"For air plot: Is TP = 89255 present at this stage? {'Yes' if (df['TP'] == 89255).any() else 'No'}")