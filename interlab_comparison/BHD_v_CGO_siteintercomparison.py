import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from numpy.fft import fft, ifft
import seaborn as sns
import datetime
import scipy.stats as stats
from cbl_curve_fitting_algorithm import cbl_curve_fit
from miller_curve_algorithm import ccgFilter
from my_functions import year_month_todecimaldate
# testing
""" 
INITIAL READ IN OF THE DATA
"""
df = pd.read_excel(r'H:\The Science\Datasets\BHD_v_CGO_NaOH_siteintercomparison.xlsx')
bhd_date = (df['bhd_naoh_date'])  # pull out the date data
bhd_date2 = (df['date_as_number'])
bhd_14c = (df['bhd_del14c'])
bhd_14c_err = (df['bhd_naoh_stdev'])

cgo_date = (df['cgo_date'])  # pull out the date data
cgo_14C = (df['cgo_del14C'])  # pull out the date data
cgo_err = (df['cgo_del14C_stdev'])  # pull out the date data

""" 
Call the curve fitting programs
"""

# call in the curve fitting programs
smoothed_trend = cbl_curve_fit(bhd_date2, bhd_14c)
cbl_smooth_cgo = cbl_curve_fit(bhd_date2, cgo_14C)

""" 
Plot the data
"""

colors = sns.color_palette("rocket", 6)
seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']
#            0sangre,   1neptune,  2pumpkin,  3clover,   4denim,    5cocoa,    6cumin,    7berry

fig = plt.figure(1)
plt.plot(bhd_date, smoothed_trend, linestyle='solid', label='Smoothed Baring Head Curve', color=colors[0]) # plot data
plt.plot(bhd_date, cbl_smooth_cgo, linestyle='dashed', label='Smoothed Cape Grim Curve', color=colors[1]) # plot data
plt.errorbar(bhd_date, bhd_14c, yerr=bhd_14c_err, fmt = 'o',color=colors[2], ecolor='black', elinewidth = 1, capsize=2, label='BHD NaOH 14CO2')
plt.errorbar(cgo_date, cgo_14C, yerr=cgo_err, fmt = '^',color=colors[3], ecolor='black', elinewidth = 1, capsize=2, label='CGO NaOH 14CO2')
plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
plt.legend()
fig.autofmt_xdate()
plt.show()

""" 
Find Residuals of BHD and CGO data to the line....
"""

bhd_residual = bhd_14c - smoothed_trend
cgo_residual = cgo_14C - smoothed_trend

fig = plt.figure(3)
plt.errorbar(bhd_date, bhd_residual, yerr=bhd_14c_err, fmt = 'o',color=colors[2],
             ecolor='black', elinewidth = 1, capsize=2, label='BHD NaOH 14CO2')
plt.errorbar(bhd_date, cgo_residual, yerr=cgo_err, fmt = 'x',color=colors[1],
             ecolor='black', elinewidth = 1, capsize=2, label='CGO NaOH 14CO2')
plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
plt.legend()
plt.text(42800, 3.5, 'Error bars = raw measurement uncertainty', fontsize = 10)
fig.autofmt_xdate()
plt.show()

""" 
Perform a t-test
"""
d_mean = np.average(bhd_residual) - np.average(cgo_residual)
d_of_f = (len(bhd_residual) + len(cgo_residual)) - 2
var_a = np.var(bhd_residual)
var_b = np.var(cgo_residual)

X = d_mean / (np.sqrt((var_a / len(bhd_residual)) + (var_b / len(cgo_residual))))
print(X)  # t-value =  0.11652854103985533
# critical value at 95% confidence = 2.021, if crit val > t-value, no difference.
#
