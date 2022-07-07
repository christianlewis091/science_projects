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
fake_x_temp = np.linspace(1986, 2016, 1920)  # create arbitrary set of x-values to control output
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
n = 100
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


def offset_calc(y1, y1err, y2, y2err, date):

    difference = np.subtract(y1, y2)                  # subtract the data from each other
    difference_error = np.sqrt(y1err**2 + y2err**2)   # propagate the error of differencing
    mean_of_differences = np.average(difference)
    standard_error = np.std(difference) / np.sqrt(len(y1))  # standard error of the subtraction array
    return difference, difference_error, mean_of_differences, standard_error, date


# The following for loop will calculate all the offsets for the different DataFrames in the array we created above
# SMOOTH
differences = []
difference_errors = []
mean_of_difference = []
std_error = []
dates = []
for i in range(0, len(df_array)):
    df = df_array[i]                                                        # access the first dataframe
    x = offset_calc(df["rafter_means_smooth"], df["rafter_stdevs_smooth"], df["heid_means_smooth"], df["heid_stdevs_smooth"], df['Decimal_date'])
    dif = x[0]
    dif_er = x[1]
    m = x[2]
    stderr = x[3]
    date = x[4]
    differences.append(dif)
    difference_errors.append(dif_er)
    mean_of_difference.append(m)
    std_error.append(stderr)
    dates.append(date)


dates_dataframe = pd.DataFrame({'I1 Dates': dates[0],
                              'I2 Dates': dates[1],
                              'I3 Dates': dates[2],
                              'I4 Dates': dates[3],
                              'I5 Dates': dates[4],
                              'I6 Dates': dates[5],
                              'I7 Dates': dates[6],
                              'I8 Dates': dates[7],
                              'I9 Dates': dates[8]})
smooth_differences = pd.DataFrame({
                                   'I1 Differences': differences[0],
                                    'I2 Differences': differences[1],
                                    'I3 Differences': differences[2],
                                    'I4 Differences': differences[3],
                                    'I5 Differences': differences[4],
                                    'I6 Differences': differences[5],
                                    'I7 Differences': differences[6],
                                    'I8 Differences': differences[7],
                                    'I9 Differences': differences[8]})
smooth_difference_errors = pd.DataFrame({'I1 Differences 1-sigma error': differences[0],
                                         'I2 Differences 1-sigma error': differences[1],
                                         'I3 Differences 1-sigma error': differences[2],
                                         'I4 Differences 1-sigma error': differences[3],
                                         'I5 Differences 1-sigma error': differences[4],
                                         'I6 Differences 1-sigma error': differences[5],
                                         'I7 Differences 1-sigma error': differences[6],
                                         'I8 Differences 1-sigma error': differences[7],
                                         'I9 Differences 1-sigma error': differences[8]})
smooth_diff_summary2 = pd.DataFrame({'Time Period': intervals,'Means': mean_of_difference, "Standard error": std_error})


# TREND
differences = []
difference_errors = []
mean_of_difference = []
std_error = []
dates = []
for i in range(0, len(df_array)):
    df = df_array[i]                                                        # access the first dataframe
    x = offset_calc(df["rafter_means_trend"], df["rafter_stdevs_trend"], df["heid_means_trend"], df["heid_stdevs_trend"], df['Decimal_date'])
    dif = x[0]
    dif_er = x[1]
    m = x[2]
    stderr = x[3]
    date = x[4]
    differences.append(dif)
    difference_errors.append(dif_er)
    mean_of_difference.append(m)
    std_error.append(stderr)

trend_differences = pd.DataFrame({'I1 Differences': differences[0],
                                   'I2 Differences': differences[1],
                                   'I3 Differences': differences[2],
                                   'I4 Differences': differences[3],
                                   'I5 Differences': differences[4],
                                   'I6 Differences': differences[5],
                                   'I7 Differences': differences[6],
                                   'I8 Differences': differences[7],
                                   'I9 Differences': differences[8]})
trend_difference_errors = pd.DataFrame({'I1 Differences 1-sigma error': differences[0],
                                         'I2 Differences 1-sigma error': differences[1],
                                         'I3 Differences 1-sigma error': differences[2],
                                         'I4 Differences 1-sigma error': differences[3],
                                         'I5 Differences 1-sigma error': differences[4],
                                         'I6 Differences 1-sigma error': differences[5],
                                         'I7 Differences 1-sigma error': differences[6],
                                         'I8 Differences 1-sigma error': differences[7],
                                         'I9 Differences 1-sigma error': differences[8]})
trend_diff_summary2 = pd.DataFrame({'Time Period': intervals,'Means': mean_of_difference, "Standard error": std_error})

# what about the t-tests
for i in range(0, 8):  # for the 9 time intervals that we're exploring for the data
    x = df_array[i]    # access the first dataframe, which contains the means for the first time interval:
    paired_t = intercomparison_ttest(x['rafter_means_smooth'], x['heid_means_smooth'], 'Rafter vs Heidelberg Paired T-test, smoothed Result', 'paired')

for i in range(0, 8):  # for the 9 time intervals that we're exploring for the data
    x = df_array[i]    # access the first dataframe, which contains the means for the first time interval:
    paired_t = intercomparison_ttest(x['rafter_means_trend'], x['heid_means_trend'], 'Rafter vs Heidelberg Paired T-test, trend Result', 'paired')

# The following data will be written to a file beacuse when I read it into the vizualization data,
# I don't want the data to have to run through 10,000 iterations of Monte Carlo each time I want to make a plot.
# SO, I'm going to run once at 10,000 and save the files, then set n back to 10.

# What do I need to go to Excel?
# df_array: array of the result dataframes from the 9 different time intervals
# smooth_diff_summary
# smooth_diff_summary2
# trend_diff_summary
# trend_diff_summary2

# write the data to excel
sheetnames = ['Means 1986 - 2016', 'Means 1986 - 1990','Means 1990 - 1994', 'Means 1986 - 1994','Means 1994 - 2006','Means 2006 - 2016','Means 2006 - 2009','Means 2009 - 2012','Means 2012 - 2016']
writer = pd.ExcelWriter('Heidelberg_intercomparison_result_10000_July82022.xlsx', engine='openpyxl')
for i in range(0, len(df_array)):
    df = df_array[i]
    df.to_excel(writer, sheet_name=str(sheetnames[i]))
writer.save()

# add the differences sheet
writer = pd.ExcelWriter('Heidelberg_intercomparison_result_differences_10000_July82022.xlsx', engine='openpyxl')
dates_dataframe.to_excel(writer, sheet_name='Dates')
smooth_differences.to_excel(writer, sheet_name='Smooth Differences')
smooth_diff_summary2.to_excel(writer, sheet_name='Smoothed Differences Summary')
smooth_difference_errors.to_excel(writer, sheet_name='Smooth Differences Error')
trend_differences.to_excel(writer, sheet_name='Trend Differences')
trend_difference_errors.to_excel(writer, sheet_name='Trend Differences Error')
trend_diff_summary2.to_excel(writer, sheet_name='Trend Differences Summary')
writer.save()








