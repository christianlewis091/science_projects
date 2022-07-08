"""
This file is used to pre-process data that will compare measurements of the same Heidelberg / GNS
This file doesn't do any math, it just cleans and re-packages the data into a Pandas DataFrame for later use.
"""

import pandas as pd
import numpy as np
from X_my_functions import long_date_to_decimal_date, d14C_to_fm

heidelberg = pd.read_excel(r'H:\The Science\Datasets\heidelberg_cape_grim.xlsx', skiprows=40)  # import heidelberg data
baringhead = pd.read_excel(r'H:\The Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')  # import Baring Head data

""" TIDY UP THE DATA FILES"""
""" 
Some of the "Date formatting" can be quite tricky. The first step in cleaning the data is to convert
long-format dates to decimal dates that can be used in the CCGCRV curve smoothing algorithm. This is done using a 
function I wrote and lives in my_functions.py.
"""
x_init_heid = heidelberg['Average pf Start-date and enddate']  # extract x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)  # convert the x-values to a decimal date
heidelberg['Decimal_date'] = x_init_heid  # add these decimal dates onto the dataframe
heidelberg = heidelberg.dropna(subset=['D14C'])  # drop NaN's in the column I'm most interested in
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]  # Filtering out an outlier around 2019

heidelberg.reset_index()  # reset the index to avoid heaps of gnarly errors
baringhead = baringhead.dropna(subset=['DELTA14C'])  # drop NaN's in the column I'm most interested in
baringhead = baringhead.loc[(baringhead['DELTA14C_ERR'] > -999)]  # Filtering out data with uncertainties of -1000

heidelberg = heidelberg.drop(columns=['sampler_id', 'samplingheight', 'startdate', 'enddate',
                                      'Average pf Start-date and enddate', 'date_d_mm_yr', 'date_as_number',
                                      'samplingpattern',
                                      'wheightedanalyticalstdev_D14C', 'nbanalysis_D14C', 'd13C', 'flag_D14C',
                                      ])

heidelberg = heidelberg.rename(columns = {'#location':'Site', 'weightedstderr_D14C':'D14C_err'})

fm = d14C_to_fm(heidelberg['D14C'], heidelberg['D14C_err'], heidelberg['Decimal_date'])
fm_out = fm[0]
fm_err_out = fm[1]
heidelberg['FM'] = fm_out
heidelberg['FM_err'] = fm_err_out


baringhead = baringhead.drop(columns=['NZPREFIX', 'NZ', 'DATE_ST', 'DATE_END', 'DAYS_EXP',
                                      'DATE_COLL', 'date_as_number', 'DELTA13C_IRMS',
                                       'METH_VESSEL'])


baringhead = baringhead.rename(columns = {'SITE':'Site', 'DEC_DECAY_CORR':'Decimal_date', 'DELTA14C':'D14C', 'DELTA14C_ERR':'D14C_err', 'F14C':'FM',
                                          'F14C_ERR':'FM_err'})

baringhead['Site'] = 'BHD'
combine_heidelberg = pd.concat([heidelberg, baringhead])
