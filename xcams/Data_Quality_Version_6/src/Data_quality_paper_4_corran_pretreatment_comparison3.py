"""
On June 12 JCT request I make pooled chi2 calculation for tree rings using ANSTO method. 

We decided on a dataset to use: 
And we're going to run the same analysis that we did on _2 and _7 to get the pooled statistics on this group
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\TreeRingRepeats.xlsx").dropna(subset='AMS Submission Results Complete::F_corrected_normed')
# df['TP'] = df['AMS Submission Results Complete::TP']
# print(len(df))
# """
# RTS and RTS corr error not on Jocelyn's export from Tree Ring Database
# I can go into big RLIMS export and just grab all the TP numbers here and merge those columns: 
# """
# tps = np.unique(df['TP'])

# df_for_merge = pd.read_excel(rf"I:\C14Data\C14_blank_corrections_NEW\import_from_RLIMS\historical_data\TW3622standards.xlsx")

# df_merged = df.merge(
#     df_for_merge[['TP', 'Ratio to standard','Ratio to standard error']],
#     left_on='TP',
#     right_on='TP',
#     how='left'
# )

# print(len(df_merged))
# print(df_merged.columns)
# df_merged.to_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\TreeRingRepeats_merged.xlsx")


# """
#         .      .      .      .      .      .
#    .       🚀        .      .       🌍      .
#         .      .   ⭐    .      .       .

# ======= Re-read in merged file to save time ==========

#    .      .      .      .      .      .
#         🌑     .      .      .     🛰️
#    .      .      .      .      .      .
# """
df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\TreeRingRepeats_merged.xlsx")
df = df.rename(columns={'Ratio to standard': 'RTS_corrected',
                        'Ratio to standard error': 'RTS_corrected_error'})

# print(df.columns)
# print(np.unique(df['AMS Submission Results Complete::Quality Flag']))
# ['...' '.Q.' '.T.' '.X.' 'A..']
# we're going to drop all columns with "A.."

df = df.loc[df['AMS Submission Results Complete::Quality Flag'] != 'A..']
df = df.loc[df['AMS Submission Results Complete::Quality Flag'] != '.T.']
# also remove any TP's that were in her intercomparison test:
removes = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\Corran_Table4_2.xlsx")
removes_TP = removes['TP']
df = df.loc[~df['TP'].isin(removes_TP)]

# drop the bad kings crescent replicate: 
df = df.loc[df['Samples::Sample ID'] != 'KNG52-long-R31']

# now how many materials do I have and how many times was each measured? 
r_counts = (
    df.groupby('R')
      .size()
      .reset_index(name='length')
)

r_counts.to_excel(
    r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_4_corran_pretreatment_comparison2_output\r_counts_output_BEFORE.xlsx",
    index=False
)

tps_w_1 = r_counts.loc[r_counts['length'] == 1]
tps_w_1 = tps_w_1['R']

df = df.loc[~df['R'].isin(tps_w_1)]

r_counts = (
    df.groupby('R')
      .size()
      .reset_index(name='length')
)

r_counts.to_excel(
    r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_4_corran_pretreatment_comparison2_output\r_counts_output_AFTER.xlsx",
    index=False
)


# # how many of each R?
# # print(r_counts)

# # drop all that have only 1 measurement
# single_rs = r_counts.loc[r_counts['length'] == 1, 'R']
# df_filtered = df[~df['R'].isin(single_rs)]

# # check it worked:
# r_counts = (
#     df_filtered.groupby('R')
#       .size()
#       .reset_index(name='length')
# )
# # print(r_counts)

# # drop the bad kings crescent replicate: 
# df = df.loc[df['Samples::Sample ID'] != 'KNG52-long-R31']

# """
#         .      .      .      .      .      .
#    .       🚀        .      .       🌍      .
#         .      .   ⭐    .      .       .

# ======= Now we can run our stats... ==========

#    .      .      .      .      .      .
#         🌑     .      .      .     🛰️
#    .      .      .      .      .      .
# """

def weighted_mean(rts_corrected, rts_corrected_error):
    wmean_num = np.sum(rts_corrected/rts_corrected_error**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    wmean_dem = np.sum(1/rts_corrected_error**2)
    wmean = wmean_num / wmean_dem
    return wmean

def residual(rts_corrected, wm, rts_corrected_error):
    residual = (rts_corrected - wm) / rts_corrected_error
    return residual

def rts_to_permille_for_errors(rts, colldate):
    rts_to_FM  = (np.sqrt(rts**2)/0.95)*0.98780499
    FM_to_permille = 1000*(rts_to_FM*np.exp((1950-colldate)/8267))
    return FM_to_permille


rs = np.unique(df['R'])
k = len(rs) # number of materials we're using for pooled statistics
print(k)
df['wmean'] = df.groupby('R')['RTS_corrected'].transform(lambda x: weighted_mean(df.loc[x.index, 'RTS_corrected'], df.loc[x.index, 'RTS_corrected_error']))


"""
Calculate chi2 reduced
"""
chi2_red_num = np.sum((df['RTS_corrected']-df['wmean'])**2/df['RTS_corrected_error']**2)
chi2_red_denom = len(df)-k # subtract number of groups in degrees of freedom calc.
chi2_red = chi2_red_num/chi2_red_denom
print(chi2_red)


