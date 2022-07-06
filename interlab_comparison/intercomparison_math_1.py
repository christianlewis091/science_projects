import numpy as np
import pandas as pd
from scipy import stats
# import the data from the "Pre-Processing" files:
from Pre_Processing_ANSTO import combine_ANSTO
from Pre_Processing_Heidelberg import combine_heidelberg
from Pre_Processing_UniMagallanes import combine_Magallanes
from Pre_Processing_SIO_LLNL import combine_SIO
from X_my_functions import monte_carlo_randomization_trend, monte_carlo_randomization_smooth
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
print(baringhead)
heidelberg = combine_heidelberg.loc[(combine_heidelberg['Site'] == 'CGO')]
print(heidelberg)

baringhead_1986_1991 = baringhead.loc[(baringhead['Decimal_date'] >= 1987) & (baringhead['Decimal_date'] <= 1991)].reset_index(drop=True)
baringhead_1991_1994 = baringhead.loc[(baringhead['Decimal_date'] >= 1991) & (baringhead['Decimal_date'] <= 1994)].reset_index(drop=True)
# baringhead_1994_2006 = baringhead.loc[(baringhead['Decimal_date'] >= 1994) & (baringhead['Decimal_date'] <= 2006)].reset_index(drop=True)
baringhead_2006_2016 = baringhead.loc[(baringhead['Decimal_date'] > 2006) & (baringhead['Decimal_date'] <= 2016)].reset_index(drop=True)
baringhead_2006_2009 = baringhead.loc[(baringhead['Decimal_date'] >= 2006) & (baringhead['Decimal_date'] <= 2009)].reset_index(drop=True)
baringhead_2012_2016 = baringhead.loc[(baringhead['Decimal_date'] >= 2012) & (baringhead['Decimal_date'] <= 2016)].reset_index(drop=True)

heidelberg_1986_1991 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1987) & (heidelberg['Decimal_date'] <= 1991)].reset_index(drop=True)
heidelberg_1991_1994 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1991) & (heidelberg['Decimal_date'] <= 1994)].reset_index(drop=True)
heidelberg_2006_2016 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1994) & (heidelberg['Decimal_date'] <= 2006)].reset_index(drop=True)
heidelberg_2006_2009 = heidelberg.loc[(heidelberg['Decimal_date'] >= 2006) & (heidelberg['Decimal_date'] <= 2009)].reset_index(drop=True)
heidelberg_2012_2016 = heidelberg.loc[(heidelberg['Decimal_date'] >= 2012) & (heidelberg['Decimal_date'] <= 2016)].reset_index(drop=True)

# BARING HEAD VARIABLES
xtot_bhd = baringhead['Decimal_date']  # entire dataset x-values
ytot_bhd = baringhead['D14C']  # entire dataset y-values
ztot_bhd = baringhead['D14C_err']  # entire dataset z-values

x1_bhd = baringhead_1986_1991['Decimal_date']
x2_bhd = baringhead_1991_1994['Decimal_date']
x3_bhd = baringhead_2006_2016['Decimal_date']
x4_bhd = baringhead_2006_2009['Decimal_date']
x5_bhd = baringhead_2012_2016['Decimal_date']
y1_bhd = baringhead_1986_1991['D14C']  #
y2_bhd = baringhead_1991_1994['D14C']
y3_bhd = baringhead_2006_2016['D14C']
y4_bhd = baringhead_2006_2009['D14C']
y5_bhd = baringhead_2012_2016['D14C']
z1_bhd = baringhead_1986_1991['D14C_err']
z2_bhd = baringhead_1991_1994['D14C_err']
z3_bhd = baringhead_2006_2016['D14C_err']
z4_bhd = baringhead_2006_2009['D14C_err']
z5_bhd = baringhead_2012_2016['D14C_err']
# HEIDELBERG CAPE GRIM VARIABLES
xtot_heid = heidelberg['Decimal_date']  # entire dataset x-values
ytot_heid = heidelberg['D14C']  # entire dataset y-values
ztot_heid = heidelberg['D14C_err']  # entire dataset error(z)-values
x1_heid = heidelberg_1986_1991['Decimal_date']
print(x1_heid)
x2_heid = heidelberg_1991_1994['Decimal_date']
x3_heid = heidelberg_2006_2016['Decimal_date']
x4_heid = heidelberg_2006_2009['Decimal_date']
x5_heid = heidelberg_2012_2016['Decimal_date']
y1_heid = heidelberg_1986_1991['D14C']
y2_heid = heidelberg_1991_1994['D14C']
y3_heid = heidelberg_2006_2016['D14C']
y4_heid = heidelberg_2006_2009['D14C']
y5_heid = heidelberg_2012_2016['D14C']
z1_heid = heidelberg_1986_1991['D14C_err']
z2_heid = heidelberg_1991_1994['D14C_err']
z3_heid = heidelberg_2006_2016['D14C_err']
z4_heid = heidelberg_2006_2009['D14C_err']
z5_heid = heidelberg_2012_2016['D14C_err']

"""
So now we're almost ready to use the CCGCRV curve smoothing. One tricky bit is that - I want to compare the Cape Grim 
and Baring Head records; however, the x-values in time are not necessarily overlapping. How to best compare them? 
Luckily, the CCGCRV algorithm allows me to OUTPUT the smoothed data at any x-time that I desire. Therefore, in the next
bit of code, I create an evenly distributed set of x-values that I will output the smoothed baringhead and heidelberg 
data, in 480 points between 1980 and 2020. 
 
"fake_x_temp" is called this way because it is an x-value I have created. Not 'fake' but I was lazy in initial naming 
when first writing the code.  
 
"""
fake_x_temp = np.linspace(1980, 2020, 480)  # create arbitrary set of x-values to control output
df_fake_xs = pd.DataFrame({'x': fake_x_temp})  # put this set into a pandas DataFrame for easier use
my_x_1986_1991 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x1_heid)) & (df_fake_xs['x'] <= max(x1_heid))].reset_index(drop=True)  # index it
my_x_1991_1994 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x2_bhd))  & (df_fake_xs['x'] <= max(x2_bhd))].reset_index(drop=True)  # index it
my_x_2006_2016 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x3_heid)) & (df_fake_xs['x'] <= max(x3_heid))].reset_index(drop=True)  # index it
my_x_2006_2009 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x4_heid)) & (df_fake_xs['x'] <= max(x4_heid))].reset_index(drop=True)  # index it
my_x_2012_2016 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x5_heid)) & (df_fake_xs['x'] <= max(x5_heid))].reset_index(drop=True)  # index it
my_x_1986_1991 = my_x_1986_1991['x']  # when I wrote the function I'll be using in a few lines,
my_x_1991_1994 = my_x_1991_1994['x']  # I specify that the first 4 arguments must be input as data/variables that
my_x_2006_2016 = my_x_2006_2016['x']  # have been extracted from a pandas DataFrame, for consistency across testing
my_x_2006_2009 = my_x_2006_2009['x']
my_x_2012_2016 = my_x_2012_2016['x']

"""
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

Now comes the CCGCRV Curve smoothing, and Monte Carlo error analysis. 

The following description also can be found in the my_functions.py file. 

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
x_init: x-values of the dataset that you want to smooth. Must be in decimal date format. 
fake_x: x-values of the data you want OUTPUT
y_init: y-values of the dataset that you want to smooth. 
y_error: y-value errors of the dataset that you want to smooth. 
cutoff: for the CCGCRV algoritm, lower numbers smooth less, and higher numbers smooth more. 
    See hyperlink above for more details. 
n: how many iterations do you want to run? When writing code, keep this low. Once code is solid, increase to 10,000. 

### If you want to see this function in action, refer to "MonteCarlo_Explained.py"
https://github.com/christianlewis091/radiocarbon_intercomparison/blob/dev/interlab_comparison/MonteCarlo_Explained.py


ESSENTIALLY WHAT WE ARE DOING: 
1. RANDOMIZE THE HEIDELBERG AND BARING HEAD DATA 10,000 TIMES ALONG ITS NORMAL DISTRIBUTION
2. SMOOTH THAT DATA USING CCGCRV
3. FIND THE MEAN OF EACH X-VALUE FOR THOSE 10,000 ITERATIONS
4. COMPARE THE HEIDELBERG AND BARING HEAD DATA IN TIME. 

"""
n = 10  # set the amount of times the code will iterate (set to 10,000 once everything is final)
cutoff = 667  # FFT filter cutoff
# Curve smoothing with getSmoothValue()
heidelberg_1986_1991_results_smooth = monte_carlo_randomization_smooth(x1_heid, my_x_1986_1991, y1_heid, z1_heid, cutoff, n)
heidelberg_1991_1994_results_smooth = monte_carlo_randomization_smooth(x2_heid, my_x_1991_1994, y2_heid, z2_heid, cutoff, n)
heidelberg_2006_2016_results_smooth = monte_carlo_randomization_smooth(x3_heid, my_x_2006_2016, y3_heid, z3_heid, cutoff, n)
heidelberg_2006_2009_results_smooth = monte_carlo_randomization_smooth(x4_heid, my_x_2006_2009, y4_heid, z4_heid, cutoff, n)
heidelberg_2012_2016_results_smooth = monte_carlo_randomization_smooth(x5_heid, my_x_2012_2016, y5_heid, z5_heid, cutoff, n)
bhd_1986_1991_results_smooth = monte_carlo_randomization_smooth(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)
bhd_1991_1994_results_smooth = monte_carlo_randomization_smooth(x2_bhd, my_x_1991_1994, y2_bhd, z2_bhd, cutoff, n)
bhd_2006_2016_results_smooth = monte_carlo_randomization_smooth(x3_bhd, my_x_2006_2016, y3_bhd, z3_bhd, cutoff, n)
bhd_2006_2009_results_smooth = monte_carlo_randomization_smooth(x4_bhd, my_x_2006_2009, y4_bhd, z4_bhd, cutoff, n)
bhd_2012_2016_results_smooth = monte_carlo_randomization_smooth(x5_bhd, my_x_2012_2016, y5_bhd, z5_bhd, cutoff, n)
# Curve smoothing with getTrendValue()
heidelberg_1986_1991_results_trend = monte_carlo_randomization_trend(x1_heid, my_x_1986_1991, y1_heid, z1_heid, cutoff, n)
heidelberg_1991_1994_results_trend = monte_carlo_randomization_trend(x2_heid, my_x_1991_1994, y2_heid, z2_heid, cutoff, n)
heidelberg_2006_2016_results_trend = monte_carlo_randomization_trend(x3_heid, my_x_2006_2016, y3_heid, z3_heid, cutoff, n)
heidelberg_2006_2009_results_trend = monte_carlo_randomization_trend(x4_heid, my_x_2006_2009, y4_heid, z4_heid, cutoff, n)
heidelberg_2012_2016_results_trend = monte_carlo_randomization_trend(x5_heid, my_x_2012_2016, y5_heid, z5_heid, cutoff, n)
bhd_1986_1991_results_trend = monte_carlo_randomization_trend(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)
bhd_1991_1994_results_trend = monte_carlo_randomization_trend(x2_bhd, my_x_1991_1994, y2_bhd, z2_bhd, cutoff, n)
bhd_2006_2016_results_trend = monte_carlo_randomization_trend(x3_bhd, my_x_2006_2016, y3_bhd, z3_bhd, cutoff, n)
bhd_2006_2009_results_trend = monte_carlo_randomization_trend(x4_bhd, my_x_2006_2009, y4_bhd, z4_bhd, cutoff, n)
bhd_2012_2016_results_trend = monte_carlo_randomization_trend(x5_bhd, my_x_2012_2016, y5_bhd, z5_bhd, cutoff, n)

# TODO write a function to simplify the block of code in A_heidelberg_intercomparison.py lines 351 - 455.




