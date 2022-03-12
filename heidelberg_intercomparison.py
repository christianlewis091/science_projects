"""
Similar to the "rrl_vs_llnl_intercomparison.py, this code is meant to check the offset between the heidelberg data
and the RRl dataset.
There are three main datasets that I will have to compile for our harmonized dataest: RRL, SIO/LLNL, and Heid.
RRL is the reference, in the .py above, I calculate the offset for SIO/LLNL, and in this file, Heidelberg.

I will just be using the Cape Grim Record for this, beacuse it is their only southern hemisphere station

I will be performing this check in the following steps:
    1. upload Heidelberg Cape Grim data
    2. smooth fit it
        2.1 using my code
        2.2 using Miller Code
    3. RRL has measurements at Cape Grim. Solve eqn for RRL measurements date, and compare, how far
       is it from RRL measurement?
    4. Plot Heidelberg cape Gram, RRL Cape Grim and RRL Baring Head Together. Fit a smooth curve through it
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, ifft
import seaborn as sns


# Read in the heidelberg excel file
df1 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\heidelberg_cape_grim.xlsx', skiprows=40)
df2 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')
df3 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\BHD_v_CGO_NaOH_siteintercomparison.xlsx')
df4 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\Hua_et_al_2021.xlsx', sheet_name='SH')

# print(df4.columns)
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

#plot raw heidelberg measurements to see how its working so far
# plt.plot(df1['Average pf Start-date and enddate'], df1['D14C'], label='raw Heidelberg Cape Grim') # plot data)
# plt.plot(df2['DATE_COLL'], df2['DELTA14C'], label='Baring Head Record')
# plt.plot(df3['cgo_date'], df3['cgo_del14C'], label='raw RRL Cape Grim Data')
# # create a legend
# plt.legend()
# plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
# plt.savefig(r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/RadiocarbonIntercomparison/plots/Initialplot.png', dpi=300, bbox_inches="tight")

# extract the variables I need to smooth fit the heidelberg data
y = df1['D14C']
x = df1['date_as_number']
x_plot = df1['Average pf Start-date and enddate']

y2 = df2['DELTA14C']
x2 = df2['date_as_number']
x2_plot = df2['DATE_COLL']

y3 = df3['cgo_del14C']
x3 = df3['date_as_number']
x3_plot = df3['cgo_date']
# print(x3_plot)
# Smooth fit the heidelberg data
n = 4
empty_array = []  # pre-allocate an array where the for loop will put the coefficient outputs
cols = []  # empty array pre-allocated for the columns needed in new datafram
for i in range(0, n):
    p = np.polyfit(x, y, i, rcond=None, full=False, w=None, cov=False)  # multiple and linear polynomial fits
    empty_array.append(p)
    cols.append(i)
coeff = pd.DataFrame(empty_array, columns=cols)  # output the results from for loop into dataframe
# outputted coeffecients

# TODO write for-loop to simplify this block of code
degree0 = coeff.iloc[0]
degree1 = coeff.iloc[1]
degree2 = coeff.iloc[2]
degree3 = coeff.iloc[3]
# TODO write for-loop to simplify this block of code
y_guess_0th = degree0[0] * x ** 0
y_guess_lin = degree1[0] * x ** 1 + degree1[1] * x ** 0
y_guess_2nd = degree2[0] * x ** 2 + degree2[1] * x ** 1 + degree2[2] * x ** 0
y_guess_3rd = degree3[0] * x ** 3 + degree3[1] * x ** 2 + degree3[2] * x ** 1 + degree3[3] * x ** 0

Degree_to_test = y_guess_3rd
# TODO write for-loop to simplify this block of code
residual = y - Degree_to_test

# # TRANSFORM RESIDUAL
G = fft(residual)
G = abs(G)

# # CREATE LOW PASS FILTER
fs = 0.1  # sampling frequency
x_new = np.arange(0, len(G))
x_new = x_new * 0.1  # setting the data to be measured once per second (10 Hz)
delta = 1 / (len(G) * fs)  # parameter used to calculate the frequency
k = np.arange(0, len(G), 1)  # list from 0 to 3952
freq = k * delta
cutoff = 667
f_c = 365 / cutoff
p = 4
ln2 = -.0693
H_f = np.exp(ln2 * (freq / f_c) ** p)

# MULTIPLY FUNCTION BY FILTER AND SMOOTH LINE
residual_forinv = G * H_f
G_new = ifft(residual_forinv)
G_new = np.real(G_new)
smoothed_trend = G_new + y_guess_3rd
#

#PLOTTING: https://www.youtube.com/watch?v=fwZahTYfyxA&t=13s&ab_channel=TaylorSparks
colors = sns.color_palette("rocket", 6)
seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']
#            0sangre,   1neptune,  2pumpkin,  3clover,   4denim,    5cocoa,    6cumin,    7berry
# size = 15
# line = 0.5
# fig = plt.figure(1)
# plt.scatter(x2_plot, y2, marker='s', linewidths=line, s=size, facecolors='none', label='Baring Head Record', color='darkolivegreen')
# plt.scatter(x_plot, y, linestyle='-', linewidths=line, marker='o', facecolors='none', label='Heidelberg Cape Grim Raw Data', color='steelblue', s=size)  # plot data
# plt.plot(x_plot, y_guess_3rd, linestyle='-', marker='', label='Heidelberg Cape Grim 3rd Degree Polynomial', color='black')
# plt.plot(x_plot, smoothed_trend, linestyle='--', marker='', label='Heidelberg Cape Grim Smoothed Fit', color='chocolate')
# plt.scatter(x3_plot, y3, marker='^', linewidths=line, s=size, label='RRL Cape Grim Raw Data', color='firebrick')
# plt.legend(fontsize=6)
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
# plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
# # plt.show()
# plt.savefig(r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/RadiocarbonIntercomparison/plots/Heidelberg_overlay5.png', dpi=300, bbox_inches="tight")
# plt.close()

# fig = plt.figure(2)
# size = 15
# line = 0.5
# plt.scatter(x2, y2, marker='s', linewidths=line, s=size, label='Baring Head Record', color='darkolivegreen', facecolors='none')
# plt.scatter(x, y, linestyle='-', linewidths=line, marker='o', facecolors='none', label='Heidelberg Cape Grim Raw Data', color='steelblue', s=size)  # plot data
# plt.plot(x, y_guess_3rd, linestyle='-', marker='', label='Heidelberg Cape Grim 3rd Degree Polynomial', color='black')
# plt.plot(x, smoothed_trend, linestyle='--', marker='', label='Heidelberg Cape Grim Smoothed Fit', color='chocolate')
# plt.scatter(x3, y3, marker='^', linewidths=line, s=size, label='RRL Cape Grim Raw Data', color='firebrick')
# plt.legend(fontsize=6)
# plt.xlabel('Date as Number', fontsize=14)
# plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
# plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
# plt.ylim([0, 50])
# plt.xlim([40000, 44000])
# # plt.show()
# plt.savefig(r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/RadiocarbonIntercomparison/plots/Heidelberg_zoom2.png', dpi=300, bbox_inches="tight")
# print(x_plot)
# print(x3_plot)

"""
So, as decribed in the power point, the gap in the CGO_HDL data is a problem
SO I'm going to directly compare HDL to BHD to confirm agreement
"""

# How different is the polynomial curve from the smoothed fit?
# fig = plt.figure(3)
# diff = smoothed_trend - y_guess_3rd
# print(diff)
# plt.scatter(x, diff)
# plt.title('Smoothed Trend minus Polynomial Curve')
# plt.xlabel('Date as Number', fontsize=14)
# plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
# plt.savefig(r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/RadiocarbonIntercomparison/plots/Heidelberg_difference.png', dpi=300, bbox_inches="tight")
# plt.close()

"""
If we assume the polynomial fit is good enough for now, how far off from the HDL polynomial fit is the RRL/BHD data? 
to remind myself, here is the curve from above: 
Insert the corresponding X values from the RRL/Baring Head data into the curve 
"""
# # This will yield: Where the Y value should be according to the Heidelberg dataset
# y_guess_3rd_degree_RRL = degree3[0] * x2 ** 3 + degree3[1] * x2 ** 2 + degree3[2] * x2 ** 1 + degree3[3] * x2 ** 0
# # How far is guess from the Real Data?
# G = y2 - y_guess_3rd_degree_RRL
# plt.scatter(x2, G)
# plt.title('BHD data minus "Where BHD data should be"')
# plt.xlabel('Date as Number', fontsize=14)
# plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
# plt.savefig(r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/RadiocarbonIntercomparison/plots/Heidelberg_BHDoffset.png', dpi=300, bbox_inches="tight")
# plt.close()

"""
If one can look at my associated power point slides, I am going to next try to curve fit the BHD data and compare it to the curve fit from Heidelberg

"""
# Curve Fitting the Baring Head Data
n2 = 4
empty_array2 = []  # pre-allocate an array where the for loop will put the coefficient outputs
cols2 = []  # empty array pre-allocated for the columns needed in new datafram
for j in range(0, n2):
    p2 = np.polyfit(x2, y2, j, rcond=None, full=False, w=None, cov=False)  # multiple and linear polynomial fits
    empty_array2.append(p2)
    cols2.append(j)
coeff2 = pd.DataFrame(empty_array2, columns=cols2)  # output the results from for loop into dataframe
# outputted coeffecients

# TODO write for-loop to simplify this block of code
degree0_2 = coeff2.iloc[0]
degree1_2 = coeff2.iloc[1]
degree2_2 = coeff2.iloc[2]
degree3_2 = coeff2.iloc[3]
# TODO write for-loop to simplify this block of code

y_guess_3rd_BHD = degree3_2[0] * x2 ** 3 + degree3_2[1] * x2 ** 2 + degree3_2[2] * x2 ** 1 + degree3_2[3] * x2 ** 0

Degree_to_test2 = y_guess_3rd_BHD
# TODO write for-loop to simplify this block of code
residual_BHD = y2 - Degree_to_test2

# # TRANSFORM RESIDUAL
G = fft(residual_BHD)
G = abs(G)

# # CREATE LOW PASS FILTER
fs = 0.1  # sampling frequency
x_new = np.arange(0, len(G))
x_new = x_new * 0.1  # setting the data to be measured once per second (10 Hz)
delta = 1 / (len(G) * fs)  # parameter used to calculate the frequency
k = np.arange(0, len(G), 1)  # list from 0 to 3952
freq = k * delta
cutoff = 667
f_c = 365 / cutoff
p = 4
ln2 = -.0693
H_f = np.exp(ln2 * (freq / f_c) ** p)

# MULTIPLY FUNCTION BY FILTER AND SMOOTH LINE
residual_forinv = G * H_f
G_new = ifft(residual_forinv)
G_new = np.real(G_new)
smoothed_trend2 = G_new + y_guess_3rd_BHD

"""
Later I should try to clean up the code and write a massive function to do the curve smoothing and then I can
just apply BHD vs CGO to the function rather than changing all of the variable names
"""

"""
Now plot BHD data  / polynomial fit / smooth curve fit 
Against Heidelberg data / poly fit / smooth curve fit
"""

# fig = plt.figure(4)
# size = 15
# line = 0.5
# plt.scatter(x2_plot, y2, marker='s', linewidths=line, s=size, label='Baring Head Record', color='lightcoral', facecolors='none')
# plt.plot(x2_plot, y_guess_3rd_BHD, linestyle='-', label='Baring Head Polynomial Fit', color='maroon')  # plot data
# plt.plot(x2_plot, smoothed_trend2, linestyle='-', label='Baring Head Smoothed Fit', color='greenyellow')  # plot data
# plt.legend(fontsize=6)
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
# plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
# # plt.show()
# plt.savefig(r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/RadiocarbonIntercomparison/plots/Heidelberg_BHD_fit.png', dpi=300, bbox_inches="tight")

"""
SO - since I still don't have the miller code working, the smooth curve fit for BHD and Heidelberg are still both 
sets of discrete data points, so I cannot directly compare them by subtraction. However, I can compare the polynomial fits by appling a "fake X" 
to each and calculating the Y's and then subtracting them.
"""
# create fake X dataset
fake_x = np.linspace(32000,45000,1000)
# calculate y's for both curves using fake X dataset
calc1 = degree3[0] * fake_x ** 3 + degree3[1] * fake_x ** 2 + degree3[2] * fake_x ** 1 + degree3[3] * fake_x ** 0
calc2 = degree3_2[0] * fake_x ** 3 + degree3_2[1] * fake_x ** 2 + degree3_2[2] * fake_x ** 1 + degree3_2[3] * fake_x ** 0

fig = plt.figure(5)
plt.plot(fake_x, calc1, linestyle='--', label='Heidelberg curve', color=colors[1])  # plot data
plt.plot(fake_x, calc2, linestyle='-', label='BHD Curve', color=colors[2])  # plot data
plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
plt.xlabel('Date as number', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig(r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/RadiocarbonIntercomparison/plots/Heidelberg_curvecomparison.png', dpi=300, bbox_inches="tight")

fig = plt.figure(6)
plt.plot(x, smoothed_trend, linestyle='--', marker='', label='Heidelberg Cape Grim Smoothed Fit', color=colors[1])
plt.plot(x2, smoothed_trend2, linestyle='-', label='Baring Head Smoothed Fit', color=colors[2])  # plot data
plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
plt.ylim([0, 200])
plt.xlim([32000, 44000])
plt.xlabel('Date as number', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig(r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/RadiocarbonIntercomparison/plots/Heidelberg_curvecomparison2.png', dpi=300, bbox_inches="tight")

calc = calc1 - calc2
fig = plt.figure(7)
plt.plot(fake_x, calc, linestyle='--', marker='', label='Difference between polynomial fits', color=colors[1])
plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
plt.xlim([32000, 44000])
plt.ylim([-10, 2.5])
plt.xlabel('Date as number', fontsize=14)
plt.title('Heidelberg Poly - BHD Polynomial')
plt.ylabel('Residual \u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig(r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/RadiocarbonIntercomparison/plots/Heidelberg_residual2.png', dpi=300, bbox_inches="tight")



