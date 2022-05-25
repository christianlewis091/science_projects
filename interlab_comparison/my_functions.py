import numpy as np
import random
import pandas as pd
from miller_curve_algorithm import ccgFilter
from PyAstronomy import pyasl

"""
"long_date_to_decimal_date" function takes dates in the form of dd/mm/yyyy and converts them to a decimal. 
This was required for the heidelberg cape grim dataset, and is quite useful overall while date formatting can be in 
so many different forms. 
Arguments: 
x = column of dates in the form dd/mm/yyyy
Outputs: 
array = column of dates in the form yyyy.decimal 
To see an example, uncomment the following lines of code directly below the function definition: 
"""


def long_date_to_decimal_date(x):
    array = []  # define an empty array in which the data will be stored
    for i in range(0, len(x)):  # initialize the for loop to run the length of our dataset (x)
        j = x[i]  # assign j: grab the i'th value from our dataset (x)
        decy = pyasl.decimalYear(j)  # The heavy lifting is done via this Py-astronomy package
        decy = float(decy)  # change to a float - this may be required for appending data to the array
        array.append(decy)  # append it all together into a useful column of data
    return array  # return the new data


# df = pd.read_excel(r'H:\The Science\Datasets\my_functions_examples'
#                    r'\long_date_to_decimal_date_example.xlsx')  # import the data
# x = df['average']  # x-values from heidelberg dataset                   # grab the column
# y = long_date_to_decimal_date(x)                                        # apply the function
# df['decimal date'] = y                                                  # add the column to the dataframe
# print(df)                                                               # check that it looks right


"""
The following two functions are quite similar, so this short explanation will apply to both. 
"monte_carlo_randomization_Trend" is used heavily in the heidelberg intercomparison project. 
This function takes some time series x and y data, smooths it using the CCGCRV FFT filter algorithm: 
( https://gml.noaa.gov/ccgg/mbl/crvfit/crvfit.html ) and returns data at the x-values that you select. 
The first "trend" gets rid of seasonality and smooths more. 
The second "smooth" includes seasonality and smooths less. 

This function has three separate for-loops: 
The first for-loop: 
Takes an input array of time-series data and randomizes each data point
within its measurements uncertainty. It does this "n" times, and vertically stacks it.
For example, if you have a dataset with 10 measurements, and "n" is 1000, you will end
up with an array of dimension (10x1000).

The second for-loop: 
Takes each row of the array (each row of "randomized data") and puts it through
the ccgFilter curve smoother. It is important to define your own x-values that you want output
if you want to compare two curves (this will keep arrays the same dimension).
Each row from the fist loop is smoothed and stacked into yet another new array.

The third for-loop: 
Find the mean, standard deviation, and upper and lower uncertainty bounds of each
"point" in the dataset. This loop takes the mean of all the first measurements, then all the second, etc.

For clarty, I will define all of the arguments here below: 
x_init: x-values of the dataset that you want to smooth. Must be in decimal date format. 
fake_x: x-values of the data you want OUTPUT
y_init: y-values of the dataset that you want to smooth. 
y_error: y-value errors of the dataset that you want to smooth. 
cutoff: for the CCGCRV algoritm, lower numbers smooth less, and higher numbers smooth more. 
    See hyperlink above for more details. 
n: how many iterations do you want to run? When writing code, keep this low. Once code is solid, increase to 10,000. 
"""


# TODO edit the randomization to use a normal distribution to calculate, rather than just even probability along the
#      error bars.

def monte_carlo_randomization_trend(x_init, fake_x, y_init, y_error, cutoff, n):  # explanation of arguments above
    x_init = x_init.reset_index(drop=True)                                        # ensure x-values begin at index 0
    y_init = y_init.reset_index(drop=True)                                        # ensure y-values begin at index 0
    y_error = y_error.reset_index(drop=True)                                      # ensure y err-values begin at index 0
    fake_x_for_dataframe = fake_x.reset_index(drop=True)                          # ensure output x-values at index 0
    fake_x_for_dataframe = fake_x_for_dataframe['x']    # if not already extracted, extract the data from the DataFrame

    # First for-loop: randomize the y-values.

    # The line below: creates a copy of the y-value column. This is helpful because as I randomize the y-data, I will
    # stack each new randomized column. So if n = 10, there will 10 stacked, randomized columns. The initial column
    # was helpful to get the code running - was something to "stick the stack on". Not sure if this was required but
    # it helped me get the for-loop to run.
    new_array = y_init

    for i in range(0, n):                     # initialize the for-loop. It will run "n" times.
        empty_array = []                      # initialize an empty array to add each individual value onto.
        for j in range(0, len(y_init)):       # nested loop: run through the column of y-data, length-of-y times.

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


#
# def monte_carlo_randomization_Smooth(x_init, fake_x, y_init, y_error, cutoff, n):
#     # reset indeces for incoming data
#     x_init = x_init.reset_index(drop=True)
#     y_init = y_init.reset_index(drop=True)
#     y_error = y_error.reset_index(drop=True)
#     fake_x_for_dataframe = fake_x.reset_index(drop=True)
#     fake_x_for_dataframe = fake_x_for_dataframe['x']
#
#     # """ Randomization step """
#
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
#
#         # """ The "new_array" contains the data that will be used in the next step"""
#         # """ The "randomized_dataframe" contains a more digestible course of data that can be plotted. """
#         # """ To plot randomized data from the "Randomized Dataframe, index each row using randomized_dataframe.iloc[0]  """
#
#         new_array = np.vstack((new_array, empty_array))
#     randomized_dataframe = pd.DataFrame(new_array)
#
#     # SMOOTHING STEP
#
#     # Create an initial array on which later arrays that are created will stack
#     template_array = ccgFilter(x_init, new_array[0], cutoff).getSmoothValue(fake_x)  # inital values for stacking
#
#     # this for smooths each row of the randomized array from above, and stacks it up
#     for k in range(0, len(new_array)):
#         row = new_array[k]  # grab the first row of the data
#         smooth = ccgFilter(x_init, row, cutoff).getSmoothValue(fake_x)  # outputs smooth values at my desired times, x
#         template_array = np.hstack((template_array, smooth))
#
#     smoothed_dataframe = pd.DataFrame(template_array)
#     smoothed_dataframe_trans = pd.DataFrame.transpose(smoothed_dataframe)
#     mean_array = []
#     stdev_array = []
#     upper_array = []
#     lower_array = []
#     for i in range(0, len(template_array)):
#         element1 = smoothed_dataframe.iloc[i]
#         sum1 = np.sum(element1)  # grab the first ROW of the dataframe and take the sum
#         mean1 = sum1 / len(element1)  # find the mean of all the values from the Monte Carlo
#         mean_array.append(mean1)  # append it to a new array
#
#         stdev = np.std(element1)  # grab the first ROW of the dataframe find the stdev
#         stdev_array.append(stdev)
#
#         upper = mean1 + stdev
#         lower = mean1 - stdev
#         upper_array.append(upper)
#         lower_array.append(lower)
#
#         # create a more digestable summary dataframe
#     summary = pd.DataFrame({"Means": mean_array,
#                             "stdevs": stdev_array,
#                             "error_upperbound": upper_array,
#                             "error_lowerbound": lower_array,
#                             "my_xs": fake_x_for_dataframe})
#
#     return randomized_dataframe, smoothed_dataframe_trans, summary
#
#
# """
# The following function should determine monthly averages for a dataset.
# It will output these monthly averages along with a decimal date being the first decimal of that month.
# """
#
#
# def monthly_averages(x_values, y_values, y_err):
#     x_values = np.array(x_values)
#     y_values = np.array(y_values)
#     y_err = np.array(y_err)
#
#     Begin = 0
#     Jan = 31
#     Feb = 28 + 31
#     Mar = 31 + 31 + 28
#     Apr = 30 + 31 + 28 + 31
#     May = 31 + 31 + 28 + 31 + 30
#     June = 30 + 31 + 28 + 31 + 30 + 31
#     July = 31 + 31 + 28 + 31 + 30 + 31 + 30
#     August = 31 + 31 + 28 + 31 + 30 + 31 + 30 + 31
#     Sep = 30 + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31
#     Oct = 31 + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30
#     Nov = 30 + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30
#     Dec = 31 + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30 + 30
#     months = np.array([Begin, Jan, Feb, Mar, Apr, May, June, July, August, Sep, Oct, Nov, Dec])
#     months = months / 365
#
#     # first, enter the available years on file:
#     lin1 = np.linspace(int(min(x_values)),
#                        int(max(x_values)),
#                        (int(max(x_values)) - int(min(x_values)) + 1))
#
#     # initialize some vars
#     mean_of_date = 0
#     mean_of_y = 0
#
#     permarray_x = []
#     permarray_y = []
#     permarray_z = []
#     for i in range(0, len(lin1)):  # loop in the years
#         year = int(lin1[i])  # grab only the integer parts of the years in the data
#
#         for j in range(0, len(months)):  # loop in the months
#
#             temparray_x = []
#             temparray_y = []
#             temparray_z = []
#             # print('The current month is ' + str(months[j]) + 'in year ' + str(year))
#             months_min = months[j]
#             # TODO fix this line of code to filter between one month and the next more accurately
#             months_max = months_min + 0.08
#
#             for k in range(0, len(y_values)):  # grab the data i want to use
#                 y_current = y_values[k]
#                 x_current = x_values[k]
#                 z_current = y_err[k]
#                 x_decimal_only = x_current - int(x_current)
#                 x_int = int(x_current)
#                 # if my data exists in the time frame I'm currently searching through,
#                 if (x_int == year) and (x_decimal_only >= months_min) and (x_decimal_only < months_max):
#                     # append that x and y data to initialized arrays
#                     temparray_x.append(x_int + months_min)
#                     temparray_y.append(y_current)
#                     temparray_z.append(z_current)
#
#             # if at the end of the month, the length of the temporary arrays are non-zero,
#             # clean and append that information to a permanent array
#             if len(temparray_x) != 0:
#                 tempsum = sum(temparray_x)
#                 tempmean = tempsum / len(temparray_x)  # this works fine because it averages the same # repeatedly
#
#                 tempsum2 = sum(temparray_y)
#                 tempmean2 = tempsum2 / len(temparray_y)
#
#                 tempsum3 = sum(temparray_z)                  # todo change from simple averaging of error to proper prop
#                 tempmean3 = tempsum3 / len(temparray_z)
#
#                 permarray_x.append(tempmean)
#                 permarray_y.append(tempmean2)
#                 permarray_z.append(tempmean3)
#                 # print(permarray_x)
#                 # print(permarray_y)
#
#             # else:
#             #     permarray_x.append(x_int + months_min)
#             #     permarray_y.append(-999)
#
#     return permarray_x, permarray_y, permarray_z
#
#
# """
# This function does a paired two-tail t-test. The t-value range comes from the stdev_array in the
# Monte Carlo function above, and errors are propagated through the t-test mathematics.
# """
#
#
# def two_tail_paired_t_test(y1, y1err, y2, y2err):
#     """ Subtract the data from each other (first step in paired t-test)"""
#     difference = np.subtract(y1, y2)  # subtract the data from each other
#     """ What is the mean of the subtraction array? """
#     mean1 = np.average(difference)
#     """ What is the standard error of the subtraction array"""
#     se = np.std(difference) / np.sqrt(len(y1))
#     """ Compute the t-stat"""
#     t_stat = mean1 / se
#     t_stat = np.abs(t_stat)
#
#     """ ERROR PROPAGATION """
#     """ propagate the error from the first differencing """
#     y1err_sq = y1err * y1err  # square of errors from first dataset
#     y2err_sq = y2err * y2err  # square of errors from second dataset
#     sum_errs = y1err_sq + y2err_sq  # sum of the squared errors
#     err_differencing = np.sqrt(sum_errs)  # square root of the sums of errors
#
#     """ propagate the error from the mean1 """
#     squares = err_differencing * err_differencing  # square the propagated errors from differencing
#     sum_errs2 = 0  # initialize sums to zero
#     for i in range(0, len(squares)):
#         sum_errs2 = sum_errs2 + squares[i]  # add them all together
#         # sum_errs2 += squares[i]
#     sum_errs3 = np.sqrt(sum_errs2)  # take the square root
#     err_mean = sum_errs3 / len(squares)  # divide by number of measurements
#     ### The ERR_MEAN IS PROPOGATED ERROR, NOT STANDARD ERROR!!!
#
#     """
#     Propogate error for the denominator of t-stat calc, STANDARD ERROR
#     For this I need to propogate the error through the standard deviation calculation,
#     and then divide by sqrt(N)
#     """
#     """STEP 1: Propogate the error of (xi - u)"""
#     xi_u = err_mean ** 2 + err_differencing ** 2
#     xi_u = np.sqrt(xi_u)
#     """STEP 2: Propogate the error of (xi - u)^2 """
#     xi_u2_a = (difference - mean1) ** 2
#     xi_u2_b = xi_u / (difference - mean1)
#     xi_u2_c = xi_u2_b ** 2
#     xi_u2_d = xi_u2_c * 2
#     xi_u2_e = np.sqrt(xi_u2_d)
#     xi_u2_f = xi_u2_e * xi_u2_a
#
#     """STEP 3: Propagate the error of SIGMA(xi - u)^2 """
#     init_num = 0  # initialize a number to add errors onto
#     for i in range(0, len(xi_u2_f)):
#         xi_u2_g = xi_u2_f[i] ** 2
#         init_num = xi_u2_g + init_num
#     sigma_xi_u2 = np.sqrt(init_num)
#
#     """STEP 4: Propagate the error of SIGMA(xi - u)^2 / N """
#     sigma_xi_2_byN = sigma_xi_u2 / len(y1)
#
#     """STEP 5: Propagate the error of SQRT of SIGMA(xi - u)^2 / N """
#     sqrt_sigmaxi_2_byn = np.sqrt(sigma_xi_2_byN)
#
#     """STEP 6: Find standard error by dividing SQRT by sqrt of N """
#     se_err = sqrt_sigmaxi_2_byn / np.sqrt(len(y1))
#
#     """ final t-test error: error of mean and error of SE"""
#     t_stat_e1 = t_stat
#     t_stat_e2 = (se_err / se) ** 2
#     t_stat_e3 = (err_mean / mean1) ** 2
#     t_stat_e4 = t_stat_e2 + t_stat_e3
#     t_stat_e5 = np.sqrt(t_stat_e4)
#     t_stat_e6 = t_stat_e1 * t_stat_e5
#
#     d_of_f = len(y1) + len(y2) - 2
#     # find the degrees of freedom, and the closest number in the table to my degrees of freedom
#     dfx = pd.read_excel(
#         r'H:\The Science\Datasets\tables.xlsx',
#         sheet_name='ttable_adjusted')
#     # print(dfx)
#     # locate where the degrees of freedom is equal to my degrees of freedom:
#     value_crits = dfx['value']
#     value_crits = np.array(value_crits)
#     if d_of_f > 100:
#         value_crit = 1.98
#     else:
#         value_crit = value_crits[d_of_f - 1]
#
#     if t_stat - t_stat_e6 <= value_crit:
#
#         data = [t_stat, t_stat_e6, value_crit, mean1, err_mean]
#         headers = ['t-statistic', 't-statistic error', 'critical value', 'mean of differences', 'error of mean']
#         data = pd.DataFrame(data, headers)
#         print(data)
#         print('There is NO observed difference at 95% confidence interval')
#         print('')
#         print('')
#         result = 1
#
#     else:
#         data = [t_stat, t_stat_e6, value_crit, mean1, err_mean]
#         headers = ['t-statistic', 't-statistic error', 'critical value', 'mean of differences', 'error of mean']
#         data = pd.DataFrame(data, headers)
#         print(data)
#         print('There IS AN observed difference at 95% confidence interval')
#         print('')
#         print('')
#
#         result = 0
#
#     return result


# where is this one used?


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
