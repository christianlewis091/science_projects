from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import random
from miller_curve_algorithm import ccgFilter
from my_functions import long_date_to_decimal_date, monte_carlo_step2
from my_functions import year_month_todecimaldate
from my_functions import simple_t_test
from my_functions import monte_carlo_step1

""" IMPORT ALL THE DATA """
# Heidelberg data excel file
heidelberg = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\heidelberg_cape_grim.xlsx', skiprows=40)
# Baring Head data excel file
baringhead = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')
# Hua data excel file
hua = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\Hua_et_al_2021.xlsx', sheet_name='SH')

# Clean up the file a little: drop NaN's in the column I'm most interested in
heidelberg = heidelberg.dropna(subset=['D14C'])
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]  # filter out the one outlying measurement around 2019
baringhead = baringhead.dropna(subset=['DELTA14C'])
# Split up the baring head file so that it only takes data after the bomb peak, and removes data between 1995 and 2005
# Will need to keep baring head data split into two for accurate curve smoothing (baringhead1 and baringhead2)
baringhead = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 1980)]  # grab all values after 1980
baringhead = baringhead.loc[(baringhead['DELTA14C_ERR'] > 0)]  # get rid of data where the error flag is -1000
baringhead1 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] < 1994)]
baringhead2 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2006)]
# baringhead = pd.merge(baringhead1, baringhead2, how='outer')  # how = outer Keeps ALL Data

# reset indeces to avoid random errors that crop up
heidelberg = heidelberg.reset_index()
baringhead1 = baringhead1.reset_index()
baringhead2 = baringhead2.reset_index()

""" extract my variables"""
y_init_heid = heidelberg['D14C']  # Y values from heidelberg dataset
yerr_init_heid = heidelberg['weightedstderr_D14C']  # errors associated with Y values from heidelberg dataset
x_init_heid = heidelberg['Average pf Start-date and enddate']  # x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)  # use a function I wrote the change these values to decimal dates

y_init_bhd1 = baringhead1['DELTA14C']
yerr_init_bhd1 = baringhead1['DELTA14C_ERR']
x_init_bhd1 = baringhead1['DATE_COLL']
x_init_bhd1 = long_date_to_decimal_date(x_init_bhd1)

y_init_bhd2 = baringhead2['DELTA14C']
yerr_init_bhd2 = baringhead2['DELTA14C_ERR']
x_init_bhd2 = baringhead2['DATE_COLL']
x_init_bhd2 = long_date_to_decimal_date(x_init_bhd2)


"""  Plot of inital data  """
colors = sns.color_palette("rocket")
# keep colors consistent
size = 5
fig = plt.figure(1)
plt.scatter(x_init_bhd1, y_init_bhd1, marker='o', label='Baring Head Record > 1980', color=colors[0], s=size)
plt.scatter(x_init_bhd2, y_init_bhd2, marker='o', label='Baring Head Record > 1980', color=colors[1], s=size)
plt.scatter(x_init_heid, y_init_heid, marker='x', label='Heidelberg Data Record', color=colors[3], s=size)
plt.legend()
plt.title('Initial Data Plot')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned_Fig1_2bhd.png',
            dpi=300, bbox_inches="tight")
plt.close()

""" CALL IN THE CCGCV CURVE SMOOTHER """
# longer cutoff = smoother curve. shorter cutoff = more rugged curve
cutoff = 667

# smooth the heidelberg data
ccgcv_heid = ccgFilter(x_init_heid, y_init_heid, cutoff).getMonthlyMeans()
x_ccgcv_heid = year_month_todecimaldate(ccgcv_heid[0], ccgcv_heid[1])  # get the dates to be in decimal format
y_ccgcv_heid = ccgcv_heid[2]

# smooth the baring head data
ccgcv_bhd1 = ccgFilter(x_init_bhd1, y_init_bhd1, cutoff).getMonthlyMeans()
x_ccgcv_bhd1 = year_month_todecimaldate(ccgcv_bhd1[0], ccgcv_bhd1[1])  # get the dates to be in decimal format
y_ccgcv_bhd1 = ccgcv_bhd1[2]

# smooth the baring head data
ccgcv_bhd2 = ccgFilter(x_init_bhd2, y_init_bhd2, cutoff).getMonthlyMeans()
x_ccgcv_bhd2 = year_month_todecimaldate(ccgcv_bhd2[0], ccgcv_bhd2[1])  # get the dates to be in decimal format
y_ccgcv_bhd2 = ccgcv_bhd2[2]

"""
The above CCGCV smoothing code ouputs a different lenght of x and y values from original input
For this reason, one cannot subtract the original data from the smooth data right away (different matrix length, different x-values)
But, you can solve the smoothed curve for explicit x-values and get y-values to subtract from original data:

Below: i'm fitting the Heidelberg data using ccgcv, and then fitting x-values from Baring Head AND Heidelberg.

To find the "residual" between the Baring Head data and Heidelberg data,
    1) Fit the Baring Head x's into the CCGCV fit for Heidelberg
    2) Subtract the output y's "y-guesses" from the actual Baring Head Data.

The residuals overlap in a normal way until around 2015, where the gap in the Heidelberg Data begins.
The smooth fit tracks to a single point which falls below the normal slope of the line, which makes those residuals jump up.
For this reason, I will omit that final data point from Heidelberg analysis in future data.

I'm going to do a t-test to see if these two datasets are significantly different; however
first I must cut-off the data after 2015 to avoid skewing it based on the issue described in the three lines above.
# 
# """

# using smoothed heidelberg curve (heidelberg in ccg filter argument), find y-guess for discrete heidelberg x-values
A_heid = ccgFilter(x_init_heid, y_init_heid, cutoff).getSmoothValue(x_init_heid)
# what is the difference between Heidelberg measurements and y-guess values from the smooth fit
residual_heid = A_heid - y_init_heid

# using smoothed heidelberg curve (heidelberg in ccg filter argument), find y-guess for discrete BARING HEAD1 x-values
A_bhd1 = ccgFilter(x_init_heid, y_init_heid, cutoff).getSmoothValue(x_init_bhd1)
residual_bhd1 = A_bhd1 - y_init_bhd1

# using smoothed heidelberg curve (heidelberg in ccg filter argument), find y-guess for discrete BARING HEAD2 x-values
A_bhd2 = ccgFilter(x_init_heid, y_init_heid, cutoff).getSmoothValue(x_init_bhd2)
residual_bhd2 = A_bhd2 - y_init_bhd2


"""  Plot of curve fit over data"""
fig = plt.figure(2)
size = 10
plt.scatter(x_init_bhd1, y_init_bhd1, marker='o', label='Baring Head Part 1', color=colors[0], s=size, alpha=0.3)
plt.plot(x_ccgcv_bhd1, y_ccgcv_bhd1, label='Baring Head Part 1 SMOOTH', color=colors[0])
plt.scatter(x_init_bhd2, y_init_bhd2, marker='o', label='Baring Head Part 2', color=colors[1], s=size, alpha=0.3)
plt.plot(x_ccgcv_bhd2, y_ccgcv_bhd2, label='Baring Head Part 2 SMOOTH', color=colors[1])
plt.scatter(x_init_heid, y_init_heid, marker='x', label='Heidelberg Data Record', color=colors[3], s=size, alpha=0.3)
plt.plot(x_ccgcv_heid, y_ccgcv_heid, label='Heidelberg SMOOTH', color=colors[3])
plt.legend()
plt.title('CCGCV Curve fit over Baring Head and Heidelberg Data: 667 Day cutoff')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned_Fig2_2bhd.png',
            dpi=300, bbox_inches="tight")
plt.close()
#
"""  Plot of residuals"""
fig = plt.figure(3)
size = 5
plt.scatter(x_init_bhd1, residual_bhd1, marker='o', label='Baring Head Part 1', color=colors[0], s=size)
plt.scatter(x_init_bhd2, residual_bhd2, marker='o', label='Baring Head Part 2', color=colors[1], s=size)
plt.scatter(x_init_heid, residual_heid, marker='x', label='Heidelberg', color=colors[3], s=size)
plt.legend()
plt.title('How far is the BHD and Heidelberg data from Heidelberg Curve fit?')
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned_Fig3_2bhd.png',
            dpi=300, bbox_inches="tight")
plt.close()


""" Perform a t-test of the residuals"""
# Drop the nan's from the residual dataset or the t-test will fail
residual_heid = residual_heid.dropna()
residual_bhd1 = residual_bhd1.dropna()
residual_bhd2 = residual_bhd2.dropna()

simple_t_test(residual_bhd1, residual_heid)
simple_t_test(residual_bhd2, residual_heid)
simple_t_test(residual_bhd1, residual_bhd2)


"""
USE MONTE CARLO METHOD TO ESTIMATE DIFFERENCES BETWEEN DATASETS
"""
"""
Monte Carlo for Heidelberg Data
"""
step1 = monte_carlo_step1(y_init_heid, yerr_init_heid)
step2 = monte_carlo_step2(x_ccgcv_heid, y_ccgcv_heid, step1, x_init_heid)
# return df_dates, df_ys, mean_array, stdev_array
heidelberg_mc_dates = step2[0]  # extract the date dataframe from function output
heidelberg_mc_dates = heidelberg_mc_dates.iloc[1]
# extract the y's, the randomized data that has been smoothed through ccgcv
heidelberg_mc_ys = step2[1]
heidelberg_mc_ys_1 = heidelberg_mc_ys.iloc[10]
heidelberg_mc_ys_2 = heidelberg_mc_ys.iloc[100]
heidelberg_mc_ys_3 = heidelberg_mc_ys.iloc[250]
heidelberg_mc_ys_4 = heidelberg_mc_ys.iloc[350]
heidelberg_mc_ys_5 = heidelberg_mc_ys.iloc[550]
heidelberg_mc_mean = step2[2]
heidelberg_mc_stdev = step2[3]
heidelberg_upperbounds = step2[4]
heidelberg_lowerbounds = step2[5]
#
#
"""
Monte Carlo for BHD Data Part 1
"""
step1_bhd1 = monte_carlo_step1(y_init_bhd1, yerr_init_bhd1)
step2_bhd1 = monte_carlo_step2(x_ccgcv_bhd1, y_ccgcv_bhd1, step1_bhd1, x_init_bhd1)
# return df_dates, df_ys, mean_array, stdev_array
bhd1_mc_dates = step2_bhd1[0]  # extract the date dataframe from function output
bhd1_mc_dates = bhd1_mc_dates.iloc[1]
# extract the y's, the randomized data that has been smoothed through ccgcv
bhd1_mc_ys = step2_bhd1[1]
bhd1_mc_ys_1 = bhd1_mc_ys.iloc[10]
bhd1_mc_ys_2 = bhd1_mc_ys.iloc[100]
bhd1_mc_ys_3 = bhd1_mc_ys.iloc[250]
bhd1_mc_ys_4 = bhd1_mc_ys.iloc[350]
bhd1_mc_ys_5 = bhd1_mc_ys.iloc[550]
bhd1_mc_mean = step2_bhd1[2]
bhd1_mc_stdev = step2_bhd1[3]
bhd1_upperbounds = step2_bhd1[4]
bhd1_lowerbounds = step2_bhd1[5]
#
#
"""
Monte Carlo for BHD Data Part 2
"""
step1_bhd2 = monte_carlo_step1(y_init_bhd2, yerr_init_bhd2)
step2_bhd2 = monte_carlo_step2(x_ccgcv_bhd2, y_ccgcv_bhd2, step1_bhd2, x_init_bhd2)
# return df_dates, df_ys, mean_array, stdev_array
bhd2_mc_dates = step2_bhd2[0]  # extract the date dataframe from function output
bhd2_mc_dates = bhd2_mc_dates.iloc[1]
# extract the y's, the randomized data that has been smoothed through ccgcv
bhd2_mc_ys = step2_bhd2[1]
bhd2_mc_ys_1 = bhd2_mc_ys.iloc[10]
bhd2_mc_ys_2 = bhd2_mc_ys.iloc[100]
bhd2_mc_ys_3 = bhd2_mc_ys.iloc[250]
bhd2_mc_ys_4 = bhd2_mc_ys.iloc[350]
bhd2_mc_ys_5 = bhd2_mc_ys.iloc[550]
bhd2_mc_mean = step2_bhd2[2]
bhd2_mc_stdev = step2_bhd2[3]
bhd2_upperbounds = step2_bhd2[4]
bhd2_lowerbounds = step2_bhd2[5]



#
fig = plt.figure(6)
size = 5
alpha1 = 0.4
# plt.plot(bhd_mc_dates, bhd_mc_ys_1, color=colors[0], alpha=alpha1)
# plt.plot(bhd_mc_dates, bhd_mc_ys_2, color=colors[0], alpha=alpha1)
# plt.plot(bhd_mc_dates, bhd_mc_ys_3, color=colors[0], alpha=alpha1)
# plt.plot(bhd_mc_dates, bhd_mc_ys_4, color=colors[0], alpha=alpha1)
# plt.plot(bhd_mc_dates, bhd_mc_ys_5, color=colors[0], alpha=alpha1)
# # plt.plot(heidelberg_mc_dates, heidelberg_mc_ys_1, color=colors[3], alpha=alpha1)
# # plt.plot(heidelberg_mc_dates, heidelberg_mc_ys_2, color=colors[3], alpha=alpha1)
# # plt.plot(heidelberg_mc_dates, heidelberg_mc_ys_3, color=colors[3], alpha=alpha1)
# # plt.plot(heidelberg_mc_dates, heidelberg_mc_ys_4, color=colors[3], alpha=alpha1)
# # plt.plot(heidelberg_mc_dates, heidelberg_mc_ys_5, color=colors[3], alpha=alpha1)
plt.plot(bhd1_mc_dates, bhd1_mc_mean, color=colors[0], label='BHD MonteCarlo Mean', linestyle='solid')
plt.plot(bhd1_mc_dates, bhd1_upperbounds, color=colors[1], label='BHD MonteCarlo upperbound', linestyle='solid')
plt.plot(bhd1_mc_dates, bhd1_lowerbounds, color=colors[1], label='BHD MonteCarlo lowerbound', linestyle='solid')
plt.plot(bhd2_mc_dates, bhd2_mc_mean, color=colors[2], label='BHD MonteCarlo Mean', linestyle='solid')
plt.plot(bhd2_mc_dates, bhd2_upperbounds, color=colors[3], label='BHD MonteCarlo upperbound', linestyle='solid')
plt.plot(bhd2_mc_dates, bhd2_lowerbounds, color=colors[3], label='BHD MonteCarlo lowerbound', linestyle='solid')
plt.plot(heidelberg_mc_dates, heidelberg_mc_mean, color=colors[4], label='Heidelberg MonteCarlo Mean', linestyle='solid')
plt.plot(heidelberg_mc_dates, heidelberg_upperbounds, color=colors[5], label='Heidelberg MonteCarlo upperbound', linestyle='solid')
plt.plot(heidelberg_mc_dates, heidelberg_lowerbounds, color=colors[5], label='Heidelberg MonteCarlo lowerbound', linestyle='solid')
plt.title('Upper and lower uncertainty bounds')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.legend()
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned_Fig5_2bhd.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
Use a paired t-test to check if increments of data are the same. 

I want to do this test in increments of 5-years. 

First, I need to isolate data that are in the same years. 
For the paired t-test, I need each pair of data to be exactly the same. 
This can't be done with the original discrete data from each dataset. 

Therefore, I'm going to create a "fake" set of x's that range from 1980 - 2020, and 
I will put these through each of the smooth fit curves. Then I can explicity test 
each range of dates easily by:
1. Merging datasets
2. Filtering by date using pandas

"""
# create a new set of x-data to run through the smoothing.
fake_x = np.linspace(1980, 2020, 1000)

# run fake x through baring head 1 smooth fit (use the Monte Carlo's for error analysis)
fake_x_heid = ccgFilter(x_init_heid, y_init_heid, cutoff).getSmoothValue(fake_x)

fake_x_bhd1 = ccgFilter(x_init_bhd1, y_init_bhd1, cutoff).getSmoothValue(fake_x)

fake_x_bhd2 = ccgFilter(x_init_bhd2, y_init_bhd2, cutoff).getSmoothValue(fake_x)

# does this even work when we're adding x's to spots where the curve isn't able to smooth???
# # YES IT WORKS. The smoother only plots until the data ends!
# fig = plt.figure(7)
# plt.plot(fake_x, fake_x_bhd1, color=colors[0], label='Baring Head 1', linestyle='solid')
# plt.plot(fake_x, fake_x_bhd2, color=colors[1], label='Baring Head 2', linestyle='solid')
# plt.plot(fake_x, fake_x_heid, color=colors[2], label='Heidelberg', linestyle='solid')
# # plt.show()

# create new dataframes including keys for all sections, and then I can filter by date and still know whats what.
key_bhd1 = (np.ones(len(fake_x_bhd1))) * 1
key_bhd2 = (np.ones(len(fake_x_bhd2))) * 2
key_heid = (np.ones(len(fake_x_heid))) * 3

df = pd.DataFrame({'Date': fake_x, '14C': fake_x_bhd1, 'Key': key_bhd1})
df = df.dropna(subset=['14C'])
df1 = pd.DataFrame({'Date': fake_x, '14C': fake_x_bhd2, 'Key': key_bhd2})
df1 = df1.dropna(subset=['14C'])
df2 = pd.DataFrame({'Date': fake_x, '14C': fake_x_heid, 'Key': key_heid})
df2 = df2.dropna(subset=['14C'])
combine = pd.merge(df, df1, how='outer')  # Keeps ALL Data
combine = pd.merge(combine, df2, how='outer')

combine.to_csv(r'G:/My Drive/Work/GNS Radiocarbon Scientist/The Science/Datasets/filename.csv')
""" 
Find where duplicates x-values exist in the dataset
Then do a paired t-test on the whole thing.

"""

# find the boundaries of each dataset in time
bhd1_max = max(df['Date'])
heid_min = min(df2['Date'])

bhd2_min = min(df1['Date'])
heid_max = max(df2['Date'])

# extract the pairs of data
# extract all data from baring head 1 which have dates greater than or equal to heidelberg min
baring_head1_overlap = combine.loc[(combine['Key'] == 1) & (combine['Date'] >= heid_min)]
nv1 = baring_head1_overlap['Date']
nv2 = baring_head1_overlap['14C']

heidelberg_overlap = combine.loc[(combine['Key'] == 3) & (combine['Date'] <= bhd1_max)]
nv3 = heidelberg_overlap['Date']
nv4 = heidelberg_overlap['14C']

baring_head2_overlap = combine.loc[(combine['Key'] == 2) & (combine['Date'] <= heid_max)]
nv5 = baring_head2_overlap['Date']
nv6 = baring_head2_overlap['14C']

heidelberg_overlap2 = combine.loc[(combine['Key'] == 3) & (combine['Date'] >= bhd2_min)]
nv7 = heidelberg_overlap2['Date']
nv8 = heidelberg_overlap2['14C']

fig = plt.figure(8)
size = 4
plt.scatter(nv1, nv2, color=colors[0], label='Baring Head 1', linestyle='solid', marker='o', s=size)
plt.scatter(nv3, nv4, color=colors[1], label='Heidelberg', linestyle='solid', marker='o', s=size)
plt.legend()
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned_Fig8_pairedt-test1.png',
            dpi=300, bbox_inches="tight")
fig = plt.figure(9)
plt.scatter(nv5, nv6, color=colors[0], label='Baring Head 2', linestyle='solid', marker='o', s=size)
plt.scatter(nv7, nv8, color=colors[1], label='Heidelberg', linestyle='solid', marker='o', s=size)
plt.legend()
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned_Fig9_paired-test2.png',
            dpi=300, bbox_inches="tight")
