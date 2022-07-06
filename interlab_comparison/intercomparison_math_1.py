import numpy as np
import pandas as pd
from scipy import stats
# import the data from the "Pre-Processing" files:
from Pre_Processing_ANSTO import combine_ANSTO
from Pre_Processing_Heidelberg import combine_heidelberg
from Pre_Processing_UniMagallanes import combine_Magallanes
from Pre_Processing_SIO_LLNL import combine_SIO
from tabulate import tabulate

"""
This file uses PRE-CLEANED data from the following institutions, 
and compares them to RRL using the specified type of data:
ANSTO: Tree Rings
SIO/LLNL: Standard Materials NWT3 and NWT4
University of Magallanes: Tree Rings
University of Heidelberg: Atmospheric CO2 measurements. 
The null hypothesis for the following t-tests is: "There is NO systematic bias between institutions". If p-values 
come out less than 0.01, or 1%, or 98% confidence interval, I call that they are significantly different. 

FOR INTERCOMPARISONS, USE FM WHERE POSSIBLE

All data visualizations will appear in another .py file. 

First I'm going to just index the data I need for the t-tests for ANSTO, SIO/LLNL (NWT3 and NWT4) and Magallanes. 
"""

ansto = combine_ANSTO.loc[(combine_ANSTO['Site'] == 'ANSTO')].reset_index(drop=True)
rrl = combine_ANSTO.loc[(combine_ANSTO['Site'] == 'RRL')].reset_index(drop=True)

NWT3 = combine_SIO.loc[(combine_SIO['standard_type'] == 'NWT3')]
sio_nwt3 = NWT3.loc[(NWT3['Site'] == 'LLNL')]
rrl_nwt3 = NWT3.loc[(NWT3['Site'] == 'RRL')]

NWT4 = combine_SIO.loc[(combine_SIO['standard_type'] == 'NWT4')]
sio_nwt4 = NWT4.loc[(NWT4['Site'] == 'LLNL')]
rrl_nwt4 = NWT4.loc[(NWT4['Site'] == 'RRL')]

# Magallanes data is setup slightly different, take a look at the data to see why it is indexed this way -
# perhaps it is so only beccause I'm a novice coder...
rafter = combine_Magallanes['FM_x']
magallanes = combine_Magallanes['FM_y']

"""
Writing a quick function to save myself a few lines here...
arguements: 

Data 1, Data2: input the data you want to compare from pandas dataframe format. 
Test_name: "This is the thing I'm testing" (input as a string!)
test_type: options are 'paired' or 'not-paired'. Use 'paired' only if there are same length of points, such as two
           exact time series
        
"""

def intercomparison_ttest(data1, data2, test_name, test_type):
    print(str(test_name))  # Print the name of the thing we're comparing
    if test_type == 'paired':  # set the type of t-test
        result = stats.ttest_rel(data1, data2)  # paired t-test result
        difference = np.subtract(data1, data2)  # subtract the data from each other
        mean1 = np.average(difference)  # find the mean of the difference between the datasets
        standard_error = np.std(difference) / np.sqrt(len(difference))  # standard error of the subtraction array
        print('The average difference between the groups is ' + str(mean1))

    elif test_type == 'not-paired':
        result = stats.ttest_ind(data1, data2)
        avg1 = np.average(data1)  # compute "metadata" (wrong term maybe)?
        std1 = np.std(data1)  # compute standard deviation
        stderr1 = std1 / np.sqrt(len(data1))  # compute standard error
        avg2 = np.average(data2)
        std2 = np.std(data2)
        stderr2 = std2 / np.sqrt(len(data2))
        offset = avg1 - avg2  # compute the offset between the means of the two datasets
        error_prop = (np.sqrt(stderr1 ** 2 + stderr2 ** 2))  # propagate the error

    print(result)  # Print the t-test result
    if result[1] < 0.01:  # if statement for me to print if they are different
        print("The data are different at 98% confidence")
    else:
        print("The data are not different")
    print('\n' * 1)  # print some blank lines
    return result


# I was first supplied with FM data from ANSTO so I'm going to use FM for this calculation.
a = intercomparison_ttest(ansto['D14C'], rrl['D14C'], 'ANSTO v RRL Test: Tree Rings, D14C', 'paired')
a = intercomparison_ttest(ansto['FM'], rrl['FM'], 'ANSTO v RRL Test: Tree Rings, FM', 'paired')

# I'll do this one in FM as well because it minimizes the amount of extra calculatinos
# that can lead to fake systematic bias.
b = intercomparison_ttest(sio_nwt3['FM'], rrl_nwt3['FM'], 'SIO/LLNL v RRL, NWT3 Intercomparison', 'not-paired')
c = intercomparison_ttest(sio_nwt4['FM'], rrl_nwt4['FM'], 'SIO/LLNL v RRL, NWT3 Intercomparison', 'not-paired')

d = intercomparison_ttest(rafter, magallanes, 'Magallanes v RRL Test: Tree Rings', 'paired')

"""
Now to tackle the intercomparison between Heidelberg and Rafter, which will be done using atmospheric time series 
between Baring Head and Cape Grim.

Some data are removed: 
In 1995, sample measurement was changed from gas counting to AMS. Data from 1995 to 2005 is noisy and was corrected 
using offline δ13C measurements (Turnbull et al., 2017). We will remove data between 1995-2005 until online 
δ13C measurements were installed (Zondervan et al., 2015)

Bump in BHD record between 2006 and 2009 may be linked to NaOH sampling procedure. These will be removed. 
No flask data during this period to focus on instead.


The first few blocks include indexing the data according to time-intervals that I've established in previous iterations, 
including: 
1986 - 1991: Beginning of Heidelberg records + 5 Years
1991 - 1994: End of 1st interval until the beginning of RRL's period where data must be removed. 
2006 - 2016: From the end of RRL removal period until the end of Heidelberg's record
2006 - 2009: Early period before NaOH removal period
2012 - 2016 : Period after NaOH removal period to end of record
"""
baringhead = combine_heidelberg.loc[(combine_heidelberg['Site'] == 'CGO')]
heidelberg = combine_heidelberg.loc[(combine_heidelberg['Site'] == 'RRL')]

baringhead_1986_1991 = baringhead.loc[(baringhead['Decimal_date'] >= 1987) & (baringhead['Decimal_date'] <= 1991)].reset_index(drop=True)
baringhead_1991_1994 = baringhead.loc[(baringhead['Decimal_date'] >= 1991) & (baringhead['Decimal_date'] <= 1994)].reset_index(drop=True)
baringhead_1994_2006 = baringhead.loc[(baringhead['Decimal_date'] >= 1994) & (baringhead['Decimal_date'] <= 2006)].reset_index(drop=True)
baringhead_2006_2016 = baringhead.loc[(baringhead['Decimal_date'] > 2006) & (baringhead['Decimal_date'] <= 2016)].reset_index(drop=True)
baringhead_2006_2009 = baringhead.loc[(baringhead['Decimal_date'] >= 2006) & (baringhead['Decimal_date'] <= 2009)].reset_index(drop=True)
baringhead_2012_2016 = baringhead.loc[(baringhead['Decimal_date'] >= 2012) & (baringhead['Decimal_date'] <= 2016)].reset_index(drop=True)

heidelberg_1986_1991 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1987) & (heidelberg['Decimal_date'] <= 1991)].reset_index(drop=True)
heidelberg_1991_1994 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1991) & (heidelberg['Decimal_date'] <= 1994)].reset_index(drop=True)
heidelberg_2006_2016 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1994) & (heidelberg['Decimal_date'] <= 2006)].reset_index(drop=True)
heidelberg_2006_2009 = heidelberg.loc[(heidelberg['Decimal_date'] >= 2006) & (heidelberg['Decimal_date'] <= 2009)].reset_index(drop=True)
heidelberg_2012_2016 = heidelberg.loc[(heidelberg['Decimal_date'] >= 2012) & (heidelberg['Decimal_date'] <= 2016)].reset_index(drop=True)











