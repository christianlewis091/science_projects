"""
This file is used to pre-process data that will compare measurements of the same Uni Magallanes with RRL.
This file doesn't do any math, it just cleans and re-packages the data into a Pandas DataFrame for later use.
"""

import numpy as np
import pandas as pd

# read in our data from SOAR and Magallanes
df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\SOARTreeRingData_CBL_cleaned.xlsx')  # read in the Tree Ring data that already has flagged data removed
df = df.dropna(subset='∆14C').reset_index(drop=True)  # drop any data rows that doesn't have 14C data.
df = df.loc[(df['Site'] == 'Monte Tarn, Punta Arenas')]
df['Site'] = 'RRL'

df2 = pd.read_excel(r'H:\The Science\Datasets\Jocelyn Chile tree data 1980-2016.xlsx')
df2 = df2.loc[(df2['Sheet']) == 4]  # grab the data from Monte Tarn ONLY
df2['Decimal_date'] = np.float64(df2['Year of Growth'])  # add a new date column in the form of float.
df2['Site'] = 'Magallanes'
# I'm going to remove all the columns I don't want and put them in a new order:
df = df.drop(columns=['Unnamed: 0', 'Ring code', 'R number',
                        'Date',  'C14Flag', 'C14 comment',
                        'Elevation', 'Lat', 'Lon', 'CBL_flag'])
df = df.rename(columns = {"DecimalDate": "Decimal_date", "∆14C":"D14C", "∆14Cerr":"D14C_err", "F14C":"FM","F14Cerr":"FM_err"})

df2 = df2.drop(columns=['Sample name', 'Sheet', 'Year of Growth'])
df2 = df2.rename(columns = {"D14Cerr":"D14C_err", "Fmerr":"FM_err"})

# Currently, I want to get only the data where they overlap in date...and I need to remove the decimal points from
# RRL data
array = []
for i in range(0, len(df)):
    row = df.iloc[i]           # grab the first row
    date = row['Decimal_date']  # grab the DecimalDate
    date = str(date)           # convert it to a string
    date = date[0:4]           # grab the first 4 digits
    date = np.float64(date)    # convert back to float64
    array.append(date)

df['Decimal_date'] = array

array = []
for i in range(0, len(df2)):
    row = df2.iloc[i]           # grab the first row
    date = row['Decimal_date']  # grab the DecimalDate
    date = str(date)           # convert it to a string
    date = date[0:4]           # grab the first 4 digits
    date = np.float64(date)    # convert back to float64
    array.append(date)

df2['Decimal_date'] = array


combine_Magallanes = pd.merge(df, df2, how='outer')
combine_Magallanes.to_excel('test.xlsx')


