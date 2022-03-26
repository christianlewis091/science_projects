from __future__ import print_function, division
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from miller_curve_algorithm import ccgFilter
from PyAstronomy import pyasl

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


def monte_carlo_randomization(x_init, fake_x, y_init, y_error, cutoff):
    new_array = y_init  # create a new variable on which we will later v-stack randomized lists
    n = 10
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

    template_array = ccgFilter(x_init, y_init, cutoff).getSmoothValue(fake_x)
    for k in range(0, len(new_array)):
        row = new_array[k]  # grab the first row of the data
        smooth = ccgFilter(x_init, row, cutoff).getSmoothValue(fake_x)  # outputs smooth values at my desired times, x
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
        r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Stats and Data Analysis\Matlab and Python Files\tables.xlsx',
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

                # print(permarray_x)
                # print(permarray_y)

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
# add decimal dates to DataFrame
# x_init_bhd = baringhead['DATE_COLL']
# x_init_bhd = long_date_to_decimal_date(x_init_bhd)
# baringhead['Decimal_date'] = x_init_bhd

# add decimal dates to DataFrame
x_init_heid = heidelberg['Average pf Start-date and enddate']  # x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)  # use a function I wrote the change these values to decimal dates
heidelberg['Decimal_date'] = x_init_heid

# drop NaN's in the column I'm most interested in
heidelberg = heidelberg.dropna(subset=['D14C'])
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]  # filter out the one outlying measurement around 2019
heidelberg.reset_index()
baringhead = baringhead.dropna(subset=['DELTA14C'])

""" SLICE THE DATASETS UP FOR LATER SMOOTHING AND ANALYSIS"""
# MAIN BARING HEAD FILE
# Filter Baring Head to after bomb peak
baringhead = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 1980)]  # grab all values after 1980
baringhead = baringhead.loc[(baringhead['DELTA14C_ERR'] > 0)]  # get rid of data where the error flag is -1000
baringhead.reset_index()

# BARING HEAD SPLIT UP INTO 3 PARTS (and 1995 - 2005 bad data removed)
print('Baring Head data between 1995 and 2005 removed from all records')
baringhead_1986_1991 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 1986) & (baringhead['DEC_DECAY_CORR'] <= 1991)]
baringhead_1986_1991.reset_index(inplace=True)
baringhead_1991_1994 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] >= 1991) & (baringhead['DEC_DECAY_CORR'] <= 1994)]
baringhead_1991_1994.reset_index(inplace=True)
baringhead_2006_2016 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2006)]  # BARINGHEAD2 will include the 2009-2011
baringhead_2006_2016.reset_index(inplace=True)
# pull out the variables
xtot_bhd = baringhead['DEC_DECAY_CORR']
x1_bhd = baringhead_1986_1991['DEC_DECAY_CORR']
x2_bhd = baringhead_1991_1994['DEC_DECAY_CORR']
x3_bhd = baringhead_2006_2016['DEC_DECAY_CORR']
ytot_bhd = baringhead['DELTA14C']
y1_bhd = baringhead_1986_1991['DELTA14C']
y2_bhd = baringhead_1991_1994['DELTA14C']
y3_bhd = baringhead_2006_2016['DELTA14C']
ztot_bhd = baringhead['DELTA14C_ERR']
z1_bhd = baringhead_1986_1991['DELTA14C_ERR']
z2_bhd = baringhead_1991_1994['DELTA14C_ERR']
z3_bhd = baringhead_2006_2016['DELTA14C_ERR']

# Heidelberg SPLIT UP INTO 3 PARTS (and 1995 - 2005 bad data removed)
heidelberg_1986_1991 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1986) & (heidelberg['Decimal_date'] <= 1991)]
heidelberg_1986_1991.reset_index(inplace=True)
heidelberg_1991_1994 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1991) & (heidelberg['Decimal_date'] <= 1994)]
heidelberg_1991_1994.reset_index(inplace=True)
heidelberg_2006_2016 = heidelberg.loc[(heidelberg['Decimal_date'] > 2006)]  # BARINGHEAD2 will include the 2009-2011
heidelberg_2006_2016.reset_index(inplace=True)
xtot_heid = heidelberg['Decimal_date']
x1_heid = heidelberg_1986_1991['Decimal_date']
x2_heid = heidelberg_1991_1994['Decimal_date']
x3_heid = heidelberg_2006_2016['Decimal_date']
ytot_heid = heidelberg['D14C']
y1_heid = heidelberg_1986_1991['D14C']
y2_heid = heidelberg_1991_1994['D14C']
y3_heid = heidelberg_2006_2016['D14C']
ztot_heid = heidelberg['weightedstderr_D14C']
z1_heid = heidelberg_1986_1991['weightedstderr_D14C']
z2_heid = heidelberg_1991_1994['weightedstderr_D14C']
z3_heid = heidelberg_2006_2016['weightedstderr_D14C']

"""Can split up further in the future by following the above template and using smaller time increments."""
""" Set up x values for output data from the smooth curve. """

# x-data that I will use to solve for each of the smoothed curve functions - this way, x-data will be the same
# for any two datasets that I want to explicity compare, and I can subtract them directly.
fake_x_temp = np.linspace(1980, 2020, 480)
df_fake_xs = pd.DataFrame({'x': fake_x_temp})

# make sure to only get output at x-values where the data overlaps.
my_x_1986_1991 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x1_heid)) & (df_fake_xs['x'] <= max(x1_heid))]
my_x_1991_1994 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x2_bhd)) & (df_fake_xs['x'] <= max(x2_bhd))]
my_x_2006_2016 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x3_heid)) & (df_fake_xs['x'] <= max(x3_heid))]

"""
Put the sliced up data through the Monte Carlo randomization process, and then through the curve smoother
See my function above which does both and returns the data in an array.
"""

# function input: def monte_carlo_randomization(x_init, fake_x, y_init, y_error, cutoff):
# function return:  new_array, template_array, mean_array, stdev_array, upper_array, lower_array, fake_x
""" Smoothed, Monte Carlo'd data from 1986 to 1991 """
heidelberg_1986_1991_results = monte_carlo_randomization(x1_heid, my_x_1986_1991, y1_heid, z1_heid, 667)
bhd_1986_1991_results = monte_carlo_randomization(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, 667)
""" Smoothed, Monte Carlo'd data from 1991 to 1994 """
heidelberg_1991_1994_results = monte_carlo_randomization(x2_heid, my_x_1991_1994, y2_heid, z2_heid, 667)
bhd_1991_1994_results = monte_carlo_randomization(x2_bhd, my_x_1991_1994, y2_bhd, z2_bhd, 667)
""" Smoothed, Monte Carlo'd data from 2006_2016 """
heidelberg_2006_2016_results = monte_carlo_randomization(x3_heid, my_x_2006_2016, y3_heid, z3_heid, 667)
bhd_2006_2016_results = monte_carlo_randomization(x3_bhd, my_x_2006_2016, y3_bhd, z3_bhd, 667)
#
two_tail_paired_t_test(np.array(heidelberg_1986_1991_results[2]),
                       np.array(heidelberg_1986_1991_results[3]),
                       np.array(bhd_1986_1991_results[2]),
                       np.array(bhd_1986_1991_results[3]))

two_tail_paired_t_test(np.array(heidelberg_1991_1994_results[2]),
                       np.array(heidelberg_1991_1994_results[3]),
                       np.array(bhd_1991_1994_results[2]),
                       np.array(bhd_1991_1994_results[3]))

two_tail_paired_t_test(np.array(heidelberg_2006_2016_results[2]),
                       np.array(heidelberg_2006_2016_results[3]),
                       np.array(bhd_2006_2016_results[2]),
                       np.array(bhd_2006_2016_results[3]))

#
test = monthly_averages(xtot_bhd, ytot_bhd)
print(test)
print(len(xtot_bhd))
print(len(test[0]))
print()
print(len(ytot_bhd))
print(len(test[1]))
print('There is not that much difference in length between the original data and monthly averages.')


#
colors = sns.color_palette("rocket")
colors2 = sns.color_palette("mako")
size = 20
fig = plt.figure(1)
plt.plot(xtot_bhd, ytot_bhd, label='Baring Head ALL DATA', color='red')
# # plt.plot(xtot_heid, ytot_heid, label='Heidelberg ALL DATA', color='blue')
# # plt.scatter(x1_bhd, y1_bhd, marker='o', label='Baring Head Record Part 1', color=colors[0], s=size)
# # plt.scatter(x1_heid, y1_heid, marker='X', label='Heidelberg Part 1', color=colors2[5], s=size)
# # plt.scatter(x2_bhd, y2_bhd, marker='o', label='Baring Head Record Part 2', color=colors[1], s=size)
# # plt.scatter(x2_heid, y2_heid, marker='X', label='Heidelberg Part 2', color=colors2[4], s=size)
# # plt.scatter(x3_bhd, y3_bhd, marker='o', label='Baring Head Record Part 3', color=colors[0], s=size)
# # plt.scatter(x3_heid, y3_heid, marker='X', label='Heidelberg Part 3', color=colors2[5], s=size)
plt.scatter(test[0], test[1], label='BHD Monthly averages', color=colors2[5], s=size)

plt.legend()
plt.title('All Available Data')
# plt.xlim([2000, 2020])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
# # plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
# #             'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned3_Fig1.png',
# #             dpi=300, bbox_inches="tight")
plt.show()
