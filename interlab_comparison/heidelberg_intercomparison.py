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


from tabulate import tabulate

f = open("output.txt", "a")  # where I want the result to be stored

# TODO Make 1 singular place to change "n" and "cutoff"
# TODO Save the Smoothed and Trend data and other crunched data into an excel sheet
"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
Define all the functions that I'll be using. 
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####################################################################################################################### 
"""
"""
"long_date_to_decimal_date" takes dates of the form dd/mm/yyyy and converts
them to decimal dates more useful for performing curve smoothing on. 
"""


def long_date_to_decimal_date(x):
    array = []
    for i in range(0, len(x)):
        j = x[i]
        decy = pyasl.decimalYear(j)
        decy = float(decy)
        # print(decy)
        array.append(decy)
    # print(array)
    return array


def year_month_todecimaldate(x, y):
    L = np.linspace(0, 1, 365)
    # add the number that is 1/2 of the previous month plus the current month
    Jan = 31
    Feb = (28 / 2) + 31
    Mar = (31 / 2) + 31 + 28
    Apr = (30 / 2) + 31 + 28 + 31
    May = (31 / 2) + 31 + 28 + 31 + 30
    June = (30 / 2) + 31 + 28 + 31 + 30 + 31
    July = (31 / 2) + 31 + 28 + 31 + 30 + 31 + 30
    August = (31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31
    Sep = (30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31
    Oct = (31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30
    Nov = (30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30
    Dec = (31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30 + 30
    empty_array = []
    for i in range(0, len(x)):
        r = x[i]
        if y[i] == 1:
            r = x[i] + L[int(Jan)]
        elif y[i] == 2:
            r = x[i] + L[int(Feb)]
        elif y[i] == 3:
            r = x[i] + L[int(Mar)]
        elif y[i] == 4:
            r = x[i] + L[int(Apr)]
        elif y[i] == 5:
            r = x[i] + L[int(May)]
        elif y[i] == 6:
            r = x[i] + L[int(June)]
        elif y[i] == 7:
            r = x[i] + L[int(July)]
        elif y[i] == 8:
            r = x[i] + L[int(August)]
        elif y[i] == 9:
            r = x[i] + L[int(Sep)]
        elif y[i] == 10:
            r = x[i] + L[int(Oct)]
        elif y[i] == 11:
            r = x[i] + L[int(Nov)]
        elif y[i] == 12:
            r = x[i] + L[int(Dec)]
        empty_array.append(r)

    return empty_array


"""
"monte_carlo_randomization" has three parts (3 separate for-loops) 

Lets say we have a time-series of 10 measurements. 
The first for-loop: takes an input array of time-series data and randomizes each data point 
within its measurements uncertainty. It does this "n" times, and vertically stacks it. 
For example, if you have a dataset with 10 measurements, and "n" is 1000, you will end 
up with an array of dimension (10x1000). 

The second for-loop: takes each row of the array (each row of "randomized data") and puts it through
the ccgFilter curve smoother. It is important to define your own x-values that you want output 
if you want to compare two curves (this will keep arrays the same dimension). 
Each row from the fist loop is smoothed and stacked into yet another new array. 

The third for-loop: Find the mean, standard deviation, and upper and lower uncertainty bounds of each
"point" in the dataset. This loop takes the mean of all the first measurements, then all the second, etc.
"""


def monte_carlo_randomization_Trend(x_init, fake_x, y_init, y_error, cutoff, n):
    # reset indeces for incoming data
    x_init = x_init.reset_index(drop=True)
    y_init = y_init.reset_index(drop=True)
    y_error = y_error.reset_index(drop=True)
    fake_x_for_dataframe = fake_x.reset_index(drop=True)
    fake_x_for_dataframe = fake_x_for_dataframe['x']

    # """ Randomization step """

    new_array = y_init  # create a new variable on which we will later v-stack randomized lists
    for i in range(0, n):
        empty_array = []
        for j in range(0, len(y_init)):
            a = y_init[j]  # grab the first item in the set
            b = y_error[j]  # grab the uncertainty
            rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
            c = a + rand  # add this to the number
            empty_array.append(c)  # add this to a list
            # print(len(empty_array))

        # """ The "new_array" contains the data that will be used in the next step"""
        # """ The "randomized_dataframe" contains a more digestible course of data that can be plotted. """
        # """ To plot randomized data from the "Randomized Dataframe, index each row using randomized_dataframe.iloc[0]  """

        new_array = np.vstack((new_array, empty_array))
    randomized_dataframe = pd.DataFrame(new_array)

    # SMOOTHING STEP

    # Create an initial array on which later arrays that are created will stack
    template_array = ccgFilter(x_init, new_array[0], cutoff).getTrendValue(fake_x)  # inital values for stacking

    # this for smooths each row of the randomized array from above, and stacks it up
    for k in range(0, len(new_array)):
        row = new_array[k]  # grab the first row of the data
        smooth = ccgFilter(x_init, row, cutoff).getTrendValue(fake_x)  # outputs smooth values at my desired times, x
        template_array = np.hstack((template_array, smooth))

    smoothed_dataframe = pd.DataFrame(template_array)

    mean_array = []
    stdev_array = []
    upper_array = []
    lower_array = []
    for i in range(0, len(template_array)):
        element1 = smoothed_dataframe.iloc[i]
        sum1 = np.sum(element1)  # grab the first ROW of the dataframe and take the sum
        mean1 = sum1 / len(element1)  # find the mean of all the values from the Monte Carlo
        mean_array.append(mean1)  # append it to a new array

        stdev = np.std(element1)  # grab the first ROW of the dataframe find the stdev
        stdev_array.append(stdev)

        upper = mean1 + stdev
        lower = mean1 - stdev
        upper_array.append(upper)
        lower_array.append(lower)

        # create a more digestable summary dataframe
    summary = pd.DataFrame({"Means": mean_array,
                            "stdevs": stdev_array,
                            "error_upperbound": upper_array,
                            "error_lowerbound": lower_array,
                            "my_xs": fake_x_for_dataframe})

    return randomized_dataframe, smoothed_dataframe, summary


def monte_carlo_randomization_Smooth(x_init, fake_x, y_init, y_error, cutoff, n):
    # reset indeces for incoming data
    x_init = x_init.reset_index(drop=True)
    y_init = y_init.reset_index(drop=True)
    y_error = y_error.reset_index(drop=True)
    fake_x_for_dataframe = fake_x.reset_index(drop=True)
    fake_x_for_dataframe = fake_x_for_dataframe['x']

    # """ Randomization step """

    new_array = y_init  # create a new variable on which we will later v-stack randomized lists
    for i in range(0, n):
        empty_array = []
        for j in range(0, len(y_init)):
            a = y_init[j]  # grab the first item in the set
            b = y_error[j]  # grab the uncertainty
            rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
            c = a + rand  # add this to the number
            empty_array.append(c)  # add this to a list
            # print(len(empty_array))

        # """ The "new_array" contains the data that will be used in the next step"""
        # """ The "randomized_dataframe" contains a more digestible course of data that can be plotted. """
        # """ To plot randomized data from the "Randomized Dataframe, index each row using randomized_dataframe.iloc[0]  """

        new_array = np.vstack((new_array, empty_array))
    randomized_dataframe = pd.DataFrame(new_array)

    # SMOOTHING STEP

    # Create an initial array on which later arrays that are created will stack
    template_array = ccgFilter(x_init, new_array[0], cutoff).getSmoothValue(fake_x)  # inital values for stacking

    # this for smooths each row of the randomized array from above, and stacks it up
    for k in range(0, len(new_array)):
        row = new_array[k]  # grab the first row of the data
        smooth = ccgFilter(x_init, row, cutoff).getSmoothValue(fake_x)  # outputs smooth values at my desired times, x
        template_array = np.hstack((template_array, smooth))

    smoothed_dataframe = pd.DataFrame(template_array)
    smoothed_dataframe_trans = pd.DataFrame.transpose(smoothed_dataframe)
    mean_array = []
    stdev_array = []
    upper_array = []
    lower_array = []
    for i in range(0, len(template_array)):
        element1 = smoothed_dataframe.iloc[i]
        sum1 = np.sum(element1)  # grab the first ROW of the dataframe and take the sum
        mean1 = sum1 / len(element1)  # find the mean of all the values from the Monte Carlo
        mean_array.append(mean1)  # append it to a new array

        stdev = np.std(element1)  # grab the first ROW of the dataframe find the stdev
        stdev_array.append(stdev)

        upper = mean1 + stdev
        lower = mean1 - stdev
        upper_array.append(upper)
        lower_array.append(lower)

        # create a more digestable summary dataframe
    summary = pd.DataFrame({"Means": mean_array,
                            "stdevs": stdev_array,
                            "error_upperbound": upper_array,
                            "error_lowerbound": lower_array,
                            "my_xs": fake_x_for_dataframe})

    return randomized_dataframe, smoothed_dataframe_trans, summary


""" 
The following function should determine monthly averages for a dataset. 
It will output these monthly averages along with a decimal date being the first decimal of that month. 
"""


def monthly_averages(x_values, y_values, y_err):
    x_values = np.array(x_values)
    y_values = np.array(y_values)
    y_err = np.array(y_err)

    Begin = 0
    Jan = 31
    Feb = 28 + 31
    Mar = 31 + 31 + 28
    Apr = 30 + 31 + 28 + 31
    May = 31 + 31 + 28 + 31 + 30
    June = 30 + 31 + 28 + 31 + 30 + 31
    July = 31 + 31 + 28 + 31 + 30 + 31 + 30
    August = 31 + 31 + 28 + 31 + 30 + 31 + 30 + 31
    Sep = 30 + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31
    Oct = 31 + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30
    Nov = 30 + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30
    Dec = 31 + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30 + 30
    months = np.array([Begin, Jan, Feb, Mar, Apr, May, June, July, August, Sep, Oct, Nov, Dec])
    months = months / 365

    # first, enter the available years on file:
    lin1 = np.linspace(int(min(x_values)),
                       int(max(x_values)),
                       (int(max(x_values)) - int(min(x_values)) + 1))

    # initialize some vars
    mean_of_date = 0
    mean_of_y = 0

    permarray_x = []
    permarray_y = []
    permarray_z = []
    for i in range(0, len(lin1)):  # loop in the years
        year = int(lin1[i])  # grab only the integer parts of the years in the data

        for j in range(0, len(months)):  # loop in the months

            temparray_x = []
            temparray_y = []
            temparray_z = []
            # print('The current month is ' + str(months[j]) + 'in year ' + str(year))
            months_min = months[j]
            # TODO fix this line of code to filter between one month and the next more accurately
            months_max = months_min + 0.08

            for k in range(0, len(y_values)):  # grab the data i want to use
                y_current = y_values[k]
                x_current = x_values[k]
                z_current = y_err[k]
                x_decimal_only = x_current - int(x_current)
                x_int = int(x_current)
                # if my data exists in the time frame I'm currently searching through,
                if (x_int == year) and (x_decimal_only >= months_min) and (x_decimal_only < months_max):
                    # append that x and y data to initialized arrays
                    temparray_x.append(x_int + months_min)
                    temparray_y.append(y_current)
                    temparray_z.append(z_current)

            # if at the end of the month, the length of the temporary arrays are non-zero,
            # clean and append that information to a permanent array
            if len(temparray_x) != 0:
                tempsum = sum(temparray_x)
                tempmean = tempsum / len(temparray_x)  # this works fine because it averages the same # repeatedly

                tempsum2 = sum(temparray_y)
                tempmean2 = tempsum2 / len(temparray_y)

                tempsum3 = sum(temparray_z)                  # todo change from simple averaging of error to proper prop
                tempmean3 = tempsum3 / len(temparray_z)

                permarray_x.append(tempmean)
                permarray_y.append(tempmean2)
                permarray_z.append(tempmean3)
                # print(permarray_x)
                # print(permarray_y)

            # else:
            #     permarray_x.append(x_int + months_min)
            #     permarray_y.append(-999)

    return permarray_x, permarray_y, permarray_z


"""
This function does a paired two-tail t-test. The t-value range comes from the stdev_array in the 
Monte Carlo function above, and errors are propagated through the t-test mathematics. 
"""


def two_tail_paired_t_test(y1, y1err, y2, y2err):
    """ Subtract the data from each other (first step in paired t-test)"""
    difference = np.subtract(y1, y2)  # subtract the data from each other
    """ What is the mean of the subtraction array? """
    mean1 = np.average(difference)
    """ What is the standard error of the subtraction array"""
    se = np.std(difference) / np.sqrt(len(y1))
    """ Compute the t-stat"""
    t_stat = mean1 / se
    t_stat = np.abs(t_stat)

    """ ERROR PROPAGATION """
    """ propagate the error from the first differencing """
    y1err_sq = y1err * y1err  # square of errors from first dataset
    y2err_sq = y2err * y2err  # square of errors from second dataset
    sum_errs = y1err_sq + y2err_sq  # sum of the squared errors
    err_differencing = np.sqrt(sum_errs)  # square root of the sums of errors

    """ propagate the error from the mean1 """
    squares = err_differencing * err_differencing  # square the propagated errors from differencing
    sum_errs2 = 0  # initialize sums to zero
    for i in range(0, len(squares)):
        sum_errs2 = sum_errs2 + squares[i]  # add them all together
        # sum_errs2 += squares[i]
    sum_errs3 = np.sqrt(sum_errs2)  # take the square root
    err_mean = sum_errs3 / len(squares)  # divide by number of measurements
    ### The ERR_MEAN IS PROPOGATED ERROR, NOT STANDARD ERROR!!!

    """ 
    Propogate error for the denominator of t-stat calc, STANDARD ERROR
    For this I need to propogate the error through the standard deviation calculation, 
    and then divide by sqrt(N)
    """
    """STEP 1: Propogate the error of (xi - u)"""
    xi_u = err_mean ** 2 + err_differencing ** 2
    xi_u = np.sqrt(xi_u)
    """STEP 2: Propogate the error of (xi - u)^2 """
    xi_u2_a = (difference - mean1) ** 2
    xi_u2_b = xi_u / (difference - mean1)
    xi_u2_c = xi_u2_b ** 2
    xi_u2_d = xi_u2_c * 2
    xi_u2_e = np.sqrt(xi_u2_d)
    xi_u2_f = xi_u2_e * xi_u2_a

    """STEP 3: Propagate the error of SIGMA(xi - u)^2 """
    init_num = 0  # initialize a number to add errors onto
    for i in range(0, len(xi_u2_f)):
        xi_u2_g = xi_u2_f[i] ** 2
        init_num = xi_u2_g + init_num
    sigma_xi_u2 = np.sqrt(init_num)

    """STEP 4: Propagate the error of SIGMA(xi - u)^2 / N """
    sigma_xi_2_byN = sigma_xi_u2 / len(y1)

    """STEP 5: Propagate the error of SQRT of SIGMA(xi - u)^2 / N """
    sqrt_sigmaxi_2_byn = np.sqrt(sigma_xi_2_byN)

    """STEP 6: Find standard error by dividing SQRT by sqrt of N """
    se_err = sqrt_sigmaxi_2_byn / np.sqrt(len(y1))

    """ final t-test error: error of mean and error of SE"""
    t_stat_e1 = t_stat
    t_stat_e2 = (se_err / se) ** 2
    t_stat_e3 = (err_mean / mean1) ** 2
    t_stat_e4 = t_stat_e2 + t_stat_e3
    t_stat_e5 = np.sqrt(t_stat_e4)
    t_stat_e6 = t_stat_e1 * t_stat_e5

    d_of_f = len(y1) + len(y2) - 2
    # find the degrees of freedom, and the closest number in the table to my degrees of freedom
    dfx = pd.read_excel(
        r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Stats and Data Analysis\Matlab and Python '
        r'Files\tables.xlsx',
        sheet_name='ttable_adjusted')
    # print(dfx)
    # locate where the degrees of freedom is equal to my degrees of freedom:
    value_crits = dfx['value']
    value_crits = np.array(value_crits)
    if d_of_f > 100:
        value_crit = 1.98
    else:
        value_crit = value_crits[d_of_f - 1]

    if t_stat - t_stat_e6 <= value_crit:

        data = [t_stat, t_stat_e6, value_crit, mean1, err_mean]
        headers = ['t-statistic', 't-statistic error', 'critical value', 'mean of differences', 'error of mean']
        data = pd.DataFrame(data, headers)
        print(data, file=f)
        print('There is NO observed difference at 95% confidence interval', file=f)
        print('', file=f)
        print('', file=f)
        result = 1

    else:
        data = [t_stat, t_stat_e6, value_crit, mean1, err_mean]
        headers = ['t-statistic', 't-statistic error', 'critical value', 'mean of differences', 'error of mean']
        data = pd.DataFrame(data, headers)
        print(data, file=f)
        print('There IS AN observed difference at 95% confidence interval', file=f)
        print('', file=f)
        print('', file=f)

        result = 0

    return result


"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
Import and clean up data
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####################################################################################################################### 
"""

# Heidelberg data excel file
heidelberg = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\heidelberg_cape_grim.xlsx', skiprows=40)
# Baring Head data excel file
baringhead = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')

df2_dates = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                          r'\BHD_MeasurementDates.xlsx')
extraction_dates = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                                 r'\BHDFlasks_WithExtractionDates.xlsx')
#
""" TIDY UP THE DATA FILES"""
# add decimal dates to DataFrame if not there already
x_init_heid = heidelberg['Average pf Start-date and enddate']  # x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)
heidelberg['Decimal_date'] = x_init_heid  # add these decimal dates onto the dataframe

# drop NaN's in the column I'm most interested in
heidelberg = heidelberg.dropna(subset=['D14C'])
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]
heidelberg.reset_index()  # filter out the one outlying measurement around 2019
baringhead = baringhead.dropna(subset=['DELTA14C'])

"""CAREFULLY SPLIT UP THE DATA INTO DIFFERENT CHUNKS IN TIME AND GRAB VARIABLES """

""" Entire Baring Head File > 1980 """
baringhead = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 1980)]
baringhead = baringhead.loc[(baringhead['DELTA14C_ERR'] > 0)]  # get rid of data where the error flag is -1000
baringhead = baringhead.reset_index(drop=True)  # index currently goes to 0 :)

""" Entire Baring Head File > 1980, without 1995 - 2005 """
snipmin = 1994  # was previously 1994
snipmax = 2006  # was previously 2006
snip = baringhead.loc[(baringhead['DEC_DECAY_CORR'] < snipmin)]
snip2 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > snipmax)]
snip = pd.merge(snip, snip2, how='outer')
snip = snip.reset_index(drop=True)

"""
RECORDS SPLIT UP INTO 5 PARTS (1987 - 1991, 1991 - 1994, 2006 - 2016, 2006 - 2009, 2012 - 2016)
"""
# split up data and reset indeces to avoid random DataFrame errors
baringhead_1986_1991 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 1987) & (baringhead['DEC_DECAY_CORR'] <= 1991)]
baringhead_1991_1994 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 1991) & (baringhead['DEC_DECAY_CORR'] <= 1994)]
baringhead_2006_2016 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2006) & (baringhead['DEC_DECAY_CORR'] <= 2016)]
baringhead_2006_2009 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 2006) & (baringhead['DEC_DECAY_CORR'] <= 2009)]
baringhead_2012_2016 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 2012) & (baringhead['DEC_DECAY_CORR'] <= 2016)]
baringhead_1986_1991 = baringhead_1986_1991.reset_index(drop=True)  # index goes to zero
baringhead_1991_1994 = baringhead_1991_1994.reset_index(drop=True)  # index goes to zero
baringhead_2006_2016 = baringhead_2006_2016.reset_index(drop=True)  # index goes to zero
baringhead_2006_2009 = baringhead_2006_2009.reset_index(drop=True)  # index goes to zero
baringhead_2012_2016 = baringhead_2012_2016.reset_index(drop=True)  # index goes to zero

heidelberg_1986_1991 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1987) & (heidelberg['Decimal_date'] <= 1991)]
heidelberg_1991_1994 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1991) & (heidelberg['Decimal_date'] <= 1994)]
heidelberg_2006_2016 = heidelberg.loc[(heidelberg['Decimal_date'] > 2006)]  # BARINGHEAD2 will include the 2009-2011
heidelberg_2006_2009 = heidelberg.loc[(heidelberg['Decimal_date'] >= 2006) & (heidelberg['Decimal_date'] <= 2009)]
heidelberg_2012_2016 = heidelberg.loc[(heidelberg['Decimal_date'] >= 2012) & (heidelberg['Decimal_date'] <= 2016)]
heidelberg_1986_1991 = heidelberg_1986_1991.reset_index(drop=True)  # index goes to zero
heidelberg_1991_1994 = heidelberg_1991_1994.reset_index(drop=True)  # index goes to zero
heidelberg_2006_2016 = heidelberg_2006_2016.reset_index(drop=True)  # index goes to zero
heidelberg_2006_2009 = heidelberg_2006_2009.reset_index(drop=True)  # index goes to zero
heidelberg_2012_2016 = heidelberg_2012_2016.reset_index(drop=True)  # index goes to zero

"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
Pull out all the variables 
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####################################################################################################################### 
"""
# BARING HEAD VARIABLES
xtot_bhd = baringhead['DEC_DECAY_CORR']             # entire dataset x-values
ytot_bhd = baringhead['DELTA14C']                   # entire dataset y-values
ztot_bhd = baringhead['DELTA14C_ERR']               # entire dataset z-values
x_combined = snip['DEC_DECAY_CORR']                 # dataset x-values after we remove 1995-2005
y_combined = snip['DELTA14C']                       # dataset y-values after we remove 1995-2005
z_combined = snip['DELTA14C_ERR']                   # dataset z-values after we remove 1995-2005
x1_bhd = baringhead_1986_1991['DEC_DECAY_CORR']
x2_bhd = baringhead_1991_1994['DEC_DECAY_CORR']
x3_bhd = baringhead_2006_2016['DEC_DECAY_CORR']
x4_bhd = baringhead_2006_2009['DEC_DECAY_CORR']
x5_bhd = baringhead_2012_2016['DEC_DECAY_CORR']
y1_bhd = baringhead_1986_1991['DELTA14C']  #
y2_bhd = baringhead_1991_1994['DELTA14C']
y3_bhd = baringhead_2006_2016['DELTA14C']
y4_bhd = baringhead_2006_2009['DELTA14C']
y5_bhd = baringhead_2012_2016['DELTA14C']
z1_bhd = baringhead_1986_1991['DELTA14C_ERR']
z2_bhd = baringhead_1991_1994['DELTA14C_ERR']
z3_bhd = baringhead_2006_2016['DELTA14C_ERR']
z4_bhd = baringhead_2006_2009['DELTA14C_ERR']
z5_bhd = baringhead_2012_2016['DELTA14C_ERR']
# HEIDELBERG CAPE GRIM VARIABLES
xtot_heid = heidelberg['Decimal_date']             # entire dataset x-values
ytot_heid = heidelberg['D14C']                     # entire dataset y-values
ztot_heid = heidelberg['weightedstderr_D14C']      # entire dataset error(z)-values
x1_heid = heidelberg_1986_1991['Decimal_date']
x2_heid = heidelberg_1991_1994['Decimal_date']
x3_heid = heidelberg_2006_2016['Decimal_date']
x4_heid = heidelberg_2006_2009['Decimal_date']
x5_heid = heidelberg_2012_2016['Decimal_date']
y1_heid = heidelberg_1986_1991['D14C']
y2_heid = heidelberg_1991_1994['D14C']
y3_heid = heidelberg_2006_2016['D14C']
y4_heid = heidelberg_2006_2009['D14C']
y5_heid = heidelberg_2012_2016['D14C']
z1_heid = heidelberg_1986_1991['weightedstderr_D14C']
z2_heid = heidelberg_1991_1994['weightedstderr_D14C']
z3_heid = heidelberg_2006_2016['weightedstderr_D14C']
z4_heid = heidelberg_2006_2009['weightedstderr_D14C']
z5_heid = heidelberg_2012_2016['weightedstderr_D14C']

"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
Develop a controlled set of x-values onto which the CCGCRV curve will output y-values for paired t-tests. 
This need to be done for each time-interval that the user is interested in. 
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####################################################################################################################### 
"""
# x-data that I will use to solve for each of the smoothed curve functions - this way, x-data will be the same
# for any two datasets that I want to explicity compare, and I can subtract them directly.
fake_x_temp = np.linspace(1980, 2020, 480)
df_fake_xs = pd.DataFrame({'x': fake_x_temp})
# # TODO adjust the lenghts of the "my_x's" so they are not larger than the data themself in any given subset.
# make sure to only get output at x-values where the data overlaps.
my_x_1986_1991 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x1_heid)) & (df_fake_xs['x'] <= max(x1_heid))]
my_x_1991_1994 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x2_bhd)) & (df_fake_xs['x'] <= max(x2_bhd))]
my_x_2006_2016 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x3_heid)) & (df_fake_xs['x'] <= max(x3_heid))]
my_x_2006_2009 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x4_heid)) & (df_fake_xs['x'] <= max(x4_heid))]
my_x_2012_2016 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x5_heid)) & (df_fake_xs['x'] <= max(x5_heid))]
my_x_1986_1991 = my_x_1986_1991.reset_index(drop=True)
my_x_1991_1994 = my_x_1991_1994.reset_index(drop=True)
my_x_2006_2016 = my_x_2006_2016.reset_index(drop=True)
my_x_2006_2009 = my_x_2006_2009.reset_index(drop=True)
my_x_2012_2016 = my_x_2012_2016.reset_index(drop=True)

"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
Monte Carlo Randomization and Curve Smoothing
This block of code takes advantage of the Monte Carlo randomization code that I wrote. Then it uses the CCGCRV curve
getSmoothValues and getTrendValues
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####################################################################################################################### 
#######################################################################################################################
####################################################################################################################### 
"""
# function input: def monte_carlo_randomization(x_init, fake_x, y_init, y_error, cutoff):
# function return:  new_array, template_array, mean_array, stdev_array, upper_array, lower_array, fake_x
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time is :", current_time)

n = 10          # set the amount of times the code will iterate (set to 10,000 once everything is final)
cutoff = 667
print('For this run of heidelberg_intercomparison.py, "n" is {} and the CCGCRV cutoff is {}. This was run on {}'.format(n, cutoff, current_time), file=f)
print()
print()

# Curve smoothing with getSmoothValue()
heidelberg_1986_1991_results_smooth = monte_carlo_randomization_Smooth(x1_heid, my_x_1986_1991, y1_heid, z1_heid, cutoff, n)
heidelberg_1991_1994_results_smooth = monte_carlo_randomization_Smooth(x2_heid, my_x_1991_1994, y2_heid, z2_heid, cutoff, n)
heidelberg_2006_2016_results_smooth = monte_carlo_randomization_Smooth(x3_heid, my_x_2006_2016, y3_heid, z3_heid, cutoff, n)
heidelberg_2006_2009_results_smooth = monte_carlo_randomization_Smooth(x4_heid, my_x_2006_2009, y4_heid, z4_heid, cutoff, n)
heidelberg_2012_2016_results_smooth = monte_carlo_randomization_Smooth(x5_heid, my_x_2012_2016, y5_heid, z5_heid, cutoff, n)
bhd_1986_1991_results_smooth = monte_carlo_randomization_Smooth(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)
bhd_1991_1994_results_smooth = monte_carlo_randomization_Smooth(x2_bhd, my_x_1991_1994, y2_bhd, z2_bhd, cutoff, n)
bhd_2006_2016_results_smooth = monte_carlo_randomization_Smooth(x3_bhd, my_x_2006_2016, y3_bhd, z3_bhd, cutoff, n)
bhd_2006_2009_results_smooth = monte_carlo_randomization_Smooth(x4_bhd, my_x_2006_2009, y4_bhd, z4_bhd, cutoff, n)
bhd_2012_2016_results_smooth = monte_carlo_randomization_Smooth(x5_bhd, my_x_2012_2016, y5_bhd, z5_bhd, cutoff, n)
# Curve smoothing with getTrendValue()
heidelberg_1986_1991_results_trend = monte_carlo_randomization_Trend(x1_heid, my_x_1986_1991, y1_heid, z1_heid, cutoff, n)
heidelberg_1991_1994_results_trend = monte_carlo_randomization_Trend(x2_heid, my_x_1991_1994, y2_heid, z2_heid, cutoff, n)
heidelberg_2006_2016_results_trend = monte_carlo_randomization_Trend(x3_heid, my_x_2006_2016, y3_heid, z3_heid, cutoff, n)
heidelberg_2006_2009_results_trend = monte_carlo_randomization_Trend(x4_heid, my_x_2006_2009, y4_heid, z4_heid, cutoff, n)
heidelberg_2012_2016_results_trend = monte_carlo_randomization_Trend(x5_heid, my_x_2012_2016, y5_heid, z5_heid, cutoff, n)
bhd_1986_1991_results_trend = monte_carlo_randomization_Trend(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)
bhd_1991_1994_results_trend = monte_carlo_randomization_Trend(x2_bhd, my_x_1991_1994, y2_bhd, z2_bhd, cutoff, n)
bhd_2006_2016_results_trend = monte_carlo_randomization_Trend(x3_bhd, my_x_2006_2016, y3_bhd, z3_bhd, cutoff, n)
bhd_2006_2009_results_trend = monte_carlo_randomization_Trend(x4_bhd, my_x_2006_2009, y4_bhd, z4_bhd, cutoff, n)
bhd_2012_2016_results_trend = monte_carlo_randomization_Trend(x5_bhd, my_x_2012_2016, y5_bhd, z5_bhd, cutoff, n)

"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####################################################################################################################### 
#######################################################################################################################
####################################################################################################################### 
Extract the data back out after the smoothing process. 
The function returns:
1. A dataframe of the randomized data
2. A dataframe of the smoothed data
3. A summary dataframe (see below)
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####################################################################################################################### 
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
####################################################################################################################### 
#######################################################################################################################
#######################################################################################################################  
"""

# Function output
# summary = pd.DataFrame({"Means": mean_array,
#                        "stdevs": stdev_array,
#                        "error_upperbound": upper_array,
#                        "error_lowerbound": lower_array,
#                        "my_xs": fake_x_for_dataframe})
# return randomized_dataframe, smoothed_dataframe, summary

"""
For Figure 2 of the paper, I want to show an example of the randomization and smoothing process, for both the 
getSmoothValue and getTrendValue. I also want this to be with Baring Head data. We don't always need to extract all
of the randomized data, and multiple of the smooth curves (usually just the mean). However, for this figure / to 
illustrate the point, I will extract the data for this one case. 
"""
# bhd_1986_1991_results_smooth = monte_carlo_randomization_Smooth(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)
bhd_1986_1991_RandomData_smooth = bhd_1986_1991_results_smooth[0]  # the randomized data from 1986 - 1991
bhd_1986_1991_RandomCurves_smooth = bhd_1986_1991_results_smooth[1]  # the randomized data from 1986 - 1991
summary = bhd_1986_1991_results_smooth[2]  # the randomized data from 1986 - 1991

# Choose three data-randomizations to use for the plot:
data1 = bhd_1986_1991_RandomData_smooth.iloc[1]  # three sets of random DATA (from Monte Carlo) for the plot.
data2 = bhd_1986_1991_RandomData_smooth.iloc[2]
data3 = bhd_1986_1991_RandomData_smooth.iloc[3]

bhd_1986_1991_RandomCurves_smooth = bhd_1986_1991_results_smooth[1]
curve1 = bhd_1986_1991_RandomCurves_smooth.iloc[1]  # the accompanying curves to the data above
curve2 = bhd_1986_1991_RandomCurves_smooth.iloc[2]
curve3 = bhd_1986_1991_RandomCurves_smooth.iloc[3]

means = summary['Means']
xs = summary['my_xs']

summary2 = bhd_1986_1991_results_trend[2]
means2 = summary2['Means']

"""
Data from getSmoothValue 
"""
# extract the summary DataFrame from the function
heidelberg_1986_1991_results_smooth = heidelberg_1986_1991_results_smooth[2]
heidelberg_1991_1994_results_smooth = heidelberg_1991_1994_results_smooth[2]
heidelberg_2006_2016_results_smooth = heidelberg_2006_2016_results_smooth[2]
heidelberg_2006_2009_results_smooth = heidelberg_2006_2009_results_smooth[2]
heidelberg_2012_2016_results_smooth = heidelberg_2012_2016_results_smooth[2]
bhd_1986_1991_results_smooth = bhd_1986_1991_results_smooth[2]
bhd_1991_1994_results_smooth = bhd_1991_1994_results_smooth[2]
bhd_2006_2016_results_smooth = bhd_2006_2016_results_smooth[2]
bhd_2006_2009_results_smooth = bhd_2006_2009_results_smooth[2]
bhd_2012_2016_results_smooth = bhd_2012_2016_results_smooth[2]

# extract the means from the summary DataFrame
heidelberg_1986_1991_mean_smooth = heidelberg_1986_1991_results_smooth['Means']
heidelberg_1991_1994_mean_smooth = heidelberg_1991_1994_results_smooth['Means']
heidelberg_2006_2016_mean_smooth = heidelberg_2006_2016_results_smooth['Means']
heidelberg_2006_2009_mean_smooth = heidelberg_2006_2009_results_smooth['Means']
heidelberg_2006_2009_mean_smooth = heidelberg_2006_2009_mean_smooth.iloc[0:34]
heidelberg_2012_2016_mean_smooth = heidelberg_2012_2016_results_smooth['Means']
heidelberg_2012_2016_mean_smooth = heidelberg_2012_2016_mean_smooth.iloc[1:40]
heidelberg_2012_2016_mean_smooth = heidelberg_2012_2016_mean_smooth.reset_index(drop=True)
bhd_1986_1991_mean_smooth = bhd_1986_1991_results_smooth['Means']
bhd_1991_1994_mean_smooth = bhd_1991_1994_results_smooth['Means']
bhd_2006_2016_mean_smooth = bhd_2006_2016_results_smooth['Means']
bhd_2006_2009_mean_smooth = bhd_2006_2009_results_smooth['Means']
bhd_2006_2009_mean_smooth = bhd_2006_2009_mean_smooth.iloc[0:34]
bhd_2012_2016_mean_smooth = bhd_2012_2016_results_smooth['Means']
bhd_2012_2016_mean_smooth = bhd_2012_2016_mean_smooth.iloc[1:40]
bhd_2012_2016_mean_smooth = bhd_2012_2016_mean_smooth.reset_index(drop=True)
my_x_2012_2016_trimmed = my_x_2012_2016[1:40]


heidelberg_1986_1991_stdevs_smooth = heidelberg_1986_1991_results_smooth['stdevs']
heidelberg_1991_1994_stdevs_smooth = heidelberg_1991_1994_results_smooth['stdevs']
heidelberg_2006_2016_stdevs_smooth = heidelberg_2006_2016_results_smooth['stdevs']
heidelberg_2006_2009_stdevs_smooth = heidelberg_2006_2009_results_smooth['stdevs']
heidelberg_2006_2009_stdevs_smooth = heidelberg_2006_2009_stdevs_smooth.iloc[0:34]
heidelberg_2012_2016_stdevs_smooth = heidelberg_2012_2016_results_smooth['stdevs']
heidelberg_2012_2016_stdevs_smooth = heidelberg_2012_2016_stdevs_smooth.iloc[1:40]
heidelberg_2012_2016_stdevs_smooth = heidelberg_2012_2016_stdevs_smooth.reset_index(drop=True)
bhd_1986_1991_stdevs_smooth = bhd_1986_1991_results_smooth['stdevs']
bhd_1991_1994_stdevs_smooth = bhd_1991_1994_results_smooth['stdevs']
bhd_2006_2016_stdevs_smooth = bhd_2006_2016_results_smooth['stdevs']
# # TODO Figure out why the final row of this goes to NaN...
bhd_2006_2009_stdevs_smooth = bhd_2006_2009_results_smooth['stdevs']
# TODO currently I'm snipping the 2006-2009 files of the last row that goes to NaN cuz I can't debug it...
my_x_2006_2009_trimmed = my_x_2006_2009.iloc[0:34]
bhd_2006_2009_stdevs_smooth = bhd_2006_2009_stdevs_smooth.iloc[0:34]
bhd_2012_2016_stdevs_smooth = bhd_2012_2016_results_smooth['stdevs']
# TODO currently I'm snipping the first row because beginning is NAN of the last row that goes to NaN cuz I can't debug it...
bhd_2012_2016_stdevs_smooth = bhd_2012_2016_stdevs_smooth.iloc[1:40]
bhd_2012_2016_stdevs_smooth = bhd_2012_2016_stdevs_smooth.reset_index(drop=True)

"""
Data from gettrendValue
"""

# extract the summary DataFrame from the function
heidelberg_1986_1991_results_trend = heidelberg_1986_1991_results_trend[2]
heidelberg_1991_1994_results_trend = heidelberg_1991_1994_results_trend[2]
heidelberg_2006_2016_results_trend = heidelberg_2006_2016_results_trend[2]
heidelberg_2006_2009_results_trend = heidelberg_2006_2009_results_trend[2]
heidelberg_2012_2016_results_trend = heidelberg_2012_2016_results_trend[2]
bhd_1986_1991_results_trend = bhd_1986_1991_results_trend[2]
bhd_1991_1994_results_trend = bhd_1991_1994_results_trend[2]
bhd_2006_2016_results_trend = bhd_2006_2016_results_trend[2]
bhd_2006_2009_results_trend = bhd_2006_2009_results_trend[2]
bhd_2012_2016_results_trend = bhd_2012_2016_results_trend[2]

# extract the means from the summary DataFrame
heidelberg_1986_1991_mean_trend = heidelberg_1986_1991_results_trend['Means']
heidelberg_1991_1994_mean_trend = heidelberg_1991_1994_results_trend['Means']
heidelberg_2006_2016_mean_trend = heidelberg_2006_2016_results_trend['Means']
heidelberg_2006_2009_mean_trend = heidelberg_2006_2009_results_trend['Means']
heidelberg_2006_2009_mean_trend = heidelberg_2006_2009_mean_trend.iloc[0:34]
heidelberg_2012_2016_mean_trend= heidelberg_2012_2016_results_trend['Means']
heidelberg_2012_2016_mean_trend = heidelberg_2012_2016_mean_trend.iloc[1:40]
heidelberg_2012_2016_mean_trend = heidelberg_2012_2016_mean_trend.reset_index(drop=True)
bhd_1986_1991_mean_trend = bhd_1986_1991_results_trend['Means']
bhd_1991_1994_mean_trend = bhd_1991_1994_results_trend['Means']
bhd_2006_2016_mean_trend = bhd_2006_2016_results_trend['Means']
bhd_2006_2009_mean_trend = bhd_2006_2009_results_trend['Means']
bhd_2006_2009_mean_trend = bhd_2006_2009_mean_trend.iloc[0:34]
bhd_2012_2016_mean_trend = bhd_2012_2016_results_trend['Means']
bhd_2012_2016_mean_trend = bhd_2012_2016_mean_trend.iloc[1:40]
bhd_2012_2016_mean_trend = bhd_2012_2016_mean_trend.reset_index(drop=True)

heidelberg_1986_1991_stdevs_trend = heidelberg_1986_1991_results_trend['stdevs']
heidelberg_1991_1994_stdevs_trend = heidelberg_1991_1994_results_trend['stdevs']
heidelberg_2006_2016_stdevs_trend = heidelberg_2006_2016_results_trend['stdevs']
heidelberg_2006_2009_stdevs_trend = heidelberg_2006_2009_results_trend['stdevs']
heidelberg_2006_2009_stdevs_trend = heidelberg_2006_2009_stdevs_trend.iloc[0:34]
heidelberg_2012_2016_stdevs_trend = heidelberg_2012_2016_results_trend['stdevs']
heidelberg_2012_2016_stdevs_trend = heidelberg_2012_2016_stdevs_trend.iloc[1:40]
heidelberg_2012_2016_stdevs_trend = heidelberg_2012_2016_stdevs_trend.reset_index(drop=True)
bhd_1986_1991_stdevs_trend = bhd_1986_1991_results_trend['stdevs']
bhd_1991_1994_stdevs_trend = bhd_1991_1994_results_trend['stdevs']
bhd_2006_2016_stdevs_trend = bhd_2006_2016_results_trend['stdevs']
# # TODO Figure out why the final row of this goes to NaN...
bhd_2006_2009_stdevs_trend = bhd_2006_2009_results_trend['stdevs']
bhd_2006_2009_stdevs_trend = bhd_2006_2009_stdevs_trend.iloc[0:34]
bhd_2012_2016_stdevs_trend = bhd_2012_2016_results_trend['stdevs']
# TODO currently I'm snipping the first row because beginning is NAN of the last row that goes to NaN cuz I can't debug it...
bhd_2012_2016_stdevs_trend = bhd_2012_2016_stdevs_trend.iloc[1:40]
bhd_2012_2016_stdevs_trend = bhd_2012_2016_stdevs_trend.reset_index(drop=True)






"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
Perform paired t-tests on sets of data and write result to file.
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
"""

""" paired t-tests of each of the datasets"""
print('Baring Head vs Cape Grim between 1986 - 1991 using CCGCRV Smooth Fit', file=f)
two_tail_paired_t_test(bhd_1986_1991_mean_smooth, bhd_1986_1991_stdevs_smooth, heidelberg_1986_1991_mean_smooth,
                       heidelberg_1986_1991_stdevs_smooth)
print()
print()
print('Baring Head vs Cape Grim between 1991 - 1994 using CCGCRV Smooth Fit', file=f)
two_tail_paired_t_test(bhd_1991_1994_mean_smooth, bhd_1991_1994_stdevs_smooth, heidelberg_1991_1994_mean_smooth,
                       heidelberg_1991_1994_stdevs_smooth)
print()
print()
print('Baring Head vs Cape Grim between 2006 - 2016 using CCGCRV Smooth Fit', file=f)
two_tail_paired_t_test(bhd_2006_2016_mean_smooth, bhd_2006_2016_stdevs_smooth, heidelberg_2006_2016_mean_smooth,
                       heidelberg_2006_2016_stdevs_smooth)
print()
print()
print('Baring Head vs Cape Grim between 2006 - 2009 using CCGCRV Smooth Fit', file=f)
two_tail_paired_t_test(bhd_2006_2009_mean_smooth, bhd_2006_2009_stdevs_smooth, heidelberg_2006_2009_mean_smooth,
                       heidelberg_2006_2009_stdevs_smooth)
print()
print()
print('Baring Head vs Cape Grim between 2012 - 2016 using CCGCRV Smooth Fit', file=f)
two_tail_paired_t_test(bhd_2012_2016_mean_smooth, bhd_2012_2016_stdevs_smooth, heidelberg_2012_2016_mean_smooth,
                       heidelberg_2012_2016_stdevs_smooth)
print()
print()

""" paired t-tests of each of the datasets"""
print('Baring Head vs Cape Grim between 1986 - 1991 using CCGCRV Trend Fit', file=f)
two_tail_paired_t_test(bhd_1986_1991_mean_trend, bhd_1986_1991_stdevs_trend, heidelberg_1986_1991_mean_trend,
                       heidelberg_1986_1991_stdevs_trend)
print()
print()
print('Baring Head vs Cape Grim between 1991 - 1994 using CCGCRV Trend Fit', file=f)
two_tail_paired_t_test(bhd_1991_1994_mean_trend, bhd_1991_1994_stdevs_trend, heidelberg_1991_1994_mean_trend,
                       heidelberg_1991_1994_stdevs_trend)
print()
print()
print('Baring Head vs Cape Grim between 2000 - 2016 using CCGCRV Trend Fit', file=f)
two_tail_paired_t_test(bhd_2006_2016_mean_trend, bhd_2006_2016_stdevs_trend, heidelberg_2006_2016_mean_trend,
                       heidelberg_2006_2016_stdevs_trend)
print()
print()
print('Baring Head vs Cape Grim between 2006 - 2009 using CCGCRV Trend Fit', file=f)
two_tail_paired_t_test(bhd_2006_2009_mean_trend, bhd_2006_2009_stdevs_trend, heidelberg_2006_2009_mean_trend,
                       heidelberg_2006_2009_stdevs_trend)
print()
print()
print('Baring Head vs Cape Grim between 2012 - 2016 using CCGCRV Trend Fit', file=f)
two_tail_paired_t_test(bhd_2012_2016_mean_trend, bhd_2012_2016_stdevs_trend, heidelberg_2012_2016_mean_trend,
                       heidelberg_2012_2016_stdevs_trend)

# testing that the functions will plot later, as I've had trouble with this before...
# plt.scatter(my_x_1986_1991, bhd_1986_1991_mean_smooth)
# plt.scatter(my_x_1986_1991, bhd_1986_1991_mean_trend)
# plt.scatter(my_x_1986_1991, heidelberg_1986_1991_mean_smooth)
# plt.scatter(my_x_1986_1991, heidelberg_1986_1991_mean_trend)
# plt.scatter(my_x_1991_1994, bhd_1991_1994_mean_smooth)
# plt.scatter(my_x_1991_1994, bhd_1991_1994_mean_trend)
# plt.scatter(my_x_1991_1994, heidelberg_1991_1994_mean_smooth)
# plt.scatter(my_x_1991_1994, heidelberg_1991_1994_mean_trend)
# plt.scatter(my_x_2006_2009_trimmed, bhd_2006_2009_mean_smooth)
# plt.scatter(my_x_2006_2009_trimmed, bhd_2006_2009_mean_trend)
# plt.scatter(my_x_2006_2009_trimmed, heidelberg_2006_2009_mean_smooth)
# plt.scatter(my_x_2006_2009_trimmed, heidelberg_2006_2009_mean_trend)
# plt.scatter(my_x_2012_2016_trimmed, bhd_2012_2016_mean_smooth)
# plt.scatter(my_x_2012_2016_trimmed, bhd_2012_2016_mean_trend)
# plt.scatter(my_x_2012_2016_trimmed, heidelberg_2012_2016_mean_smooth)
# plt.scatter(my_x_2012_2016_trimmed, heidelberg_2012_2016_mean_trend)
# plt.show()

"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
Answering the Question "Does time in the collection flask alter final 14C value?
To answer this: first we looked at difference in measurement - collection time. This is good initially but doesn't
account for situation in which the CO2 was extracted from the flask early and not measured for a while.
Therefore I will rely on the data where we have all 1) collection, 2) extraction and 3) measurement data.
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
"""
"""
The below block of code was used for the file in which we have measurement but not extraction data. Ignore for now.
"""
# df2_dates = df2_dates.drop(columns=['∆14C', '∆14C_err',
#                                     'Flag', 'CollectionMethod'], axis=1)
# df2_dates = df2_dates.dropna(subset=['DateMeasured'])
# df2_dates = df2_dates.reset_index()
# # change the format of dates in the df2_dates
# forchange = df2_dates['DateMeasured']
# forchange = long_date_to_decimal_date(forchange)
# df2_dates['DateMeasured_Decimal'] = forchange
#
# # find the difference between measurement date and collection date and append this to the measurement file
# df2_dates['difference'] = df2_dates['DateMeasured_Decimal'] - np.float64(df2_dates['DecimalDateCollected'])
# # rename the New Zealand ID for easy merging along this axis
# df2_dates = df2_dates.rename(columns={"NZ/NZA": "NZ"})
# # drop more columns to simplify the merge
# df2_dates = df2_dates.drop(columns=['index', 'DecimalDateCollected', 'DateMeasured',
#                                     'DateMeasured_Decimal'], axis=1)
# df2_dates.drop_duplicates(subset ="NZ", keep = False, inplace = True)
#
# baringhead = baringhead.merge(df2_dates, how='outer')
# baringhead = baringhead.dropna(subset=['DELTA14C'])
# # baringhead.to_excel('testing2.xlsx')

"""
This block of code deals with the extraction dates.
I'll merge this data with the baring head file, and compare how far the D14C data is from the trend-line as a function
of time waiting in the flask.

"""
extraction_dates = extraction_dates.drop(columns=['Job', 'Samples::Sample Description', 'Samples::Sample ID',
                                                  'AMS Submission Results Complete::Collection Date',
                                                  'AMS Submission Results Complete::DELTA14C',
                                                  'AMS Submission Results Complete::DELTA14C_Error',
                                                  'AMS Submission Results Complete::Weight Initial',
                                                  'AMS Submission Results Complete::TP',
                                                  'AMS Submission Results Complete::TW',
                                                  'AMS Submission Results Complete::Date Run',
                                                  'AMS Submission Results Complete::delta13C_IRMS',
                                                  'AMS Submission Results Complete::delta13C_AMS',
                                                  'AMS Submission Results Complete::F_corrected_normed',
                                                  'AMS Submission Results Complete::F_corrected_normed_error',
                                                  'Graphite Completed::End Date', 'Graphite Completed::CO2_Yield',
                                                  'Graphite Completed::Prebake_Yield',
                                                  'Graphite Completed::Graphite_Yield',
                                                  'AMS Submission Results Complete::Quality Flag',
                                                  'Samples::Pretreatment by Submitter', 'Samples::Sample Date Start',
                                                  'Samples::Sample Time Start', 'Samples::Sample Date End',
                                                  'Samples::Sample Time End', 'Samples::Sample Days Exposed',
                                                  'Samples::Latitude', 'Samples::Longitude', 'Samples::Location',
                                                  'Samples::Sampling Height'], axis=1)

extraction_dates = extraction_dates.rename(columns={"NZA": "NZ"})
# With this line, the baring head data is now merged with that of the extraction dates.
baringhead = baringhead.merge(extraction_dates, how='outer')
# This line creates a new DataFrame that includes only data that has an extraction date. This
# is an easier way to dump the data into an excel file for viewing.
baringhead_plus_extract = baringhead.dropna(subset='Extraction of CO2 from Air Date')

"""
There is more data in the "extraction date" column than the other column after this merge because
There is excess data without NZ numbers in the orginal file.
Right now I'm only taking data that has a unique NZ number.
"""

baringhead_plus_extract = baringhead_plus_extract.dropna(subset='DELTA14C')
baringhead_plus_extract = baringhead_plus_extract.reset_index(drop=True)

# now I need to grab the extraction dates and convert them to decimals to compare with DEC_DECAY_CORR.
extract_date = baringhead_plus_extract['Extraction of CO2 from Air Date']
extract_date = long_date_to_decimal_date(extract_date)
baringhead_plus_extract['DateExtracted_Decimal'] = extract_date  # add the new column of decimal data onto DataFrame
# find the difference between collection and extraction in time.
baringhead_plus_extract['Differences'] = baringhead_plus_extract['DateExtracted_Decimal'] \
                                         - baringhead_plus_extract['DEC_DECAY_CORR']

# re-extract all data after 2012 from the original Baring Head data-file so we can create a new smooth curve
# to compare against (the next three lines contain the data I'll use to create the new smooth fit).
baringhead_timetest = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2012)]
x_timetest = baringhead_timetest['DEC_DECAY_CORR'].reset_index(drop=True)
y_timetest = baringhead_timetest['DELTA14C'].reset_index(drop=True)

# these are the data we want to test
x_extracts = baringhead_plus_extract['DEC_DECAY_CORR'].reset_index(drop=True)
y_extracts = baringhead_plus_extract['DELTA14C'].reset_index(drop=True)
time_extracts = baringhead_plus_extract['Differences'].reset_index(drop=True)

time_test = ccgFilter(x_timetest, y_timetest, cutoff).getTrendValue(x_extracts)
delta = y_extracts - time_test

"""
Now I want to plot: the time waiting in the flask VS deviation in the measured value from the smoothed fit.
"""


"""
LOOKS LIKE NO TREND, JUST SCATTER, using both getTREND and getSMOOTH values.
"""

"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
Answering the Question "What about the monthly means?"
We should at least do this simple analysis at the very minimum to say that we did it this way.

First, I'll grab the monthly means of both datasets (Full BHD and Heidelberg),
and then snip the BHD data to only be as large as heidelberg,
and then do a paired t-test to see where they're different.
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
"""

# TODO fix this code so it chops off the decimals or something and makes all the months the same (
test = monthly_averages(xtot_bhd, ytot_bhd, ztot_bhd)

test_x = test[0]
test_y = test[1]
test_z = test[2]
df_test = pd.DataFrame({'x': test_x, 'y_bhd': test_y, 'z_bhd': test_z})

test2 = monthly_averages(xtot_heid, ytot_heid, ztot_heid)
test2_x = test2[0]
test2_y = test2[1]
test2_z = test2[2]
df_test2 = pd.DataFrame({'x': test2_x, 'y_heid': test2_y, 'z_heid': test2_z})  # putting both into a dataframe so I can merge on the similar dates

df_test3 = df_test.merge(df_test2, how='outer')
df_test3.to_excel('testing2.xlsx')
df_test3 = df_test3.dropna(subset='y_heid')
df_test3 = df_test3.dropna(subset='y_bhd')
df_test3 = df_test3.reset_index(drop=True)
# print(df_test3)


df_test3.to_excel('testing2.xlsx')
test3_x = df_test3['x']
test3_y_bhd = df_test3['y_bhd']
test3_y_heid = df_test3['y_heid']
test3_z_bhd = df_test3['z_bhd']
test3_z_heid = df_test3['z_heid']
"""
There is 194 cases in which we have the monthly averages for both BHD and Heid in the same month.
The lines above where I dropna on both datasets is to find only the months where they are the same.

Now I can do a quick paired t-test, lets see if they are the same...
"""

# plt.scatter(test3_x, test3_y_bhd)
# plt.scatter(test3_x, test3_y_heid)
# # plt.show()

#  order to do a two-tail paired t-test, I need to propogate the uncertainties in the monthly averages function...
print('Here is the result of the paired t-test between BHD and CGO Monthly means for all instances where data overlaps', file=f)
two_tail_paired_t_test(test3_y_bhd, test3_z_bhd, test3_y_heid, test3_z_heid)


f.close()

"""
Monthly averages two-tailed t-test also finds a difference.
"""

"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
MAIN FIGURES FOR THE PAPER
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################




# REMEMBER WHEN PLOTTING, THE FOLLOWING SETS OF DATA GO TOGETHER:

PRE - CCGCRV FIT:

x1_bhd -> y1_bhd (the raw data)
my_x_1986_1991 -> y - output from the CCGCRV curve smoother.

"""

# """ FIGURE 1: OVERVIEW OF DATA WE'RE INTERESTED IN """
# general plot parameters
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5
"""
Figure 1. All the data together
"""
fig = plt.figure(1)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size1)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size1)
plt.legend()
plt.title('All available data after 1980')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison2/interlab_comparison/plots/FirstDraft_Fig1.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
Figure 2. Visual Example of the randomization and smoothing process.
"""
fig = plt.figure(2)

plt.title('Visualization of Monte Carlo and CCGCRV Process: 1987-1991 BHD')
plt.errorbar(xtot_bhd, ytot_bhd, label='CGO Data' , yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
plt.scatter(x1_bhd, data1, color = colors[0], label = 'Monte Carlo Iteration 1', alpha = 0.35, marker = 'x')
plt.scatter(x1_bhd, data2, color = colors[1],  label = 'Monte Carlo Iteration 2', alpha = 0.35, marker = '^')
plt.scatter(x1_bhd, data3, color = colors[2],  label = 'Monte Carlo Iteration 3', alpha = 0.35, marker = 's')
plt.plot(xs, curve1, color = colors[0], alpha = 0.35, linestyle = 'dotted')
plt.plot(xs, curve2, color = colors[1], alpha = 0.35, linestyle = 'dashed')
plt.plot(xs, curve3, color = colors[2], alpha = 0.35, linestyle = 'dashdot')
plt.plot(xs, means, color = 'red',  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
plt.plot(xs, means2, color = 'blue',  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([1989, 1991])
plt.ylim([140, 170])
plt.legend()
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison2/interlab_comparison/plots/FirstDraft_Figure2.png',
            dpi=300, bbox_inches="tight")
# plt.show()
plt.close()

"""
Figure 3. A breakdown of the 4 period of time that we test for the intercomparison,
and how the smooth and trend data compare for each.
"""
size2 = 15
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.1)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.1)
plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_smooth, color=colors[3], label = 'BHD CCGCRV Smooth Fit')
plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_trend, color=colors[3], label = 'BHD CCGCRV Trend Fit', linestyle = 'dashed')
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_smooth, color=colors2[3], label = 'CGO CCGCRV Smooth Fit')
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_trend, color=colors2[3], label = 'CGO CCGCRV Trend Fit', linestyle = 'dashed')
plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_trend, color=colors[3], linestyle = 'dashed')
plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_trend, color=colors2[3], linestyle = 'dashed')
plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_trend, color=colors[3], linestyle = 'dashed')
plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_trend, color=colors2[3], linestyle = 'dashed')
plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_trend, color=colors[3], linestyle = 'dashed')
plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_trend, color=colors2[3], linestyle = 'dashed')
plt.axvline(x = 1987, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 1991, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 1994, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2006, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2009, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2012, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2016, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.arrow(1994, 50, -6, 0,  fc="k", ec="k",head_width=0.05, head_length=0.1 )
plt.xlabel('Date', fontsize=14)  # label the y axis
plt.ylim([0, 200])
plt.xlim([1986, 2020])
plt.legend()
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison2/interlab_comparison/plots/FirstDraft_Figuretest.png',
            dpi=300, bbox_inches="tight")
# plt.show()
plt.close()

fig = plt.figure(4, figsize=(10 ,3))
gs = gridspec.GridSpec(1, 8)
gs.update(wspace=1, hspace=0.1)
# Generate first panel
# remember, the grid spec is rows, then columns

print(type(my_x_1986_1991))
print(type(np.array(my_x_1986_1991)))
print(type(bhd_1986_1991_mean_smooth))

xtr_subsplot = fig.add_subplot(gs[0:1, 0:2])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_smooth, color=colors[3])
# plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_trend, color=colors[3])
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_smooth, color=colors2[3])
# plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1986_1991)), max(np.array(my_x_1986_1991))])
plt.ylim([min(bhd_1986_1991_mean_smooth), max(bhd_1986_1991_mean_smooth)])
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:1, 2:4])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_smooth, color=colors[3])
# plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_trend, color=colors[3])
plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_smooth, color=colors2[3])
# plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1991_1994)), max(np.array(my_x_1991_1994))])
plt.ylim([min(bhd_1991_1994_mean_smooth), max(bhd_1991_1994_mean_smooth)])


xtr_subsplot = fig.add_subplot(gs[0:1, 4:6])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_smooth, color=colors[3])
# plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_trend, color=colors[3])
plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_smooth, color=colors2[3])
# plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2006_2009_trimmed)), max(np.array(my_x_2006_2009_trimmed))])
plt.ylim([min(bhd_2006_2009_mean_smooth), max(bhd_2006_2009_mean_smooth)])

xtr_subsplot = fig.add_subplot(gs[0:1, 6:8])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_smooth, color=colors[3], label='Baring Head CCGCRV Fit')
# plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_trend, color=colors[3])
plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_smooth, color=colors2[3], label='Cape Grim CCGCRV Fit')
# plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2012_2016_trimmed)), max(np.array(my_x_2012_2016_trimmed))])
plt.ylim([min(bhd_2012_2016_mean_smooth), max(bhd_2012_2016_mean_smooth)])
plt.legend(loc=(1.04,0.5))
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison2/interlab_comparison/plots/FirstDraft_Figure3a.png',
            dpi=300, bbox_inches="tight")
# plt.show()
plt.close()


fig = plt.figure(4, figsize=(10 ,3))
gs = gridspec.GridSpec(1, 8)
gs.update(wspace=1, hspace=0.1)
# Generate first panel
# remember, the grid spec is rows, then columns

print(type(my_x_1986_1991))
print(type(np.array(my_x_1986_1991)))
print(type(bhd_1986_1991_mean_smooth))

xtr_subsplot = fig.add_subplot(gs[0:1, 0:2])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_trend, color=colors[3])
# plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1986_1991)), max(np.array(my_x_1986_1991))])
plt.ylim([min(bhd_1986_1991_mean_smooth), max(bhd_1986_1991_mean_smooth)])

plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:1, 2:4])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_trend, color=colors[3])
# plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1991_1994)), max(np.array(my_x_1991_1994))])
plt.ylim([min(bhd_1991_1994_mean_smooth), max(bhd_1991_1994_mean_smooth)])


xtr_subsplot = fig.add_subplot(gs[0:1, 4:6])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_trend, color=colors[3])
# plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2006_2009_trimmed)), max(np.array(my_x_2006_2009_trimmed))])
plt.ylim([min(bhd_2006_2009_mean_smooth), max(bhd_2006_2009_mean_smooth)])

xtr_subsplot = fig.add_subplot(gs[0:1, 6:8])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_trend, color=colors[3])
# plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2012_2016_trimmed)), max(np.array(my_x_2012_2016_trimmed))])
plt.ylim([min(bhd_2012_2016_mean_smooth), max(bhd_2012_2016_mean_smooth)])
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison2/interlab_comparison/plots/FirstDraft_Figure3b.png',
            dpi=300, bbox_inches="tight")
# plt.show()
plt.close()


"""
Figure S1. Visual Example of the randomization and smoothing process, broken into 4 panels.
"""
fig = plt.figure(4, figsize=(10,3))
gs = gridspec.GridSpec(1, 8)
gs.update(wspace=1, hspace=0.1)
# Generate first panel
# remember, the grid spec is rows, then columns
size2 = 15
xtr_subsplot = fig.add_subplot(gs[0:1, 0:2])
# plot data for left panel
plt.text(1990.75, 167.5, "A", fontsize=12)
plt.errorbar(xtot_bhd, ytot_bhd, label='CGO Data' , yerr=ztot_bhd, fmt='none', color='black', ecolor='black', elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color='black', s=size2)
plt.scatter(x1_bhd, data1, color = colors[0], label = 'Monte Carlo Iteration 1', alpha = 0.35, marker = 'x', s = size2)
plt.scatter(x1_bhd, data2, color = colors[1],  label = 'Monte Carlo Iteration 2', alpha = 0.35, marker = '^', s = size2)
plt.scatter(x1_bhd, data3, color = colors[2],  label = 'Monte Carlo Iteration 3', alpha = 0.35, marker = 's', s = size2)
# plt.plot(xs, curve1, color = colors[0], alpha = 0.35, linestyle = 'dotted')
# plt.plot(xs, curve2, color = colors[1], alpha = 0.35, linestyle = 'dashed')
# plt.plot(xs, curve3, color = colors[2], alpha = 0.35, linestyle = 'dashdot')
# plt.plot(xs, means, color = 'red',  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
# plt.plot(xs, means2, color = 'blue',  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([1989, 1991])
plt.ylim([140, 170])

plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:1, 2:4])
# plot data for left panel
plt.text(1990.75, 167.5, "B", fontsize=12)
plt.errorbar(xtot_bhd, ytot_bhd, label='CGO Data' , yerr=ztot_bhd, fmt='none', color='black', ecolor='black', elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color='black', s=size2)
plt.scatter(x1_bhd, data1, color = colors[0], label = 'Monte Carlo Iteration 1', alpha = 0.35, marker = 'x', s = size2)
plt.scatter(x1_bhd, data2, color = colors[1],  label = 'Monte Carlo Iteration 2', alpha = 0.35, marker = '^', s = size2)
plt.scatter(x1_bhd, data3, color = colors[2],  label = 'Monte Carlo Iteration 3', alpha = 0.35, marker = 's', s = size2)
plt.plot(xs, curve1, color = colors[0], alpha = 0.35, linestyle = 'dotted')
plt.plot(xs, curve2, color = colors[1], alpha = 0.35, linestyle = 'dashed')
plt.plot(xs, curve3, color = colors[2], alpha = 0.35, linestyle = 'dashdot')
# plt.plot(xs, means, color = 'red',  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
# plt.plot(xs, means2, color = 'blue',  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([1989, 1991])
plt.ylim([140, 170])
plt.text(1991.5,135,'Date')
xtr_subsplot.set_yticklabels([])

xtr_subsplot = fig.add_subplot(gs[0:1, 4:6])
# plot data for left panel
plt.text(1990.75, 167.5, "C", fontsize=12)
plt.errorbar(xtot_bhd, ytot_bhd, label='CGO Data' , yerr=ztot_bhd, fmt='none', color='black', ecolor='black', elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color='black', s=size2)
plt.scatter(x1_bhd, data1, color = colors[0], label = 'Monte Carlo Iteration 1', alpha = 0.35, marker = 'x', s = size2)
plt.scatter(x1_bhd, data2, color = colors[1],  label = 'Monte Carlo Iteration 2', alpha = 0.35, marker = '^', s = size2)
plt.scatter(x1_bhd, data3, color = colors[2],  label = 'Monte Carlo Iteration 3', alpha = 0.35, marker = 's', s = size2)
plt.plot(xs, curve1, color = colors[0], alpha = 0.35, linestyle = 'dotted')
plt.plot(xs, curve2, color = colors[1], alpha = 0.35, linestyle = 'dashed')
plt.plot(xs, curve3, color = colors[2], alpha = 0.35, linestyle = 'dashdot')
plt.plot(xs, means, color = 'red',  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
# plt.plot(xs, means2, color = 'blue',  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([1989, 1991])
plt.ylim([140, 170])
xtr_subsplot.set_yticklabels([])

xtr_subsplot = fig.add_subplot(gs[0:1, 6:8])
# plot data for left panel
plt.text(1990.75, 167.5, "D", fontsize=12)
plt.errorbar(xtot_bhd, ytot_bhd, label='CGO Data' , yerr=ztot_bhd, fmt='none', color='black', ecolor='black', elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color='black', s=size2)
plt.scatter(x1_bhd, data1, color = colors[0], label = 'Monte Carlo Iteration 1', alpha = 0.35, marker = 'x', s = size2)
plt.scatter(x1_bhd, data2, color = colors[1],  label = 'Monte Carlo Iteration 2', alpha = 0.35, marker = '^', s = size2)
plt.scatter(x1_bhd, data3, color = colors[2],  label = 'Monte Carlo Iteration 3', alpha = 0.35, marker = 's', s = size2)
plt.plot(xs, curve1, color = colors[0], alpha = 0.35, linestyle = 'dotted')
plt.plot(xs, curve2, color = colors[1], alpha = 0.35, linestyle = 'dashed')
plt.plot(xs, curve3, color = colors[2], alpha = 0.35, linestyle = 'dashdot')
plt.plot(xs, means, color = 'red',  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
plt.plot(xs, means2, color = 'blue',  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([1989, 1991])
plt.ylim([140, 170])
plt.legend(loc=(1.04,0.5))
xtr_subsplot.set_yticklabels([])

plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison2/interlab_comparison/plots/FirstDraft_S1.png',
            dpi=300, bbox_inches="tight")
# plt.show()
plt.close()

"""
Figure S2. Does the time CO2 sits in flask between collection and extraction impact 14C value?
"""
fig = plt.figure(1)
plt.scatter(time_extracts, delta, marker='o', label='Rafter Baring Head Record (BHD)', color=colors2[3], s=20)
plt.legend()
plt.title('Does the time CO2 sits in flask between collection and extraction impact 14C value? ')
plt.xlabel('Decimal interval (Extraction - Collection)', fontsize=14)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison2/interlab_comparison/plots/FirstDraft_S2.png',
            dpi=300, bbox_inches="tight")
plt.close()