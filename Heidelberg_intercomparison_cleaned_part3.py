from __future__ import print_function, division
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from miller_curve_algorithm import ccgFilter
import math
from my_functions import long_date_to_decimal_date, monte_carlo_step2
from my_functions import year_month_todecimaldate
from my_functions import monte_carlo_step1
from my_functions import two_tail_paired_t_test

"""
DEFINE ALL THE FUNCTIONS THAT I WILL BE USING DURING THIS INTERCOMPARISON
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

    # CODE WORKS UP TO ABOVE

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
              ', mean: ' + str(mean1) + '\u00B1 ' + str(err_mean))
        result = 1

    else:
        print('There is A DIFFERENCE. ' +
              'Critical value: ' + str(value_crit) +
              ', t-stat: ' + str(t_stat) + '\u00B1 ' + str(t_stat_e6) +
              ', mean: ' + str(mean1) + '\u00B1 ' + str(err_mean))
        result = 0

    return result


""" IMPORT ALL THE DATA """
# Heidelberg data excel file
heidelberg = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\heidelberg_cape_grim.xlsx', skiprows=40)
# Baring Head data excel file
baringhead = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')

""" TIDY UP THE DATA FILES"""
# add decimal dates to DataFrame
x_init_bhd = baringhead['DATE_COLL']
x_init_bhd = long_date_to_decimal_date(x_init_bhd)
baringhead['Decimal_date'] = x_init_bhd

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
baringhead_1986_1991 = baringhead.loc[(baringhead['Decimal_date'] >= 1986) & (baringhead['Decimal_date'] <= 1991)]
baringhead_1991_1994 = baringhead.loc[(baringhead['Decimal_date'] >= 1991) & (baringhead['Decimal_date'] <= 1994)]
baringhead_2006_2016 = baringhead.loc[(baringhead['Decimal_date'] > 2006)]  # BARINGHEAD2 will include the 2009-2011
# pull out the variables
xtot_bhd = baringhead['Decimal_date']
x1_bhd = baringhead_1986_1991['Decimal_date']
x2_bhd = baringhead_1991_1994['Decimal_date']
x3_bhd = baringhead_2006_2016['Decimal_date']
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
heidelberg_1991_1994 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1991) & (heidelberg['Decimal_date'] <= 1994)]
heidelberg_2006_2016 = heidelberg.loc[(heidelberg['Decimal_date'] > 2006)]  # BARINGHEAD2 will include the 2009-2011
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

my_x_1986_1991 = df_fake_xs.loc[(df_fake_xs['x'] >= min(y1_heid)) & (df_fake_xs['x'] <= max(y1_heid))]



# my_x_1991_1994 = df_fake_xs.loc[(df_fake_xs['x'] >= 1991) & (df_fake_xs['x'] <= 1994)]
# my_x_2006_2016 = df_fake_xs.loc[(df_fake_xs['x'] >= 2006) & (df_fake_xs['x'] <= 2016)]
#
# # """
# Put the sliced up data through the Monte Carlo randomization process, and then through the curve smoother
# See my function above which does both and returns the data in an array
# """
# heidelberg_1986_1991_results = monte_carlo_randomization(heidelberg_1986_1991['Decimal_date'],
#                                                          my_x_1986_1991,
#                                                          heidelberg_1986_1991['D14C'],
#                                                          heidelberg_1986_1991['weightedstderr_D14C'],
#                                                          667)
# print(heidelberg_1986_1991_results)
# # heidelberg_1991_1994_results = monte_carlo_randomization(heidelberg_1991_1994['Decimal_date'],
# #                                                          my_x_1991_1994,
# #                                                          heidelberg_1991_1994['D14C'],
# #                                                          heidelberg_1991_1994['weightedstderr_D14C'],
# #                                                          667)























colors = sns.color_palette("rocket")
colors2 = sns.color_palette("mako")
size = 20
fig = plt.figure(1)
# plt.plot(xtot_bhd, ytot_bhd, label='Baring Head ALL DATA', color='red')
# plt.plot(xtot_heid, ytot_heid, label='Heidelberg ALL DATA', color='blue')
plt.scatter(x1_bhd, y1_bhd, marker='o', label='Baring Head Record Part 1', color=colors[0], s=size)
plt.scatter(x1_heid, y1_heid, marker='X', label='Heidelberg Part 1', color=colors2[5], s=size)
plt.scatter(x2_bhd, y2_bhd, marker='o', label='Baring Head Record Part 2', color=colors[1], s=size)
plt.scatter(x2_heid, y2_heid, marker='X', label='Heidelberg Part 2', color=colors2[4], s=size)
plt.scatter(x3_bhd, y3_bhd, marker='o', label='Baring Head Record Part 3', color=colors[0], s=size)
plt.scatter(x3_heid, y3_heid, marker='X', label='Heidelberg Part 3', color=colors2[5], s=size)
plt.legend()
plt.title('All Available Data')
plt.xlim([1985, 1995])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned3_Fig1.png',
            dpi=300, bbox_inches="tight")
