"""
As we make version 6 in order to add data up to the present, 
It means I need to re-do a lot of work where I add labels to firi and oxalic pretreatments. 
For instance, I download all of RLIMS but there is no more BHDamb and BHDspike than my original analysis? Its likely because there haven't had FLASK oxalic pretreatments added, and they're getting cut
I need to make sure the data is all clean and no weird stuff is happening before I feed it into the scripts for flagging, note-taking (_1) and analysis (_2)
"""
import pandas as pd
import numpy as np

# LIST OF R NUMBERS FOR SECONDARIES AND BLANKS
seconds = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\seconds_April3_2026.xlsx", sheet_name='new', comment='#')
rs_of_secondaries_and_blanks = np.unique(seconds['Job::R'])

""""
Here is the original file I used for version 1-5 of the data quality paper work.
Lets just broadly check that the new export has a lot more data that we're interested in, than the old export (it should!)
"""
df = pd.read_csv(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\FINAL_WORKING_DATASET.csv")
df = df.dropna(subset='F_corrected_normed') # get rid of rows where there's no data! 
df = df.loc[df['Job::R'].isin(rs_of_secondaries_and_blanks)]
summary_V0to5 = df.groupby('Job::R').size().reset_index(name='V0to5')

df_new = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\new_full_export_may25_2026.xlsx")
df_new = df_new.dropna(subset='F_corrected_normed') # get rid of rows where there's no data! 
df_new = df_new.loc[df_new['F_corrected_normed'] != 0] # rows where there's no data is showing up as FM is 0 
# are there duplicate values here? 
dupe_values = df_new[df_new.duplicated('TP', keep=False)]['TP'].unique()
print(f'Duplicates values are: {dupe_values}')
df_new = df_new.drop_duplicates(subset='TP') # drop the duplicates!
dupe_values = df_new[df_new.duplicated('TP', keep=False)]['TP'].unique()
print(f'Duplicates values are: {dupe_values}')

df_new = df_new.loc[df_new['Job::R'].isin(rs_of_secondaries_and_blanks)]
summary_V6 = df_new.groupby('Job::R').size().reset_index(name='V6')
df_new.to_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\new_export_SECONDARIESONLY.xlsx")
print(len(df_new))

summary = summary_V0to5.merge(summary_V6, on='Job::R', how='outer').fillna(0)
print(summary)

"""
OK so now we can build a little summary of the differences in data between versions 0-5 and versions 6
"""
# grab some summary numbers
v05_minTP = np.min(df['TP'])
v05_maxTP = np.max(df['TP'])
v05_minTW = np.min(df['TW'])
v05_maxTW = np.max(df['TW'])

print(f'The original dataset, in versions 0-5 included TPs{v05_minTP} to {v05_maxTP}, and wheels {v05_minTW} to {v05_maxTW}.')

# grab some summary numbers
v05_minTP = np.min(df_new['TP'])
v05_maxTP = np.max(df_new['TP'])
v05_minTW = np.min(df_new['TW'])
v05_maxTW = np.max(df_new['TW'])

print(f'The NEW dataset, in version 6 includes TPs{v05_minTP} to {v05_maxTP}, and wheels {v05_minTW} to {v05_maxTW}.')