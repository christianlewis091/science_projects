"""
Purpose:

We have two long-term record of 14C02 from the Southern Hemisphere (among some other shorter ones).
One is the Baring Head Record, from the GNS Rafter Radiocarbon Lab (measured by gas counting, then AMS)
Next is Ingeborg Levin and Sam Hammer's Tasmania Cape Grim CO2 record (measured by gas counting).
This script is meant to compare the differences between the datasets over time, to determine if
temporally consistent offsets exist, and if so, how to best correct them to create a harmonized background reference
dataset for future carbon cycle studies.

The script first imports and cleans the data, before using a CCGCRV Curve smoothing program to smooth through the data.
There is precedent for this procedure in the scientific literature following
https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JD094iD06p08549 (Thoning et al., 1989): use of the CCGCRV
https://acp.copernicus.org/articles/17/14771/2017/ (Turnbull et al., 2017): use of CCGCRV in the Baring Head Record
https://gml.noaa.gov/ccgg/mbl/crvfit/crvfit.html: NOAA details about the CCGCRV curve smoothing.

A Monte Carlo simulation is used to determine errors on the CCGCRV smoothing data. These errors are important because
we will need them for comparison with other carbon cycle datasets, of course.

The file outputs a text file with the t-test results. However, it will keep adding to the file, so if you want a fresh
one, delete the remaining text file from the directory.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import seaborn as sns
from X_my_functions import long_date_to_decimal_date
from X_my_functions import monte_carlo_randomization_smooth
from X_my_functions import monte_carlo_randomization_trend
from Pre_Processing_Heidelberg import combine_heidelberg
from scipy import stats

# general plot parameters
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

heidelberg = pd.read_excel(r'H:\Science\Datasets\heidelberg_cape_grim.xlsx', skiprows=40)  # import heidelberg data
baringhead = pd.read_excel(r'H:\Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')  # import Baring Head data
df2_dates = pd.read_excel(r'H:\Science\Datasets\BHD_MeasurementDates.xlsx')  # CO2 measure date
extraction_dates = pd.read_excel(r'H:\Science\Datasets\BHDFlasks_WithExtractionDates.xlsx')  # CO2 extract date

""" TIDY UP THE DATA FILES"""
""" 
Some of the "Date formatting" can be quite tricky. The first step in cleaning the data is to convert
long-format dates to decimal dates that can be used in the CCGCRV curve smoothing algorithm. This is done using a 
function I wrote and lives in my_functions.py.
"""
heidelberg = combine_heidelberg.loc[(combine_heidelberg['Site'] == 'CGO')]
baringhead = combine_heidelberg.loc[(combine_heidelberg['Site'] == 'BHD')]

"""CAREFULLY SPLIT UP THE DATA INTO DIFFERENT TIME BINS AND GRAB VARIABLES """
"""
Entire Baring Head File > 1980.
In this first time-indexing, we only care about values after 1980 because the earliest date from the Heidelberg
group is 1987. For this comparison, we only care about the relevant, overlapping time periods. So we can ignore the
early periods, and early part of the bomb-spike.
 """
bforplot_x = baringhead['Decimal_date']
bforplot_y = baringhead['D14C']
baringhead = baringhead.loc[(baringhead['Decimal_date'] > 1980)]  # index the data. Only take post-1980 data
baringhead = baringhead.loc[(baringhead['D14C_err'] > 0)]  # get rid of data where the error flag is -1000
baringhead = baringhead.reset_index(drop=True)  # re-index to avoid gnarly errors

"""
Entire Baring Head File > 1980, without 1995 - 2005.
There is precedent for this indexing as well. In this period of time, GNS RRL switched to AMS measurements, and there
was a significant period of anomalously high values.
This was also highlighted in Section 3.3 of (Turnbull et al., 2017)
To accomplish this, I have to split the data into two, before 1994, and after 2006, and re-merge them.
 """
snipmin = 1994  # was previously 1994
snipmax = 2006  # was previously 2006
snip = baringhead.loc[(baringhead['Decimal_date'] < snipmin)]  # index 1980 - 1994
snip2 = baringhead.loc[(baringhead['Decimal_date'] > snipmax)]  # index 2006 - end
snip = pd.merge(snip, snip2, how='outer')  # merge the files back together
snip = snip.reset_index(drop=True)  # reset the index to avoid gnarly errors

"""
RECORDS SPLIT UP INTO 5 PARTS (1987 - 1991, 1991 - 1994, 2006 - 2016, 2006 - 2009, 2012 - 2016)
Now, I'm indexing further into smaller time intervals. The later period is broken up from 2006 - 2009 and 2012 - 2016
because there is another small issue with the data between 2009 - 2012. This can be observed by comparing the indexed
file baringhead_2006_2016 to the other indexed records.

Because these time bins are 3-4 year periods, I also decided to similarly split up the earlier times (1987 - 1994)
in a similar way - although I could have left this time period whole.
"""
baringhead_1986_1991 = baringhead.loc[(baringhead['Decimal_date'] >= 1987) & (baringhead['Decimal_date'] <= 1991)].reset_index(drop=True)
baringhead_1991_1994 = baringhead.loc[(baringhead['Decimal_date'] >= 1991) & (baringhead['Decimal_date'] <= 1994)].reset_index(drop=True)
baringhead_2006_2016 = baringhead.loc[(baringhead['Decimal_date'] > 2006) & (baringhead['Decimal_date'] <= 2016)].reset_index(drop=True)
baringhead_2006_2009 = baringhead.loc[(baringhead['Decimal_date'] >= 2006) & (baringhead['Decimal_date'] <= 2009)].reset_index(drop=True)
baringhead_2012_2016 = baringhead.loc[(baringhead['Decimal_date'] >= 2012) & (baringhead['Decimal_date'] <= 2016)].reset_index(drop=True)
heidelberg_1986_1991 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1987) & (heidelberg['Decimal_date'] <= 1991)].reset_index(drop=True)
heidelberg_1991_1994 = heidelberg.loc[(heidelberg['Decimal_date'] >= 1991) & (heidelberg['Decimal_date'] <= 1994)].reset_index(drop=True)
heidelberg_2006_2009 = heidelberg.loc[(heidelberg['Decimal_date'] >= 2006) & (heidelberg['Decimal_date'] <= 2009)].reset_index(drop=True)
heidelberg_2012_2016 = heidelberg.loc[(heidelberg['Decimal_date'] >= 2012) & (heidelberg['Decimal_date'] <= 2016)].reset_index(drop=True)
heidelberg_2006_2016 = heidelberg.loc[(heidelberg['Decimal_date'] > 2006) & (heidelberg['Decimal_date'] <= 2016)].reset_index(drop=True)
"""
After indexing into all these time-bins, now I have to extract all the x, y, and y-error variables from each and
every one of them. This region of the code could likely be vastly improved, although I don't know if there is a
fast / easy way to get around this besides simply typing it out.
"""
# BARING HEAD VARIABLES
xtot_bhd = baringhead['Decimal_date']  # entire dataset x-values
ytot_bhd = baringhead['D14C']  # entire dataset y-values
ztot_bhd = baringhead['D14C_err']  # entire dataset z-values
x_combined = snip['Decimal_date']  # dataset x-values after we remove 1995-2005
y_combined = snip['D14C']  # dataset y-values after we remove 1995-2005
z_combined = snip['D14C_err']  # dataset z-values after we remove 1995-2005
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
step_size = (2016 - 1987) * 12
fake_x_temp = np.linspace(1986, 2016, step_size)  # create arbitrary set of x-values to control output
df_fake_xs = pd.DataFrame({'x': fake_x_temp})  # put this set into a pandas DataFrame for easier use
my_x_1986_1991 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x1_heid)) & (df_fake_xs['x'] <= max(x1_heid))].reset_index(drop=True)  # index it
my_x_1991_1994 = df_fake_xs.loc[(df_fake_xs['x'] >= min(x2_bhd)) & (df_fake_xs['x'] <= max(x2_bhd))].reset_index(drop=True)  # index it
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

I'm going to run it once below as a proof of concept with this dataset, and run a plot to show its working.
"""
n = 10  # set the amount of times the code will iterate (set to 10,000 once everything is final)
cutoff = 667  # FFT filter cutoff

bhd_1986_1991_results_smooth = monte_carlo_randomization_smooth(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)

"""
Extract the data back out after the smoothing process.
The function returns:
1. A dataframe of the randomized data
2. A dataframe of the smoothed data
3. A summary dataframe (see below)

    summary = pd.DataFrame({"Means": mean_array, "Error": stdev_array})

    return randomized_dataframe, smoothed_dataframe, summary

For Figure 2 of the paper, I want to show an example of the randomization and smoothing process, for both the
getSmoothValue and getTrendValue.
We don't always need to extract all of the randomized data and multiple of the smooth curves (usually we just need
the mean). However, for this figure / to illustrate the point, I will extract the data for this one case.
"""
# bhd_1986_1991_results_smooth = monte_carlo_randomization_Smooth(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)
bhd_1986_1991_RandomData_smooth = bhd_1986_1991_results_smooth[0]  # the randomized data from 1986 to 1991
bhd_1986_1991_RandomCurves_smooth = bhd_1986_1991_results_smooth[1]  # the smoothed data from 1986 to 1991
summary = bhd_1986_1991_results_smooth[2]  # the means and stdevs from 1986 to 1991

# Choose three data-randomization's to use for the plot:
data1 = bhd_1986_1991_RandomData_smooth.iloc[1]  # three sets of random DATA (from Monte Carlo) for the plot.
data2 = bhd_1986_1991_RandomData_smooth.iloc[2]
data3 = bhd_1986_1991_RandomData_smooth.iloc[3]

bhd_1986_1991_RandomCurves_smooth = bhd_1986_1991_results_smooth[1]
curve1 = bhd_1986_1991_RandomCurves_smooth.iloc[1]  # the accompanying curves to the data above
curve2 = bhd_1986_1991_RandomCurves_smooth.iloc[2]
curve3 = bhd_1986_1991_RandomCurves_smooth.iloc[3]

means = summary['Means']  # extracts the summary DataFrame
# extracts the means from the summary DataFrame

fig = plt.figure(1)
plt.title('Visualization of Monte Carlo and CCGCRV Process: 1987-1991 BHD')
plt.errorbar(xtot_bhd, ytot_bhd, label='CGO Data', yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1,
             capsize=2)
plt.scatter(x1_bhd, data1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
plt.scatter(x1_bhd, data2, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
plt.scatter(x1_bhd, data3, color=colors[2], label='Monte Carlo Iteration 3', alpha=0.35, marker='s')
plt.plot(my_x_1986_1991, curve1, color=colors[0], alpha=0.35, linestyle='dotted')
plt.plot(my_x_1986_1991, curve2, color=colors[1], alpha=0.35, linestyle='dashed')
plt.plot(my_x_1986_1991, curve3, color=colors[2], alpha=0.35, linestyle='dashdot')
plt.plot(my_x_1986_1991, means, color='red', label='CCGCRV Smooth Values', alpha=1, linestyle='solid')
plt.xlim([1989, 1991])
plt.ylim([140, 170])
plt.legend()
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/FirstDraft_figure2.png',
    dpi=300, bbox_inches="tight")
plt.close()

"""
Now that we've shown that it works, let's run the rest of the smoothings.
"""
# Curve smoothing with getSmoothValue()
heidelberg_1986_1991_results_smooth = monte_carlo_randomization_smooth(x1_heid, my_x_1986_1991, y1_heid, z1_heid,cutoff, n)
heidelberg_1991_1994_results_smooth = monte_carlo_randomization_smooth(x2_heid, my_x_1991_1994, y2_heid, z2_heid,cutoff, n)
heidelberg_2006_2016_results_smooth = monte_carlo_randomization_smooth(x3_heid, my_x_2006_2016, y3_heid, z3_heid,cutoff, n)
heidelberg_2006_2009_results_smooth = monte_carlo_randomization_smooth(x4_heid, my_x_2006_2009, y4_heid, z4_heid, cutoff, n)
heidelberg_2012_2016_results_smooth = monte_carlo_randomization_smooth(x5_heid, my_x_2012_2016, y5_heid, z5_heid,cutoff, n)
bhd_1986_1991_results_smooth = monte_carlo_randomization_smooth(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)
bhd_1991_1994_results_smooth = monte_carlo_randomization_smooth(x2_bhd, my_x_1991_1994, y2_bhd, z2_bhd, cutoff, n)
bhd_2006_2016_results_smooth = monte_carlo_randomization_smooth(x3_bhd, my_x_2006_2016, y3_bhd, z3_bhd, cutoff, n)
bhd_2006_2009_results_smooth = monte_carlo_randomization_smooth(x4_bhd, my_x_2006_2009, y4_bhd, z4_bhd, cutoff, n)
bhd_2012_2016_results_smooth = monte_carlo_randomization_smooth(x5_bhd, my_x_2012_2016, y5_bhd, z5_bhd, cutoff, n)
# Curve smoothing with getTrendValue()
heidelberg_1986_1991_results_trend = monte_carlo_randomization_trend(x1_heid, my_x_1986_1991, y1_heid, z1_heid, cutoff,n)
heidelberg_1991_1994_results_trend = monte_carlo_randomization_trend(x2_heid, my_x_1991_1994, y2_heid, z2_heid, cutoff, n)
heidelberg_2006_2016_results_trend = monte_carlo_randomization_trend(x3_heid, my_x_2006_2016, y3_heid, z3_heid, cutoff,n)
heidelberg_2006_2009_results_trend = monte_carlo_randomization_trend(x4_heid, my_x_2006_2009, y4_heid, z4_heid, cutoff,n)
heidelberg_2012_2016_results_trend = monte_carlo_randomization_trend(x5_heid, my_x_2012_2016, y5_heid, z5_heid, cutoff,n)
bhd_1986_1991_results_trend = monte_carlo_randomization_trend(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)
bhd_1991_1994_results_trend = monte_carlo_randomization_trend(x2_bhd, my_x_1991_1994, y2_bhd, z2_bhd, cutoff, n)
bhd_2006_2016_results_trend = monte_carlo_randomization_trend(x3_bhd, my_x_2006_2016, y3_bhd, z3_bhd, cutoff, n)
bhd_2006_2009_results_trend = monte_carlo_randomization_trend(x4_bhd, my_x_2006_2009, y4_bhd, z4_bhd, cutoff, n)
bhd_2012_2016_results_trend = monte_carlo_randomization_trend(x5_bhd, my_x_2012_2016, y5_bhd, z5_bhd, cutoff, n)

"""
The next giant block of code below is the process of actually extracting the output from the function. Of course we
need to do this in to test the data and do further analysis.
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
#
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
#

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
heidelberg_2012_2016_mean_trend = heidelberg_2012_2016_results_trend['Means']
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
Now that we have smoothed the data, and extracted all of the means, after running some iterations, we can
visually and statistically have a look at the differences between the data.
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html

This is a test for the null hypothesis that two related time series have identical average (expected) values.
Examples for use are scores of the same set of student in different exams, or repeated sampling from the same units.
The test measures whether the average score differs significantly across samples (e.g. exams). If we observe a
large p-value, for example greater than 0.05 or 0.1 then we cannot reject the null hypothesis of identical average
scores.
If the p-value is smaller than the threshold, e.g. 1%, 5% or 10%, then we reject the null hypothesis of equal
averages. Small p-values are associated with large t-statistics.

Small p value = difference.

Just after the following t-tests, I aim to find the mean of the differences between the datasets. Before I redeveloped
this file for our meeting with Dr. Levin and Hammer, my original output was in output_10000.txt. See that file for more
information on the initial calculated differences in means.
"""


def difference_in_means(y1, y2):
    difference = np.subtract(y1, y2)  # subtract the data from each other
    mean1 = np.average(difference)
    standard_error = np.std(difference) / np.sqrt(len(y1))  # standard error of the subtraction array
    return mean1, standard_error


# TODO before publishing / presenting - figure out the use of the t-test more.

period1 = stats.ttest_rel(bhd_1986_1991_mean_smooth, heidelberg_1986_1991_mean_smooth)
period2 = stats.ttest_rel(bhd_1991_1994_mean_smooth, heidelberg_1991_1994_mean_smooth)
period3 = stats.ttest_rel(bhd_2006_2016_mean_smooth, heidelberg_2006_2016_mean_smooth)
period4 = stats.ttest_rel(bhd_2006_2009_mean_smooth, heidelberg_2006_2009_mean_smooth)
period5 = stats.ttest_rel(bhd_2012_2016_mean_smooth, heidelberg_2012_2016_mean_smooth)

period6 = stats.ttest_rel(bhd_1986_1991_mean_trend, heidelberg_1986_1991_mean_trend)
period7 = stats.ttest_rel(bhd_1991_1994_mean_trend, heidelberg_1991_1994_mean_trend)
period8 = stats.ttest_rel(bhd_2006_2016_mean_trend, heidelberg_2006_2016_mean_trend)
period9 = stats.ttest_rel(bhd_2006_2009_mean_trend, heidelberg_2006_2009_mean_trend)
period10 = stats.ttest_rel(bhd_2012_2016_mean_trend, heidelberg_2012_2016_mean_trend)

period1_d_means = difference_in_means(bhd_1986_1991_mean_smooth, heidelberg_1986_1991_mean_smooth)
period2_d_means = difference_in_means(bhd_1991_1994_mean_smooth, heidelberg_1991_1994_mean_smooth)
period3_d_means = difference_in_means(bhd_2006_2016_mean_smooth, heidelberg_2006_2016_mean_smooth)
period4_d_means = difference_in_means(bhd_2006_2009_mean_smooth, heidelberg_2006_2009_mean_smooth)
period5_d_means = difference_in_means(bhd_2012_2016_mean_smooth, heidelberg_2012_2016_mean_smooth)

period6_d_means = difference_in_means(bhd_1986_1991_mean_trend, heidelberg_1986_1991_mean_trend)
period7_d_means = difference_in_means(bhd_1991_1994_mean_trend, heidelberg_1991_1994_mean_trend)
period8_d_means = difference_in_means(bhd_2006_2016_mean_trend, heidelberg_2006_2016_mean_trend)
period9_d_means = difference_in_means(bhd_2006_2009_mean_trend, heidelberg_2006_2009_mean_trend)
period10_d_means = difference_in_means(bhd_2012_2016_mean_trend, heidelberg_2012_2016_mean_trend)

"""
UNCOMMENT FOLLOWING BLOCK TO PRINT RESULTS
"""
print('The following results were computed using CCGCRV Smooth (D14C), with an n of {}'.format(n))
print('Paired t-test result and difference in means for 1986 - 1991')
print(period1)
print(period1_d_means)

print('Paired t-test result and difference in means for 1991 - 1994')
print(period2)
print(period2_d_means)

print('Paired t-test result and difference in means for 2006 - 2016')
print(period3)
print(period3_d_means)

print('Paired t-test result and difference in means for 2006 - 2009')
print(period4)
print(period4_d_means)

print('Paired t-test result and difference in means for 2012 - 2016')
print(period5)
print(period5_d_means)

print()
print()
print('The following results were computed using CCGCRV Trend (D14C), with an n of {}'.format(n))
print('Paired t-test result and difference in means for 1986 - 1991')
print(period6)
print(period6_d_means)

print('Paired t-test result and difference in means for 1991 - 1994')
print(period7)
print(period7_d_means)

print('Paired t-test result and difference in means for 2006 - 2016')
print(period8)
print(period8_d_means)

print('Paired t-test result and difference in means for 2006 - 2009')
print(period9)
print(period9_d_means)

print('Paired t-test result and difference in means for 2012 - 2016')
print(period10)
print(period10_d_means)
print()
print()
print()
print()


"""
The following block of code is VERY Important (aren't they all???)...
I've listed below a series of offsets. There are the offsets that are found for Heidelberg data during different time intervals.
For publication, it will be very important how we use these data that come out of this program. One way to use them is to have a
blanket offset during each interval - but there are gaps. So we could then do a pre and Post AMS offset. But couldn't we smooth it?
We could smooth it, but with very limited data to feed the curve fitting algorithm, there is very little actual smoothing done.
See the block below, and later, I will use this block of code to see how different types of offset calculations impacts our final analyis

When you eventually use the smoothed offset for another data, you'll have to copy and paste the lines of code into that file because
you'll also need to create a desired group of x-values to output
"""
"""
PRE v POST AMS OFFSET SETTINGS
"""
# PRE-AMS AT RRL
offset1 = 1.80  # 1986 - 1991
offset2 = 1.88  # 1991 - 1994
offset3 = (offset2 + offset1) / 2  # 1994-2006. In this time period, we have removed data where RRL AMS
# measurements were high. But, it's likely reasonable to say that we can prescribe the PRE-AMS offset to this data,
# otherwise if we do not apply anything, there will be a "step" in the harmonized dataset.
offset4 = 0.49  # 2006 - 2016
offset5 = 0   # 2006 - 2009
offset6 = -.52  # 2012 - 2016.
# One can see that if we seperate the data in from 06 - 09 and 12 - 16, the sign in the difference changes.
# Initially, I would think to apply a broad "post-AMS" offset to both two time periods (06-09, 12-16); however,
# since we know there is a sign change, it may be better to leave the intermedite time period at 0.
error1 = .18
error2 = .16
error3 = np.sqrt(error2**2 + error1) / 2  # propagating the error from the average of offset1 and offset2 above.
error4 = 0.07
error5 = 0
error6 = 0.06
