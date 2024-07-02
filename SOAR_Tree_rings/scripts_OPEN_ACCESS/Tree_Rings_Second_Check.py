"""
Jocelyn asked Pene to re-process and re-run two sites (Raul Marin and Monte Tarn) so we can be sure that the signals
were seeing are real.

Here's a first look at the results.

This code is adapted from tree_ring_analysis.py.

We have two more wheels coming so I hope this can be made to run smoothly to deal with new data
"""

import matplotlib as mpl
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import seaborn as sns
from reference1 import reference1
import matplotlib.pyplot as plt

# function to extract Tree and Core number, used later on
def extract_text(s):
    parts = s.split('-')
    if len(parts) < 3:
        return ""
    return '-'.join(parts[1:-1])

markers = ['o','D','X','^']

# preamble to set up plots for later
plt.close()
colors = sns.color_palette("rocket", 6)  # import sns color pallet rocket
colors2 = sns.color_palette("mako", 6)  # import sns color pallet mako.
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10

# read in the tree ring data that I cleaned up previously
df_old = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\SOARTreeRingData_CBL_cleaned.xlsx')
df_old['Comment'] = 'Old Runs'

# read in the data from Pene's first wheel of data, remove useless columns, rename columns to match old data

df_new = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\Pene_Tree_Ring_Check.xlsx').dropna(subset='F_corrected_normed')
df_new['Comment'] = 'TW3516'
df_new2 = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\TW3519.xlsx').dropna(subset='F_corrected_normed')
df_new2['Comment'] = 'TW3519'
df_new3 = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\TW3522.xlsx').dropna(subset='F_corrected_normed')
df_new3['Comment'] = 'TW3522'

df_new = pd.concat([df_new, df_new2])
df_new = pd.concat([df_new, df_new3])
df_new.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\test.xlsx')

# drop some columns for simplicity
df_new = df_new[['Job::R','Quality Flag','F_corrected_normed','F_corrected_normed_error','DELTA14C', 'DELTA14C_Error','Comment','TP','TW']]
df_new = df_new.rename(columns={'DELTA14C':'∆14C', 'DELTA14C_Error':'∆14Cerr','Job::R':'R number','F_corrected_normed':'F14C','F_corrected_normed_error':'F14C_err'})

# currnetly, I dont know where any of the samples are. I need the R numbers to be coordinated with real data
# merge with tree ring database
tree_core = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\tree_core_v2.xlsx')
tree_core = tree_core[['R number','Ring code','Ring year','StudySites::Site name']]
tree_core = tree_core.rename(columns={'StudySites::Site name':'Site'})
#
df_new_tree_core_merge = df_new.merge(tree_core, on='R number', how='outer')
df_new_tree_core_merge = df_new_tree_core_merge.dropna(subset='Site')
#

# set my old data to match the columns of the new data for clarity
df_old = df_old[['Ring code', 'R number', 'Site', 'F14C', 'F14Cerr',
                 'DecimalDate', '∆14C', '∆14Cerr', 'CBL_flag', 'Comment']].rename(columns={'DecimalDate':'Ring year'})
#
#THIS IS THE DATA FILE THATS COMPLETE AND WE CAN FILTER ON PROPERLY
df_total = pd.concat([df_old, df_new_tree_core_merge])
df_total = df_total.dropna(subset='Site')  # there's still some data from primary ox's and tuning
df_total = df_total.dropna(subset='Ring code')
df_total.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\dftotal.xlsx')

# use the function from earlier to find Tree and Core
df_total['TX_CY'] = df_total['Ring code'].apply(extract_text)
#
# create a list of sites from the new dataset
new_sites = df_total.loc[(df_total['Comment'] == 'TW3516') | (df_total['Comment'] == 'TW3519')| (df_total['Comment'] == 'TW3522')]
sites = np.unique(new_sites['Site'])
#
# importing Reference 1 from the previous python file.
harm_xs = reference1['Decimal_date']  # see dataset_harmonization.py
harm_ys = reference1['D14C']  # see dataset_harmonization.py
harm_y_errs = reference1['weightedstderr_D14C']
# #
# #
for i in range(0, len(sites)):

    # loop into the first site
    this_site = df_total.loc[df_total['Site'] == sites[i]]
    old = this_site.loc[this_site['Comment'] == 'Old Runs']
    new = this_site.loc[this_site['Comment'] == 'TW3516']
    new2 = this_site.loc[this_site['Comment'] == 'TW3519']
    new3 = this_site.loc[this_site['Comment'] == 'TW3522']
    print(new3)

    # how many unique tree cores are in this site?
    cores = np.unique(old['TX_CY'])
    fig = plt.figure()
    for j in range(0, len(cores)):
        old = old.loc[old['TX_CY'] == cores[j]]
        # used to do errorbar but they're too small to se anyway compared to the data
        plt.errorbar(old['Ring year'], old['∆14C'], yerr=old['∆14Cerr'], label=f'{cores[j]}, OLD RUNS', color='red', marker=markers[j], linestyle='')

    # how many unique tree cores are in this site?
    cores = np.unique(new['TX_CY'])
    for j in range(0, len(cores)):
        new = new.loc[new['TX_CY'] == cores[j]]
        # used to do errorbar but they're too small to se anyway compared to the data
        plt.errorbar(new['Ring year'], new['∆14C'], yerr=new['∆14Cerr'], label=f'{cores[j]}, TW3516', color='blue', marker=markers[j], linestyle='')

    cores = np.unique(new2['TX_CY'])
    for j in range(0, len(cores)):
        new = new2.loc[new2['TX_CY'] == cores[j]]
        # used to do errorbar but they're too small to se anyway compared to the data
        plt.errorbar(new['Ring year'], new['∆14C'], yerr=new['∆14Cerr'], label=f'{cores[j]}, TW3519', color='purple', marker=markers[j], linestyle='')

    cores = np.unique(new3['TX_CY'])
    for j in range(0, len(cores)):
        new = new3.loc[new3['TX_CY'] == cores[j]]
        # used to do errorbar but they're too small to se anyway compared to the data
        plt.errorbar(new['Ring year'], new['∆14C'], yerr=new['∆14Cerr'], label=f'{cores[j]}, TW3522', color='green', marker='s', linestyle='')

    plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
    plt.legend()
    plt.xlabel('Date', fontsize=14)
    plt.xlim(1970, 2020)
    plt.ylim(0, 400)
    plt.title(f'{sites[i]}')
    plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
    plt.savefig(
        f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/Tree_Ring_Second_Check/{sites[i]}_errorbar_TRE3.png',
        dpi=300, bbox_inches="tight")
    plt.close()


"""
isolate and look at duplicates
"""
merged = df_old.merge(df_new, on='R number')
# merged.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\test2.xlsx')
# merged = merged.drop_duplicates(subset='R number')
merged['diff_d14C'] = merged['∆14C_y'] - merged['∆14C_x']
merged['diff_FM'] = merged['F14C_y'] - merged['F14C_x']
merged.to_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/Tree_Ring_Second_Check/Duplicatelook.xlsx')







































































#
# # read in, remove useless coolumns, rename columns to match old data
# df_new = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\Pene_Tree_Ring_Check.xlsx').dropna(subset='F_corrected_normed')
# df_new = df_new[['Job::R','Quality Flag','F_corrected_normed','F_corrected_normed_error','D14C', 'D14C_Error']]
# df_new = df_new.rename(columns={'D14C':'∆14C', 'D14C_Error':'∆14Cerr','Job::R':'R number','F_corrected_normed':'F14C','F_corrected_normed_error':'F14C_err'})
# df_new.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\Pene_Tree_Ring_Check2.xlsx')
# df_new['Comment'] = 'New Runs'
#
# tree_core = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\tree_core_v2.xlsx')
# tree_core = tree_core[['R number','Ring code','Ring year','StudySites::Site name']]
#
# df_new = df_new.merge(tree_core, on='R number', how='outer')
# # df_new.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\test.xlsx')
#
# # only keep data from the most recent wheel
# df_new = df_new.loc[df_new['Comment'] == 'New Runs']
#
# # Read in the old data to compare with
# df_old = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\data\SOARTreeRingData_CBL_cleaned.xlsx')
# df_old['Comment'] = 'Original Run'
#
# old_RMB = df_old.loc[df_old['Site'] == 'Raul Marin Balmaceda']
# new_RMB = df_new.loc[df_new['StudySites::Site name'] == 'Raul Marin Balmaceda']
#
# plt.scatter(new_RMB['Ring year'], new_RMB['F14C'], label='New')
# plt.scatter(old_RMB['DecimalDate'], old_RMB['F14C'], label='Old')
# plt.legend()
# plt.close()
#
# old_WLT = df_old.loc[df_old['Site'] == 'Raul Marin Balmaceda']
# new_WLT = df_new.loc[df_new['StudySites::Site name'] == 'Raul Marin Balmaceda']
#
# plt.scatter(new_RMB['Ring year'], new_RMB['F14C'], label='New')
# plt.scatter(old_RMB['DecimalDate'], old_RMB['F14C'], label='Old')
# plt.legend()
# plt.close()
