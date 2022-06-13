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

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from X_my_functions import long_date_to_decimal_date
from A_heidelberg_intercomparison import offset1, offset2, offset3, offset4, offset5, offset6
from A_heidelberg_intercomparison import error1, error2, error3, error4, error5, error6
from A_heidelberg_intercomparison import dff  # import the dataframe to produce the smoothed offset calcs
from A_heidelberg_intercomparison import cutoff
from X_miller_curve_algorithm import ccgFilter
from X_my_functions import monte_carlo_randomization_trend

"""
Because I’ll need a harmonized dataset as a reference to understand the
tree-rings, I’m going to create a python file to do dataset harmonization.
I know we may change the corrections for the later half of the available
data; however, I can at least get the code ready so we can quickly
run it later and get the answer.
"""

# What are the current offsets (these are subject to change!)
# See End of Heidelberg_intercomparison.py
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
x = heidelberg['Decimal_date']
y = heidelberg['D14C']
age_corr = np.exp((1950 - x) / 8267)
fm = ((y / 1000) + 1) / age_corr
fm_err = heidelberg['weightedstderr_D14C'] / 1000
x = np.float_(x)                                         # in order to create dictionary, first change briefly to array
fm = np.float_(fm)
new_frame = pd.DataFrame({"Decimal_date": x, "F14C": fm, "F14C_ERR": fm_err})  # create dictionary with common column to merge on.

heidelberg = pd.merge(heidelberg, new_frame, how = 'outer')  # merge the dataframes.

""" 
STEP 2: INDEX THE DATA ACCORDING TO TIMES LISTED ABOVE
index 1 = "h1" for heidelberg-1, and so on. 
h1 = 1986 - 1991
h2 = 1991 - 1994
h3 = 1994 - 2006
h4 = 2006 - 2009
h5 = 2009 - 2012
h6 = 2012 - 2016
"""
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
# apply offsets using Pre and POst AMS OFFset
h1['D14C_1'] = h1['D14C'] + offset1  # store offset values in new column
h2['D14C_1'] = h2['D14C'] + offset2
h3['D14C_1'] = h3['D14C'] + offset3
h4['D14C_1'] = h4['D14C'] + offset4
h5['D14C_1'] = h5['D14C'] + offset5
h6['D14C_1'] = h6['D14C'] + offset6
h1['weightedstderr_D14C_1'] = np.sqrt(h1['weightedstderr_D14C']**2 + error1**2)  # propogate the error and REPLACE original
h2['weightedstderr_D14C_1'] = np.sqrt(h2['weightedstderr_D14C']**2 + error2**2)
h3['weightedstderr_D14C_1'] = np.sqrt(h3['weightedstderr_D14C']**2 + error3**2)
h4['weightedstderr_D14C_1'] = np.sqrt(h4['weightedstderr_D14C']**2 + error4**2)
h5['weightedstderr_D14C_1'] = np.sqrt(h5['weightedstderr_D14C']**2 + error5**2)
h6['weightedstderr_D14C_1'] = np.sqrt(h6['weightedstderr_D14C']**2 + error6**2)

# merge heidelberg file back onto itself, after adding the first TYPE of offset...
heidelberg = pd.merge(h1, h2, how='outer')
heidelberg = pd.merge(heidelberg, h3, how='outer')
heidelberg = pd.merge(heidelberg, h4, how='outer')
heidelberg = pd.merge(heidelberg, h5, how='outer')
heidelberg = pd.merge(heidelberg, h6, how='outer')

# APPLY OFFSET USING SMOOTHED OFFSET
# template_array = ccgFilter(x_init, new_array[0], cutoff).getSmoothValue(fake_x)
offset_smoothed = monte_carlo_randomization_trend(dff['offset_xs'], heidelberg['Decimal_date'], dff['offset_ys'], dff['offset_errs'], cutoff, 100)
offset_smoothed_summary = offset_smoothed[2]
offset_smoothed_mean = offset_smoothed_summary['Means']
offset_smoothed_stdevs = offset_smoothed_summary['stdevs']
heidelberg['D14C_2'] = heidelberg['D14C'] + offset_smoothed_mean
heidelberg['weightedstderr_D14C_2'] = np.sqrt(heidelberg['weightedstderr_D14C']**2 + offset_smoothed_summary['stdevs']**2)
heidelberg.to_excel('CapeGrim_offset.xlsx')




""" STEP 4: MERGE OFFSET CORRECTED CAPE GRIM DATA WITH BARING HEAD RECORD TO MAKE HARMONIZED BACKGROUND """
# for simplicity (and because I'm indexing the Heidelberg dataset much
# more than the Baring Head dataset right now, I'm going to change the
# baringhead column names to match those of the Heidelberg dataset
# print(baringhead.columns)
# print(h1.columns)
# df2_dates = df2_dates.rename(columns={"NZ/NZA": "NZ"})
baringhead = baringhead.rename(columns={"DEC_DECAY_CORR": "Decimal_date"})
baringhead = baringhead.rename(columns={"DELTA14C": "D14C"})
baringhead = baringhead.rename(columns={"DELTA14C_ERR": "weightedstderr_D14C"})

harmonized = pd.merge(baringhead, h1, how='outer')  # have to merge in stages but it's all good.
harmonized = pd.merge(harmonized, h2, how='outer')
harmonized = pd.merge(harmonized, h3, how='outer')
harmonized = pd.merge(harmonized, h4, how='outer')
harmonized = pd.merge(harmonized, h5, how='outer')
harmonized = pd.merge(harmonized, h6, how='outer')




"""
A few of the data have errors of -1000 and this is throwing everything off
in later calculations...
I need to get rid of these...
"""
harmonized = harmonized.loc[(harmonized['weightedstderr_D14C'] > 0)]
harmonized = harmonized.drop(columns=['index'], axis=1)
harmonized = harmonized.dropna()
harmonized.sort_values(by=['Decimal_date'], inplace=True)
# harmonized.to_excel('harmonized_dataset.xlsx')
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
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Harmonized_dataset.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
In Rachel's thesis, she talks about comparing the tree-ring values to the BHD data, but only using the data from the
growing season, which is November to February. The following code slices the harmonized data to ONLY INCLUDE data from 
during the growing season. While this code took ~ 1 hour to write, I don't know how to get from here to a yearly 
average because the SH summer crosses the year-line (January). Can come back to this later. 
The following code retains only the summer months. 
"""

L = np.linspace(0, 1, 365)
# add the number that is 1/2 of the previous month plus the current month
Jan = 31 / 365
Feb = ((28 / 2) + 31) / 365
Mar = ((31 / 2) + 31 + 28) / 365
Apr = ((30 / 2) + 31 + 28 + 31)/ 365
May = ((31 / 2) + 31 + 28 + 31 + 30)/ 365
June = ((30 / 2) + 31 + 28 + 31 + 30 + 31)/ 365
July = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30)/ 365
August = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31)/ 365
Sep = ((30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31)/ 365
Oct = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30)/ 365
Nov = ((30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30)/ 365
Dec = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30 + 30)/ 365
# print(Nov)
# print(Dec)
# print(Jan)
# print(Feb)
# harmonized['Summer_index'] = harmonized['Decimal_date']  # makes a copy of the DecimalDate column
mt_array = []                                    # initialize an empty array to dump sliced date-data
harmonized = harmonized.reset_index(drop=True)   # re-index the harmonized dataset to avoid confusion
for i in range(0, len(harmonized)):
    row = harmonized.iloc[i]                     # grab i'th row
    element = row['Decimal_date']                # extract the date
    element = str(element)                       # convert to a string so it is indexable
    element = element[4:9:1]                     # index the decimal portion
    element = np.float_(element)                 # convert back to float for indexing a few lines later
    mt_array.append(element)                     # append to the new array
indexed = pd.DataFrame({"decimals": mt_array, "Decimal_date": harmonized['Decimal_date']})                 # put the array into a DataFrame format

harmonized_summer = pd.merge(harmonized, indexed)   # merge the datasets

# print(harmonized_summer)
harmonized_summer = harmonized_summer.loc[((harmonized_summer['decimals']) < .124) | ((harmonized_summer['decimals']) > .870)]   # grab data only in the months that I want
# harmonized_summer.to_excel('test.xlsx')
# print(harmonized.columns)
# print(harmonized_summer.columns)
# test the dates fall into the bounds that I want using a histogram
x = harmonized_summer['decimals']
plt.hist(x, bins=12)
# plt.show()
#
plt.close()
# plt.scatter(harmonized['Decimal_date'], harmonized['F14C'])
# plt.show()

