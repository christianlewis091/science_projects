"""
Which airs have flask pretreatment?

I did this before in the main analysis. 
But now that we're adding more data and I need to re-do it (to add more new data into the present), I'm going to put it in the front so its cleaner! 
"""

import pandas as pd
import numpy as np

# See Data_Quality_Paper_0.py
df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\new_export_SECONDARIESONLY.xlsx")
print(f'Lets make sure we dont lose data when merging: initial length: {len(df)}')

# Grab the pretreatment type
spt = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\AirMaterial_PrepType.xlsx")

# there are some missing potentially due to historical TW re-use bugs. So I'll add them back in
toadd = [91080,83519,83520,83521,91043, 91048,91070,91112,91201,91200]
spt.loc[spt['TP'].isin(toadd), 'AMS Timetable From Results::Standard Prep Type'] = 'FLASK'

spt = spt.drop_duplicates(subset='TP', keep='first') # get rid of duplicates on the prep type output from RLIMS
df = df.merge(spt, on='TP', how='left')
print(f'Lets make sure we dont lose data when merging: final length: {len(df)}')

df.to_excel(rf'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\SECONDARIESONLY_FLASKLABELS.xlsx')
# experiencing some confusion based on the flask stuff.
# I've filtered for flasks only below but I'm still getting data for pre-TW3010 when flasks were introduced. The reason this is confusion is because, while I'm taking flask-only data for the statistical group calculations,
# The EA and ST ones are still left in the database presented at the end. This can be confusinng for someone who looks in there and sees ST or EA.


