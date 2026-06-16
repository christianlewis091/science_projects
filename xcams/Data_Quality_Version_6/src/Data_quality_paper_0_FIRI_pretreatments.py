"""
For the organics, I need to report which were done with Cellulose and AAA, and which were done with sealed tube combustion or EA. 
Much of this work has been done already in a previous version. 
See Firi_edited_V0to5. 
"""
import pandas as pd

# these are the materials were interested in matting pretreatments of for organics. 
organic_r = ['24889/4', '24889/6','24889/5','24889/7','24889/9']

# # this is work i've already done on mapping those pretreatments (but I don't think I'll need it anymore)
# df = pd.read_excel(rf'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\firis_edited_V0to5.xlsx', comment='#')
# print(f'Lets make sure we dont lose data when merging: initial length: {len(df)}')

# here is the data I'm building up for analysis, starting from _0, and _0_airpretreatments
df = pd.read_excel(rf'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\SECONDARIESONLY_FLASKLABELS.xlsx')
print(f'Lets make sure we dont lose data when merging: initial length: {len(df)}')

# does it contain duplicates? No! 
dupe_values = df[df.duplicated('TP', keep=False)]['TP'].unique()
print(dupe_values)

# I've found I can just grab some data from the AAA or cellulose treatment pages as a proxy to see if the process was complete, 
# and this can be how I filter on the data...
pretreat = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\FIRI_pretreatment_export.xlsx")
# are there duplicate values here? 
dupe_values = pretreat[pretreat.duplicated('TP', keep=False)]['TP'].unique()
print(f'Duplicates values are: {dupe_values}')
pretreat = pretreat.drop_duplicates(subset='TP') # drop the duplicates!
dupe_values = pretreat[pretreat.duplicated('TP', keep=False)]['TP'].unique()
print(f'Duplicates values are: {dupe_values}')

# now merge the data
df = df.merge(pretreat, on='TP', how='left')
df.to_excel(rf'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\SECONDARIESONLY_FLASKLABELS_FIRILABLES.xlsx')
print(f'Lets make sure we dont lose data when merging: final length: {len(df)}')



