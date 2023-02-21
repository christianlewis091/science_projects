import pandas as pd
import numpy as np

# import and clean the raw data
# df = pd.read_csv('H:\Science\Datasets\simplified_RLIMS_dataset.csv').replace('Missing[]', '-999')
#
# # isolate only the sample columns I'm interested in
# df = df[['TW','TP','R','job','NZA','client','sampleID','sampleTYPE','AMScateg','AMScategID','sampleFRAC','servTYPE','CALCcateg','daysAsGrap',
#          'RTSmode','RTS','RTSerr','RTSB','RTSBerr','FracMOD','FracMODerr','CRA','CRAerr','MCC','MCCerr','DCC','DCCerr','DEL14C','DEL14Cerr','del13Cams','del13Csil1']]
#
# df.to_csv('H:\Science\Datasets\simplified_RLIMS_dataset_cleaned_CBL.csv')

# write a function for quality flagging
def quality_flag_1(df):

    arr = []
    arr2 = []
    for i in range(0, len(df)):
        row = df.iloc[i]

        if row['RTSmode'].astype(float) != 5:
            arr.append('X')
            arr2.append('Wrong analysis mode')

        else:
            arr.append('-999')
            arr2.append('-999')

    df['CBL Flag'] = arr
    df['CBL Flag Note'] = arr2



    return df

# open the file I wrote from the few lines of cleaning above...
df1 = pd.read_csv('H:\Science\Datasets\simplified_RLIMS_dataset_cleaned_CBL.csv')

# initialize a column where I can apply data flags, and a column where I can write notes about those flags
df1['CBL Flag'] = -999
df1['CBL Flag Note'] = -999

# run the data quality function
df1 = quality_flag_1(df1)
print(df1)
print(np.unique(df1['CBL Flag Note']))
