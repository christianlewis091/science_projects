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

# steps to harmonize the dataset
# 1. Check what Rachel did. (see her page 203. It seems she just applied
# the offsets that she calculated and combined the datasets.

# 2. Load up all the data.

# 3. Index them according to the times above, and apply the offsets.

# 4. Merge the datasets into one.

# 5. Create a template of x-values to output

# (in the future, users can just add their samples x-values to this template and
# get the output they need to do subtraction)

# 6. Re-smooth the data using CCGCRV getTrendValues, with specific x's in mind
# (what x-values do I want to return that will be most useful?

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
heidelberg = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\heidelberg_cape_grim.xlsx', skiprows=40)
# Baring Head data excel file
baringhead = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
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
                                      'F14C', 'F14C_ERR', 'FLAG', 'METH_VESSEL',
                                      'METH_COLL'])

""" STEP 2: INDEX THE DATA ACCORDING TO TIMES LISTED ABOVE"""
# Baring head data does not need indexing because we will not apply corrections to it
# What are the current offsets (these are subject to change!)

# 1986 - 1991: Add 1.80 +- 0.18 to Heidelberg Data
# 1991 - 1994: Add 1.88 +- 0.16 to Heidelberg Data
# 1994 - 2006: No offset applied
# 2006 - 2009: Add 0.49 +- 0.07 to Heidelberg
# 2009 - 2012: Apply NO offset
# 2012 - 2016: Subtract 0.52 +- 0.06 to Heidelberg.

h1 = heidelberg.loc[(heidelberg['Decimal_date'] < 1991)].reset_index()
h2 = heidelberg.loc[(heidelberg['Decimal_date'] > 1991) & (heidelberg['Decimal_date'] < 1994)].reset_index()
h3 = heidelberg.loc[(heidelberg['Decimal_date'] > 1994) & (heidelberg['Decimal_date'] < 2006)].reset_index()
h4 = heidelberg.loc[(heidelberg['Decimal_date'] > 2006) & (heidelberg['Decimal_date'] < 2009)].reset_index()
h5 = heidelberg.loc[(heidelberg['Decimal_date'] > 2009) & (heidelberg['Decimal_date'] < 2012)].reset_index()
h6 = heidelberg.loc[(heidelberg['Decimal_date'] > 2012) & (heidelberg['Decimal_date'] < 2016)].reset_index()
"""
In order to apply the offsets, I'm going to add a new column with the new value, rather than try 
to change to original value
"""
offset1 = 1.80
offset2 = 1.88
offset3 = 0
offset4 = 0.49
offset5 = 0
offset6 = -.52
error1 = .18
error2 = .16
error3 = 0
error4 = 0.07
error5 = 0
error6 = 0.06

h1['D14C'] = h1['D14C'] + offset1
h2['D14C'] = h2['D14C'] + offset2
h3['D14C'] = h3['D14C'] + offset3
h4['D14C'] = h4['D14C'] + offset4
h5['D14C'] = h5['D14C'] + offset5
h6['D14C'] = h6['D14C'] + offset6
h1['weightedstderr_D14C'] = np.sqrt(h1['weightedstderr_D14C']**2 + error1**2) # propogate the error and REPLACE original
h2['weightedstderr_D14C'] = np.sqrt(h2['weightedstderr_D14C']**2 + error2**2)
h3['weightedstderr_D14C'] = np.sqrt(h3['weightedstderr_D14C']**2 + error3**2)
h4['weightedstderr_D14C'] = np.sqrt(h4['weightedstderr_D14C']**2 + error4**2)
h5['weightedstderr_D14C'] = np.sqrt(h5['weightedstderr_D14C']**2 + error5**2)
h6['weightedstderr_D14C'] = np.sqrt(h6['weightedstderr_D14C']**2 + error6**2)

""" STEP 4: MERGE ALL THE DATA! """

# TODO: need to change all the column names to be the same!
# for simplicity (and beacuse I'm indexing the Heidelberg dataset much
# more than the Baring Head dataset right now, I'm going to change the
# baringhead column names to match those of the Heidelberg dataset
# print(baringhead.columns)
# print(h1.columns)
# df2_dates = df2_dates.rename(columns={"NZ/NZA": "NZ"})
baringhead = baringhead.rename(columns={"DEC_DECAY_CORR": "Decimal_date"})
baringhead = baringhead.rename(columns={"DELTA14C": "D14C"})
baringhead = baringhead.rename(columns={"DELTA14C_ERR": "weightedstderr_D14C"})

harmonized = pd.merge(baringhead, h1, how='outer')
harmonized = pd.merge(harmonized, h2, how='outer')
harmonized = pd.merge(harmonized, h3, how='outer')
harmonized = pd.merge(harmonized, h4, how='outer')
harmonized = pd.merge(harmonized, h5, how='outer')
harmonized = pd.merge(harmonized, h6, how='outer')

harmonized.sort_values(by=['Decimal_date'], inplace=True)
harmonized.to_excel('harmonized_dataset.xlsx')
harm1 = harmonized.loc[(harmonized['key'] == 0)]
harm2 = harmonized.loc[(harmonized['key'] == 1)]
x_bars = harm1['Decimal_date']
y_bars = harm1['D14C']
x_heids = harm2['Decimal_date']
y_heids = harm2['D14C']


colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5
"""
Figure 1. All the data together
"""
fig = plt.figure(1)
plt.scatter(x_bars, y_bars, marker='o', label='Data from Baring Head (RRL)', color=colors[3], s=size1, alpha = 0.5)
plt.scatter(x_heids, y_heids, marker='o', label='Data from CGO (Heidelberg)', color=colors2[3], s=size1, alpha = 0.5)
plt.legend()
# plt.title('All available data after 1980')
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison2/interlab_comparison/plots/Harmonized_dataset.png',
            dpi=300, bbox_inches="tight")
plt.close()



