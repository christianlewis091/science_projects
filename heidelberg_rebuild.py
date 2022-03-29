from __future__ import print_function, division
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from miller_curve_algorithm import ccgFilter
from PyAstronomy import pyasl
import math
from my_functions import year_month_todecimaldate, \
    long_date_to_decimal_date, \
    monte_carlo_randomization, \
    two_tail_paired_t_test, \
    monthly_averages

"""
To simplify this code, I'm put all the functions I'll use in my file my_functions.py. 

In this version of the code, I'm going to try to build it so the code can be used 
to compare any two datasets, not exclusively these two. 

"""
"""
Import and tidy your data
"""

df1 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\heidelberg_cape_grim.xlsx', skiprows=40)

df2 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\BHD_14CO2_datasets_20211013.xlsx')
df2_dates = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                          r'\BHD_MeasurementDates.xlsx')

# tidy up the file(s).
df1 = df1.dropna(subset=['D14C'])  # drop NaN's in column I'm most interested in
df1 = df1.loc[(df1['D14C'] > 10)]  # filter out an outlying measurement in 2019
df1 = df1.reset_index()
x = df1['date_d_mm_yr']  # grab the x-values in the long-date format
x = long_date_to_decimal_date(x)  # convert them to decimal dates using my code
df1['Decimal_date'] = x  # attach this new column onto the DataFrame

# merge Baring Head datafile with the "measurement times" data file (how long were flasks sitting around?)
df2 = df2.drop(columns=['SITE', 'DATE_ST', 'DATE_END', 'DAYS_EXP',
                        'DATE_COLL', 'date_as_number', 'FLAG'], axis=1)
df2_dates = df2_dates.drop(columns=['∆14C', '∆14C_err',
                                    'Flag', 'CollectionMethod'], axis=1)

# will drop all columns in df2_dates where we don't have DateMeasured data.
df2_dates = df2_dates.dropna(subset=['DateMeasured'])
df2_dates = df2_dates.reset_index()
# need to make DateCollected and DateMeasured the same format or it won't work.
forchange = df2_dates['DateMeasured']
forchange = long_date_to_decimal_date(forchange)
df2_dates['DateMeasured_Decimal'] = forchange

df2_dates['difference'] = df2_dates['DateMeasured_Decimal'] - np.float64(df2_dates['DecimalDateCollected'])
df2_dates = df2_dates.rename(columns={"NZ/NZA": "NZ"})
df2_dates = df2_dates.drop(columns=['index', 'DecimalDateCollected', 'DateMeasured',
                                    'DateMeasured_Decimal'], axis=1)
print(df2.columns)
print(df2_dates.columns)











# difference = []
# test = 2009.534 - 2007.8
# print(test)
# print()
# for i in range(0, len(x1)):
#     x1_i = x1[i]
#     x2_i = x2[i]
#     print(type(x1_i))
#     print(type(x2_i))
#     x3 = x1_i - x2_i
#     difference.append(x3)
# print(difference)



# df2_dates['Delta_Collection_Measured'] = list(df2_dates['DateMeasured_Decimal']) - list(df2_dates['DecimalDateCollected'])
# print(df2_dates)



# print(df2.head(5))
# print(df2_dates.head(5))
# # rename columns from df2_dates so it matches df2 if the data is identical
# df2_dates.rename(columns = {"DecimalDateCollected": "DEC_DECAY_CORR",
#                             "NZ/NZA": "NZ",
#                             "∆14C":"D14C_dates_file"})
#
# df2_dates = df2_dates.dropna(subset=['DateMeasured'])
# df2_dates.reset_index()
# x2 = df2_dates['DateMeasured']  # grab the x-values in the long-date format
# x2 = long_date_to_decimal_date(x2)  # convert them to decimal dates using my code
# df2_dates['DateMeasured_Decimal'] = x2  # attach this new column onto the DataFrame
#
#


# print(df2_dates)


# # rename / add a new column which shares a name with DataFrame df2_dates, so I can merge them properly.
# df2['DecimalDateCollected'] = df2['DEC_DECAY_CORR']
# df2 = pd.merge(df2, df2_dates)
# df2.to_excel('testing.xlsx')  # check that the column addition worked

# df2 = df2.dropna(subset=['DELTA14C'])  # drop NaN's in column I'm most interested in
# df2 = df2.loc[(df2['DEC_DECAY_CORR'] > 1980)]  # only take data after the bomb peak.
# df2 = df2.loc[(df2['DELTA14C_ERR'] > 0)]  # this line gets rid of flags at -1000 or -999
#
#
#
#
# df2 = df2.reset_index()

# split the files up into different time-chunks that I'll be using.
# first order of business: if we're doing an intercomparison, filter both of the datafiles
# so that data only exists within the boundaries of the other dataset. For example, in this case,
# the Baring Head record extends further in time before and after the Heidelberg dataset.
# Filter the Baring Head record so it only appears after the min and before the max of
# the Heidelberg data

# # df2 = df2.loc[(df2['DEC_DECAY_CORR'] > heidelberg min date) & (df2['DEC_DECAY_CORR'] < heidelberg max date)]
# df2_original = df2  # before the next time, I want to save the un-filtered dataset as something.
# df2 = df2.loc[(df2['DEC_DECAY_CORR'] > min(df1['Decimal_date'])) & (df2['DEC_DECAY_CORR'] < max(df1['Decimal_date']))]
