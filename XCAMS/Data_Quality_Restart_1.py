"""
Restarting with a fresh script after I realized that my filtering method for quality flags was too simply and failed,
but I had already manually checked so many TPs, I'd need to restart in order to do things properly while still using
the data I'd manually checked.
"""
# IMPORT STATEMENTS
import pandas as pd

# READ IN THE MAIN, ENTIRE DATA
df = pd.read_csv(r'H:\Science\Datasets\Alberts_dataquality\FINAL_WORKING_DATASET.csv')
original_length = len(df)

# IN THE PAST ITERATION/WORK ON THE DATA QUALITY STUFF, I MANUALLY CHECKED A TON OF TP'S.
# I DON'T WANT THAT WORK TO BE LOST, SO I'LL IMPORT THE LIST OF TP'S THAT I FLAGGED FOR REMOVAL HERE...
# See Data_Quality_paper_1.py
df1 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/SoftFlags_REIMPORT.xlsx', comment='#')
df1 = df1[['TP','Job::Job notes','Keep_Remove']]
df1['Comment'] = 'Keep/Remove added after manual checking during export of "Soft Flag" batch in Data_Quality_Paper1.py June 10, 2024'

df2 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/NoFlags_needsManCheck_DONE.xlsx')
df2 = df2[['TP','Job::Job notes','Keep_Remove']]
df2['Comment'] = 'Keep/Remove added after manual checking during export of "No Flag" batch in Data_Quality_Paper1.py June 10, 2024'

df3 = pd.concat([df1, df2])
df3 = df3[['TP','Keep_Remove','Comment']]

df = df.merge(df3, on='TP', how='outer')
df.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Restart_1_output/test.xlsx')
yet_to = df[df['Comment'].isna() | (df['Comment'] == '')]
# The rest of the data that I haven't manually checked can be dealt with as I was doing in Data_Quality_Paper_1.py

"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
The abundance of different types of flags
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""

print('Summary Below')
print(f'The original length of the data is {original_length}. Keep/Remove has been added to {original_length-len(yet_to)} rows based on prior work.')







