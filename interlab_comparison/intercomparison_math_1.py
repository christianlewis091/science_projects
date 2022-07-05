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


All data visualizations will appear in another .py file. 

First I'm going to just index the data I need for the t-tests for ANSTO, SIO/LLNL (NWT3 and NWT4) and Magallanes. 
"""

ansto = combine_ANSTO.loc[(combine_ANSTO['Site'] == 'ANSTO')]
rrl = combine_ANSTO.loc[(combine_ANSTO['Site'] == 'RRL')]
A = stats.ttest_rel(ansto['D14C'], rrl['D14C'])

NWT3 = combine_SIO.loc[(combine_SIO['standard_type'] == 'NWT3')]
sio_nwt3 = NWT3.loc[(NWT3['Site'] == 'LLNL')]
rrl_nwt3 = NWT3.loc[(NWT3['Site'] == 'RRL')]

NWT4 = combine_SIO.loc[(combine_SIO['standard_type'] == 'NWT4')]
sio_nwt4 = NWT4.loc[(NWT4['Site'] == 'LLNL')]
rrl_nwt4 = NWT4.loc[(NWT4['Site'] == 'RRL')]

# Magallanes data is setup slightly different, take a look at the data to see why it is indexed this way -
# perhaps it is so only beccause I'm a novice coder...
rafter = combine_Magallanes['D14C_x']
magallanes = combine_Magallanes['D14C_y']

"""
Writing a quick function to save myself a few lines here...
"""


def intercomparison_ttest(data1, data2, test_name, test_type):

    print(str(test_name))  # Print the name of the thing we're comparing
    if test_type == 'paired':  # set the type of t-test
        result = stats.ttest_rel(data1, data2)

    elif test_type == 'not-paired':
        result = stats.ttest_ind(data1, data2)
        avg1 = np.average(data1)                # compute "metadata" (wrong term maybe)?
        std1 = np.std(data1)
        avg2 = np.average(data2)
        std2 = np.std(data2)
        offset = avg1 - avg2
        print('The average of first input is' + str(avg1) + 'plusminus' + str(std1))
        print('The average of second input is' + str(avg1) + 'plusminus' + str(std2))
        print('The offset is' + str(offset))

    print(result)  # Print the t-test result
    if result[1] < 0.01:  # if statement for me to print if they are different
        print("The data are different at 98% confidence")
    else:
        print("The data are not different")
    print('\n' * 1)                            # print some blank lines
    return result


a = intercomparison_ttest(ansto['D14C'], rrl['D14C'], 'ANSTO v RRL Test: Tree Rings', 'paired')
b = intercomparison_ttest(sio_nwt3['D14C'], rrl_nwt3['D14C'], 'SIO/LLNL v RRL, NWT3 Intercomparison', 'not-paired')
c = intercomparison_ttest(sio_nwt4['D14C'], rrl_nwt4['D14C'], 'SIO/LLNL v RRL, NWT3 Intercomparison', 'not-paired')
d = intercomparison_ttest(rafter, magallanes, 'Magallanes v RRL Test: Tree Rings', 'paired')

# TODO next, clean up function that does "Basic analysis" to be more broadly used and apply here to get fast averages and such
