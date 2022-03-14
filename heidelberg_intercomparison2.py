from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import random
from miller_curve_algorithm import ccgFilter
from my_functions import long_date_to_decimal_date, simple_t_test
from my_functions import year_month_todecimaldate
import array as arr

""" IMPORT ALL THE DATA """
# Read in the heidelberg excel file
df1 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\heidelberg_cape_grim.xlsx', skiprows=40)
df2 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')
df3 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\BHD_v_CGO_NaOH_siteintercomparison.xlsx')
df4 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\Hua_et_al_2021.xlsx', sheet_name='SH')

""" CLEAN UP THE FILES AND EXTRACT VARIABLES """

# drop columns I'm not interested in
df1 = df1.drop(columns=['#location', 'sampler_id', 'samplingheight', 'startdate', 'enddate',
                        'samplingpattern',
                        'wheightedanalyticalstdev_D14C',
                        'nbanalysis_D14C', 'd13C', 'flag_D14C'], axis=1)

df2 = df2.drop(columns=['SITE', 'NZPREFIX', 'NZ', 'DATE_ST', 'DATE_END', 'DAYS_EXP',
                        'DELTA13C_IRMS', 'F14C', 'F14C_ERR', 'FLAG', 'METH_VESSEL', 'METH_COLL'], axis=1)

df3 = df3.drop(columns=['bhd_naoh_date', 'bhd_del14c', 'bhd_naoh_stdev'], axis=1)

# drop NaN's in the column I'm most interested in
df1 = df1.dropna(subset=['D14C'])
df2 = df2.dropna(subset=['DELTA14C'])
df2 = df2.loc[(df2['DEC_DECAY_CORR'] > 1980)]  # filter out all values after 1980
df3 = df3.dropna(subset=['cgo_del14C'])

# reset all the indeces after reformatting to avoid random errors
df1 = df1.reset_index()
df2 = df2.reset_index()
df3 = df3.reset_index()

# extract the variables I need
y = df1['D14C']  # Heidelberg CGO
print(type(y))
print(type(y[1]))
y_err = df1['weightedstderr_D14C']
x = df1['date_as_number']  # Heidelberg CGO
x_plot = df1['Average pf Start-date and enddate']  # Heidelberg CGO
x_plot = long_date_to_decimal_date(x_plot)

y2 = df2['DELTA14C']
y2_err = df2['DELTA14C_ERR']
x2 = df2['date_as_number']
x2_plot = df2['DATE_COLL']
x2_plot = long_date_to_decimal_date(x2_plot)

y3 = df3['cgo_del14C']
x3 = df3['date_as_number']
x3_plot = df3['cgo_date']
x3_plot = long_date_to_decimal_date(x3_plot)

""" CALL IN THE CURVE SMOOTHER """

miller = ccgFilter(x_plot, y).getMonthlyMeans()
miller_x = year_month_todecimaldate(miller[0], miller[1])  # get the dates to be in decimal format
miller_y = miller[2]

""" 
When I use the Miller curve smoother, it spits out an array of values with
different length than then original file. Run this below to see. 

print(len(y))
print(len(miller_y)) 
 
For this reason, I can plot it, 
but I cannot simply subtract other value from it to get the residuals. However, there is another 
function that I can use to input any x and get out a y.

 """
heidelberg_guesses = ccgFilter(x_plot, y).getSmoothValue(
    x_plot)  # find appropriate Y-values in smooth curve for BHD X's
residual_heidelberg = y - heidelberg_guesses
d = {'decimal dates': x_plot, 'y_guesses': heidelberg_guesses, 'residual': residual_heidelberg}
df_heid = pd.DataFrame(data=d)  # create a dataframe to make future manipulation of data simpler

bhd_guesses = ccgFilter(x_plot, y).getSmoothValue(x2_plot)  # find appropriate Y-values in smooth curve for BHD X's
# the above line returns many Nan's as the BHD record extends in both ways outside the heidelberg dataset
residual_bhd = y2 - bhd_guesses
d2 = {'decimal dates': x2_plot, 'y_guesses': bhd_guesses, 'residual': residual_bhd}
df_bhd = pd.DataFrame(data=d2)  # create a dataframe to make future manipulation of data simpler
df_bhd = df_bhd.dropna(subset=['y_guesses'])  # drop the Nan's from the dataset I just created (see line 85)

""" 
The residuals overlap in a normal way until around 2015, where the gap in the Heidelberg Data begins.
The smooth fit tracks to a single point which falls below the normal slope of the line, which makes those residuals jump up. 
For this reason, I will omit that final data point from Heidelberg analysis in future data. 

I'm going to do a t-test to see if these two datasets are significantly different; however
first I must cut-off the data after 2015 to avoid skewing it based on the issue described in the three lines above. 
 """
df_bhd = df_bhd.loc[df_bhd['decimal dates'] <= 2015]  # drop the Nan's from the dataset I just created (see line 85)
residual_bhd_new = df_bhd['residual']
x2_plot_new = df_bhd['decimal dates']

""" 
Now that I've cleaned up the data, I can do a t-test the see if there is any meaningful
difference between the residual datasets. 
 """

simple_t_test(residual_bhd_new, residual_heidelberg)

""" 
My t-test says there is no difference in the residuals. That is one good first step toward no-offset. 
What is another way...a better way...to test that these data are the same? 

If I fit a line through BHD and sample for Heidelberg, I should get the same result. 

What about fitting a line through both, and comparing the smoothed curve fits? 
Below I'll fit the BHD data
 """
bhd_fit = ccgFilter(x2_plot, y2).getMonthlyMeans()
bhd_fit_x = year_month_todecimaldate(bhd_fit[0], bhd_fit[1])  # get the dates to be in decimal format
bhd_fit_y = bhd_fit[2]  # values output from the curve
# print(bhd_fit)

heidelberg_guesses_2 = ccgFilter(x2_plot, y2).getSmoothValue(x_plot)  # find Heidelberg Y's in the BHD curve
bhd_guesses_2 = ccgFilter(x2_plot, y2).getSmoothValue(x2_plot)  # find BHD guesses in BHD curve

""" 
The difference between bhd_guesses and bhd_guesses_2 will show the difference in the lines with time.
Same for heidelberg_guesses and heidelberg_guesses_2
"""
var = heidelberg_guesses_2 - heidelberg_guesses  # BHD curve minus heidelberg curve
var2 = bhd_guesses_2 - bhd_guesses  # BHD curve minus heidelberg curve

""" 
run Monte Carlo Program I wrote
"""








""" 
MONTE CARLO ANALYSIS

Been stuck with the loops (see Monte_carlo_test.py)
Try this next: 
https://astrofrog.github.io/py4sci/_static/Practice%20Problem%20-%20Monte-Carlo%20Error%20Propagation%20-%20Sample%20Solution.html 
or this:
http://www-personal.umd.umich.edu/~wiclarks/AstroLab/HOWTOs/NotebookStuff/MonteCarloHOWTO.html
or this: 
http://www.eg.bucknell.edu/physics/ph310/jupyter/error_propagation_examples.ipynb.pdf

Also learn about dictionaries in python

GOT IT TO WORK ON MY OWN!! 
The following code will iterate over the original data ... 
y = df1['D14C'] , heidelberg 14C data
y2 = df2['DELTA14C'], BHD 14C data
... and create a new array of data within the uncertainty range.
"""
new_array = y  # just creating a new variable that contains the Heidelberg Y-values
n = 1000
cols = np.linspace(0, len(y))

for i in range(0, n):
    empty_array = []
    for j in range(0, len(y)):
        a = y[j]  # grab the first item in the set
        b = y_err[j]  # grab the uncertainty
        rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
        c = a + rand  # add this to the number
        empty_array.append(c)  # add this to a list
        # print(len(empty_array))
    new_array = np.vstack((new_array, empty_array))
# print(new_array)
# print(len(new_array[1]))
# print(len(new_array))
# print(new_array[1])
# Put the new randomize data through the Miller Code to smooth it:
""" code works up to here...don't change anything above!!!!
Now we run those randomized data through the miller code and get 1000 smoothed curves:
"""

empty_array_for_date = miller_x  # I'm initializing the new array as the original output from the Miller file, so there's something the v-stack onto.
empty_array_for_y = miller_y  # I'm initializing the new array as the original output from the Miller file, so there's something the v-stack onto.
for i in range(0, len(new_array)):
    monte1 = new_array[i]  # grab the first row of the array
    monte_output = ccgFilter(x_plot, monte1).getMonthlyMeans() # put that first row through the miler CCG filter...
    # use my other function to convert Miller code output to decimal dates
    monte_output_date = year_month_todecimaldate(monte_output[0], monte_output[1])
    # also grab the y-data
    monte_output_y = monte_output[2]
    empty_array_for_date = np.vstack((empty_array_for_date, monte_output_date))
    empty_array_for_y = np.vstack((empty_array_for_y, monte_output_y))

print(np.shape(empty_array_for_y))
print(np.shape(empty_array_for_date))
print(empty_array_for_y[1])
testing = empty_array_for_y[1]
print(testing[1])

# up to here, the code works, and creates a nice group of Monte_Carlo'd data.
# Next, I need to find the uncertainty associated with the Monte Carlo, beacuse that's the whole point, right?

""" Find the mean of all y's associated with every x-value: I think we'll need another for loop.
You can associate the array you already have with a dataframe.
"""
dataf = pd.DataFrame(empty_array_for_y)  # output the results from for loop into dataframe
mean_array = []
stdev_array = []
for i in range(0, len(empty_array_for_y[1])):
    element1 = np.sum(dataf[i])  # grab the first column of the dataframe and take the sum
    element1 = element1 / len(empty_array_for_y)  # find the mean of the first column of the dataframe
    mean_array.append(element1)  # append it to a new array
    stdev_monte = np.std(dataf[i])  # find the stdev of the first column of the dataframe
    stdev_array.append(stdev_monte)
print(mean_array)
print(stdev_array)

""" Now that I have means and standard deviations for all of the monte carlo runs, what do I do with them??? PLOT! and compare with Baring Head....

Repeating a whole bunch of code to get Baring Head means...
"""

new_array = y2  # just creating a new variable that contains the Heidelberg Y-values
n = 1000
cols = np.linspace(0, len(y))

for i in range(0, n):
    empty_array = []
    for j in range(0, len(y2)):
        a = y2[j]  # grab the first item in the set
        b = y2_err[j]  # grab the uncertainty
        rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
        c = a + rand  # add this to the number
        empty_array.append(c)  # add this to a list
        # print(len(empty_array))
    new_array = np.vstack((new_array, empty_array))
# print(new_array)
# print(len(new_array[1]))
# print(len(new_array))
# print(new_array[1])
# Put the new randomize data through the Miller Code to smooth it:
""" code works up to here...don't change anything above!!!!
Now we run those randomized data through the miller code and get 1000 smoothed curves:
"""

empty_array_for_date = bhd_fit_x  # I'm initializing the new array as the original output from the Miller file, so there's something the v-stack onto.
empty_array_for_y = bhd_fit_y  # I'm initializing the new array as the original output from the Miller file, so there's something the v-stack onto.
for i in range(0, len(new_array)):
    monte1 = new_array[i]  # grab the first row of the array
    monte_output = ccgFilter(x2_plot, monte1).getMonthlyMeans() # put that first row through the miler CCG filter...
    # use my other function to convert Miller code output to decimal dates
    monte_output_date = year_month_todecimaldate(monte_output[0], monte_output[1])
    # also grab the y-data
    monte_output_y = monte_output[2]
    empty_array_for_date = np.vstack((empty_array_for_date, monte_output_date))
    empty_array_for_y = np.vstack((empty_array_for_y, monte_output_y))

print(np.shape(empty_array_for_y))
print(np.shape(empty_array_for_date))
print(empty_array_for_y[1])
testing = empty_array_for_y[1]
print(testing[1])

# up to here, the code works, and creates a nice group of Monte_Carlo'd data.
# Next, I need to find the uncertainty associated with the Monte Carlo, beacuse that's the whole point, right?

""" Find the mean of all y's associated with every x-value: I think we'll need another for loop.
You can associate the array you already have with a dataframe.
"""
dataf = pd.DataFrame(empty_array_for_y)  # output the results from for loop into dataframe
mean_array_bhd = []
stdev_array_bhd = []
for i in range(0, len(empty_array_for_y[1])):
    element1 = np.sum(dataf[i])  # grab the first column of the dataframe and take the sum
    element1 = element1 / len(empty_array_for_y)  # find the mean of the first column of the dataframe
    mean_array_bhd.append(element1)  # append it to a new array
    stdev_monte = np.std(dataf[i])  # find the stdev of the first column of the dataframe
    stdev_array_bhd.append(stdev_monte)
print(mean_array_bhd)
print(stdev_array_bhd)






# """  Plot of inital residuals  """
#
# # colors = sns.color_palette("crest")
# # # keep colors consistent
# # bhd_data_color = 'tab:blue'
# # bhd_smooth_color = 'blue'
# # heid_data_color = 'tab:red'
# # heid_smooth_color = 'red'
# #
# # size = 10
# # fig = plt.figure(1)
# # plt.plot(bhd_fit_x, bhd_fit_y, linestyle='solid', label='RRL Baring Head Smooth Fit', color=bhd_smooth_color)
# # plt.plot(miller_x, miller_y, linestyle='solid', marker='', label='Heidelberg Data Smoothed (Miller Algorithm)',
# #          color=heid_smooth_color)
# # # plt.scatter(x2_plot, bhd_guesses, marker='x', label='BHD Y-guesses', s=size, color=bhd_data_color)
# # # plt.scatter(x_plot, heidelberg_guesses, marker='*', label='Heidelberg Y-guesses', s=size, color=heid_data_color)
# # # plt.scatter(x_plot, var, marker='*', label='Heidelberg', s=size, color=heid_data_color)
# # # plt.scatter(x2_plot, var2, marker='x', label='BHD', s=size, color=bhd_data_color)
# # plt.legend()
# # # plt.title('Difference between the BHD fit and Heidelberg fit using the y = f(x) values for each')
# # plt.xlim([1980, 2020])
# # plt.ylim([0, 300])
# # plt.xlabel('Date', fontsize=14)
# # plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
# # plt.savefig(
# #     r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/Radiocarbonintercomparison/plots/PLot9.png',
# #     dpi=300, bbox_inches="tight")
# # plt.close
#
colors2 = sns.color_palette("rocket")
# keep colors consistent
# run1 = 50
# run2 = 150
# run3 = 350
# run4 = 500
# run5 = 760
# size = 10
# fig = plt.figure(1)
# plt.plot(empty_array_for_date[run1], empty_array_for_y[run1], linestyle='solid', color=colors2[0], label='MC run 50')
# plt.plot(empty_array_for_date[run2], empty_array_for_y[run2], linestyle='solid', color=colors2[1], label='MC run 150')
# plt.plot(empty_array_for_date[run3], empty_array_for_y[run3], linestyle='solid', color=colors2[2], label='MC run 350')
# plt.plot(empty_array_for_date[run4], empty_array_for_y[run4], linestyle='solid', color=colors2[3], label='MC run 500')
# plt.plot(empty_array_for_date[run5], empty_array_for_y[run5], linestyle='solid', color=colors2[4], label='MC run 760')
# plt.legend()
# # plt.title('Difference between the BHD fit and Heidelberg fit using the y = f(x) values for each')
# plt.xlim([1990, 1995])
# plt.ylim([120, 150])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
# plt.savefig(
#     r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/radiocarbon_intercomparison/plots/PLot11.png',
#     dpi=300, bbox_inches="tight")
#
# size = 10
# fig = plt.figure(1)
# plt.plot(bhd_fit_x, mean_array_bhd, linestyle='solid', color=colors2[0], label='BHD Monte Carlo Means')
# plt.plot(miller_x, mean_array, linestyle='solid', color=colors2[1], label='BHD Monte Carlo Means')
#
# plt.legend()
# # plt.title('Difference between the BHD fit and Heidelberg fit using the y = f(x) values for each')
# # plt.xlim([1990, 1995])
# # plt.ylim([120, 150])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
# plt.savefig(
#     r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/radiocarbon_intercomparison/plots/PLot12.png',
#     dpi=300, bbox_inches="tight")
