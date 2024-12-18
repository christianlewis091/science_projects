"""
December 4, 2024: Final check that the script still runs successfully before I submit the paper etc.
Still runs :)

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
df_old = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_submission\Data_Files\SOARTreeRingData_CBL_cleaned_aug_1_2024.xlsx').dropna(subset='F14C')
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
df_new_tree_core_merge = df_new_tree_core_merge.dropna(subset='Comment')
df_new_tree_core_merge = df_new_tree_core_merge.dropna(subset='Site')
df_new_tree_core_merge = df_new_tree_core_merge.dropna(subset='Ring year')

# THE DATA BELOW WILL BE ADDED TO df = pd.read_excel(r'H:\Science\Datasets\SOARTreeRingData2022-02-01.xlsx') before reading into "tree_ring_analysis"
df_new_tree_core_merge.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_submission\Data_Files\penes_data.xlsx')

