"""
Purpose:

This file merges and corrects Heidelberg group's Cape Grim data to GNS Baring Head data.
The corrections were calculated using heidelberg_intercomparison.py, although there is no explicit dependencies
between that file and this file. I just write the number in a certain part of the code below.
Currently, we are waiting to speak with collaborators before finalizing the corrections we will
use in THIS file.
However, the following code is ready to run once those final changes are made.

Outcome:

This file creates a new DataFrame that can be referenced in future analyses, such as the
SOAR tree ring analyses.

"""
#
import numpy as np
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import seaborn as sns
from miller_curve_algorithm import ccgFilter
from PyAstronomy import pyasl
from datetime import datetime
from my_functions import long_date_to_decimal_date

"""
Because I’ll need a harmonized dataset as a reference to understand the
tree-rings, I’m going to create a python file to do dataset harmonization.
I know we may change the corrections for the later half of the available
data; however, I can at least get the code ready so we can quickly
run it later and get the answer.
"""

# What are the current offsets (these are subject to change!)
# 1986 - 1991: Add 1.80 +- 0.18 to Heidelberg Data
# 1991 - 1994: Add 1.88 +- 0.16 to Heidelberg Data
# 1994 - 2006: No offset applied
# 2006 - 2009: Add 0.49 +- 0.07 to Heidelberg
# 2009 - 2012: Apply NO offset
# 2012 - 2016: Subtract 0.52 +- 0.06 to Heidelberg.
#
# # steps to harmonize the dataset
# # 1. Check what Rachel did. (see her page 203. It seems she just applied
# # the offsets that she calculated and combined the datasets.
#
# # 2. Load up all the data.
#
# # 3. Index them according to the times above, and apply the offsets.
#
# # 4. Merge the datasets into one.
#
# # 5. Create a template of x-values to output
#
# # (in the future, users can just add their samples x-values to this template and
# # get the output they need to do subtraction)
#
# # 6. Re-smooth the data using CCGCRV getTrendValues, with specific x's in mind
# # (what x-values do I want to return that will be most useful?
#
"""
#######################################################################
#######################################################################
#######################################################################
#######################################################################
EXECUTE THE ABOVE STEPS
#######################################################################
#######################################################################
#######################################################################
#######################################################################
"""
""" STEP 1: LOAD UP AND TIDY THE DATA"""
heidelberg = pd.read_excel(r'H:\The Science\Datasets'
                           r'\heidelberg_cape_grim.xlsx', skiprows=40)
print(heidelberg.columns)
# Baring Head data excel file
baringhead = pd.read_excel(r'H:\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')
# remove some of the columns that I dont want/need, to simplify the later merge
heidelberg['key'] = np.ones(len(heidelberg))
baringhead['key'] = np.zeros(len(baringhead))
# print(baringhead.columns)
# tidy up the data
# add decimal dates to DataFrame if not there already
x_init_heid = heidelberg['Average pf Start-date and enddate']  # x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)
heidelberg['Decimal_date'] = x_init_heid  # add these decimal dates onto the dataframe

# drop NaN's in the column I'm most interested in
heidelberg = heidelberg.dropna(subset=['D14C'])
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]
baringhead = baringhead.dropna(subset=['DELTA14C'])

# snip out 1995 - 2005, and 2009 - 2012
snip = baringhead.loc[(baringhead['DEC_DECAY_CORR'] < 1994)]
snip2 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2006) & (baringhead['DEC_DECAY_CORR'] < 2009)]
snip3 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2012)]
snip = pd.merge(snip, snip2, how='outer')
snip = pd.merge(snip, snip3, how='outer')
baringhead = snip.reset_index(drop=True)
# plt.scatter(baringhead['DEC_DECAY_CORR'], baringhead['DELTA14C'])
# plt.show()
# print(heidelberg.columns)
heidelberg = heidelberg.drop(columns=['#location', 'sampler_id', 'samplingheight', 'startdate', 'enddate',
                                      'Average pf Start-date and enddate', 'date_d_mm_yr', 'date_as_number',
                                      'samplingpattern',
                                      'wheightedanalyticalstdev_D14C', 'nbanalysis_D14C', 'd13C', 'flag_D14C',
                                      ], axis=1)
baringhead = baringhead.drop(columns=['SITE', 'NZPREFIX', 'NZ', 'DATE_ST', 'DATE_END', 'DAYS_EXP',
                                      'DATE_COLL', 'date_as_number', 'DELTA13C_IRMS',
                                      'FLAG', 'METH_VESSEL',
                                      'METH_COLL'])

# I realized that I was missing FM from the Heidelberg dataset, so I'm going to add that here...
# age_corr = exp((1950 - sample year)/8267)
# D14C = 1000*(FM-1)
# Del14C = 1000*(FM*age_corr-1)
# mt_array = []
# for i in range(0, len(heidelberg)):    # initialize for loop to the length of heidelberg dataset
#     row = heidelberg.iloc[i]           # grab the first row
#     row = np.array(row)                # change it to an array
#     date = row[3]
#     print(date)


x = heidelberg['Decimal_date']
y = heidelberg['D14C']
age_corr = np.exp((1950 - y) / 8267)
fm = ((y / 1000) + 1) / age_corr
fm_err = heidelberg['weightedstderr_D14C'] / 1000
x = np.float_(x)                                         # in order to create dictionary, first change briefly to array
fm = np.float_(fm)
new_frame = pd.DataFrame({"Decimal_date": x, "FM": fm, "FM_err": fm_err})  # create dictionary with common column to merge on.

heidelberg = pd.merge(heidelberg, new_frame, how = 'outer')  # merge the dataframes.
print(heidelberg.columns)







