"""
The reviewers asked me to compare my data with that of Hua 2022.
I realized that Hua is a compilation, of data including Jocelyn's 2017 paper, and Turney 2018.

I realize that BHD and Nikau (2 tree-ring sites from Eastbourne) might be being duplicately published by accident here.
I need to cross reference the ring codes in MY data, with HER data. If they all match, it's a big problem I need to sort out.
"""
import numpy as np
import pandas as pd

jct = pd.read_excel(r'H:\Science\Papers\In Prep Work\2023_Lewis_SOARTreeRings\V9_Jan282025_reviewer_comments\turnbull_2017_supplements/BHD_14CO2_Datasets_20170803.xlsx', sheet_name = 'BHD_TREERING_DATA', skiprows=5)
trd = pd.read_excel(r'H:\Science\Papers\In Prep Work\2023_Lewis_SOARTreeRings\V9_Jan282025_reviewer_comments\turnbull_2017_supplements/rlimstrd.xlsx')
cbl = pd.read_excel(r'H:\Science\Papers\In Prep Work\2023_Lewis_SOARTreeRings\V8_EGU_Resubmission_colors_and_suppinfonames/Data.xlsx', skiprows=2)

# JCT's data uses NZA numbers.
# CBL's uses R number, and ring code

# what are the NZA numbers used in Jocelyn's 2017 paper?
nzas = jct['NZ']
nzas = list(nzas)
print(f'The length of Jocelyns 2017 dataset including BHD and NIK sites is {len(nzas)}')

# from the tree-ring database, lets find the data associated with these nza's.
# print(len(trd))
trd = trd.loc[trd['NZA'].isin(nzas)]
# print(len(trd))
# print(trd.columns)

# and now lets find the tree-ring code's associated with these...
jct_2017_ringcodes = trd['Ring code'].reset_index(drop=True)
# print(jct_2017_ringcodes)

# now how many of Jocelyn's ring codes overlap with mine?
jct_2017_ringcodes = list(jct_2017_ringcodes)
cbl_bad = cbl.loc[cbl['Ring code'].isin(jct_2017_ringcodes)].reset_index(drop=True)
# print(len(cbl_bad))
print(f'The number of Jocelyns ring codes that overlap with my dataset is {len(cbl_bad)}')

# # 107 of my tree-rings were previously published in Jocelyn's 2017 paper.
# # but this means that ~40 of the measurements from BHD, and Nikau st's ARE new. Which ones are new?
# sites = ['Baring Head, NZ', 'Eastbourne 1, NZ', 'Eastbourne 1, NZ']
# cbl_good = cbl.loc[(cbl['Ring code'].isin(jct_2017_ringcodes) == False) & (cbl['Site'].isin(sites))]
# print(len(cbl_good))
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns (if needed)
pd.set_option('display.expand_frame_repr', False)  # Prevent line wrapping

cbl_sites = np.unique(cbl['Site'])
for i in range(0,len(cbl_sites)):
    cbl_i = cbl.loc[cbl['Site'] == cbl_sites[i]]
    # how many unique ring codes exist?
    id_counts = cbl_i['Ring code'].value_counts()
    print(cbl_sites[i])
    print(id_counts)
