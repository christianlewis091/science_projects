"""
This file is used to pre-process data that will compare measurements of the same SIO/LLNL with RRL.
This file doesn't do any math, it just cleans and re-packages the data into a Pandas DataFrame for later use.
"""

import pandas as pd
import numpy as np
from X_my_functions import long_date_to_decimal_date

# read in the data from the spreadsheets
llnl = pd.read_excel(r'H:\Science\Datasets\LLNLwheelcomparisons.xlsx',
                     sheet_name='Data', skiprows=24)
rrl = pd.read_excel(r'H:\Science\Datasets\NWT_FARI_RRL_2022-02-15.xlsx')
rrl = rrl.dropna(subset=['AMS Submission Results Complete::DELTA14C'])
# immediately slice off the following values from RRL data, Jocelyn deemed them not good, see excel sheet
rrl = rrl.iloc[0:202]
rrl = rrl.reset_index(drop=True)

# dealing with date formatting again...
# add some important columns
rrl['Site'] = 'RRL'
llnl['Site'] = 'LLNL'
llnl['standard_type'] = llnl['Comment']

rrl = rrl.drop(columns=['Samples::Sample Description',
                        'AMS Submission Results Complete::Collection Date', 'Unnamed: 6',
                        'AMS Submission Results Complete::Weight Initial',
                        'AMS Submission Results Complete::TP',
                        'AMS Submission Results Complete::TW',
                        'AMS Submission Results Complete::Quality Flag', 'Samples::Location',
                        'Unnamed: 19'])
rrl = rrl.rename(columns={'Samples::Sample ID':'standard_type',
                          'AMS Submission Results Complete::DELTA14C':'D14C',
                          'AMS Submission Results Complete::DELTA14C_Error':'D14C_err',
                          'AMS Submission Results Complete::Date Run':'Decimal_date',
                          'AMS Submission Results Complete::delta13C_IRMS':'IRMS_13C',
                          'AMS Submission Results Complete::delta13C_AMS':'AMS_13C',
                          'F14C':'FM',
                          'F14C_err':'FM_err'})
llnl = llnl.drop(columns=['Arbitrary_Sample_Number', 'Wheel', 'AMS_Lab', 'CURL', 'NSRL',
                          'Mass_C', 'Flag', 'Flag1', 'Flag2', 'Comment',
                          'Flag3', 'Uncertainty Using 1.8‰ and 2.7‰ as min error',
                          'All data (xi-xbar)2/s2', 'by wheel (xi-xbar)2/s2',
                          'All data (xi-xbar)2/s2.1', 'by wheel (xi-xbar)2/s2.1', 'Unnamed: 23',
                          'Unnamed: 24', 'Unnamed: 25', 'Unnamed: 26', 'Unnamed: 27',
                          'Unnamed: 28', 'Unnamed: 29', 'Unnamed: 30'])


rrl_date = rrl['Decimal_date']  # extract x-values from heidelberg dataset
rrl_date = long_date_to_decimal_date(rrl_date)  # convert the x-values to a decimal date
rrl['Decimal_date'] = rrl_date  # add these decimal dates onto the dataframe
llnl['Decimal_date'] = list(range(0, len(llnl)))
llnl = llnl.rename(columns={'Fm':'FM', 'Fm_err':'FM_err','D14C_Err':'D14C_err'})
print(len(llnl))
combine_SIO = pd.concat([rrl, llnl])
combine_SIO = combine_SIO.loc[(combine_SIO['standard_type'] == 'NWT3') | (combine_SIO['standard_type'] == 'NWT4')]

# combined SIO needs a x-data for the LLNL, so I'm just going to add a linspace to it.
# DONE!

