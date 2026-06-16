"""
The excel sheet read in below was created by findnig the NZA's in Rachel's Thesis Table 4.2
Initial .loc functions are added to recreate the metadata from this table. 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings 
warnings.filterwarnings(
    "ignore",
    message="Workbook contains no default style, apply openpyxl's default")

df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\Corran_Table4_2_OUTPUT_FOR_CHECK_edited.xlsx")

"""
A bit more cleanup still..
Would have been helpful to assign gruops in the last script...
And I want to be able to sort so the values appear on the plots in the order I want, that I feel makes sense 
"""

group1 = [56840,56843,56179,56842,56181,56178,56841,56180]
group2 = [57793,57795,57794,57792,57791]
group3 = [62645,62647,62646,62648]
group4 = [57788,57790,57789,57787,57786]
group5 = [62643,62644]
group6 = [62329,62330]
group7 = [62327, 62328]
group8=[56187,56189, 56186,56188]
group9=[62641,62642]
group10=[56191,56193,56190,56192]
group11=[62325,62326]
group11_1 =[62323,62324]
group12=[62639,62640]
group13=[56183,56185,56182,56184]
group14=[62638,62637]
group15 = [62313,62625,62311,62626]
group16 = [56174,56176,56173,56175]
group17 = [56167,56169,56166,56168,62322,62635,62321,62636]
group18 = [12357,12358,64289,64290]
group19 = [12340,12341,64291,64292]
group20 = [12954,12955,12956,12957,64293,64294]

groups = {
    1: group1,
    2: group2,
    3: group3,
    4: group4,
    5: group5,
    6: group6,
    7: group7,
    8: group8,
    9: group9,
    10: group10,
    11: group11,
    11.1: group11_1,
    12: group12,
    13: group13,
    14: group14,
    15: group15,
    16: group16,
    17: group17,
    18: group18,
    19: group19,
    20: group20,
}

# Flatten into TP -> group lookup
tp_to_group = {
    tp: group_num
    for group_num, tps in groups.items()
    for tp in tps
}

df['Group'] = df['Job::NZA'].map(tp_to_group)

# df.to_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\Corran_Table4_2_OUTPUT_FOR_CHECK_edited_2.xlsx")

"""
ADD SHORTNAME
"""

df['Shortname'] = 'nan'
df.loc[df['Manual Check Metods'] == 'Whole wood, untreated', 'Shortname'] =  'ww'

# Solvent Washes only, no cellulose 
df.loc[df['Manual Check Metods'] == 'RRL Soxhlet wash only, (no cellulose)', 'Shortname'] =  'Rs'
df.loc[df['Manual Check Metods'] == 'ANSTO soxhlet wash only (no cellulose extraction)', 'Shortname'] =  'As'

# RRL or ANSTO Solvents, RRL or ANSTO cellulose
df.loc[df['Manual Check Metods'] == 'RRL Soxlet, RRL cellulose', 'Shortname'] =  'Rs_R'
df.loc[df['Manual Check Metods'] ==  'RRL soxlet, ANSTO cellulose', 'Shortname'] =  'Rs_A'

df.loc[df['Manual Check Metods'] == 'ANSTO soxhlet, RRL cellulose', 'Shortname'] =  'As_R'
df.loc[df['Manual Check Metods'] ==  'ANSTO soxhlet, ANSTO cellulose', 'Shortname'] =  'As_A'

df.loc[df['Manual Check Metods'] ==  'ASE, ANSTO Cellulose', 'Shortname'] =  'ASE_A'


"""
try to sort based on name
"""

# print(np.unique(df['Manual Check Metods']))
df['SortVal'] = -999
df.loc[df['Manual Check Metods'] == 'Whole wood, untreated', 'SortVal'] =  0

# Solvent Washes only, no cellulose 
df.loc[df['Manual Check Metods'] == 'RRL Soxhlet wash only, (no cellulose)', 'SortVal'] =  1
df.loc[df['Manual Check Metods'] == 'ANSTO soxhlet wash only (no cellulose extraction)', 'SortVal'] =  2

# RRL or ANSTO Solvents, RRL or ANSTO cellulose
df.loc[df['Manual Check Metods'] == 'RRL Soxlet, RRL cellulose', 'SortVal'] =  3
df.loc[df['Manual Check Metods'] == 'ANSTO soxhlet, RRL cellulose', 'SortVal'] =  4

df.loc[df['Manual Check Metods'] ==  'RRL soxlet, ANSTO cellulose', 'SortVal'] = 5
df.loc[df['Manual Check Metods'] ==  'ANSTO soxhlet, ANSTO cellulose', 'SortVal'] =  6

df.loc[df['Manual Check Metods'] ==  'ASE, ANSTO Cellulose', 'SortVal'] =  7

df = df.loc[df['SortVal'] != -999]

# assign a weighted mean
def weighted_mean(F_corrected_normed, F_corrected_normed_error):
    wmean_num = np.sum(F_corrected_normed/F_corrected_normed_error**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    wmean_dem = np.sum(1/F_corrected_normed_error**2)
    wmean = wmean_num / wmean_dem
    return wmean

df['wmean'] = df.groupby('Group')['F_corrected_normed'].transform(lambda x: weighted_mean(df.loc[x.index, 'F_corrected_normed'], df.loc[x.index, 'F_corrected_normed_error']))
df['mean'] = df.groupby('Group')['F_corrected_normed'].transform('mean')
df['std'] = df.groupby('Group')['F_corrected_normed'].transform('std')

# df.to_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\test.xlsx")


# """
#         .      .      .      .      .      .
#    .       🚀        .      .       🌍      .
#         .      .   ⭐    .      .       .

# ======= FM PLOTS ==========
# THE FIRST ONE WILL JUST CONTAIN ALL THE DATA, AND WE"LL LEAVE IT IN THE SUPP INFO 
# NEXT PLOT WILL CONTAIN JUST A SUBSET FOR THE PAPER

#    .      .      .      .      .      .
#         🌑     .      .      .     🛰️
#    .      .      .      .      .      .
# """


"""
Plotting Differences from Mean
"""
# can assess, for each METHOD type, how far is each value from the mean? 
# def residual(rts_corrected, wm, rts_corrected_error):
#     residual = (rts_corrected - wm) / rts_corrected_error
#     return residual

df['delta'] = df['F_corrected_normed'] - df['wmean']
df['delta_err'] = np.sqrt(df['F_corrected_normed_error']**2 + df['std']**2)
# df['residual'] = residual(df['F_corrected_normed_error'],df['wmean'],df['F_corrected_normed_error'])

fig, axes = plt.subplots(5, 1, figsize=(6.5, 8), sharex=True, constrained_layout=True)

"""
SUBPLOT 1
"""
groups = {
    1: ('1950 Oak',  '#000000', 'o'),
    2: ('1956 Oak',  '#0072B2', 's'),
    3: ('1957 Kauri', '#E69F00', '^'),
    4: ('1958 Oak',  '#009E73', 'D'),
    5: ('1961 Kauri', '#D55E00', 'v'),
    6: ('1966 Kauri', '#CC79A7', 'P'),
    7: ('1968 Kauri', '#56B4E9', 'X'),
}

# use a loop for cleaner plotting of all these guys
for g, (label, color, marker) in groups.items():
    grp = df.loc[df['Group'] == g]
    axes[0].errorbar(grp['SortVal'],grp['delta'], yerr=grp['delta_err'], linestyle='', marker=marker, color=color, label=label, markersize=6, capsize=2)

axes[0].legend(loc='center left', bbox_to_anchor=(1., 0.5), frameon=False)

"""
SUBPLOT 2
"""
groups = {
    8: ('1986 Pine',  '#000000', 'o'),
    9: ('1988 Pine',  '#0072B2', 's'),
    10: ('1990 Chestnut', '#E69F00', '^'),
    11: ('1991 Chestnut',  '#009E73', 'D'),
    12: ('1994 Chestnut', '#D55E00', 'v'),
    13: ('1999 Pine', '#CC79A7', 'P'),
    14: ('2000 Pine', '#56B4E9', 'X'),
}

# use a loop for cleaner plotting of all these guys
for g, (label, color, marker) in groups.items():
    grp = df.loc[df['Group'] == g]
    axes[1].errorbar(grp['SortVal'],grp['delta'], yerr=grp['delta_err'], linestyle='', marker=marker, color=color, label=label, markersize=6, capsize=2)

axes[1].legend(loc='center left', bbox_to_anchor=(1., 0.5), frameon=False)


"""
SUBPLOT 3 Ancient Woods 
"""
groups = {
    15: ('Firi-D',  '#000000', 'o'),
    16: ('SIRI-F',  '#0072B2', 's'),
}

# use a loop for cleaner plotting of all these guys
for g, (label, color, marker) in groups.items():
    grp = df.loc[df['Group'] == g]
    axes[2].errorbar(grp['SortVal'],grp['delta'], yerr=grp['delta_err'], linestyle='', marker=marker, color=color, label=label, markersize=6, capsize=2)

axes[2].legend(loc='center left', bbox_to_anchor=(1., 0.5), frameon=False)


"""
SUBPLOT 4 Other Organics
"""
groups = {
    18: ('Leather',  '#000000', 'o'),
    19: ('Parchment',  '#0072B2', 's'),
    20: ('Textile', '#E69F00', '^'),
}

# use a loop for cleaner plotting of all these guys
for g, (label, color, marker) in groups.items():
    grp = df.loc[df['Group'] == g]
    axes[3].errorbar(grp['SortVal'],grp['delta'], yerr=grp['delta_err'], linestyle='', marker=marker, color=color, label=label, markersize=6, capsize=2)

axes[3].legend(loc='center left', bbox_to_anchor=(1., 0.5), frameon=False)


"""
SUBPLOT 5 Blank
"""
groups = {
    17: ('Blank',  '#000000', 'o'),
}

# use a loop for cleaner plotting of all these guys
for g, (label, color, marker) in groups.items():
    grp = df.loc[df['Group'] == g]
    axes[4].errorbar(grp['SortVal'],grp['delta'], yerr=grp['delta_err'], linestyle='', marker=marker, color=color, label=label, markersize=6, capsize=2)

axes[4].legend(loc='center left', bbox_to_anchor=(1., 0.5), frameon=False)

for ax in axes:
    # ax.set_ylabel('F14C')
    # ax.legend()
    ax.axhline(y=0, color='k', alpha=0.5)
    ax.set_ylim(-0.02,0.02)

axes[2].set_ylabel('Measured-Wmean F14C')
plt.xlabel('Pretreatment Code')

plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_4_corran_pretreatment_comparison2_output/all_diff.png", dpi=300, bbox_inches="tight")



# """
#         .      .      .      .      .      .
#    .       🚀        .      .       🌍      .
#         .      .   ⭐    .      .       .

# ======= SUBSET FOR PAPER, REMOVING Rs and As, and Leather, Parchment and Textile Subplot ==========
# 

#    .      .      .      .      .      .
#         🌑     .      .      .     🛰️
#    .      .      .      .      .      .
# """

"""
Removing the pretreatment types we're not focused on
"""

print(len(df))
df = df.loc[~df['Shortname'].isin(['Rs', 'As'])]
print(len(df))

"""
Turns out the 1957 Kauri only has 1 point for ASE and two for RS_A which isn't so helpful since its only
1 point out of the 4 main to compare. But then it turns out that a fey other of the datasets are the same, including the 1961 and 1966 Kauri.
The code below edits the pretreatment types to merge ASE and soxhlet. But its in vain because we need points that hit the RRL cellulose, merging means more of the same. 
(hello future self realizng this comment is so unhelpful, but I'm pressed for time!)

Because of this, we'll just comment out those rows from the "groups" below. 
"""

# # print(np.unique(df['Manual Check Metods']))

# """
# ['ANSTO soxhlet, ANSTO cellulose' 
# 'ANSTO soxhlet, RRL cellulose'
#  'ASE, ANSTO Cellulose' 
#  'RRL Soxlet, RRL cellulose'
#  'RRL soxlet, ANSTO cellulose' 
#  'Whole wood, untreated']

#  There are a few that go ASE, ANSTO cellulose. 
#  These (assuming as we have that the OSW's are all the same) could be re-classified as RRL Sox_ASE, ANSTO cellulose
#  This will allow us to keep more data for the comparison
# """
# df_s = df # make a copy to make these changes to
# df_s['Methods2'] = 'nan' # a new column to edit here

# df_s.loc[df_s['Manual Check Metods'] == 'ASE, ANSTO Cellulose', 'Manual Check Metods'] =  'RRL ASE or Soxhlet, then ANSTO cellulose'
# df_s.loc[df_s['Manual Check Metods'] == 'RRL soxlet, ANSTO cellulose' , 'Manual Check Metods'] =  'RRL ASE or Soxhlet, then ANSTO cellulose'

# # print(np.unique(df['Manual Check Metods']))

# """
# So now our 5 categories are 
# 'Whole wood, untreated'

# 'RRL Soxlet, RRL cellulose'
# 'ANSTO soxhlet, RRL cellulose'

# 'RRL ASE or Soxhlet, then ANSTO cellulose'
# 'ANSTO soxhlet, ANSTO cellulose' 
# """

# """
# 1957 Kauri is still unhelpful with all 3 pretreatments the same now...
# Remove it. 
# Same with 1961
# Same with 1968.
# """
"""
On to the plot.
"""

# the whole group of changes above is benefitial only for one sample so I'll just do that one manually: 
df.loc[(df['TP'] == 71485), 'Manual Check Metods'] = 'RRL soxlet, ANSTO cellulose'
df.loc[(df['TP'] == 71485), 'Shortname'] = 'Rs_A'
df.to_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\Corran_Table4_2_OUTPUT_FOR_CHECK_edited_3.xlsx")

# now I can get rid of the rest of ASE samples. Couldn't do it before beacuse I had to change the one above...
df = df.loc[~df['Shortname'].isin(['Rs', 'As', 'ASE_A'])]
print(len(df))

fig, axes = plt.subplots(3, 1, figsize=(6, 7.5), sharex=True, constrained_layout=True)

df.loc[df['Manual Check Metods'] == 'Whole wood, untreated', 'SortVal'] =  0

# RRL or ANSTO Solvents, RRL or ANSTO cellulose
df.loc[df['Manual Check Metods'] == 'RRL Soxlet, RRL cellulose', 'SortVal'] =  1
df.loc[df['Manual Check Metods'] == 'ANSTO soxhlet, RRL cellulose', 'SortVal'] =  2

df.loc[df['Manual Check Metods'] ==  'RRL soxlet, ANSTO cellulose', 'SortVal'] = 3
df.loc[df['Manual Check Metods'] ==  'ANSTO soxhlet, ANSTO cellulose', 'SortVal'] =  4

"""
SUBPLOT 1
"""
groups = {
    1: ('1950 Oak',  '#000000', 'o'),
    2: ('1956 Oak',  '#0072B2', 's'),
    # 3: ('1957 Kauri', '#E69F00', '^'),
    4: ('1958 Oak',  '#009E73', 'D'),
    # 5: ('1961 Kauri', '#D55E00', 'v'),
    6: ('1966 Kauri', '#CC79A7', 'P'),
    # 7: ('1968 Kauri', '#56B4E9', 'X'),
}

# use a loop for cleaner plotting of all these guys
for g, (label, color, marker) in groups.items():
    grp = df.loc[df['Group'] == g]
    axes[0].errorbar(grp['SortVal'],grp['delta'], yerr=grp['delta_err'], linestyle='', marker=marker, color=color, label=label, markersize=6, capsize=2)

axes[0].legend(loc='center left', bbox_to_anchor=(1., 0.5), frameon=False)

"""
SUBPLOT 2
"""
groups = {
    8: ('1986 Pine',  '#000000', 'o'),
    9: ('1988 Pine',  '#0072B2', 's'),
    10: ('1990 Chestnut', '#E69F00', '^'),
    11: ('1991 Chestnut',  '#009E73', 'D'),
    12: ('1994 Chestnut', '#D55E00', 'v'),
    13: ('1999 Pine', '#CC79A7', 'P'),
    14: ('2000 Pine', '#56B4E9', 'X'),
}

# use a loop for cleaner plotting of all these guys
for g, (label, color, marker) in groups.items():
    grp = df.loc[df['Group'] == g]
    axes[1].errorbar(grp['SortVal'],grp['delta'], yerr=grp['delta_err'], linestyle='', marker=marker, color=color, label=label, markersize=6, capsize=2)

axes[1].legend(loc='center left', bbox_to_anchor=(1., 0.5), frameon=False)


"""
SUBPLOT 3 Ancient Woods 
"""
groups = {
    15: ('Firi-D',  '#000000', 'o'),
    16: ('SIRI-F',  '#0072B2', 's'),
}

# use a loop for cleaner plotting of all these guys
for g, (label, color, marker) in groups.items():
    grp = df.loc[df['Group'] == g]
    axes[2].errorbar(grp['SortVal'],grp['delta'], yerr=grp['delta_err'], linestyle='', marker=marker, color=color, label=label, markersize=6, capsize=2)

axes[2].legend(loc='center left', bbox_to_anchor=(1., 0.5), frameon=False)


for ax in axes:
    # ax.set_ylabel('F14C')
    # ax.legend()
    ax.axhline(y=0, color='k', alpha=0.5)
    ax.set_ylim(-0.02,0.02)


axes[1].set_ylabel('Measured-Wmean F14C')
plt.xlabel('Pretreatment Code')

plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_4_corran_pretreatment_comparison2_output/all_diff_subset.png", dpi=300, bbox_inches="tight")
plt.close()

# """
#         .      .      .      .      .      .
#    .       🚀        .      .       🌍      .
#         .      .   ⭐    .      .       .

# ======= SUBSET FOR PAPER, REMOVING Rs and As, and Leather, Parchment and Textile Subplot ==========
# 

#    .      .      .      .      .      .
#         🌑     .      .      .     🛰️
#    .      .      .      .      .      .
# """

# we only care about these groups, for pre-bomb 
groups = {
    1: ('1950 Oak',  '#000000', 'o'),
    2: ('1956 Oak',  '#0072B2', 's'),
    3: ('1957 Kauri', '#E69F00', '^'),
    4: ('1958 Oak',  '#009E73', 'D'),
    5: ('1961 Kauri', '#D55E00', 'v'),
    6: ('1966 Kauri', '#CC79A7', 'P'),
    7: ('1968 Kauri', '#56B4E9', 'X'),
}

df2 = df.loc[df['Group'] < 8]
ww = df2.loc[df2['Manual Check Metods'] == 'Whole wood, untreated'] 
Rs_R = df2.loc[df2['Manual Check Metods'] == 'RRL Soxlet, RRL cellulose']
Rs_A = df2.loc[df2['Manual Check Metods'] ==  'RRL soxlet, ANSTO cellulose']
As_R = df2.loc[df2['Manual Check Metods'] == 'ANSTO soxhlet, RRL cellulose']
As_A = df2.loc[df2['Manual Check Metods'] ==  'ANSTO soxhlet, ANSTO cellulose']

fig = plt.figure(figsize=(6,5))
plt.axhline(y=0, color='k', alpha=0.5)
plt.boxplot([ww['delta'], Rs_R['delta'], As_R['delta'], Rs_A['delta'], As_A['delta']],
            labels=["ww", "Rs_R", "As_R", "Rs_A", "As_A"])
plt.ylabel('Measured-Wmean F14C')
plt.xlabel('Pretreatment Code')

plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_4_corran_pretreatment_comparison2_output/bomb_whisker.png", dpi=300, bbox_inches="tight")
plt.close()
