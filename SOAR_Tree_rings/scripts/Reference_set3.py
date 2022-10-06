"""
Status Update to this file on October 6, 2022.

This file creates the third and final reference dataset for the SOAR Project Part 1, which can be seen in my handdrawn
schematic in my binder and latex document. It will add CGO data only into the gaps in the BHD record.

This script is quite similar to B_CGO_BHD_harmonization because I began this script by copying and editing that one.

"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from X_my_functions import long_date_to_decimal_date

""" LOAD UP AND TIDY THE DATA"""
# cape grim data
heidelberg = pd.read_excel(r'H:\Science\Datasets'
                           r'\heidelberg_cape_grim.xlsx', skiprows=40)
# Baring Head data excel file
baringhead = pd.read_excel(r'H:\Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')

# adding a key that can be useful later.
heidelberg['key'] = np.ones(len(heidelberg))
baringhead['key'] = np.zeros(len(baringhead))

# tidy up the data
# add decimal dates to DataFrame if not there already
x_init_heid = heidelberg['Average pf Start-date and enddate']  # x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)
heidelberg['Decimal_date'] = x_init_heid  # add these decimal dates onto the dataframe

# drop NaN's in the column I'm most interested in
heidelberg = heidelberg.dropna(subset=['D14C'])
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]
baringhead = baringhead.dropna(subset=['DELTA14C'])

# snip out the gaps: 1994 - 2006, and 2009 - 2012, and then merge back together
snip = baringhead.loc[(baringhead['DEC_DECAY_CORR'] < 1994)]
snip2 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2006) & (baringhead['DEC_DECAY_CORR'] < 2009)]
snip3 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2012)]
snip = pd.merge(snip, snip2, how='outer')
snip = pd.merge(snip, snip3, how='outer')
baringhead = snip.reset_index(drop=True)

cgo = heidelberg.loc[(heidelberg['Decimal_date'] > 1994) & (heidelberg['Decimal_date'] < 2006)]
cgo2 = heidelberg.loc[(heidelberg['Decimal_date'] > 2009) & (heidelberg['Decimal_date'] < 2012)]
cgo = pd.merge(cgo, cgo2, how='outer')

# drop some of the unnecessary columns that add clutter to the process
heidelberg = heidelberg.drop(columns=['#location', 'sampler_id', 'samplingheight', 'startdate', 'enddate',
                                      'Average pf Start-date and enddate', 'date_d_mm_yr', 'date_as_number',
                                      'samplingpattern',
                                      'wheightedanalyticalstdev_D14C', 'nbanalysis_D14C', 'd13C', 'flag_D14C',
                                      ], axis=1)
baringhead = baringhead.drop(columns=['SITE', 'NZPREFIX', 'NZ', 'DATE_ST', 'DATE_END', 'DAYS_EXP',
                                      'DATE_COLL', 'date_as_number', 'DELTA13C_IRMS',
                                      'F14C', 'F14C_ERR', 'FLAG', 'METH_VESSEL',
                                      'METH_COLL'])

# for simplicity (and because I'm indexing the Heidelberg dataset much more than the Baring Head dataset right now, I'm going to change the
# baringhead column names to match those of the Heidelberg dataset
baringhead = baringhead.rename(columns={"DEC_DECAY_CORR": "Decimal_date"})
baringhead = baringhead.rename(columns={"DELTA14C": "D14C"})
baringhead = baringhead.rename(columns={"DELTA14C_ERR": "weightedstderr_D14C"})

reference3 = pd.merge(baringhead, cgo, how='outer')
reference3.sort_values(by=['Decimal_date'], inplace=True)
reference3.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/reference3.xlsx')

