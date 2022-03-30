import numpy as np
from PyAstronomy import pyasl
import pandas as pd
from numpy.fft import fft, ifft
from tabulate import tabulate
import random
from miller_curve_algorithm import ccgFilter
import matplotlib.pyplot as plt
import seaborn as sns

# dfx = pd.read_excel(
#     r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Stats and Data Analysis\Matlab and Python Files\tables.xlsx',
#     sheet_name='t-table0_05')
# dfx = dfx.reset_index()
# t_table_05 = dfx[0.05]
x = random.sample(range(10, 30), 10)  # for testing
x2 = random.sample(range(10, 20), 10)  # for testing

"""
In the Miller code, it getMonthlymeans returns a column of years, and a column of
months, and I need a way to get decimal dates out of it for plotting. This code does that.
you need:
x = year data
y = month data
"""


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
The following code will transfer a date in form:
dd/mm/yyyy to a decimal date, more useful for curve smoothing
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


# returns the array/list back but in the decimal form

"""
My rough attempt to curve fit a line before I got the John Miller Code working
Ensure the data has been re-indexed before putting through here or it won't work.
"""


def cbl_curve_fit(x, y):
    n = 4
    empty_array = []  # pre-allocate an array where the for loop will put the coefficient outputs
    cols = []  # empty array pre-allocated for the columns needed in new dataframe
    for i in range(0, n):
        p = np.polyfit(x, y, i, rcond=None, full=False, w=None, cov=False)  # multiple and linear polynomial fits
        print(type(p))
        empty_array.append(p)
        cols.append(i)
    coeff = pd.DataFrame(empty_array, columns=cols)  # output the results from for loop into dataframe
    coeffs = pd.DataFrame(empty_array, columns=['0', '1', '2', '3'])  # output the results from for loop into dataframe

    degree0 = coeff.iloc[0]
    degree1 = coeff.iloc[1]
    degree2 = coeff.iloc[2]
    degree3 = coeff.iloc[3]

    y_guess_0th = degree0[0] * x ** 0
    y_guess_lin = degree1[0] * x ** 1 + degree1[1] * x ** 0
    y_guess_2nd = degree2[0] * x ** 2 + degree2[1] * x ** 1 + degree2[2] * x ** 0
    y_guess_3rd = degree3[0] * x ** 3 + degree3[1] * x ** 2 + degree3[2] * x ** 1 + degree3[3] * x ** 0
    #
    Degree_to_test = y_guess_3rd
    residual = y - Degree_to_test

    # # TRANSFORM RESIDUAL
    G = fft(residual)
    G = abs(G)

    # # CREATE LOW PASS FILTER
    fs = 0.1  # sampling frequency
    x_new = np.arange(0, len(G))
    x_new = x_new * 0.1  # setting the data to be measured once per second (10 Hz)
    delta = 1 / (len(G) * fs)  # parameter used to calculate the frequency
    k = np.arange(0, len(G), 1)  # list from 0 to 3952
    freq = k * delta
    cutoff = 667
    f_c = 365 / cutoff
    p = 4
    ln2 = -.0693
    H_f = np.exp(ln2 * (freq / f_c) ** p)

    # MULTIPLY FUNCTION BY FILTER AND SMOOTH LINE
    residual_forinv = G * H_f
    G_new = ifft(residual_forinv)
    G_new = np.real(G_new)
    smoothed_trend = G_new + y_guess_3rd

    return smoothed_trend, print(type(p))


"""
A standard student's two-tail t-test that will require two lists/arrays as input
https://www.youtube.com/watch?v=pTmLQvMM-1M&ab_channel=BozemanScience
Null Hypothesis = there is NO difference between the samples
If t-value is lower than critical value, DON'T REJECT NULL = NO DIFFERENCE
If t-value is higher than critical value, REJECT = DIFFERENCE EXISTS

this test uses 0.05 probability

THIS METHOD DOES NOT WORK YET - MUST DEAL WITH VARIABLE D_of_F's not equal to those in table
"""


# def simple_t_test(x1, x2):
# TODO FIX CRITICAL VALUE LOOKUP
# dfx = pd.read_excel(
#     r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Stats and Data Analysis\Matlab and Python Files\tables.xlsx',
#     sheet_name='t table', skiprows=6)
# dfx = dfx.reset_index()
# t_table_05 = dfx[0.05]
#
# # get the rough data needed for a t-test
# mean_x1 = np.average(x1)
# mean_x2 = np.average(x2)
# var_x1 = np.var(x1)
# var_x2 = np.var(x2)
#
# # the math
# mean = abs(mean_x2 - mean_x1)
# denominator = np.sqrt((var_x1 / len(x1)) + (var_x2 / len(x2)))
# t_value = mean / denominator
# d_of_f = len(x1) + len(x2) - 2 + 2  # usually you subtract two, but length starts at zero so I add them back in
#
# # find the degrees of freedom, and the closest number in the table to my degrees of freedom
# aux = []
# for valor in t_table_05:
#     aux.append(abs(d_of_f - valor))
# index = aux.index(min(aux))
# value_crit = t_table_05[index]
#
# if t_value <= value_crit:
#     result = print('There is NO DIFFERENCE')
# else:
#     result = print('There IS A DIFFERENCE')
# return result


# http://ipl.physics.harvard.edu/wp-uploads/2013/03/PS3_Error_Propagation_sp13.pdf
# computes the basic analytical data for TWO (ONLY TWO) datasets


def basic_analysis(x, y, name1, name2):
    # compute data for individual datasets

    x_mean = np.average(x)
    y_mean = np.average(y)
    x_stddev = np.std(x)
    y_stddev = np.std(y)
    x_std_err = x_stddev / np.sqrt(len(x))
    y_std_err = y_stddev / np.sqrt(len(y))

    # compute data for datasets together
    average = (x_mean + y_mean) / 2
    error_prop = (np.sqrt(x_stddev ** 2 + y_stddev ** 2)) / 2

    data = [[name1, x_mean, x_std_err, len(x)],
            [name2, y_mean, y_std_err, len(y)],
            ['Both Series', average, error_prop]]
    table2 = (tabulate(data, headers=["Label", "Average", "Std Error / Prop Error"]))
    df = pd.DataFrame(data=data)
    return df


# def monte_carlo_randomization_trend(x_init, fake_x, y_init, y_error, cutoff, n):
#     """ Part 1 of this long function randomizes that data within its uncertainty "n" times. """
#     new_array = y_init  # create a new variable on which we will later v-stack randomized lists
#     for i in range(0, n):
#         empty_array = []
#         for j in range(0, len(y_init)):
#             a = y_init[j]  # grab the first item in the set
#             b = y_error[j]  # grab the uncertainty
#             rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
#             c = a + rand  # add this to the number
#             empty_array.append(c)  # add this to a list
#             # print(len(empty_array))
#         new_array = np.vstack((new_array, empty_array))
#     print(new_array)

#     template_array = ccgFilter(x_init, y_init, cutoff).getTrendValue(fake_x)  # inital values for stacking
#     for k in range(0, len(new_array)):
#         row = new_array[k]  # grab the first row of the data
#         smooth = ccgFilter(x_init, row, cutoff).getTrendValue(fake_x)  # outputs smooth values at my desired times, x
#         template_array = np.hstack((template_array, smooth))
#
#     df = pd.DataFrame(template_array)
#
#     mean_array = []
#     stdev_array = []
#     upper_array = []
#     lower_array = []
#     for i in range(0, len(template_array)):
#         element1 = np.sum(template_array[i])  # grab the first ROW of the dataframe and take the sum
#         mean = element1 / len(template_array[i])  # find the mean of all the values from the Monte Carlo
#         mean_array.append(mean)  # append it to a new array
#
#         stdev = np.std(template_array[i])  # grab the first ROW of the dataframe find the stdev
#         stdev_array.append(stdev)
#
#         upper = mean + stdev
#         lower = mean - stdev
#         upper_array.append(upper)
#         lower_array.append(lower)
#
#     return new_array, template_array, mean_array, stdev_array, upper_array, lower_array, fake_x
#
#
# def monte_carlo_randomization_smooth(x_init, fake_x, y_init, y_error, cutoff, n):
#     """ Part 1 of this long function randomizes that data within its uncertainty "n" times. """
#     new_array = y_init  # create a new variable on which we will later v-stack randomized lists
#     for i in range(0, n):
#         empty_array = []
#         for j in range(0, len(y_init)):
#             a = y_init[j]  # grab the first item in the set
#             b = y_error[j]  # grab the uncertainty
#             rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
#             c = a + rand  # add this to the number
#             empty_array.append(c)  # add this to a list
#             # print(len(empty_array))
#         new_array = np.vstack((new_array, empty_array))
#
#     template_array = ccgFilter(x_init, y_init, cutoff).getSmoothValue(fake_x)  # inital values for stacking
#     for k in range(0, len(new_array)):
#         row = new_array[k]  # grab the first row of the data
#         smooth = ccgFilter(x_init, row, cutoff).getTrendValue(fake_x)  # outputs smooth values at my desired times, x
#         template_array = np.hstack((template_array, smooth))
#
#     df = pd.DataFrame(template_array)
#
#     mean_array = []
#     stdev_array = []
#     upper_array = []
#     lower_array = []
#     for i in range(0, len(template_array)):
#         element1 = np.sum(template_array[i])  # grab the first ROW of the dataframe and take the sum
#         mean = element1 / len(template_array[i])  # find the mean of all the values from the Monte Carlo
#         mean_array.append(mean)  # append it to a new array
#
#         stdev = np.std(template_array[i])  # grab the first ROW of the dataframe find the stdev
#         stdev_array.append(stdev)
#
#         upper = mean + stdev
#         lower = mean - stdev
#         upper_array.append(upper)
#         lower_array.append(lower)
#
#     return new_array, template_array, mean_array, stdev_array, upper_array, lower_array, fake_x
#

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
    print('Error of mean is' + str(err_mean))

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
        print('There is NO DIFFERENCE. ' +
              'Critical value: ' + str(value_crit) +
              ', t-stat: ' + str(t_stat) + '\u00B1 ' + str(t_stat_e6) +
              ', mean: ' + str(mean1) + '\u00B1 ' + str(err_mean) +
              'degrees of freedom = ' + str(d_of_f))
        result = 1

    else:
        print('There is A DIFFERENCE. ' +
              ' Critical value: ' + str(value_crit) +
              ', t-stat: ' + str(t_stat) + ' \u00B1 ' + str(t_stat_e6) +
              ', mean: ' + str(mean1) + ' \u00B1 ' + str(err_mean) +
              'degrees of freedom = ' + str(d_of_f))
        result = 0

    return result


def monthly_averages(x_values, y_values):
    x_values = np.array(x_values)
    y_values = np.array(y_values)

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
    for i in range(0, len(lin1)):  # loop in the years
        year = int(lin1[i])  # grab only the integer parts of the years in the data

        for j in range(0, len(months)):  # loop in the months

            temparray_x = []
            temparray_y = []
            # print('The current month is ' + str(months[j]) + 'in year ' + str(year))
            months_min = months[j]
            # TODO fix this line of code to filter between one month and the next more accurately
            months_max = months_min + 0.08

            for k in range(0, len(y_values)):  # grab the data i want to use
                y_current = y_values[k]
                x_current = x_values[k]
                x_decimal_only = x_current - int(x_current)
                x_int = int(x_current)
                # if my data exists in the time frame I'm currently searching through,
                if (x_int == year) and (x_decimal_only >= months_min) and (x_decimal_only < months_max):
                    # append that x and y data to initialized arrays
                    temparray_x.append(x_int + months_min)
                    temparray_y.append(y_current)

            # if at the end of the month, the length of the temporary arrays are non-zero,
            # clean and append that information to a permanent array
            if len(temparray_x) != 0:
                tempsum = sum(temparray_x)
                tempmean = tempsum / len(temparray_x)

                tempsum2 = sum(temparray_y)
                tempmean2 = tempsum2 / len(temparray_y)

                permarray_x.append(tempmean)
                permarray_y.append(tempmean2)

            # else:
            #     permarray_x.append(x_int + months_min)
            #     permarray_y.append(-999)

    return permarray_x, permarray_y


"""
The next three functions are integral to the intercomparison of time series radiocarbon data
"""
def randomization(y_init, y_error, n):
    """ this first randomizes that data within its uncertainty "n" times. """
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
        new_array = np.vstack((new_array, empty_array))
    new_array_dataframe = pd.DataFrame(new_array)  # each row is a randomized array
    return new_array, new_array_dataframe

""" 
this second function puts the output from the first function through the ccgcrv curve smoother
and outputs the data
"""

def ccgcrv_trend(x_init, y_init, cutoff, fake_x, randomized_array):
    template_array = ccgFilter(x_init, y_init, cutoff).getTrendValue(fake_x)  # inital values for stacking
    for i in range(0, len(randomized_array) - 1):  # minus 1 because there is one randomized row already stacked.
        row = randomized_array[i]  # grab the first row of the data

        trend = ccgFilter(x_init, row, cutoff).getTrendValue(fake_x)  # outputs smooth values at my desired times, x
        template_array = np.hstack((template_array, trend))

    template_array = pd.DataFrame(template_array)

    mean_array = []
    stdev_array = []
    upper_array = []
    lower_array = []
    for i in range(0, len(template_array)):
        row = template_array.iloc[i]  # grab the first row of the transformed DataFrame
        sums = np.sum(row)  # take the sum of all the numbers in that row
        mean = sums / len(row)  # find the mean
        mean_array.append(mean)  # append each mean to an array

        stdevs = np.std(row)
        stdev_array.append(stdevs)

        upper = mean + stdevs
        lower = mean - stdevs
        upper_array.append(upper)
        lower_array.append(lower)
    print(mean_array)
    return template_array, mean_array, stdev_array, upper_array, lower_array

def ccgcrv_smooth(x_init, y_init, cutoff, fake_x, randomized_array):
    template_array = ccgFilter(x_init, y_init, cutoff).getSmoothValue(fake_x)  # inital values for stacking
    for i in range(0, len(randomized_array) - 1):  # minus 1 because there is one randomized row already stacked.
        row = randomized_array[i]  # grab the first row of the data

        trend = ccgFilter(x_init, row, cutoff).getSmoothValue(fake_x)  # outputs smooth values at my desired times, x
        template_array = np.hstack((template_array, trend))

    template_array = pd.DataFrame(template_array)

    mean_array = []
    stdev_array = []
    upper_array = []
    lower_array = []
    for i in range(0, len(template_array)):
        row = template_array.iloc[i]  # grab the first row of the transformed DataFrame
        sums = np.sum(row)  # take the sum of all the numbers in that row
        mean = sums / len(row)  # find the mean
        mean_array.append(mean)  # append each mean to an array

        stdevs = np.std(row)
        stdev_array.append(stdevs)

        upper = mean + stdevs
        lower = mean - stdevs
        upper_array.append(upper)
        lower_array.append(lower)
    print(mean_array)
    return template_array, mean_array, stdev_array, upper_array, lower_array















































#
# def ccgcrv_trend(x_init, y_init, cutoff, fake_x, randomized_array):
#     template_array = ccgFilter(x_init, y_init, cutoff).getTrendValue(fake_x)  # inital values for stacking
#     for i in range(0, len(randomized_array) - 1):  # minus 1 because there is one randomized row already stacked.
#         row = randomized_array[i]  # grab the first row of the data
#         trend = ccgFilter(x_init, row, cutoff).getTrendValue(fake_x)  # outputs smooth values at my desired times, x
#         template_array = np.vstack((template_array, trend))
#     print(np.shape(template_array))
#     template_array = pd.DataFrame(template_array)
#     template_array_trans = pd.DataFrame.transpose(template_array)
#
#     mean_array = []
#     stdev_array = []
#     upper_array = []
#     lower_array = []
#     for i in range(0, len(template_array_trans)):
#         row = template_array_trans.iloc[i]  # grab the first row of the transformed DataFrame
#         sums = np.sum(row)                  # take the sum of all the numbers in that row
#         mean = sums / len(row)              # find the mean
#         mean_array.append(mean)             # append each mean to an array
#
#         stdevs = np.std(row)
#         stdev_array.append(stdevs)
#
#         upper = mean + stdevs
#         lower = mean - stdevs
#         upper_array.append(upper)
#         lower_array.append(lower)
#
#     return mean_array, stdev_array, upper_array, lower_array
#
# def ccgcrv_smooth(x_init, y_init, cutoff, fake_x, randomized_array):
#     template_array = ccgFilter(x_init, y_init, cutoff).getSmoothValue(fake_x)  # inital values for stacking
#     for i in range(0, len(randomized_array) - 1):  # minus 1 because there is one randomized row already stacked.
#         row = randomized_array[i]  # grab the first row of the data
#         trend = ccgFilter(x_init, row, cutoff).getSmoothValue(fake_x)  # outputs smooth values at my desired times, x
#         template_array = np.vstack((template_array, trend))
#     print(np.shape(template_array))
#     template_array = pd.DataFrame(template_array)
#     template_array_trans = pd.DataFrame.transpose(template_array)
#
#     mean_array = []
#     stdev_array = []
#     upper_array = []
#     lower_array = []
#     for i in range(0, len(template_array_trans)):
#         row = template_array_trans.iloc[i]  # grab the first row of the transformed DataFrame
#         sums = np.sum(row)                  # take the sum of all the numbers in that row
#         mean = sums / len(row)              # find the mean
#         mean_array.append(mean)             # append each mean to an array
#
#         stdevs = np.std(row)
#         stdev_array.append(stdevs)
#
#         upper = mean + stdevs
#         lower = mean - stdevs
#         upper_array.append(upper)
#         lower_array.append(lower)
#
#     return mean_array, stdev_array, upper_array, lower_array
