"""
Purpose:

We have two long-term record of 14C02 from the Southern Hemisphere (among some other shorter ones).
One is the Baring Head Record, from the GNS Rafter Radiocarbon Lab (measured by gas counting, then AMS)
Next is Ingeborg Levin and Sam Hammer's Tasmania Cape Grim CO2 record (measured by gas counting).
This script is meant to compare the differences between the datasets over time, to determine if
temporally consistent offsets exist, and if so, how to best correct them to create a harmonized background reference
dataset for future carbon cycle studies.

The script first imports and cleans the data, before using a CCGCRV Curve smoothing program to smooth through the data.
There is precedent for this procedure in the scientific literature following
https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JD094iD06p08549 (Thoning et al., 1989): use of the CCGCRV
https://acp.copernicus.org/articles/17/14771/2017/ (Turnbull et al., 2017): use of CCGCRV in the Baring Head Record
https://gml.noaa.gov/ccgg/mbl/crvfit/crvfit.html: NOAA details about the CCGCRV curve smoothing.

A Monte Carlo simulation is used to determine errors on the CCGCRV smoothing data. These errors are important because
we will need them for comparison with other carbon cycle datasets, of course.

The file outputs a text file with the t-test results. However, it will keep adding to the file, so if you want a fresh
one, delete the remaining text file from the directory.
"""

# TODO:  ADD / TEST AN ALREADY CODED T_TEST to SIMPLIFY MY LIFE AND HELP PROVIDE CONFIDENCE. FINISH FIXING MY_FINCTIONS FILE.
# from __future__ import print_function, division
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
from my_functions import monte_carlo_randomization_smooth
from my_functions import monte_carlo_randomization_trend
from scipy import stats

# general plot parameters
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

heidelberg = pd.read_excel(r'H:\The Science\Datasets\heidelberg_cape_grim.xlsx', skiprows=40)  # import heidelberg data
baringhead = pd.read_excel(r'H:\The Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')  # import Baring Head data
df2_dates = pd.read_excel(r'H:\The Science\Datasets\BHD_MeasurementDates.xlsx')  # CO2 measure date
extraction_dates = pd.read_excel(r'H:\The Science\Datasets\BHDFlasks_WithExtractionDates.xlsx')  # CO2 extract date

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

"""CAREFULLY SPLIT UP THE DATA INTO DIFFERENT TIME BINS AND GRAB VARIABLES """
""" 
Entire Baring Head File > 1980.
In this first time-indexing, we only care about values after 1980 because the earliest date from the Heidelberg 
group is 1987. For this comparison, we only care about the relevant, overlapping time periods. So we can ignore the
early periods, and early part of the bomb-spike. 
 """

baringhead = baringhead.loc[(baringhead['DELTA14C_ERR'] > 0)]  # get rid of data where the error flag is -1000
baringhead = baringhead.reset_index(drop=True)  # re-index to avoid gnarly errors

""" 
Entire Baring Head File > 1980, without 1995 - 2005. 
There is precedent for this indexing as well. In this period of time, GNS RRL switched to AMS measurements, and there 
was a significant period of anomalously high values. 
This was also highlighted in Section 3.3 of (Turnbull et al., 2017)
To accomplish this, I have to split the data into two, before 1994, and after 2006, and re-merge them. 
 """
snipmin = 1994  # was previously 1994
snipmax = 2006  # was previously 2006
snip = baringhead.loc[(baringhead['DEC_DECAY_CORR'] < snipmin)]  # index 1980 - 1994
snip2 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > snipmax)]  # index 2006 - end
snip = pd.merge(snip, snip2, how='outer')  # merge the files back together
snip = snip.reset_index(drop=True)  # reset the index to avoid gnarly errors

"""
RECORDS SPLIT UP INTO 5 PARTS (1987 - 1991, 1991 - 1994, 2006 - 2016, 2006 - 2009, 2012 - 2016)
Now, I'm indexing further into smaller time intervals. The later period is broken up from 2006 - 2009 and 2012 - 2016 
because there is another small issue with the data between 2009 - 2012. This can be observed by comparing the indexed
file baringhead_2006_2016 to the other indexed records.

Because these time bins are 3-4 year periods, I also decided to similarly split up the earlier times (1987 - 1994) 
in a similar way - although I could have left this time period whole. 
"""
baringhead_1986_1991 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 1987) & (baringhead['DEC_DECAY_CORR'] <= 1991)]
baringhead_1991_1994 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 1991) & (baringhead['DEC_DECAY_CORR'] <= 1994)]
baringhead_2006_2016 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2006) & (baringhead['DEC_DECAY_CORR'] <= 2016)]
baringhead_2006_2009 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 2006) & (baringhead['DEC_DECAY_CORR'] <= 2009)]
baringhead_2012_2016 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 2012) & (baringhead['DEC_DECAY_CORR'] <= 2016)]
baringhead_1986_1991 = baringhead_1986_1991.reset_index(drop=True)  # re-index to avoid gnarly errors
baringhead_1991_1994 = baringhead_1991_1994.reset_index(drop=True)  # re-index to avoid gnarly errors
baringhead_2006_2016 = baringhead_2006_2016.reset_index(drop=True)  # re-index to avoid gnarly errors
baringhead_2006_2009 = baringhead_2006_2009.reset_index(drop=True)  # re-index to avoid gnarly errors
baringhead_2012_2016 = baringhead_2012_2016.reset_index(drop=True)  # re-index to avoid gnarly errors

heidelberg_1986_1991 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1987) & (heidelberg['Decimal_date'] <= 1991)]
heidelberg_1991_1994 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1991) & (heidelberg['Decimal_date'] <= 1994)]
heidelberg_2006_2016 = heidelberg.loc[(heidelberg['Decimal_date'] > 2006)]  # BARINGHEAD2 will include the 2009-2011
heidelberg_2006_2009 = heidelberg.loc[(heidelberg['Decimal_date'] >= 2006) & (heidelberg['Decimal_date'] <= 2009)]
heidelberg_2012_2016 = heidelberg.loc[(heidelberg['Decimal_date'] >= 2012) & (heidelberg['Decimal_date'] <= 2016)]
heidelberg_1986_1991 = heidelberg_1986_1991.reset_index(drop=True)  # re-index to avoid gnarly errors
heidelberg_1991_1994 = heidelberg_1991_1994.reset_index(drop=True)  # re-index to avoid gnarly errors
heidelberg_2006_2016 = heidelberg_2006_2016.reset_index(drop=True)  # re-index to avoid gnarly errors
heidelberg_2006_2009 = heidelberg_2006_2009.reset_index(drop=True)  # re-index to avoid gnarly errors
heidelberg_2012_2016 = heidelberg_2012_2016.reset_index(drop=True)  # re-index to avoid gnarly errors

"""
After indexing into all these time-bins, now I have to extract all the x, y, and y-error variables from each and
every one of them. This region of the code could likely be vastly improved, although I don't know if there is a 
fast / easy way to get around this besides simply typing it out. 
"""
# BARING HEAD VARIABLES
xtot_bhd = baringhead['DEC_DECAY_CORR']  # entire dataset x-values
ytot_bhd = baringhead['DELTA14C']  # entire dataset y-values
ztot_bhd = baringhead['DELTA14C_ERR']  # entire dataset z-values


print(min(xtot_bhd))
print(max(xtot_bhd))
print(len(xtot_bhd))
print(min(x_init_heid))
print(max(x_init_heid))
print(len(x_init_heid))