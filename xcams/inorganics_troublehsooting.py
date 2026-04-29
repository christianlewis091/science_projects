import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Export RLIMS of 41347/3, include JOB # (TP, TW, JOB, RTS_corr, RTS_corr_err)
Merge with my list of comments based on JOB # 
Merge with my list post filtering for data quality (d1_res = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/Final_results.xlsx', sheet_name='Clean Dataset')) (TP, TW, JOB, RTS_corr, RTS_corr_err, Reference for Collection Date)

Now dataset will have a record of what's in database with good comments, what's in the DQ paper, and new samples POST DQ paper time period

Are any with new comments from physical pretreatment in the DQ paper at this time? They should be flagged and removed. 

Calculate residual

Plot the data according to samples from top bottom middle or unknown, is there a trend with residual?

What is new chi2 with up-to-date data? 

"""
"""
Export RLIMS of 41347/3, include JOB # (TP, TW, JOB, RTS_corr, RTS_corr_err)
Merge with my list of comments based on JOB # 
Merge with my list post filtering for data quality (d1_res = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/Final_results.xlsx', sheet_name='Clean Dataset')) (TP, TW, JOB, RTS_corr, RTS_corr_err, Reference for Collection Date)
"""

rlims = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\sandbox_post_April3_meeting_output\troubleshooting_inorganics_data\RLIMS_41347_3_export.xlsx", comment='#')
rlims['Origin'] = 'RLIMS'
# print(len(rlims))

pretreat = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\sandbox_post_April3_meeting_output\troubleshooting_inorganics_data\Pretreatment_comments.xlsx", comment='#')

#
df = rlims.merge(pretreat, on='Job', how='left')  # merge
#df.to_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\sandbox_post_April3_meeting_output\troubleshooting_inorganics_data\troubleshooting_step1.xlsx")
# print(len(df))

# merge with list post-data quality filter
# reading from the end of script 1 so I can compare the Keep Removes to the RLIMS data
d1_res = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/12_manual_plotly_drop.xlsx', sheet_name= 'Whole Dataframe')
d1_res = d1_res.loc[d1_res['Job::R'] == '41347/3']
d1_res = d1_res[['TP','Keep_Remove']]
df = df.merge(d1_res, on='TP', how='left')  # merge
df.to_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\sandbox_post_April3_meeting_output\troubleshooting_inorganics_data\troubleshooting_step2.xlsx")
print(len(df))

# add date since etch
etch = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\sandbox_post_April3_meeting_output\troubleshooting_inorganics_data\date_since_etch.xlsx')
df = df.merge(etch, on='TP', how='left')  # merge

"""
FROM ORIGINAL RLIMS DATA TO PRESENT STATUS OF PAPER (FINAL_RESULTS, WE WENT FROM 23-17 data points. 
"""
"""
I'm curious what we get if we run the chi2 test with full current dataset (2026)
"""

def residual(rts_corrected, wm, rts_corrected_error):
    residual = (rts_corrected - wm) / rts_corrected_error
    return residual

def weighted_mean(rts_corrected, rts_corrected_error):
    wmean_num = np.sum(rts_corrected/rts_corrected_error**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    wmean_dem = np.sum(1/rts_corrected_error**2)
    wmean = wmean_num / wmean_dem
    return wmean

def chi2(rts, rts_err, length):
    # calculate WM
    wmean_num = np.sum(rts/rts_err**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    wmean_dem = np.sum(1/rts_err**2)
    wmean = wmean_num / wmean_dem

    # residual = (rts - wmean) / rts_err

    # calculate chi2
    chi2_red_num = np.sum((rts-wmean)**2/rts_err**2)
    chi2_red_denom = length-1 # subtract number of groups in degrees of freedom calc.
    chi2_red = chi2_red_num/chi2_red_denom
    return chi2_red

"""
Chi2 test with all data in RLIMS
"""
print('All data from RLIMS, nothing removed')
chi2_val = chi2(df['RTS_corrected'], df['RTS_corrected_error'],len(df))
print(chi2_val)
print(len(df))
print()

"""
Lets remove the problematic data: (from the future, post-DQ time period, but in RLIMS)
"""
print('Only rows removed that were post DQ time period and should have flags based on job comments \n We lose 7 based on some having weird job notes like removing black hair, and one that says it may be a swap ')
df = df.loc[df['CBL_comment1'] != 'Potentially Marble wrong sample']
df = df.loc[df['CBL_comment1'] != 'REMOVE, job notes say there may be a swap']
chi2_val = chi2(df['RTS_corrected'], df['RTS_corrected_error'],len(df))
print(chi2_val)
print(len(df))
print()

"""
14C gradient in the coral? 
"""
print('Removing samples taken from bottom and middle of coral (most were from top). Nonhomogeneous?')
df = df.loc[df['CBL_comment1'] != 'Bottom']
df = df.loc[df['CBL_comment1'] != 'Middle']
chi2_val = chi2(df['RTS_corrected'], df['RTS_corrected_error'],len(df))
print(chi2_val)
print(len(df))
print()

"""
DQ paper only 
"""
print('Double check results from just data in DQ paper...')
df_keep = df.loc[df['Keep_Remove'] == 'Keep'].copy()
chi2_val = chi2(df_keep['RTS_corrected'], df_keep['RTS_corrected_error'],len(df_keep))

print(chi2_val)
print(len(df_keep))

# DID I SOLVE IT???? LETS RUN THE MAIN SCRIPT WITH THESE TPs AND SEE IF RESULT MATCHES
# I didn't solve it....there was a bug...
df_keep.to_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\sandbox_post_April3_meeting_output\troubleshooting_inorganics_data\troubleshooting_step3.xlsx")
potential_list = df_keep['TP']

wmean_num = np.sum(df_keep['RTS_corrected']/df_keep['RTS_corrected_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
wmean_dem = np.sum(1/df_keep['RTS_corrected_error']**2)
df_keep['wmean'] = wmean_num / wmean_dem

chi2_red_num = np.sum((df_keep['RTS_corrected']-df_keep['wmean'])**2/df_keep['RTS_corrected_error']**2)
chi2_red_denom = len(df_keep)-1 # subtract number of groups in degrees of freedom calc.
chi2_red = chi2_red_num/chi2_red_denom
print()
print(chi2_red)
print(len(df_keep))

"""
check date since etching
I've manually looked at difference from physical pretreament to CO2 evolution for all samples in data quality paper (from 12_plotly_manual_drop = Keep (none were set to remove anyway!))
There is a very wide range of date lengths in there...

It doesn't seem to be this either!
"""
chi2_val = chi2(df_keep['RTS_corrected'], df_keep['RTS_corrected_error'], len(df_keep))

df_keep['Residual'] = residual(df_keep['RTS_corrected'],df_keep['wmean'],df_keep['RTS_corrected_error'])

fig, axs = plt.subplots(2, 1, figsize=(6, 8))  # 3 rows, 1 column

# Residuals on the bottom
axs[1].scatter(df_keep['Days Etch to CO2'], df_keep['Residual'], color='black', linestyle='')
axs[0].errorbar(df_keep['TP'], df_keep['Residual'])

axs[0].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
axs[0].set_xlabel('TP')

axs[1].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
axs[1].set_xlabel('Days since etch')
plt.show()
plt.close()


"""
What about size? 
"""

fig, axs = plt.subplots(2, 1, figsize=(6, 8))  # 3 rows, 1 column

# Residuals on the bottom
axs[1].scatter(df_keep['wtgraph'], df_keep['Residual'], color='black', linestyle='')
axs[0].errorbar(df_keep['TP'], df_keep['Residual'])

axs[0].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
axs[0].set_xlabel('TP')

axs[1].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
axs[1].set_xlabel('wtgraph')
plt.show()
plt.close()

"""
Check if LAA1 from carbonates behaves worse than LAC if given smaller errors
"""

df3 = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/Final_results.xlsx', sheet_name='Clean Dataset')

df3 = df3.loc[df3['Job::R'] == '41347/13']

# apply average RTS corr err to LAA1_watesr and see how chi2 reuslts...are high water line errors masking variabilty????
# mean error for laa1_carbonate is .00137
df3['RTS_err_test'] = .00137

# check it first under normal case
wmean_num = np.sum(df3['RTS_corrected']/df3['RTS_corrected_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
wmean_dem = np.sum(1/df3['RTS_corrected_error']**2)
df3['wmean'] = wmean_num / wmean_dem

chi2_red_num = np.sum((df3['RTS_corrected']-df3['wmean'])**2/df3['RTS_corrected_error']**2)
chi2_red_denom = len(df3)-1 # subtract number of groups in degrees of freedom calc.
chi2_red = chi2_red_num/chi2_red_denom
print('LAA1 waters chi2 check with real errorbars')
print(chi2_red)


# check it first under normal case
wmean_num = np.sum(df3['RTS_corrected']/df3['RTS_err_test']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
wmean_dem = np.sum(1/df3['RTS_err_test']**2)
df3['wmean'] = wmean_num / wmean_dem

chi2_red_num = np.sum((df3['RTS_corrected']-df3['wmean'])**2/df3['RTS_err_test']**2)
chi2_red_denom = len(df3)-1 # subtract number of groups in degrees of freedom calc.
chi2_red = chi2_red_num/chi2_red_denom
print()
print('LAA1 waters chi2 check with fake, smaller errorbars matching LAA1 carboante')
print(chi2_red)

"""
Here we have it????? 
If you use smaller errors for the LAA1 corals on waterline, we find the chi2 sucks too. 
This may mean that LAA1 coral actually isn't so reproducible after all, and that we should remove it? 
Anyway for the paper we can just say that it's masked by water line blank values
"""


























