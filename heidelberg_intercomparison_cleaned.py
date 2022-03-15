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

"""
I got the Heidelberg Intercomparison file initially working in the file "heidelberg_intercomparison2.py" 
However, the file is quite cumbersome and confusing for myself or anyone else to interpret, and make progress on
I'm going to re-write the file here from scratch, hopefully cleaning up the code for future data-analysis and understanding
"""

""" IMPORT ALL THE DATA """
# Read in the heidelberg excel file
heidelberg = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\heidelberg_cape_grim.xlsx', skiprows=40)
baringhead = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')
hua = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\Hua_et_al_2021.xlsx', sheet_name='SH')

""" Clean up the file a little: drop NaN's in the column I'm most interested in """
heidelberg = heidelberg.dropna(subset=['D14C'])
baringhead = baringhead.dropna(subset=['DELTA14C'])
# Filter = df.loc[(df['Type 1'] == 'Grass') & (df['Type 2'] == 'Poison') & (df['HP'] > 70)]
# TODO  adjust values to after 1980 (get rid of bomb peak) and remove 1995 - 2005, bad AMS data
baringhead = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 1980)]  # grab all values after 1980
# baringhead = baringhead.loc[(baringhead['DEC_DECAY_CORR'] )]
baringhead = baringhead.loc[(baringhead['DELTA14C_ERR'] > 0)]  # have to currently get rid of data where the error is -1000
""" reset indeces to avoid random errors that crop up """
heidelberg = heidelberg.reset_index()
baringhead = baringhead.reset_index()

""" extract my variables"""
y_init_heid = heidelberg['D14C']  # Y values from heidelberg dataset
yerr_init_heid = heidelberg['weightedstderr_D14C']  # errors associated with Y values from heidelberg dataset
x_init_heid = heidelberg['Average pf Start-date and enddate']  # x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)  # use a function I wrote the change these values to decimal dates

y_init_bhd = baringhead['DELTA14C']
yerr_init_bhd = baringhead['DELTA14C_ERR']
x_init_bhd = baringhead['DATE_COLL']
x_init_bhd = long_date_to_decimal_date(x_init_bhd)

"""  Plot of inital data  """
colors = sns.color_palette("rocket")
# keep colors consistent
size = 5
fig = plt.figure(1)
plt.scatter(x_init_bhd, y_init_bhd, marker='o', label='Baring Head Record > 1980', color=colors[0], s=size)
plt.scatter(x_init_heid, y_init_heid, marker='x', label='Heidelberg Data Record', color=colors[3], s=size)
plt.legend()
plt.title('Initial Data Plot')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned_Fig1.png',
            dpi=300, bbox_inches="tight")
plt.close()

""" CALL IN THE CCGCV CURVE SMOOTHER """
# smooth the heidelberg data
cutoff = 667
ccgcv_heid = ccgFilter(x_init_heid, y_init_heid, cutoff).getMonthlyMeans()
x_ccgcv_heid = year_month_todecimaldate(ccgcv_heid[0], ccgcv_heid[1])  # get the dates to be in decimal format
y_ccgcv_heid = ccgcv_heid[2]
# smooth the baring head data
ccgcv_bhd = ccgFilter(x_init_bhd, y_init_bhd, cutoff).getMonthlyMeans()
x_ccgcv_bhd = year_month_todecimaldate(ccgcv_bhd[0], ccgcv_bhd[1])  # get the dates to be in decimal format
y_ccgcv_bhd = ccgcv_bhd[2]

""" 
The CCGCV smoothing code ouputs a different lenght of x and y values from original input
For this reason, one cannot subtract the original data from the smooth data right away (different matrix length, different x-values)
But, you can solve the smoothed curve for explicity x-values and get y-values to subtract from original data: 

Below: i'm fitting the Heidelberg data using ccgcv, and then fitting x-values from Baring Head AND Heidelberg. 

To find the "residual" between the Baring Head data and Heidelberg data, 
    1) Fit the Baring Head x's into the CCGCV fit for Heidelberg
    2) Subtract the output y's "y-guesses" from the actual Baring Head Data. 
    
The residuals overlap in a normal way until around 2015, where the gap in the Heidelberg Data begins.
The smooth fit tracks to a single point which falls below the normal slope of the line, which makes those residuals jump up. 
For this reason, I will omit that final data point from Heidelberg analysis in future data. 

I'm going to do a t-test to see if these two datasets are significantly different; however
first I must cut-off the data after 2015 to avoid skewing it based on the issue described in the three lines above.    
"""

# find appropriate Y-values in smooth curve for BHD X's
A_heid = ccgFilter(x_init_heid, y_init_heid, cutoff).getSmoothValue(x_init_heid)
residual_heid = A_heid - y_init_heid
A_bhd = ccgFilter(x_init_heid, y_init_heid, cutoff).getSmoothValue(x_init_bhd)  # BARING HEAD DATA into CURVE FIT FOR HEIDELBERG
residual_bhd = A_bhd - y_init_bhd
d_bhd = {'decimal dates': x_init_bhd, 'y_guesses': A_bhd, 'residual': residual_bhd}
df_bhd_residual = pd.DataFrame(data=d_bhd)  # create a dataframe to make future manipulation of data simpler
df_bhd_residual = df_bhd_residual.dropna(subset=[
    'residual'])  # get rid of all the nan's associated with when there isn't Heidelberg data relative to BHD data
df_bhd_residual = df_bhd_residual.loc[df_bhd_residual['decimal dates'] <= 2015]
residual_bhd = df_bhd_residual['residual']
x_resid = df_bhd_residual['decimal dates']  # new x to fig the adjusted y without 2015 dates
# print(residual_bhd)


"""  Plot of curve fit over data"""
fig = plt.figure(2)
size = 10
plt.scatter(x_init_bhd, y_init_bhd, marker='o', label='Baring Head Record > 1980', color=colors[0], s=size, alpha=0.3)
plt.plot(x_ccgcv_bhd, y_ccgcv_bhd, label='Baring Head SMOOTH', color=colors[0])
plt.scatter(x_init_heid, y_init_heid, marker='x', label='Heidelberg Data Record', color=colors[3], s=size, alpha=0.3)
plt.plot(x_ccgcv_heid, y_ccgcv_heid, label='Heidelberg SMOOTH', color=colors[3])
plt.legend()
plt.title('CCGCV Curve fit over Baring Head and Heidelberg Data')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned_Fig2.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""  Plot of residuals"""
fig = plt.figure(3)
size = 5
plt.scatter(x_resid, residual_bhd, marker='o', label='Baring Head', color=colors[0], s=size)
plt.scatter(x_init_heid, residual_heid, marker='x', label='Heidelberg', color=colors[3], s=size)
plt.legend()
plt.title('How far is the BHD and Heidelberg data from Heidelberg Curve fit?')
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned_Fig3.png',
            dpi=300, bbox_inches="tight")
plt.close()


""" Perform a t-test of the residuals"""
simple_t_test(residual_bhd, residual_heid)

""" How far apart is the smooth fit using BHD data to smooth fit using Heidelberg data?
 Compare by: 
 Fitting heidelberg data through BHD curve fit. How different is this that Heidelberg data through Heidelberg fit? 
 
 """
B_heid = ccgFilter(x_init_bhd, y_init_bhd, cutoff).getSmoothValue(x_init_heid)  # heidelberg x's fit to Baring Head CCGRV Curve
delta_curves = B_heid - A_heid
simple_t_test(B_heid, A_heid)
"""  How different are the smooth curves? """
fig = plt.figure(4)
size = 5
plt.scatter(x_init_heid, delta_curves, marker='o', color=colors[0], s=size)
# plt.legend()
plt.title('How far apart are the two smooth curves?')
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned_Fig4.png',
            dpi=300, bbox_inches="tight")
plt.close()

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


""" 
Monte Carlo for BHD Data
"""
step1_bhd = monte_carlo_step1(y_init_bhd, yerr_init_bhd)
step2_bhd = monte_carlo_step2(x_ccgcv_bhd, y_ccgcv_bhd, step1_bhd, x_init_bhd)
# return df_dates, df_ys, mean_array, stdev_array
bhd_mc_dates = step2_bhd[0]  # extract the date dataframe from function output
bhd_mc_dates = bhd_mc_dates.iloc[1]
# extract the y's, the randomized data that has been smoothed through ccgcv
bhd_mc_ys = step2_bhd[1]
bhd_mc_ys_1 = bhd_mc_ys.iloc[10]
bhd_mc_ys_2 = bhd_mc_ys.iloc[100]
bhd_mc_ys_3 = bhd_mc_ys.iloc[250]
bhd_mc_ys_4 = bhd_mc_ys.iloc[350]
bhd_mc_ys_5 = bhd_mc_ys.iloc[550]
bhd_mc_mean = step2_bhd[2]
bhd_mc_stdev = step2_bhd[3]
bhd_upperbounds = step2_bhd[4]
bhd_lowerbounds = step2_bhd[5]



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
plt.plot(bhd_mc_dates, bhd_mc_mean, color=colors[0], label='BHD MonteCarlo Mean', linestyle='solid')
plt.plot(bhd_mc_dates, bhd_upperbounds, color=colors[1], label='BHD MonteCarlo upperbound', linestyle='solid')
plt.plot(bhd_mc_dates, bhd_lowerbounds, color=colors[1], label='BHD MonteCarlo lowerbound', linestyle='solid')
plt.plot(heidelberg_mc_dates, heidelberg_mc_mean, color=colors[3], label='Heidelberg MonteCarlo Mean', linestyle='solid')
plt.plot(heidelberg_mc_dates, heidelberg_upperbounds, color=colors[4], label='Heidelberg MonteCarlo upperbound', linestyle='solid')
plt.plot(heidelberg_mc_dates, heidelberg_lowerbounds, color=colors[4], label='Heidelberg MonteCarlo lowerbound', linestyle='solid')
plt.title('Upper and lower uncertainty bounds')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.legend()
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/heidelberg_intercomparison_cleaned_Fig5.png',
            dpi=300, bbox_inches="tight")
plt.close()
