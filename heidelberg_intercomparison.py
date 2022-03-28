from __future__ import print_function, division
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from miller_curve_algorithm import ccgFilter
from PyAstronomy import pyasl

colors = sns.color_palette("rocket")
colors2 = sns.color_palette("mako")
size = 20

"""
################################################
################################################
DEFINE ALL THE FUNCTIONS THAT I WILL BE USING
################################################
################################################
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

n = 100
def monte_carlo_randomization(x_init, fake_x, y_init, y_error, cutoff):
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

    template_array = ccgFilter(x_init, y_init, cutoff).getSmoothValue(fake_x) # inital values for stacking
    for k in range(0, len(new_array)):
        row = new_array[k]  # grab the first row of the data
        smooth = ccgFilter(x_init, row, cutoff).getSmoothValue(fake_x) # outputs smooth values at my desired times, x
        template_array = np.hstack((template_array, smooth))

    df = pd.DataFrame(template_array)

    mean_array = []
    stdev_array = []
    upper_array = []
    lower_array = []
    for i in range(0, len(template_array)):
        element1 = np.sum(template_array[i])  # grab the first ROW of the dataframe and take the sum
        mean = element1 / len(template_array[i])  # find the mean of all the values from the Monte Carlo
        mean_array.append(mean)  # append it to a new array

        stdev = np.std(template_array[i])  # grab the first ROW of the dataframe find the stdev
        stdev_array.append(stdev)

        upper = mean + stdev
        lower = mean - stdev
        upper_array.append(upper)
        lower_array.append(lower)

    return new_array, template_array, mean_array, stdev_array, upper_array, lower_array, fake_x


"""
This function will calculate monthly averages for any input dataset. 
Must have decimal dates
"""
# def monthly_averages(y1, yerr):


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


""" 
The following function should determine monthly averages for a dataset. 
It will output these monthly averages along with a decimal date being the first decimal of that month. 
"""


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
################################################
################################################
IMPORT THE DATA AND BEGIN THE ANALYSIS
################################################
################################################
"""
# Heidelberg data excel file
heidelberg = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\heidelberg_cape_grim.xlsx', skiprows=40)
# Baring Head data excel file
baringhead = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')

""" TIDY UP THE DATA FILES"""
# add decimal dates to DataFrame if not there already
x_init_heid = heidelberg['Average pf Start-date and enddate']  # x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)
heidelberg['Decimal_date'] = x_init_heid  # add these decimal dates onto the dataframe

# drop NaN's in the column I'm most interested in
heidelberg = heidelberg.dropna(subset=['D14C'])
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]
heidelberg.reset_index()   # filter out the one outlying measurement around 2019
baringhead = baringhead.dropna(subset=['DELTA14C'])


"""CAREFULLY SPLIT UP THE DATA INTO DIFFERENT CHUNKS IN TIME AND GRAB VARIABLES """

""" Entire Baring Head File > 1980 """
baringhead = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 1980)]
baringhead = baringhead.loc[(baringhead['DELTA14C_ERR'] > 0)]  # get rid of data where the error flag is -1000
baringhead.reset_index(inplace=True)
# variables:
xtot_bhd = baringhead['DEC_DECAY_CORR']
ytot_bhd = baringhead['DELTA14C']
ztot_bhd = baringhead['DELTA14C_ERR']

""" Entire Baring Head File > 1980, without 1995 - 2005 """
snipmin = 1994  # was previously 1994
snipmax = 2006  # was previously 2006
snip = baringhead.loc[(baringhead['DEC_DECAY_CORR'] < snipmin)]
snip2 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > snipmax)]
snip = pd.merge(snip, snip2, how='outer')
# variables:
x_combined = snip['DEC_DECAY_CORR']
y_combined = snip['DELTA14C']
z_combined = snip['DELTA14C_ERR']
"""
BARING HEAD RECORD SPLIT UP INTO 3 PARTS (1987 - 1991, 1991 - 1994, 2006 - 2016)
"""
baringhead_1986_1991 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 1987) & (baringhead['DEC_DECAY_CORR'] <= 1991)]
baringhead_1986_1991.reset_index(inplace=True)
baringhead_1991_1994 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 1991) & (baringhead['DEC_DECAY_CORR'] <= 1994)]
baringhead_1991_1994.reset_index(inplace=True)
baringhead_2006_2016 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2006)]  # BARINGHEAD2 will include the 2009-2011
baringhead_2006_2016.reset_index(inplace=True)
# x- variables
x1_bhd = baringhead_1986_1991['DEC_DECAY_CORR']
x2_bhd = baringhead_1991_1994['DEC_DECAY_CORR']
x3_bhd = baringhead_2006_2016['DEC_DECAY_CORR']
# y- variables
y1_bhd = baringhead_1986_1991['DELTA14C']
y2_bhd = baringhead_1991_1994['DELTA14C']
y3_bhd = baringhead_2006_2016['DELTA14C']
# error - variables
z1_bhd = baringhead_1986_1991['DELTA14C_ERR']
z2_bhd = baringhead_1991_1994['DELTA14C_ERR']
z3_bhd = baringhead_2006_2016['DELTA14C_ERR']

""" Cape Grim Heidelberg ENTIRE datafile: """
# variables
xtot_heid = heidelberg['Decimal_date']
ytot_heid = heidelberg['D14C']
ztot_heid = heidelberg['weightedstderr_D14C']

"""
Heidelberg RECORD SPLIT UP INTO 3 PARTS (1987 - 1991, 1991 - 1994, 2006 - 2016)
"""
heidelberg_1986_1991 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1987) & (heidelberg['Decimal_date'] <= 1991)]
heidelberg_1986_1991.reset_index(inplace=True)
heidelberg_1991_1994 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1991) & (heidelberg['Decimal_date'] <= 1994)]
heidelberg_1991_1994.reset_index(inplace=True)
heidelberg_2006_2016 = heidelberg.loc[(heidelberg['Decimal_date'] > 2006)]  # BARINGHEAD2 will include the 2009-2011
heidelberg_2006_2016.reset_index(inplace=True)

x1_heid = heidelberg_1986_1991['Decimal_date']
x2_heid = heidelberg_1991_1994['Decimal_date']
x3_heid = heidelberg_2006_2016['Decimal_date']

y1_heid = heidelberg_1986_1991['D14C']
y2_heid = heidelberg_1991_1994['D14C']
y3_heid = heidelberg_2006_2016['D14C']

z1_heid = heidelberg_1986_1991['weightedstderr_D14C']
z2_heid = heidelberg_1991_1994['weightedstderr_D14C']
z3_heid = heidelberg_2006_2016['weightedstderr_D14C']
#

""" Simple curve smoothing of all the different data for visual analysis  """
# Whole baring head record
cutoff = 667

baringhead_smooth_total = ccgFilter(xtot_bhd, ytot_bhd, cutoff).getMonthlyMeans()
baringhead_xtot_smoothed = year_month_todecimaldate(baringhead_smooth_total[0], baringhead_smooth_total[1])  # get the dates to be in decimal format
baringhead_ytot_smoothed = baringhead_smooth_total[2]

heidelberg_smooth_total = ccgFilter(xtot_heid, ytot_heid, cutoff).getMonthlyMeans()
heidelberg_xtot_smoothed = year_month_todecimaldate(heidelberg_smooth_total[0], heidelberg_smooth_total[1])  # get the dates to be in decimal format
heidelberg_ytot_smoothed = heidelberg_smooth_total[2]


"""
Onto curve smoothing and Monte Carlo analysis with the data broken into three parts
"""
# x-data that I will use to solve for each of the smoothed curve functions - this way, x-data will be the same
# for any two datasets that I want to explicity compare, and I can subtract them directly.
fake_x_temp = np.linspace(1980, 2020, 480)
df_fake_xs = pd.DataFrame({'x': fake_x_temp})
#
# make sure to only get output at x-values where the data overlaps.
my_x_1986_1991 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x1_heid)) & (df_fake_xs['x'] <= max(x1_heid))]
my_x_1991_1994 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x2_bhd)) & (df_fake_xs['x'] <= max(x2_bhd))]
my_x_2006_2016 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x3_heid)) & (df_fake_xs['x'] <= max(x3_heid))]
"""
Put the sliced up data through the Monte Carlo randomization process, and then through the curve smoother
See my function above which does both and returns the data in an array.
"""
temporarycutoff = 667
ccgcv_bhd = ccgFilter(x1_bhd, y1_bhd, temporarycutoff).getMonthlyMeans()
x_ccgcv_bhd1 = year_month_todecimaldate(ccgcv_bhd[0], ccgcv_bhd[1])  # get the dates to be in decimal format
y_ccgcv_bhd1 = ccgcv_bhd[2]
ccgcv_bhd = ccgFilter(x2_bhd, y2_bhd, temporarycutoff).getMonthlyMeans()
x_ccgcv_bhd2 = year_month_todecimaldate(ccgcv_bhd[0], ccgcv_bhd[1])  # get the dates to be in decimal format
y_ccgcv_bhd2 = ccgcv_bhd[2]
ccgcv_bhd = ccgFilter(x3_bhd, y3_bhd, temporarycutoff).getMonthlyMeans()
x_ccgcv_bhd3 = year_month_todecimaldate(ccgcv_bhd[0], ccgcv_bhd[1])  # get the dates to be in decimal format
y_ccgcv_bhd3 = ccgcv_bhd[2]

# smooth the heidelberg data
ccgcv_heid = ccgFilter(x1_heid, y1_heid, temporarycutoff).getMonthlyMeans()
x_ccgcv_heid1 = year_month_todecimaldate(ccgcv_heid[0], ccgcv_heid[1])  # get the dates to be in decimal format
y_ccgcv_heid1 = ccgcv_heid[2]
ccgcv_heid = ccgFilter(x2_heid, y2_heid, temporarycutoff).getMonthlyMeans()
x_ccgcv_heid2 = year_month_todecimaldate(ccgcv_heid[0], ccgcv_heid[1])  # get the dates to be in decimal format
y_ccgcv_heid2 = ccgcv_heid[2]
ccgcv_heid = ccgFilter(x3_heid, y3_heid, temporarycutoff).getMonthlyMeans()
x_ccgcv_heid3 = year_month_todecimaldate(ccgcv_heid[0], ccgcv_heid[1])  # get the dates to be in decimal format
y_ccgcv_heid3 = ccgcv_heid[2]

# function input: def monte_carlo_randomization(x_init, fake_x, y_init, y_error, cutoff):
# function return:  new_array, template_array, mean_array, stdev_array, upper_array, lower_array, fake_x

""" Smoothed, Monte Carlo'd data from 1986 to 1991 """
heidelberg_1986_1991_results = monte_carlo_randomization(x1_heid, my_x_1986_1991, y1_heid, z1_heid, 667)
bhd_1986_1991_results = monte_carlo_randomization(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, 667)
# testing results
randos = bhd_1986_1991_results[0]  # extract the first of returned arrays for plotting / visualization
randos = pd.DataFrame(randos)
# randos = pd.DataFrame.transpose(randos)
x_randos = np.array(x1_bhd)
randos1 = np.array(randos.iloc[5])
randos2 = np.array(randos.iloc[1])
randos3 = np.array(randos.iloc[2])
randos4 = np.array(randos.iloc[3])
randos5 = np.array(randos.iloc[4])
print(np.shape(xtot_bhd))
print(np.shape(randos1))

smoothed_randomized_data = bhd_1986_1991_results[1]
montes = pd.DataFrame(bhd_1986_1991_results[1])
montes = pd.DataFrame.transpose(montes)

my_x_1986_1991_arr = np.array(my_x_1986_1991)
monte_it1 = np.array(montes.iloc[5])
monte_it2 = np.array(montes.iloc[1])
monte_it3 = np.array(montes.iloc[2])
monte_it4 = np.array(montes.iloc[3])
monte_it5 = np.array(montes.iloc[4])

""" Smoothed, Monte Carlo'd data from 1991 to 1994 """
heidelberg_1991_1994_results = monte_carlo_randomization(x2_heid, my_x_1991_1994, y2_heid, z2_heid, 667)
bhd_1991_1994_results = monte_carlo_randomization(x2_bhd, my_x_1991_1994, y2_bhd, z2_bhd, 667)
""" Smoothed, Monte Carlo'd data from 2006_2016 """
heidelberg_2006_2016_results = monte_carlo_randomization(x3_heid, my_x_2006_2016, y3_heid, z3_heid, 667)
bhd_2006_2016_results = monte_carlo_randomization(x3_bhd, my_x_2006_2016, y3_bhd, z3_bhd, 667)
#
# two_tail_paired_t_test(np.array(heidelberg_1986_1991_results[2]),
#                        np.array(heidelberg_1986_1991_results[3]),
#                        np.array(bhd_1986_1991_results[2]),
#                        np.array(bhd_1986_1991_results[3]))
#
# two_tail_paired_t_test(np.array(heidelberg_1991_1994_results[2]),
#                        np.array(heidelberg_1991_1994_results[3]),
#                        np.array(bhd_1991_1994_results[2]),
#                        np.array(bhd_1991_1994_results[3]))
#
# two_tail_paired_t_test(np.array(heidelberg_2006_2016_results[2]),
#                        np.array(heidelberg_2006_2016_results[3]),
#                        np.array(bhd_2006_2016_results[2]),
#                        np.array(bhd_2006_2016_results[3]))
#
# #
# test = monthly_averages(xtot_bhd, ytot_bhd)
# print(test)
# print(len(xtot_bhd))
# print(len(test[0]))
# print()
# print(len(ytot_bhd))
# print(len(test[1]))
# print('There is not that much difference in length between the original data and monthly averages.')
