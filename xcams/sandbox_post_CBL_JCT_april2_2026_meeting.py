"""
IMPORT STATEMENT
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

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

"""
here we can decide to add a size filter or not. 
By comparing these two datasets which include or excluide this line, we find it only affects some blanks, the rest are unaffected. 
Because large blanks are more representative of what we're after in this paper; we'll continue WITH the size filter for writing. 
You may have to re-write them by re-running the script with the line commented and not commented, potentially after more changes are made. 
"C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output\statistics_including_size_filter.xlsx"
"C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output\statistics_no_size_filter.xlsx"
"""
df = df.loc[df['wtgraph'] > 0.2]

print()
print(f"Length before I say - remove those selected for removal in _1! is {len(df)}")
df = df.loc[df['Keep_Remove'] == 'Keep']
print(f"Length after I say - remove those selected for removal in _1! is {len(df)}")

# September 12, merge with STD prep type: We only want air secondaries run with Flask OX
spt = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/flask_ox_label.xlsx')
spt = spt.drop_duplicates(subset='TP', keep='first') # get rid of duplicates on the prep type output from RLIMS
df = df.merge(spt, on='TP')
df.to_excel('C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/data_checks_along_the_way/ox_prep_labels_added.xlsx')
# experiencing some confusion based on the flask stuff.
# I've filtered for flasks only below but I'm still getting data for pre-TW3010 when flasks were introduced. The reason this is confusion is beacuse, while I'm taking flask-only data for the statistical group calculations,
# The EA and ST ones are still left in the database presented at the end. This can be confusinng for someone who looks in there and sees ST or EA.

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
FIRI_F'schanged to FIRI'D's later
"""
firilist = ['24889/4','24889/5','24889/9','26281/1','24889/7'] # here is the list of R numbers I want to check
firis = df.loc[(df['Job::R'].isin(firilist))]        # make a subset dataframe where these FIRIs are found
firis.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/firis.xlsx')  # write it to excel
firis = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/firis_edited.xlsx', comment='#') # I edited it by checking RLIMS. Read it back in
# change firi F's to FIRI-D's (it was a blind copy, now we can just change


firis = firis[['TP','EA_ST','AAA_CELL']]  # drop columns to prep for merge
firis = firis.drop_duplicates(subset='TP', keep='first') # get rid of duplicates on the prep type output from RLIMS
df = df.merge(firis, on='TP', how='left')  # merge
df.to_excel(f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/data_checks_along_the_way/mergecheck.xlsx') # output to recheck
print()
print(f"Lets make sure we haven't lost any data: Length after adding air FIRI pretreatment types: {len(df)}")
print()

"""
Last bit of STEP 0: we need to associate each R number with its final group
"""

df = df.merge(seconds[['Job::R', 'Collection Date', 'Group','Merge Comment','Reference for Collection Date','Expected FM']], on='Job::R', how='left')
print()
print(f"Lets make sure we haven't lost any data after mergeing with seconds: Length after merge: {len(df)}")
print()

df.to_excel(f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/data_checks_along_the_way/mergecheck2.xlsx') # output to recheck

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
df.to_excel(f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/data_checks_along_the_way/step1_groupbycheck.xlsx') # output to recheck

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
        # according to the eqn, if chi2 is less than 1,, you'd be taking sqrt of negative number which doesn't work. So if less than 1, set to 0.
        sigbw = 0
        print('I found a zero!')

    else:
        term2 = np.sqrt(chi2_red - 1)
        #term1 = np.nanmean(df2['RTS_corrected_error'])
        term1 = np.nanmean(df2['RTS_corrected_error'])/np.nanmean(df2['RTS_corrected']) # TODO here I think is where we would put a normalization to FM/RTS
        # TODO when thinking about where to put that normalization to RTS_corrected (line above), it must be there, it one put it below, one would be normalizing
        # TODO multiple grouped sigma_bw values to one RTS, it would be too late.
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

output_grouped = pd.DataFrame({
    'Group': desc_arr,
    'Data Length (n)': length,
    'Chi2 Reduced': chi2_red_arr,
    'sigmabw_rts': sigbw_arr,
    'sigmabw_pm': sig_bw_pm_arr,
})


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
# We can do this like above
# IMPORTANT! Air secondaries are calculated based on flask ONLY but wtw error is mapped on ALL! Flask only reindexed later for individual secondaries
df = df.merge(output_grouped[['sigmabw_rts','sigmabw_pm','Group']], on='Group', how='left')

# use newly appended sigma_bw to calculate new FM errors for later residual plot
# some groups have sigmabw as 0 becuse chi2 were >1, see output from module above. Others have 0 beacuse they don't have WTW error applied. These include blanks, and things in "tuning" or "removed" categories
df["sigmabw_rts"] = df["sigmabw_rts"].fillna(0) # dupliactes line later but I left that later one cuz it was added first and don't want to break the code

# HOW DIFFERENT IS FM_err WITH NEW SIGMA_BW versus PREVIOUS WTW ERROR?
df['FM_err_new_sigbw'] = (np.sqrt(df['RTS_corrected_error']**2 + (df['sigmabw_rts']*.01*df['RTS_corrected'])**2)/0.95)*0.98780499
df['diff_err'] = df['F_corrected_normed_error'] - df['FM_err_new_sigbw'] # calculate the percent change with the new FM_err_new_sigmba.
df['diff_err_percent'] = ((df['F_corrected_normed_error'] - df['FM_err_new_sigbw'])/df['F_corrected_normed_error'])*100 # calculate the percent change with the new FM_err_new_sigmba.

df.to_excel("C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/data_checks_along_the_way/sigbw_merge_calc_check.xlsx")

# One important thing to note:
# At this point, the blanks and Travertine were not included in the grouped calculation of sigbw.
# We know the Travertine is bad, so we don't want it in there.
# Blanks are highly variable and don't repreesnt our secondaries
# However, now that we've calulated sigma_bw for each pretreatment, we can probably go ahread and add it onto these,
# - for calculations coming up. We'll need it for conversion to FM and D14C errors.
# - Why not just leave the travertine out completely? We want to be able to discuss data before and after travertine incorporation, show how it was variable

# grab values and map onto the travertines...
# NO WTW errors needed for blanks!
grab_inorganic = df.loc[df["Group"] == "Inorganic", ["sigmabw_rts", "sigmabw_pm"]].iloc[0]
df.loc[df["Job::R"] == "14047/2", ["sigmabw_rts", "sigmabw_pm"]] = grab_inorganic.values

grab_water = df.loc[df["Group"] == "Water", ["sigmabw_rts", "sigmabw_pm"]].iloc[0]
df.loc[df["Job::R"] == "14047/12", ["sigmabw_rts", "sigmabw_pm"]] = grab_water.values

print()
print(f"Lets make sure we haven't lost any data: Length after mergeing big gruop sigma_bws: {len(df)}")
print()

print(df.columns)
dfprint = df[['Job::R','Group', 'F_corrected_normed', 'F_corrected_normed_error', 'DELTA 14C',
              'DELTA 14C_Error', 'Reference for Collection Date', 'Expected FM', 'wmean', 'residual', 'sigmabw_rts', 'sigmabw_pm']]

dfprint.to_excel("C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/data_checks_along_the_way/sigma_bw_merged_to_df.xlsx")
# having some problems with downstream calculations probably related to this mapping above


"""
 # STEP 2.2: INDEX BASED ON PRETREATMENTS
 - - Then, we've been asked to index/seperate a lot of the organics based on pre-treatment. This will be a chunk of messy code

# I'm taking this from Data_Quality_Paper_2_2026_v1.py
"""

kapuni = df.loc[(df['Job::R'] == '40699/1')].copy()

airdeadCO2 = df.loc[(df['Job::R'] == '40430/3')].copy()
bhdamb_flask = df.loc[(df['Job::R'] == '40430/1') & (df['preptype'] == 'FLASK')].copy()
bhdspike_flask = df.loc[(df['Job::R'] == '40430/2') & (df['preptype'] == 'FLASK')].copy()
# for simplicity, lets just remove non-OX-flask prepared Airs frmo the databased because its confusing to find them later!
df = df.drop(df[(df['Job::R'] == '40430/1') & (df['preptype'] != 'FLASK')].index)
df = df.drop(df[(df['Job::R'] == '40430/2') & (df['preptype'] != 'FLASK')].index)

carr_marb_carb = df.loc[(df['Job::R'] == '14047/1')].copy()
travertine_carb = df.loc[(df['Job::R'] == '14047/2')].copy()
lac1carb = df.loc[(df['Job::R'] == '41347/2')].copy()
laa1carb = df.loc[(df['Job::R'] == '41347/3')].copy()
firi_l = df.loc[(df['Job::R'] == '26281/1')].copy()

carr_marb_water = df.loc[(df['Job::R'] == '14047/11')].copy()
travertine_water = df.loc[(df['Job::R'] == '14047/12')].copy()
lac1water = df.loc[(df['Job::R'] == '41347/12')].copy()
laa1water = df.loc[(df['Job::R'] == '41347/13')].copy()

kauri_all = df.loc[((df['Job::R'] == '40142/1') | (df['Job::R'] == '40142/2'))].copy()
kauri_aaa = df.loc[(df['Job::R'] == '40142/2')].copy()
kauri_cell = df.loc[(df['Job::R'] == '40142/1')].copy()
kauri_aaa_ea = df.loc[((df['Job::R'] == '40142/2') & (df['EA_ST'] =='EA'))].copy()
kauri_aaa_st = df.loc[((df['Job::R'] == '40142/2') & (df['EA_ST'].isna()))].copy()
kauri_cell_ea = df.loc[((df['Job::R'] == '40142/1') & (df['EA_ST'] =='EA'))].copy()
kauri_cell_st = df.loc[((df['Job::R'] == '40142/1') & (df['EA_ST'].isna()))].copy()

# we're setting the FIRI-F R numbers to go into the FIRI D category too....
# will be simplest to first set all FIRI-F's to FIRI D...the line below accomplishes that
df.loc[(df['Job::R'] == '24889/6'),'Job::R'] = '24889/4'

firi_d_all = df.loc[(df['Job::R'] == '24889/4')].copy()
firi_d_aaa_ea = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA')].copy()
firi_d_aaa_st = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna())].copy()
firi_d_cell_ea = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA')].copy()
firi_d_cell_st = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'].isna())].copy()
firi_d_cell = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose')].copy()
firi_d_aaa = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA')].copy()

firi_d_rpo = df.loc[(df['Job::R'] == '24889/14')].copy()

firi_e_aaa_st = df.loc[(df['Job::R'] == '24889/5') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna())].copy()

firi_g_all = df.loc[(df['Job::R'] == '24889/7')].copy()
firi_g_aaa_ea = df.loc[(df['Job::R'] == '24889/7') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA')].copy()
firi_g_aaa_st = df.loc[(df['Job::R'] == '24889/7') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna())].copy()

firi_i_all = df.loc[(df['Job::R'] == '24889/9')].copy()
# JOCELYN SAID THAT WE SHOULD REMOVE ANY FIRI-I THAT HAVE PRETREATMENT. HOWEVER, THEY ALL ARE EITHER CELLULOSE OR AAA. SHE SPECIFICALLY SAID TO GET RID OF AAA, SO WE"LL JST KEEP CELLULOSE
# firi_i_aaa_ea = df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA')].copy()
# firi_i_cell_ea = df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA')].copy()
# firi_i_aaa = df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='AAA')].copy()
firi_i_cell = df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='Cellulose')].copy()

datasets = [kapuni,
            airdeadCO2, bhdamb_flask, bhdspike_flask,
            carr_marb_carb, travertine_carb, lac1carb, laa1carb,
            carr_marb_water, travertine_water, lac1water, laa1water,
            firi_l,
            kauri_all,
            kauri_aaa, kauri_aaa_ea, kauri_aaa_st,
            kauri_cell, kauri_cell_ea, kauri_cell_st,
            firi_d_all, firi_d_aaa_ea, firi_d_aaa_st, firi_d_cell_ea, firi_d_cell_st, firi_d_cell, firi_d_aaa,
            firi_d_rpo,
            firi_e_aaa_st,
            firi_g_all, firi_g_aaa_ea, firi_g_aaa_st,
            firi_i_all,
            # firi_i_aaa_ea, firi_i_cell_ea, firi_i_aaa,
            firi_i_cell]

names = ['KAPUNI',
         'AIRDEADCO2','BHDAMB_FLASK','BHDSPIKE_FLASK',
         'CARR_MARB_CARB','TRAV_CARB','LAC1_CARB','LAA1_CARB',
         'CARR_MARB_WATER','TRAV_WATER','LAC1_WATER','LAA1_WATER',
         'FIRI_L',
         'KAURI_ALL',
         'KAURI_AAA','KAURI_AAA_EA','KAURI_AAA_ST',
         'KAURI_CELL','KAURI_CELL_EA','KAURI_CELL_ST',
         'FIRI_D_ALL', 'FIRI_D_AAA_EA','FIRI_D_AAA_ST','FIRI_D_CELL_EA','FIRI_D_CELL_ST', 'FIRI_D_CELL','FIRI_D_AAA',
         'FIRI_D_RPO',
         'FIRI_E_AAA_EA',
         'FIRI_G_ALL','FIRI_G_AAA_EA','FIRI_G_AAA_ST',
         'FIRI_I_ALL','FIRI_I_AAA_EA', 'FIRI_I_CELL_EA', 'FIRI_I_AAA','FIRI_I_CELL']

"""
lets loop through the R numbers and get means and stats assigned to each value in the database...
The loop will compare R numbers from the 'seconds.xlsx' with the R numbers from the dataframe
"""

# set output for plotly file later
outdir = r"C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/plotly_check"

# set inital value for wmean so i can calc residual later
df['wmean_subsets'] = -999

group_name = []
R_num = []
desc_arr = []
length = []
wmean_arr = []
chi2_red_arr = []
fm_arr = []
fm_err_arr = []
coll_date_arr = []
d14C_arr = []
d14C_err_arr = []

for i in range(0, len(datasets)):

    # Create figure and 2 vertical subplots
    fig, axs = plt.subplots(2, 1, figsize=(6, 8), sharex=True)  # 3 rows, 1 column

    # holdover from previous version
    df2 = datasets[i]

    R_num.append(df2['Job::R'].iloc[0]) # append R number, description, group name
    desc_arr.append(names[i])
    group_name.append(df2['Group'].iloc[0])
    length.append(len(df2))

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

    subset1["sigmabw_rts"] = subset1["sigmabw_rts"].fillna(0) # This line is important. For blanks, and Kapuni (tuning), no WTW error is applied. But if there is no data there, the rest of the calcualtions won't run. So we just need to set it to 0.
    sigbw_rts = (subset1['sigmabw_rts'].iloc[0])

    F_corrected_normed = (wmean/0.95)*0.98780499 #wmean converted to FM
    F_corrected_normed_error = (np.sqrt(term1**2 + (sigbw_rts*0.01*wmean)**2)/0.95)*0.98780499
    fm_arr.append(F_corrected_normed)
    fm_err_arr.append(F_corrected_normed_error)

    """
    Conversion to D14C
    """
    colldate1 = subset1['Collection Date_y'].iloc[0]
    coll_date_arr.append(colldate1)
    delta_14C =  1000*(F_corrected_normed*np.exp((1950-colldate1)/8267)-1)
    delta_14C_err = 1000*(F_corrected_normed_error*np.exp((1950-colldate1)/8267))
    d14C_arr.append(delta_14C)
    d14C_err_arr.append(delta_14C_err)

    """
    Draw a nice plot with residuals and FM's (we're not using D14C because the collection dates for FIRI are too difficult to pin down)...
    """

    # Residuals on the bottom
    axs[1].scatter(subset1['TP'], subset1['residual'], color='black', linestyle='')
    axs[1].axhline(y=0, color='black')

    # Second subplot
    subset1['F_corrected_normed'] = pd.to_numeric(df['F_corrected_normed'], errors="coerce")
    subset1['F_corrected_normed_error'] = pd.to_numeric(df['F_corrected_normed_error'], errors="coerce")
    subset1['TP'] = pd.to_numeric(df['TP'], errors="coerce")
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

    plt.tight_layout()

    """
    IF YOU WANT TO HOVER OVER TO CHECK, USE BOX BELOW
    """
    # Connect the mplcursors library to the plot
    # mplcursors.cursor(hover=True)
    # plt.show()
    """
    """

    plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/mpl_output/{i}.png',
                dpi=300, bbox_inches="tight")
    plt.close()

output_R_specific = pd.DataFrame({'Group': group_name,
                        'Job::R': R_num,
                        'Description': desc_arr,
                        'n': length,
                        'wmean': wmean_arr,
                        'chi2red': chi2_red_arr,
                        'Fraction Modern': fm_arr,
                        'Fraction Modern Err':fm_err_arr,
                        'Collection Date': coll_date_arr,
                        'D14C': d14C_arr,
                        'D14C_err': d14C_err_arr,
                        })


# NOW RUN SOME T-TESTS BEFORE OUTPUTTING THE RESULTS!
results_lines = []

# EA versus ST shown via FIRI-D's
t1, p1 = stats.ttest_ind(firi_d_cell_ea['F_corrected_normed'], firi_d_cell_st['F_corrected_normed'])
results_lines.append(
    f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_D_CELL_EA and FIRI_D_CELL_ST. Results <0.05 shows there is no observable difference")

# EA versus ST shown via FIRI-G's
t1, p1 = stats.ttest_ind(firi_g_aaa_ea['F_corrected_normed'], firi_g_aaa_st['F_corrected_normed'])
results_lines.append(
    f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_G_CELL_EA and FIRI_G_CELL_ST. Results <0.05 shows there is no observable difference")

results_lines.append('#The results above show that there is no observable difference between EA and ST for organic pretreatments. Since thats settled, we can recombined all and do t-tests with the AAA and Cell main groupings'
                     )

# CELL vs AAA using FIRI D
t1, p1 = stats.ttest_ind(firi_d_cell['F_corrected_normed'], firi_d_aaa['F_corrected_normed'])
results_lines.append(
    f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_D_CELL and FIRI_D_AAA. Results <0.05 shows there is no observable difference")

# # CELL vs AAA using FIRI I
# t1, p1 = stats.ttest_ind(firi_i_aaa['F_corrected_normed'], firi_i_cell['F_corrected_normed'])
# results_lines.append(
#     f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_I_CELL and FIRI_I_AAA. Results <0.05 shows there is no observable difference")

results_df = pd.DataFrame({"T-test Results": results_lines})

output_dir = (f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/Final_results.xlsx')

df_columns_cleaned = df[[
      'RTS_corrected', 'RTS_corrected_error',
      'MCC',
      'F_corrected_normed', 'F_corrected_normed_error', 'DELTA 14C',
      'DELTA 14C_Error',
      'wtgraph', 'preptype',
      'TP', 'TW', 'Quality Flag',
      'Job::R', 'Samples::Sample Description',
      'EA_ST', 'AAA_CELL', 'Collection Date_y', 'Group', 'Merge Comment',
      'Reference for Collection Date', 'Expected FM', 'wmean', 'residual']]

# Write to Excel
with pd.ExcelWriter(output_dir, engine="openpyxl", mode="w") as writer:
    df_columns_cleaned.to_excel(writer, sheet_name="Clean Dataset", index=False)
    output_grouped.to_excel(writer, sheet_name="Group Statistics", index=False)
    output_R_specific.to_excel(writer, sheet_name="Secondaries Statistics", index=False)
    results_df.to_excel(writer, sheet_name="T-test results", index=False)




