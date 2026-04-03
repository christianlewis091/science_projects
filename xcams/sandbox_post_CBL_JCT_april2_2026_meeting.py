"""
IMPORT STATEMENT
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

"""
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
   ## our groups are: air_r = ['40430/1','40430/2'];
                   inor_r = ['41347/2','41347/3'];
                   water_r = ['41347/12','41347/13'];
                   organic_r = ['24889/4','24889/5','24889/7','24889/9'];
                   rpo = ['24889/14']
"""
#
# # READ IN THE DATASETS THAT WE'LL BE USING HERE!
# df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/12_manual_plotly_drop.xlsx', sheet_name= 'Whole Dataframe')
seconds = pd.read_excel("C:/Users\clewis\IdeaProjects\GNS/xcams\seconds_April3_2026.xlsx", sheet_name='new', comment='#')
# # CREATE A LIST OF R NUMBERS BASED ON THOSE IN SECONDARIES FILE, THESE ARE WHAT WE KEEP
# rs_of_secondaries_and_blanks = np.unique(seconds['R_number'])
#
# # WE ONLY WANT TO KEEP/ANALYZE THOSE DATA IN R NUMBERS USED FOR SECONDARIES AND BLANKS!
# print(f"Full datset from _1 script has length {len(df)}")
# df = df.loc[df['Job::R'].isin(rs_of_secondaries_and_blanks)]
# print(f"Subset only including data from secondaries and blanks R numbers has length {len(df)}")
#
# df.to_excel("C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/secondaries_subset.xlsx")


# Now I'll read that back in to save time when writing/debugging:
df = pd.read_excel("C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/secondaries_subset.xlsx")
print()
print(f"Length before I say - remove those selected for removal in _1! is {len(df)}")
df = df.loc[df['Keep_Remove'] == 'Keep']
print(f"Length after I say - remove those selected for removal in _1! is {len(df)}")

# September 12, merge with STD prep type: We only want air secondaries run with Flask OX
spt = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/flask_ox_label.xlsx')
spt = spt.drop_duplicates(subset='TP', keep='first') # get rid of duplicates on the prep type output from RLIMS
df = df.merge(spt, on='TP')
df.to_excel('C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/ox_prep_labels_added.xlsx')
print()
print(f"Lets make sure we haven't lost any data: Length after adding air standard prep types: {len(df)}")
print()

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

"""
firilist = ['24889/4','24889/5','24889/9','26281/1','24889/7'] # here is the list of R numbers I want to check
firis = df.loc[(df['Job::R'].isin(firilist))]        # make a subset dataframe where these FIRIs are found
firis.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/firis.xlsx')  # write it to excel
firis = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/firis_edited.xlsx', comment='#') # I edited it by checking RLIMS. Read it back in
firis = firis[['TP','EA_ST','AAA_CELL']]  # drop columns to prep for merge
firis = firis.drop_duplicates(subset='TP', keep='first') # get rid of duplicates on the prep type output from RLIMS
df = df.merge(firis, on='TP', how='left')  # merge
df.to_excel(f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/mergecheck.xlsx') # output to recheck
print()
print(f"Lets make sure we haven't lost any data: Length after adding air FIRI pretreatment types: {len(df)}")
print()

"""
Last bit of STEP 0: we need to associate each R number with its final group
"""

df = df.merge(seconds[['Job::R', 'Collection Date', 'Group','Merge Comment','Reference for Collection Date']], on='Job::R', how='left')
print()
print(f"Lets make sure we haven't lost any data after mergeing with seconds: Length after merge: {len(df)}")
print()

df.to_excel(f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/mergecheck2.xlsx') # output to recheck

# Quick housekeeping/troubleshooting check before any math is done
# Try converting to numeric and see if anything fails
pd.to_numeric(df['RTS_corrected_error'], errors='raise')
pd.to_numeric(df['RTS_corrected'], errors='raise')
pd.to_numeric(df['Collection Date_y'], errors='raise')

"""
        .      .      .      .      .      .
   .       🚀        .      .       🌍      .
        .      .   ⭐    .      .       .

======= ENTERING NEXT ANALYSIS PHASE ==========

   .      .      .      .      .      .
        🌑     .      .      .     🛰️
   .      .      .      .      .      .
"""

"""
## STEP 1.1: CALCULATE CHI2 FOR EACH GROUP (chi2 requires RTS, weighted mean (from each R NUMBER, and RTS_err)
 - calculate weighted mean in RTS space using eqn from _2 FOR EACH R NUMBER. Use groupby for cleanliness
 - now calculate chi2 reduced

## STEP 1.2: CALCULATE SIGMA_BW FOR GROUPS
 - assign collection date for each group using the secondaries.xlsx file and take careful notes about
   how we're lucky all secondaries have the same collection date...otherwise this would be more
   complicated (sigma_bw is grouped from different R's, so if different R's had different collection dates,
   it would be difficult to convert sigma_bw to per mil based on those collection dates

 - calculate sigma_bw using RTS and chi2 from above.
 - output n, chi2 reduced, and sigma_bw to an excel file.
"""

# CHAT GPT AIDED BIT OF CODE TO CALCULATE WMEAN
# Calculate Weighted mean. One for each R number
# we can also calculate residuals here. One for every ROW!
df['wmean'] = df.groupby('Job::R')['RTS_corrected'].transform(lambda x: weighted_mean(df.loc[x.index, 'RTS_corrected'], df.loc[x.index, 'RTS_corrected_error']))
df['residual'] = residual(df['RTS_corrected'],df['wmean'],df['RTS_corrected_error'])

print()
print(f"Length after wmean - groupby: {len(df)}")
print()
df.to_excel(f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/step1_groupbycheck.xlsx') # output to recheck

# NOW CALCULATE CHI2 REDUCED
# HAD TROUBLE HERE SO DOING IT MANUALLY TO TROUBLESHOOT
# Set list of R numbers for each group, then create new dataframes for each group
air_r = ['40430/1','40430/2']
inor_r = ['41347/2','41347/3']
water_r = ['41347/12','41347/13']
organic_r = ['24889/4','24889/5','24889/7','24889/9']
rpo_r = ['24889/14']
bone_r = ['26281/1']

air_materials = df.loc[(df['Job::R'].isin(air_r)) & (df['preptype'] == 'FLASK')].copy()
inorganic_materials = df.loc[(df['Job::R'].isin(inor_r))].copy()
water_materials = df.loc[(df['Job::R'].isin(water_r))].copy()
organic_materials = df.loc[(df['Job::R'].isin(organic_r))].copy()
rpo_materials = df.loc[(df['Job::R'].isin(rpo_r))].copy()
bone_materials = df.loc[(df['Job::R'].isin(bone_r))].copy()

datasets = [air_materials, inorganic_materials, water_materials, organic_materials, rpo_materials, bone_materials]
names = ['Air', 'Inorganic', 'Water', 'Organic','RPO', 'Bone']

# SET SOME ARRAYS TO FILL WITH DATA!
length = []
desc_arr = []
chi2_red_arr = []
sigbw_arr = []
sig_bw_pm_arr = []

for i in range(0, len(datasets)):

    df2 = datasets[i]  # access first subset
    length.append(len(df2))  # append length of data
    desc_arr.append(names[i]) # append description of data

    """
    Calculate chi2 reduced
    """
    chi2_red_num = np.sum((df2['RTS_corrected']-df2['wmean'])**2/df2['RTS_corrected_error']**2)
    chi2_red_denom = len(df2)-1 # subtract number of groups in degrees of freedom calc.
    chi2_red = chi2_red_num/chi2_red_denom
    print(chi2_red)
    chi2_red_arr.append(chi2_red)

    """
    calculate sigma_bw striaght up (This is the turnbull 2015 method) (if this doesn't work, its beacuse the sqrt function went negative because chi2 was less than 1)
    See Eqn at bottom of page 1 of scan file:///I:/C14Data/Data%20Quality%20Paper/CBL_V3/Data_Quality_Eqns_CBL_JCT.pdf
    """
    if chi2_red < 1:
        sigbw = 0
        print('I found a zero!')

    else:
        term2 = np.sqrt(chi2_red - 1)
        # term1 = np.nanmean(df2['RTS_corrected_error'])
        term1 = np.nanmean(df2['RTS_corrected_error'])/np.nanmean(df2['RTS_corrected']) # TODO here I think is where we would put a normalization to FM/RTS
        sigbw = term1*term2
    sigbw_arr.append(sigbw)

    colldate1 = df2['Collection Date_y'].iloc[0]
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
    plt.savefig(f"C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/mpl_output/{i}.png",
                dpi=300, bbox_inches="tight")
    plt.close()

output1 = pd.DataFrame({
    'Group': desc_arr,
    'Data Length (n)': length,
    'Chi2 Reduced': chi2_red_arr,
    'sigmabw_rts': sigbw_arr,
    'sigmabw_pm': sig_bw_pm_arr,
})

output1.to_excel("C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/statistics_grouped.xlsx")

"""
        .      .      .      .      .      .
   .       🚀        .      .       🌍      .
        .      .   ⭐    .      .       .

======= ENTERING NEXT ANALYSIS PHASE ==========

   .      .      .      .      .      .
        🌑     .      .      .     🛰️
   .      .      .      .      .      .
"""

"""
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

"""

# First thing to do is merge the sigma_BW (the wheel to wheel error essentially) onto the main dataframe.
# We can do this
df = df.merge(output1[['sigmabw_rts','sigmabw_pm','Group']], on='Group', how='left')

print()
print(f"Lets make sure we haven't lost any data: Length after mergeing big gruop sigma_bws: {len(df)}")
print()














