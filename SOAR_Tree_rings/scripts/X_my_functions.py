import numpy as np
from X_miller_curve_algorithm import ccgFilter
from PyAstronomy import pyasl
from tabulate import tabulate
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import stats

# general plot parameters
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

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
        print('The average difference between the groups is ' + str(mean1) + 'and std error is ' + str(standard_error))

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
        print('The average difference between the groups is ' + str(offset) + 'and std error is ' + str(error_prop))
    print(result)  # Print the t-test result
    if result[1] < 0.01:  # if statement for me to print if they are different
        print("The data are different at 98% confidence")
    else:
        print("The data are not different")
    print('\n' * 1)  # print some blank lines
    return result


def scatter_plot(x1, y1, x2=None, y2=None, x3=None, y3=None, x4=None, y4=None,
                 label1=None, label2=None, label3=None, label4=None,
                 color1=None, color2=None, color3=None, color4=None,
                 xmin=None, xmax=None, ymin=None, ymax=None, title=None, xlabel=None,
                 ylabel=None, savename=None, size1=None, **kwargs):
    if color1 is None:
        color1 = colors[3]
    if color2 is None:
        color2 = colors2[3]
    if color3 is None:
        color3 = colors[4]
    if color4 is None:
        color4 = colors2[4]

    plt.scatter(x1, y1, marker='o', label='{}'.format(label1), color=color1, s=size1)
    if y2 is not None:
        plt.scatter(x2, y2, marker='D', label='{}'.format(label2), color=color2, s=size1)

    if y3 is not None:
        plt.scatter(x3, y3, marker='^', label='{}'.format(label3), color=color3, s=size1)

    if y4 is not None:
        plt.scatter(x4, y4, marker='X', label='{}'.format(label4), color=color4, s=size1)

    if title is not None:
        plt.title('{}'.format(title))
    if xmin is not None:
        plt.xlim([xmin, xmax])
    if ymin is not None:
        plt.ylim([ymin, ymax])
    if xlabel is not None:
        plt.xlabel('{}'.format(xlabel), fontsize=14)
    if ylabel is not None:
        plt.ylabel('{}'.format(ylabel), fontsize=14)
    plt.legend()
    plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/{}.png'.format(
        savename),
        dpi=300, bbox_inches="tight")
    plt.close()


def error_plot(x1, y1, z1, x2=None, y2=None, x3=None, y3=None, x4=None, y4=None,
               label1=None, label2=None, label3=None, label4=None,
               color1=None, color2=None, color3=None, color4=None,
               xmin=None, xmax=None, ymin=None, ymax=None, title=None, xlabel=None,
               ylabel=None, savename=None, size1=None,
               z2=None, z3=None, z4=None,
               **kwargs):
    if color1 is None:
        color1 = colors[3]
    if color2 is None:
        color2 = colors2[3]
    if color3 is None:
        color3 = colors[4]
    if color4 is None:
        color4 = colors2[4]

    plt.errorbar(x1, y1, yerr=z1, marker='o', label='{}'.format(label1), color=color1, ecolor=color1, elinewidth=1,
                 capsize=2)
    # if y2 is not None:
    plt.errorbar(x2, y2, yerr=z2, marker='D', label='{}'.format(label2), color=color2, ecolor=color2, elinewidth=1,
                 capsize=2)

    if y3 is not None:
        plt.errorbar(x3, y3, marker='^', label='{}'.format(label3), color=color3, ecolor=color3, elinewidth=1,
                     capsize=2)

    if y4 is not None:
        plt.errorbar(x4, y4, marker='X', label='{}'.format(label4), color=color4, ecolor=color4, elinewidth=1,
                     capsize=2)

    if title is not None:
        plt.title('{}'.format(title))
    if xmin is not None:
        plt.xlim([xmin, xmax])
    if ymin is not None:
        plt.ylim([ymin, ymax])
    if xlabel is not None:
        plt.xlabel('{}'.format(xlabel), fontsize=14)
    if ylabel is not None:
        plt.ylabel('{}'.format(ylabel), fontsize=14)
    plt.legend()
    plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/{}.png'.format(
        savename),
        dpi=300, bbox_inches="tight")
    plt.close()


# IDEA IS THERE BUT NEEDS MORE WORK.
# def subplot_plot(plot_num, x1, y1, label1=None, color1=None, size1=None, savename=None,
#                  x2= None, y2= None,  label2=None, color2=None,
#                  x3= None, y3= None,  label3=None, color3=None,
#                  x4= None, y4= None,  label4=None, color4=None,
#                  x5= None, y5= None,  label5=None, color5=None,
#                  x6= None, y6= None,  label6=None, color6=None,
#                  **kwargs):
#     fig = plt.figure(1, figsize=(10, 5))  # how big do you want the figure?
#     if plot_num == 2:
#         gs = gridspec.GridSpec(1, 2)
#         xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
#         plt.scatter(x1, y1, marker='o', label='{}'.format(label1), color=color1, s=size1)
#         xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
#         plt.savefig(
#             'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/{}.png'.format(
#                 savename),
#             dpi=300, bbox_inches="tight")
#
#
# x = [1, 2, 3]
# y = [3, 4, 5]
# subplot_plot(2, x, y)


"""
This function will convert FM to D14C. 
"""


def d14C_to_fm(D14C, D14C_err, date):
    # D14C = 1000*(fm - 1)   # first, find D14C (without the age correction)
    age_corr = np.exp((1950 - date) / 8267)
    FM = ((D14C / 1000) + 1) / age_corr
    FM_err = D14C_err / 1000
    return FM, FM_err


# TO TEST, RUN THE CODE BELOW.
# df = pd.read_excel(r'H:\The Science\Datasets\function_testing.xlsx')  # import Baring Head data
# x = d14C_to_fm(df['D14C'], df['D14C_err'], 2020)
#
# FM_out = x[0]
# FM_err_out = x[1]
#
# df['FM_out'] = FM_out
# df['FM_out_err'] = FM_err_out
# df.to_excel('function_testing_check.xlsx')


"""
This function will convert FM to D14C. 
"""


def fm_to_d14c(fm, fm_err, date):
    # D14C = 1000*(fm - 1)   # first, find D14C (without the age correction)
    age_corr = np.exp((1950 - date) / 8267)
    Del14C = 1000 * ((fm * age_corr) - 1)
    Del14C_err = 1000 * fm_err
    return Del14C, Del14C_err


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
If you're interested in re-testing how the normal distribution randomization works, you can copy and paste the 
following few lines of code. This shows that indeed, the randomization does have a higher probability of putting the 
randomized point closer to the mean, but actually the distribution follows the gaussian curve. 
###########################
array = []
for i in range(0,10000):
    rand = np.random.normal(10, 2, size=None)
    array.append(rand)
plt.hist(array, bins=100)
plt.show()
###########################

The second for-loop: 
Takes each row of the array (each row of "randomized data") and puts it through
the ccgFilter curve smoother. It is important to define your own x-values that you want output
if you want to compare two curves (this will keep arrays the same dimension).
Each row from the fist loop is smoothed and stacked into yet another new array.

The third for-loop: 
Find the mean, standard deviation, and upper and lower uncertainty bounds of each
"point" in the dataset. This loop takes the mean of all the first measurements, then all the second, etc.

For clarty, I will define all of the arguments here below: 
FIRST 4 ARGUMENTS MUST BE EXTRACTED FROM A PANDAS DATAFRAME. If your code doesn't work, try checking the format.
x_init: x-values of the dataset that you want to smooth. Must be in decimal date format. 
fake_x: x-values of the data you want OUTPUT
y_init: y-values of the dataset that you want to smooth. 
y_error: y-value errors of the dataset that you want to smooth. 
cutoff: for the CCGCRV algoritm, lower numbers smooth less, and higher numbers smooth more. 
    See hyperlink above for more details. 
n: how many iterations do you want to run? When writing code, keep this low. Once code is solid, increase to 10,000. 

### If you want to see this function in action, refer to "MonteCarlo_Explained.py"
https://github.com/christianlewis091/radiocarbon_intercomparison/blob/dev/interlab_comparison/MonteCarlo_Explained.py

"""


def monte_carlo_randomization_smooth(x_init, fake_x, y_init, y_error, cutoff, n):  # explanation of arguments above
    # THE WAY I AM WRITING THE CODE:
    # ALL VARIABLES MUST BE EXTRACTED FROM A PANDAS DATAFRAME. If your code doesn't work, try checking the format.

    x_init = x_init.reset_index(drop=True)  # ensure x-values begin at index 0
    y_init = y_init.reset_index(drop=True)  # ensure y-values begin at index 0
    y_error = y_error.reset_index(drop=True)  # ensure y err-values begin at index 0
    # fake_x_for_dataframe = fake_x.reset_index(drop=True)  # ensure output x-values at index 0
    # fake_x_for_dataframe = fake_x_for_dataframe['x']  # if not already extracted, extract the data from the DataFrame

    # First for-loop: randomize the y-values.

    # The line below: creates a copy of the y-value column. This is helpful because as I randomize the y-data, I will
    # stack each new randomized column. So if n = 10, there will 10 stacked, randomized columns. The initial column
    # was helpful to get the code running - was something to "stick the stack on". Not sure if this was required, but
    # it helped me get the for-loop to run.
    new_array = y_init

    for i in range(0, n):  # initialize the for-loop. It will run "n" times.
        empty_array = []  # initialize an empty array to add each individual value onto.
        for j in range(0, len(y_init)):  # nested loop: run through the column of y-data, length-of-y times.
            a = y_init[j]  # grab the j'th item in the y-value set
            b = y_error[j]  # grab the j'th item in the uncertainty set
            # return a random value in the normal distribution of a data point/error
            rand = np.random.normal(a, b, size=None)
            # (https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html)
            empty_array.append(rand)  # append this randomized value to my growing list, the "empty_array"
        # the nested loop just finished filling another iteration of the empty array.
        # Now stack this onto our initialized "new_array" from line 89.
        new_array = np.vstack((new_array, empty_array))
        # The line below takes the new array and puts it into a pandas DataFrame.
        # This helps format the data in a way where it can be more quickly tested, and used in the future.
        # To plot the randomized data, index each row using randomized_dataframe.iloc[0]
    randomized_dataframe = pd.DataFrame(new_array)

    # end of first for-loop
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    # Second for-loop: smooth the randomized data using John Miller's CCGCRV.

    # Create an initial, trended array on which later arrays that are created will stack
    template_array = ccgFilter(x_init, new_array[0], cutoff).getSmoothValue(fake_x)

    # this for smooths each row of the randomized array from above, and stacks it up
    for k in range(0, len(new_array)):
        row = new_array[k]  # grab the first row of the data
        smooth = ccgFilter(x_init, row, cutoff).getSmoothValue(fake_x)  # outputs smooth values at my desired times, x
        template_array = np.vstack((template_array, smooth))

    # over time I have had to go between horizontal and vertical stacking of the data as I learn more about programming.
    # beacuse it could lead to confusion, I've provided both types of DataFrames here on the two following lines,
    # one where each iteration is contained as ROWS and one where each iteration is contained as a COLUMN.

    # each ROW is a new iteration. each COLUMN in a given X value
    smoothed_dataframe = pd.DataFrame(template_array)
    # each COLUMN is a new iteration. Each ROW is a given X value
    smoothed_dataframe_trans = pd.DataFrame.transpose(smoothed_dataframe)

    mean_array = []
    stdev_array = []
    for i in range(0, len(smoothed_dataframe_trans)):
        row = smoothed_dataframe_trans.iloc[i]  # grab the first row of data
        stdev = np.std(row)  # compute the standard deviation of that row
        sum1 = np.sum(row)  # take the sum, and then mean (next line) of that data
        mean1 = sum1 / len(row)  # find the mean of that row
        mean_array.append(mean1)  # append the mean it to a new array
        stdev_array.append(stdev)  # append the stdev to a new array

    summary = pd.DataFrame({"Means": mean_array, "stdevs": stdev_array})

    return randomized_dataframe, smoothed_dataframe, summary


def monte_carlo_randomization_trend(x_init, fake_x, y_init, y_error, cutoff, n):  # explanation of arguments above
    # THE WAY I AM WRITING THE CODE:
    # ALL VARIABLES MUST BE EXTRACTED FROM A PANDAS DATAFRAME. If your code doesn't work, try checking the format.

    x_init = x_init.reset_index(drop=True)  # ensure x-values begin at index 0
    y_init = y_init.reset_index(drop=True)  # ensure y-values begin at index 0
    y_error = y_error.reset_index(drop=True)  # ensure y err-values begin at index 0
    # fake_x_for_dataframe = fake_x.reset_index(drop=True)  # ensure output x-values at index 0
    # fake_x_for_dataframe = fake_x_for_dataframe['x']  # if not already extracted, extract the data from the DataFrame

    # First for-loop: randomize the y-values.

    # The line below: creates a copy of the y-value column. This is helpful because as I randomize the y-data, I will
    # stack each new randomized column. So if n = 10, there will 10 stacked, randomized columns. The initial column
    # was helpful to get the code running - was something to "stick the stack on". Not sure if this was required, but
    # it helped me get the for-loop to run.
    new_array = y_init

    for i in range(0, n):  # initialize the for-loop. It will run "n" times.
        empty_array = []  # initialize an empty array to add each individual value onto.
        for j in range(0, len(y_init)):  # nested loop: run through the column of y-data, length-of-y times.
            a = y_init[j]  # grab the j'th item in the y-value set
            b = y_error[j]  # grab the j'th item in the uncertainty set
            # return a random value in the normal distribution of a data point/error
            rand = np.random.normal(a, b, size=None)
            # (https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html)
            empty_array.append(rand)  # append this randomized value to my growing list, the "empty_array"
        # the nested loop just finished filling another iteration of the empty array.
        # Now stack this onto our initialized "new_array" from line 89.
        new_array = np.vstack((new_array, empty_array))
        # The line below takes the new array and puts it into a pandas DataFrame.
        # This helps format the data in a way where it can be more quickly tested, and used in the future.
        # To plot the randomized data, index each row using randomized_dataframe.iloc[0]
    randomized_dataframe = pd.DataFrame(new_array)

    # end of first for-loop
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    # Second for-loop: smooth the randomized data using John Miller's CCGCRV.

    # Create an initial, trended array on which later arrays that are created will stack
    template_array = ccgFilter(x_init, new_array[0], cutoff).getTrendValue(fake_x)

    # this for smooths each row of the randomized array from above, and stacks it up
    for k in range(0, len(new_array)):
        row = new_array[k]  # grab the first row of the data
        smooth = ccgFilter(x_init, row, cutoff).getTrendValue(fake_x)  # outputs smooth values at my desired times, x
        template_array = np.vstack((template_array, smooth))

    # over time I have had to go between horizontal and vertical stacking of the data as I learn more about programming.
    # beacuse it could lead to confusion, I've provided both types of DataFrames here on the two following lines,
    # one where each iteration is contained as ROWS and one where each iteration is contained as a COLUMN.

    # each ROW is a new iteration. each COLUMN in a given X value
    smoothed_dataframe = pd.DataFrame(template_array)
    # each COLUMN is a new iteration. Each ROW is a given X value
    smoothed_dataframe_trans = pd.DataFrame.transpose(smoothed_dataframe)

    mean_array = []
    stdev_array = []
    for i in range(0, len(smoothed_dataframe_trans)):
        row = smoothed_dataframe_trans.iloc[i]  # grab the first row of data
        stdev = np.std(row)  # compute the standard deviation of that row
        sum1 = np.sum(row)  # take the sum, and then mean (next line) of that data
        mean1 = sum1 / len(row)  # find the mean of that row
        mean_array.append(mean1)  # append the mean it to a new array
        stdev_array.append(stdev)  # append the stdev to a new array

    summary = pd.DataFrame({"Means": mean_array, "stdevs": stdev_array})

    return randomized_dataframe, smoothed_dataframe, summary


"""
######################################################################################################################
######################################################################################################################
######################################################################################################################
RETIRED FUNCTIONS NO LONGER IN USE
######################################################################################################################
######################################################################################################################
######################################################################################################################
"""


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


"""
This function does a paired two-tail t-test. The t-value range comes from the stdev_array in the
Monte Carlo function above, and errors are propagated through the t-test mathematics.

This has been replaced by
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html
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
        r'H:\The Science\Datasets\tables.xlsx',
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
        print(data)
        print('There is NO observed difference at 95% confidence interval')
        print('')
        print('')
        result = 1

    else:
        data = [t_stat, t_stat_e6, value_crit, mean1, err_mean]
        headers = ['t-statistic', 't-statistic error', 'critical value', 'mean of differences', 'error of mean']
        data = pd.DataFrame(data, headers)
        print(data)
        print('There IS AN observed difference at 95% confidence interval')
        print('')
        print('')

        result = 0

    return result


"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
PLOTTING FUNCTIONS
"""
"""Setup some colors for later"""
# https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3
# Skyblue to distant mountain green
a1, a2, a3, a4, a5, a6 = '#253494','#7fcdbb','#2c7fb8','#c7e9b4','#41b6c4','#ffffcc'
c1, c2, c3 = '#ece2f0', '#a6bddb', '#1c9099'
d1, d2 = '#ef8a62', '#67a9cf'
size1 = 10

"""
can plot ONE line plot, and up to 4 overlaid scatters
"""


def plotfunc_line(px1, py1, label_p1=None, color_p1=a1, alpha_p1=None,
                  sx1=None, sy1=None, label_s1=None, color_s1=a2, alpha_s1=None, marker_s1='o', size1=None,
                  sx2=None, sy2=None, label_s2=None, color_s2=a3, alpha_s2=None, marker_s2='D',
                  sx3=None, sy3=None, label_s3=None, color_s3=a4, alpha_s3=None, marker_s3='x',
                  sx4=None, sy4=None, label_s4=None, color_s4=a5, alpha_s4=None, marker_s4='^',
                  xmin=None, xmax=None, ymin=None, ymax=None,
                  ylab='\u0394$^1$$^4$CO$_2$ (\u2030)', xlab='Date', name='unnamed'):
    plt.plot(px1, py1, label='{}'.format(label_p1), color=color_p1, alpha=alpha_p1)
    plt.scatter(sx1, sy1, label='{}'.format(label_s1), color=color_s1, alpha=alpha_s1, marker=marker_s1, s=size1)
    plt.scatter(sx2, sy2, label='{}'.format(label_s2), color=color_s2, alpha=alpha_s2, marker=marker_s2, s=size1)
    plt.scatter(sx3, sy3, label='{}'.format(label_s3), color=color_s3, alpha=alpha_s3, marker=marker_s3, s=size1)
    plt.scatter(sx4, sy4, label='{}'.format(label_s4), color=color_s4, alpha=alpha_s4, marker=marker_s4, s=size1)
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])
    plt.xlabel(xlab, fontsize=14)
    plt.ylabel(ylab, fontsize=14)  # label the y axis
    plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/{0}.png'.format(name),
                dpi=300, bbox_inches="tight")
    plt.close()


"""
can plot up to 4 overlaid scatters
"""


def plotfunc_scat(sx1, sy1, label_s1=None, color_s1=a1, alpha_s1=None, marker_s1='o', size1=None,
                  sx2=None, sy2=None, label_s2=None, color_s2=a2, alpha_s2=None, marker_s2='D',
                  sx3=None, sy3=None, label_s3=None, color_s3=a3, alpha_s3=None, marker_s3='x',
                  sx4=None, sy4=None, label_s4=None, color_s4=a4, alpha_s4=None, marker_s4='^',
                  xmin=None, xmax=None, ymin=None, ymax=None,
                  ylab='\u0394$^1$$^4$CO$_2$ (\u2030)', xlab='Date', name='unnamed'):
    plt.scatter(sx1, sy1, label='{}'.format(label_s1), color=color_s1, alpha=alpha_s1, marker=marker_s1, s=size1)
    plt.scatter(sx2, sy2, label='{}'.format(label_s2), color=color_s2, alpha=alpha_s2, marker=marker_s2, s=size1)
    plt.scatter(sx3, sy3, label='{}'.format(label_s3), color=color_s3, alpha=alpha_s3, marker=marker_s3, s=size1)
    plt.scatter(sx4, sy4, label='{}'.format(label_s4), color=color_s4, alpha=alpha_s4, marker=marker_s4, s=size1)
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])
    plt.xlabel(xlab, fontsize=14)
    plt.ylabel(ylab, fontsize=14)  # label the y axis
    plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/{0}.png'.format(name),
                dpi=300, bbox_inches="tight")
    plt.close()


"""
can plot ONE line plot, and up to 4 overlaid scatters
"""


def plotfunc_2line(px1, py1, px2, py2,
                   label_p1=None, color_p1=a1, alpha_p1=None,
                   label_p2=None, color_p2=a2, alpha_p2=None, size1=None,
                   sx1=None, sy1=None, label_s1=None, color_s1=a3, alpha_s1=None, marker_s1='o',
                   sx2=None, sy2=None, label_s2=None, color_s2=a4, alpha_s2=None, marker_s2='D',
                   sx3=None, sy3=None, label_s3=None, color_s3=a5, alpha_s3=None, marker_s3='x',
                   sx4=None, sy4=None, label_s4=None, color_s4=a6, alpha_s4=None, marker_s4='^',
                   xmin=None, xmax=None, ymin=None, ymax=None,
                   ylab='\u0394$^1$$^4$CO$_2$ (\u2030)', xlab='Date', name='unnamed'):
    plt.plot(px1, py1, label='{}'.format(label_p1), color=color_p1, alpha=alpha_p1)
    plt.plot(px2, py2, label='{}'.format(label_p2), color=color_p2, alpha=alpha_p2)
    plt.scatter(sx1, sy1, label='{}'.format(label_s1), color=color_s1, alpha=alpha_s1, marker=marker_s1, s=size1)
    plt.scatter(sx2, sy2, label='{}'.format(label_s2), color=color_s2, alpha=alpha_s2, marker=marker_s2, s=size1)
    plt.scatter(sx3, sy3, label='{}'.format(label_s3), color=color_s3, alpha=alpha_s3, marker=marker_s3, s=size1)
    plt.scatter(sx4, sy4, label='{}'.format(label_s4), color=color_s4, alpha=alpha_s4, marker=marker_s4, s=size1)
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])
    plt.xlabel(xlab, fontsize=14)
    plt.ylabel(ylab, fontsize=14)  # label the y axis
    plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/{0}.png'.format(name),
                dpi=300, bbox_inches="tight")
    plt.close()


"""
can plot up to 4 overlaid scatters
"""


def plotfunc_error(sx1, sy1, sz1, xmin=None, xmax=None, ymin=None, ymax=None,
                   ylab='\u0394$^1$$^4$CO$_2$ (\u2030)', xlab='Date', name='unnamed'):

    plt.errorbar(sx1, sy1, yerr=sz1, fmt='o', color=a1, ecolor=a1, elinewidth=1, capsize=2, label='RRL NWT3')
    fig = plt.figure(1, figsize=(16.1, 10))
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])
    plt.xlabel(xlab, fontsize=14)
    plt.ylabel(ylab, fontsize=14)  # label the y axis
    plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/{0}.png'.format(name),
                dpi=300, bbox_inches="tight")
    plt.close()



