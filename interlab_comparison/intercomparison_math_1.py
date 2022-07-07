import numpy as np
import pandas as pd
from scipy import stats
# import the data from the "Pre-Processing" files:
from Pre_Processing_ANSTO import combine_ANSTO
from Pre_Processing_Heidelberg import combine_heidelberg
from Pre_Processing_UniMagallanes import combine_Magallanes
from Pre_Processing_SIO_LLNL import combine_SIO
from X_my_functions import monte_carlo_randomization_trend, monte_carlo_randomization_smooth
from X_miller_curve_algorithm import ccgFilter
import matplotlib.pyplot as plt
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


# UNCOMMENT WHEN DONE WRITING THIS FILE! HERE ARE THE OTHER INTERCOMPARISON!
# # I was first supplied with FM data from ANSTO so I'm going to use FM for this calculation.
# a = intercomparison_ttest(ansto['D14C'], rrl['D14C'], 'ANSTO v RRL Test: Tree Rings, D14C', 'paired')
# a = intercomparison_ttest(ansto['FM'], rrl['FM'], 'ANSTO v RRL Test: Tree Rings, FM', 'paired')
#
# # I'll do this one in FM as well because it minimizes the amount of extra calculatinos
# # that can lead to fake systematic bias.
# b = intercomparison_ttest(sio_nwt3['FM'], rrl_nwt3['FM'], 'SIO/LLNL v RRL, NWT3 Intercomparison', 'not-paired')
# c = intercomparison_ttest(sio_nwt4['FM'], rrl_nwt4['FM'], 'SIO/LLNL v RRL, NWT3 Intercomparison', 'not-paired')
#
# d = intercomparison_ttest(rafter, magallanes, 'Magallanes v RRL Test: Tree Rings', 'paired')

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
baringhead = combine_heidelberg.loc[(combine_heidelberg['Site'] == 'BHD')]
# BARING HEAD VARIABLES
xtot_bhd = baringhead['Decimal_date'].reset_index(drop=True)  # entire dataset x-values
ytot_bhd = baringhead['D14C'].reset_index(drop=True)  # entire dataset y-values
ztot_bhd = baringhead['D14C_err'].reset_index(drop=True)  # entire dataset z-values

heidelberg = combine_heidelberg.loc[(combine_heidelberg['Site'] == 'CGO')]
# BARING HEAD VARIABLES
xtot_heid = heidelberg['Decimal_date'].reset_index(drop=True)  # entire dataset x-values
ytot_heid = heidelberg['D14C'].reset_index(drop=True)  # entire dataset y-values
ztot_heid = heidelberg['D14C_err'].reset_index(drop=True)  # entire dataset z-values

# Now we'll index the data based on intervals
i1 = [1986, 2016]  # this interval can be used to assess the data as a whole
i2 = [1986, 1990]  # this interval goes from the beginning of the Heidelberg dataset +5 years
i3 = [1990, 1994]  # this interval goes from the end of i2 + 4 years (comes from precedent of Turnbull 2017 doing 5-year increments)
i4 = [1986, 1994]  # I'd like to use this test to see if there is a difference between splitting up into 4-year/5-year intervals or not
i5 = [1994, 2006]  # this data will be removed as described in the precedent above.
i6 = [2006, 2016]  # post-AMS period begin until the end of the Heidelberg record
i7 = [2006, 2009]  # first interval of the second major chunk, as we will remove 2009-2012 because of NaOH issues
i8 = [2009, 2012]  # interval when there was an issue with NaOH sampling, see precedent described above
i9 = [2012, 2016]  # post NaOH problem interval until the end of the Heidelberg data
intervals = [i1, i2, i3, i4, i5, i6, i7, i8, i9]
fake_x_temp = np.linspace(1980, 2020, 480)  # create arbitrary set of x-values to control output
df_fake_xs = pd.DataFrame({'Decimal_date': fake_x_temp})  # put this set into a pandas DataFrame

# The following block of code will index the data according the time intervals set above, into three arrays for each variable, (time, D14C, D14C_err)
interval_array_x_bhd = []
interval_array_y_bhd = []
interval_array_z_bhd = []
interval_array_x_heid = []
interval_array_y_heid = []
interval_array_z_heid = []
interval_array_fakex = []
for i in range(0, len(intervals)):
    x = intervals[i]
    min = x[0]
    max = x[1]
    indexed_df = baringhead.loc[(baringhead['Decimal_date'] >= min) & (baringhead['Decimal_date'] <= max)].reset_index(
        drop=True)
    indexed_df2 = heidelberg.loc[(heidelberg['Decimal_date'] >= min) & (heidelberg['Decimal_date'] <= max)].reset_index(
        drop=True)
    indexed_fakex = df_fake_xs.loc[
        (df_fake_xs['Decimal_date'] >= min) & (df_fake_xs['Decimal_date'] <= max)].reset_index(drop=True)
    indexed_fakex = np.array(indexed_fakex['Decimal_date'])
    interval_array_fakex.append(indexed_fakex)

    interval_x = np.array(indexed_df['Decimal_date'])  # extract the x-values from the data we just indexed
    interval_y = np.array(indexed_df['D14C'])  # extract the x-values from the data we just indexed
    interval_z = np.array(indexed_df['D14C_err'])  # extract the x-values from the data we just indexed

    interval_x2 = np.array(indexed_df2['Decimal_date'])  # extract the x-values from the data we just indexed
    interval_y2 = np.array(indexed_df2['D14C'])  # extract the x-values from the data we just indexed
    interval_z2 = np.array(indexed_df2['D14C_err'])  # extract the x-values from the data we just indexed

    interval_array_x_bhd.append(interval_x)
    interval_array_y_bhd.append(interval_y)
    interval_array_z_bhd.append(interval_z)
    interval_array_x_heid.append(interval_x2)
    interval_array_y_heid.append(interval_y2)
    interval_array_z_heid.append(interval_z2)

"""
In the past, I've experience some issues with the curve smoother not liking some of the time-intervals for an unknown
reason, so the next block of code is going to 
1) set the time intervals that we'll be using for the rest of the intercomparison and 
2) test that the smoother is successful before running it through the Monte Carlo function
"""
cutoff = 667
n = 1000
for i in range(0, len(interval_array_x_bhd)):
    test_run = ccgFilter(interval_array_x_bhd[i], interval_array_y_bhd[i], cutoff).getSmoothValue(
        interval_array_x_bhd[i])

for i in range(0, len(interval_array_x_heid)):
    test_run = ccgFilter(interval_array_x_heid[i], interval_array_y_heid[i], cutoff).getSmoothValue(
        interval_array_x_heid[i])

"""
Up to this point there seems to be no NaN problems with the data, perhaps this is related to me mostly working with the 
data in "array" format instead of Pandas DataFrame format. Now I'll write a for loop to run the Monte Carlo and get the
data out: 
"""
bhd_output_array_smooth_means = []
bhd_output_array_smooth_stdevs = []

for i in range(0,
               len(interval_array_x_bhd)):  # run this loop the same amount of times as the length of the array (9 times for 9 time intervals)
    # beacuse when I originally wrote the function, I had everything in pandas dataframes, I'm going to quickly change the arrays to Pd Dataframes inside the loop:
    df = pd.DataFrame({"x": interval_array_x_bhd[i], "y": interval_array_y_bhd[i], "z": interval_array_z_bhd[i]})
    df2 = pd.DataFrame({"fake_x": interval_array_fakex[i]})

    x = monte_carlo_randomization_smooth(df['x'], df2['fake_x'], df['y'], df['z'], cutoff, n)
    # running this function should return the following (see X_my_functions.py):
    # summary = pd.DataFrame({"Means": mean_array, "stdevs": stdev_array})
    # return randomized_dataframe, smoothed_dataframe, summary
    summary = x[2]  # grab summary, the third output from the line above
    means = summary['Means']
    means = np.array(means)

    bhd_output_array_smooth_means.append(means)

    stdevs = summary['stdevs']
    stdevs = np.array(stdevs)
    bhd_output_array_smooth_stdevs.append(stdevs)

# running same loop as above but for heidelberg
heid_output_array_smooth_means = []
heid_output_array_smooth_stdevs = []
for i in range(0,
               len(interval_array_x_heid)):  # run this loop the same amount of times as the length of the array (9 times for 9 time intervals)
    df = pd.DataFrame({"x": interval_array_x_heid[i], "y": interval_array_y_heid[i], "z": interval_array_z_heid[i]})
    df2 = pd.DataFrame({"fake_x": interval_array_fakex[i]})
    x = monte_carlo_randomization_smooth(df['x'], df2['fake_x'], df['y'], df['z'], cutoff, n)
    summary = x[2]  # grab summary, the third output from the line above
    means = summary['Means']
    means = np.array(means)

    heid_output_array_smooth_means.append(means)
    stdevs = summary['stdevs']
    stdevs = np.array(stdevs)
    heid_output_array_smooth_stdevs.append(stdevs)

# running same loop as above but for BARING HEAD (TREND)
bhd_output_array_trend_means = []
bhd_output_array_trend_stdevs = []
for i in range(0,
               len(interval_array_x_bhd)):  # run this loop the same amount of times as the length of the array (9 times for 9 time intervals)
    df = pd.DataFrame({"x": interval_array_x_bhd[i], "y": interval_array_y_bhd[i], "z": interval_array_z_bhd[i]})
    df2 = pd.DataFrame({"fake_x": interval_array_fakex[i]})
    x = monte_carlo_randomization_trend(df['x'], df2['fake_x'], df['y'], df['z'], cutoff, n)
    summary = x[2]  # grab summary, the third output from the line above
    means = summary['Means']
    means = np.array(means)
    bhd_output_array_trend_means.append(means)
    stdevs = summary['stdevs']
    stdevs = np.array(stdevs)
    bhd_output_array_trend_stdevs.append(stdevs)

# running same loop as above but for heidelberg (TREND)
heid_output_array_trend_means = []
heid_output_array_trend_stdevs = []
for i in range(0,
               len(interval_array_x_heid)):  # run this loop the same amount of times as the length of the array (9 times for 9 time intervals)
    df = pd.DataFrame({"x": interval_array_x_heid[i], "y": interval_array_y_heid[i], "z": interval_array_z_heid[i]})
    df2 = pd.DataFrame({"fake_x": interval_array_fakex[i]})
    x = monte_carlo_randomization_trend(df['x'], df2['fake_x'], df['y'], df['z'], cutoff, n)
    summary = x[2]  # grab summary, the third output from the line above
    means = summary['Means']
    means = np.array(means)
    heid_output_array_trend_means.append(means)
    stdevs = summary['stdevs']
    stdevs = np.array(stdevs)
    heid_output_array_trend_stdevs.append(stdevs)

"""
Now, the Monte Carlo has finished and I'm to re-insert the data into pandas Dataframes for easier use in checking
Each output file has 9 different arrays within, one for each interval. I want to index and smush them together so I 
have the comparisons between Heidelberg and Rafter in one dataframe and can get rid of 0's and NaN's. 
"""
df_array = []
# ignore a warning I get from the following block of code.
np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
for i in range(0, len(interval_array_x_heid)):  # 9 time intervals
    newdf = pd.DataFrame({"Decimal_date": interval_array_fakex[i],
                          "rafter_means_smooth": bhd_output_array_smooth_means[i],
                          "rafter_stdevs_smooth": bhd_output_array_smooth_stdevs[i],
                          "heid_means_smooth": heid_output_array_smooth_means[i],
                          "heid_stdevs_smooth": heid_output_array_smooth_stdevs[i],
                          "rafter_means_trend": bhd_output_array_trend_means[i],
                          "rafter_stdevs_trend": bhd_output_array_trend_stdevs[i],
                          "heid_means_trend": heid_output_array_trend_means[i],
                          "heid_stdevs_trend": heid_output_array_trend_stdevs[i]})
    newdf = newdf.dropna()
    df_array.append(newdf)  # append the dataframes onto an array for later analysis

# print(df_array[0])

"""
Let's calculate the mean offsets between the data
"""


def offset_calc(y1, y1err, y2, y2err):

    difference = np.subtract(y1, y2)                  # subtract the data from each other
    difference_error = np.sqrt(y1err**2 + y2err**2)   # propagate the error of differencing
    mean_of_differences = np.average(difference)
    standard_error = np.std(difference) / np.sqrt(len(y1))  # standard error of the subtraction array
    return difference, difference_error, mean_of_differences, standard_error


# The following for loop will calculate all the offsets for the different DataFrames in the array we created above
# SMOOTH
differences = []
difference_errors = []
mean_of_difference = []
std_error = []
for i in range(0, len(df_array)):
    df = df_array[i]                                                        # access the first dataframe
    x = offset_calc(df["rafter_means_smooth"], df["rafter_stdevs_smooth"], df["heid_means_smooth"], df["heid_stdevs_smooth"])
    dif = x[0]
    dif_er = x[1]
    m = x[2]
    stderr = x[3]
    differences.append(dif)
    difference_errors.append(dif_er)
    mean_of_difference.append(m)
    std_error.append(stderr)
# create summary dataframe:
smooth_diff_summary = pd.DataFrame({'Differences': differences, "1-sigma_error": difference_errors})
smooth_diff_summary2 = pd.DataFrame({'Time Period': intervals,'Means': mean_of_difference, "Standard error": std_error})

print(smooth_diff_summary2)

# TREND
differences = []
difference_errors = []
mean_of_difference = []
std_error = []
for i in range(0, len(df_array)):
    df = df_array[i]                                                        # access the first dataframe
    x = offset_calc(df["rafter_means_trend"], df["rafter_stdevs_trend"], df["heid_means_trend"], df["heid_stdevs_trend"])
    dif = x[0]
    dif_er = x[1]
    m = x[2]
    stderr = x[3]
    differences.append(dif)
    difference_errors.append(dif_er)
    mean_of_difference.append(m)
    std_error.append(stderr)
# create summary dataframe:
trend_diff_summary = pd.DataFrame({'Differences': differences, "1-sigma_error": difference_errors})
trend_diff_summary2 = pd.DataFrame({'Time Period': intervals,'Means': mean_of_difference, "Standard error": std_error})

print(trend_diff_summary2)

#

#
#
#
# plt.scatter(xtot_bhd, ytot_bhd)
# plt.plot(xtot_bhd, template_array)
# plt.show()
# Commenting out rest of heidelberg stuff. Going to set through and ensure that I can figure out the later NaN issue by
# stepping through more categorically...


# x1_bhd = baringhead_1986_1991['Decimal_date']
# x2_bhd = baringhead_1991_1994['Decimal_date']
# x3_bhd = baringhead_2006_2016['Decimal_date']
# x4_bhd = baringhead_2006_2009['Decimal_date']
# x5_bhd = baringhead_2012_2016['Decimal_date']
# y1_bhd = baringhead_1986_1991['D14C']  #
# y2_bhd = baringhead_1991_1994['D14C']
# y3_bhd = baringhead_2006_2016['D14C']
# y4_bhd = baringhead_2006_2009['D14C']
# y5_bhd = baringhead_2012_2016['D14C']
# z1_bhd = baringhead_1986_1991['D14C_err']
# z2_bhd = baringhead_1991_1994['D14C_err']
# z3_bhd = baringhead_2006_2016['D14C_err']
# z4_bhd = baringhead_2006_2009['D14C_err']
# z5_bhd = baringhead_2012_2016['D14C_err']
# # HEIDELBERG CAPE GRIM VARIABLES
# xtot_heid = heidelberg['Decimal_date']  # entire dataset x-values
# ytot_heid = heidelberg['D14C']  # entire dataset y-values
# ztot_heid = heidelberg['D14C_err']  # entire dataset error(z)-values
# x1_heid = heidelberg_1986_1991['Decimal_date']
# x2_heid = heidelberg_1991_1994['Decimal_date']
# x3_heid = heidelberg_2006_2016['Decimal_date']
# x4_heid = heidelberg_2006_2009['Decimal_date']
# x5_heid = heidelberg_2012_2016['Decimal_date']
# y1_heid = heidelberg_1986_1991['D14C']
# y2_heid = heidelberg_1991_1994['D14C']
# y3_heid = heidelberg_2006_2016['D14C']
# y4_heid = heidelberg_2006_2009['D14C']
# y5_heid = heidelberg_2012_2016['D14C']
# z1_heid = heidelberg_1986_1991['D14C_err']
# z2_heid = heidelberg_1991_1994['D14C_err']
# z3_heid = heidelberg_2006_2016['D14C_err']
# z4_heid = heidelberg_2006_2009['D14C_err']
# z5_heid = heidelberg_2012_2016['D14C_err']
#
# """
# So now we're almost ready to use the CCGCRV curve smoothing. One tricky bit is that - I want to compare the Cape Grim
# and Baring Head records; however, the x-values in time are not necessarily overlapping. How to best compare them?
# Luckily, the CCGCRV algorithm allows me to OUTPUT the smoothed data at any x-time that I desire. Therefore, in the next
# bit of code, I create an evenly distributed set of x-values that I will output the smoothed baringhead and heidelberg
# data, in 480 points between 1980 and 2020.
#
# "fake_x_temp" is called this way because it is an x-value I have created. Not 'fake' but I was lazy in initial naming
# when first writing the code.
#
# """
# fake_x_temp = np.linspace(1980, 2020, 480)  # create arbitrary set of x-values to control output
# df_fake_xs = pd.DataFrame({'x': fake_x_temp})  # put this set into a pandas DataFrame for easier use
# my_x_1986_1991 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x1_heid)) & (df_fake_xs['x'] <= max(x1_heid))].reset_index(drop=True)  # index it
# my_x_1991_1994 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x2_bhd))  & (df_fake_xs['x'] <= max(x2_bhd))].reset_index(drop=True)  # index it
# my_x_2006_2016 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x3_heid)) & (df_fake_xs['x'] <= max(x3_heid))].reset_index(drop=True)  # index it
# my_x_2006_2009 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x4_heid)) & (df_fake_xs['x'] <= max(x4_heid))].reset_index(drop=True)  # index it
# my_x_2012_2016 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x5_heid)) & (df_fake_xs['x'] <= max(x5_heid))].reset_index(drop=True)  # index it
# my_x_1986_1991 = my_x_1986_1991['x']  # when I wrote the function I'll be using in a few lines,
# my_x_1991_1994 = my_x_1991_1994['x']  # I specify that the first 4 arguments must be input as data/variables that
# my_x_2006_2016 = my_x_2006_2016['x']  # have been extracted from a pandas DataFrame, for consistency across testing
# my_x_2006_2009 = my_x_2006_2009['x']
# my_x_2012_2016 = my_x_2012_2016['x']
#
# """
# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################
#
# Now comes the CCGCRV Curve smoothing, and Monte Carlo error analysis.
#
# The following description also can be found in the my_functions.py file.
#
# This function has three separate for-loops:
# The first for-loop:
# Takes an input array of time-series data and randomizes each data point
# within its measurements uncertainty. It does this "n" times, and vertically stacks it.
# For example, if you have a dataset with 10 measurements, and "n" is 1000, you will end
# up with an array of dimension (10x1000).
# If you're interested in re-testing how the normal distribution randomization works, you can copy and paste the
# following few lines of code. This shows that indeed, the randomization does have a higher probability of putting the
# randomized point closer to the mean, but actually the distribution follows the gaussian curve.
# ###########################
# array = []
# for i in range(0,10000):
#     rand = np.random.normal(10, 2, size=None)
#     array.append(rand)
# plt.hist(array, bins=100)
# plt.show()
# ###########################
#
# The second for-loop:
# Takes each row of the array (each row of "randomized data") and puts it through
# the ccgFilter curve smoother. It is important to define your own x-values that you want output
# if you want to compare two curves (this will keep arrays the same dimension).
# Each row from the fist loop is smoothed and stacked into yet another new array.
#
# The third for-loop:
# Find the mean, standard deviation, and upper and lower uncertainty bounds of each
# "point" in the dataset. This loop takes the mean of all the first measurements, then all the second, etc.
#
# For clarty, I will define all of the arguments here below:
# x_init: x-values of the dataset that you want to smooth. Must be in decimal date format.
# fake_x: x-values of the data you want OUTPUT
# y_init: y-values of the dataset that you want to smooth.
# y_error: y-value errors of the dataset that you want to smooth.
# cutoff: for the CCGCRV algoritm, lower numbers smooth less, and higher numbers smooth more.
#     See hyperlink above for more details.
# n: how many iterations do you want to run? When writing code, keep this low. Once code is solid, increase to 10,000.
#
# ### If you want to see this function in action, refer to "MonteCarlo_Explained.py"
# https://github.com/christianlewis091/radiocarbon_intercomparison/blob/dev/interlab_comparison/MonteCarlo_Explained.py
#
#
# ESSENTIALLY WHAT WE ARE DOING:
# 1. RANDOMIZE THE HEIDELBERG AND BARING HEAD DATA 10,000 TIMES ALONG ITS NORMAL DISTRIBUTION
# 2. SMOOTH THAT DATA USING CCGCRV
# 3. FIND THE MEAN OF EACH X-VALUE FOR THOSE 10,000 ITERATIONS
# 4. COMPARE THE HEIDELBERG AND BARING HEAD DATA IN TIME.
#
# """
# n = 10  # set the amount of times the code will iterate (set to 10,000 once everything is final)
# cutoff = 667  # FFT filter cutoff
# # Curve smoothing with getSmoothValue()
# heidelberg_1986_1991_results_smooth = monte_carlo_randomization_smooth(x1_heid, my_x_1986_1991, y1_heid, z1_heid, cutoff, n)
# heidelberg_1991_1994_results_smooth = monte_carlo_randomization_smooth(x2_heid, my_x_1991_1994, y2_heid, z2_heid, cutoff, n)
# heidelberg_2006_2016_results_smooth = monte_carlo_randomization_smooth(x3_heid, my_x_2006_2016, y3_heid, z3_heid, cutoff, n)
# heidelberg_2006_2009_results_smooth = monte_carlo_randomization_smooth(x4_heid, my_x_2006_2009, y4_heid, z4_heid, cutoff, n)
# heidelberg_2012_2016_results_smooth = monte_carlo_randomization_smooth(x5_heid, my_x_2012_2016, y5_heid, z5_heid, cutoff, n)
# bhd_1986_1991_results_smooth = monte_carlo_randomization_smooth(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)
# bhd_1991_1994_results_smooth = monte_carlo_randomization_smooth(x2_bhd, my_x_1991_1994, y2_bhd, z2_bhd, cutoff, n)
# bhd_2006_2016_results_smooth = monte_carlo_randomization_smooth(x3_bhd, my_x_2006_2016, y3_bhd, z3_bhd, cutoff, n)
# bhd_2006_2009_results_smooth = monte_carlo_randomization_smooth(x4_bhd, my_x_2006_2009, y4_bhd, z4_bhd, cutoff, n)
# bhd_2012_2016_results_smooth = monte_carlo_randomization_smooth(x5_bhd, my_x_2012_2016, y5_bhd, z5_bhd, cutoff, n)
# # Curve smoothing with getTrendValue()
# heidelberg_1986_1991_results_trend = monte_carlo_randomization_trend(x1_heid, my_x_1986_1991, y1_heid, z1_heid, cutoff, n)
# heidelberg_1991_1994_results_trend = monte_carlo_randomization_trend(x2_heid, my_x_1991_1994, y2_heid, z2_heid, cutoff, n)
# heidelberg_2006_2016_results_trend = monte_carlo_randomization_trend(x3_heid, my_x_2006_2016, y3_heid, z3_heid, cutoff, n)
# heidelberg_2006_2009_results_trend = monte_carlo_randomization_trend(x4_heid, my_x_2006_2009, y4_heid, z4_heid, cutoff, n)
# heidelberg_2012_2016_results_trend = monte_carlo_randomization_trend(x5_heid, my_x_2012_2016, y5_heid, z5_heid, cutoff, n)
# bhd_1986_1991_results_trend = monte_carlo_randomization_trend(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)
# bhd_1991_1994_results_trend = monte_carlo_randomization_trend(x2_bhd, my_x_1991_1994, y2_bhd, z2_bhd, cutoff, n)
# bhd_2006_2016_results_trend = monte_carlo_randomization_trend(x3_bhd, my_x_2006_2016, y3_bhd, z3_bhd, cutoff, n)
# bhd_2006_2009_results_trend = monte_carlo_randomization_trend(x4_bhd, my_x_2006_2009, y4_bhd, z4_bhd, cutoff, n)
# bhd_2012_2016_results_trend = monte_carlo_randomization_trend(x5_bhd, my_x_2012_2016, y5_bhd, z5_bhd, cutoff, n)
#
# # TODO write a function to simplify the block of code in A_heidelberg_intercomparison.py lines 351 - 455.
# # the [2] contains the means and stdevs summary dataframe
# smooths_array = []  # initialize empty array for "data-dump"
# list = [heidelberg_1986_1991_results_smooth[2],
#         heidelberg_1991_1994_results_smooth[2],
#         heidelberg_2006_2016_results_smooth[2],
#         heidelberg_2006_2009_results_smooth[2],
#         heidelberg_2012_2016_results_smooth[2],
#         bhd_1986_1991_results_smooth[2],
#         bhd_1991_1994_results_smooth[2],
#         bhd_2006_2016_results_smooth[2],
#         bhd_2006_2009_results_smooth[2],
#         bhd_2012_2016_results_smooth[2]]
#
#
#
#
# # testing = monte_carlo_randomization_smooth(x3_bhd, my_x_2006_2016, y3_bhd, z3_bhd, cutoff, n)
# # testing the function
# x_init = x3_bhd.reset_index(drop=True)  # ensure x-values begin at index 0
# y_init = y3_bhd.reset_index(drop=True)  # ensure y-values begin at index 0
# y_error = z3_bhd.reset_index(drop=True)  # ensure y err-values begin at index 0
# # fake_x_for_dataframe = fake_x.reset_index(drop=True)  # ensure output x-values at index 0
# # fake_x_for_dataframe = fake_x_for_dataframe['x']  # if not already extracted, extract the data from the DataFrame
#
# # First for-loop: randomize the y-values.
#
# # The line below: creates a copy of the y-value column. This is helpful because as I randomize the y-data, I will
# # stack each new randomized column. So if n = 10, there will 10 stacked, randomized columns. The initial column
# # was helpful to get the code running - was something to "stick the stack on". Not sure if this was required, but
# # it helped me get the for-loop to run.
# new_array = y_init
#
# for i in range(0, n):  # initialize the for-loop. It will run "n" times.
#     empty_array = []  # initialize an empty array to add each individual value onto.
#     for j in range(0, len(y_init)):  # nested loop: run through the column of y-data, length-of-y times.
#         a = y_init[j]  # grab the j'th item in the y-value set
#         b = y_error[j]  # grab the j'th item in the uncertainty set
#         # return a random value in the normal distribution of a data point/error
#         rand = np.random.normal(a, b, size=None)
#         # (https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html)
#         empty_array.append(rand)  # append this randomized value to my growing list, the "empty_array"
#     # the nested loop just finished filling another iteration of the empty array.
#     # Now stack this onto our initialized "new_array" from line 89.
#     new_array = np.vstack((new_array, empty_array))
#     # The line below takes the new array and puts it into a pandas DataFrame.
#     # This helps format the data in a way where it can be more quickly tested, and used in the future.
#     # To plot the randomized data, index each row using randomized_dataframe.iloc[0]
# randomized_dataframe = pd.DataFrame(new_array)
# print(randomized_dataframe)
# # end of first for-loop
# ##################################################################################################################
# ##################################################################################################################
# ##################################################################################################################
# # Second for-loop: smooth the randomized data using John Miller's CCGCRV.
#
# # Create an initial, trended array on which later arrays that are created will stack
# template_array = ccgFilter(x_init, new_array[0], cutoff).getSmoothValue(my_x_2006_2016)
# summary = pd.DataFrame({"x_init": x_init, "y": new_array[0]})
# summary.to_excel('testing.xlsx')
# print(template_array)
# plt.scatter(x_init, new_array[0])
# plt.show()
#
#
#
#
#
#
#
#
#
# # this for smooths each row of the randomized array from above, and stacks it up
# for k in range(0, len(new_array)):
#     row = new_array[k]  # grab the first row of the data
#     smooth = ccgFilter(x_init, row, cutoff).getSmoothValue(my_x_2006_2016)  # outputs smooth values at my desired times, x
#     template_array = np.vstack((template_array, smooth))
#
# # over time I have had to go between horizontal and vertical stacking of the data as I learn more about programming.
# # beacuse it could lead to confusion, I've provided both types of DataFrames here on the two following lines,
# # one where each iteration is contained as ROWS and one where each iteration is contained as a COLUMN.
#
# # each ROW is a new iteration. each COLUMN in a given X value
# smoothed_dataframe = pd.DataFrame(template_array)
# # each COLUMN is a new iteration. Each ROW is a given X value
# smoothed_dataframe_trans = pd.DataFrame.transpose(smoothed_dataframe)
#
# mean_array = []
# stdev_array = []
# for i in range(0, len(smoothed_dataframe_trans)):
#     row = smoothed_dataframe_trans.iloc[i]  # grab the first row of data
#     stdev = np.std(row)  # compute the standard deviation of that row
#     sum1 = np.sum(row)  # take the sum, and then mean (next line) of that data
#     mean1 = sum1 / len(row)  # find the mean of that row
#     mean_array.append(mean1)  # append the mean it to a new array
#     stdev_array.append(stdev)  # append the stdev to a new array
#
# summary = pd.DataFrame({"Means": mean_array, "stdevs": stdev_array})
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # summary = testing[2]
# #
# # testdf = pd.DataFrame({"x": x3_bhd, "y": y3_bhd, "z": z3_bhd})
# #
# # testdf.to_excel('testing.xlsx')
# # summary.to_excel('testing2.xlsx')
#
#
#
#
#
#
#
