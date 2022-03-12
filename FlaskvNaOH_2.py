import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from numpy.fft import fft, ifft
import seaborn as sns

df1 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist'
                    r'\The Science\Datasets\BHD_naoh_v_flask_methodintercomparison.xlsx')
                    # import the data with the flask and naoh data i'm interested in comparing
df2 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist'
                    r'\The Science\Datasets\BHD_winds.xlsx')
                    # import the data with the wind data I want to add

df1 = df1.drop(columns=['Collection_Date_Rachel_Curran_xcel',
                        'collection_decimaldate',
                        'measurement_decimaldate',
                        'Del14C',
                        'SE',
                        'Δ14C(‰)'], axis = 1) # dropping columns for simplicity
df2 = df2.drop(columns=['GNS Sample Number', 'NIWA Sample Number',
                        'Flask ID', 'R Number',
                        'Site Code', 'FlaskSites::Location', 'Latitude',
                        'Longitude', 'Elevation', 'collection_date_ddmmyyyy',
                        'Time Collected', 'Initial Pressure',
                        'CO2C14 Flag', 'CO2', 'CO2 Error', 'CO2 Flag', 'CO', 'CO Error',
                        'CO Flag', 'CH4', 'CH4 Error', 'CH4 Flag', 'Comments',
                        'NIWA analysis comments', 'Wind Speed', 'Weather',
                        'Temperature', 'Site Type', 'NZA'], axis = 1)
# dropping columns for simplicity

combine = pd.merge(df1,df2, how='outer')
# print(combine.columns)

x = (combine['Collection Date Mean'])
x = x.dropna()
y_naoh = (combine['naoh_del14C'])
y_naoh = y_naoh.dropna()
y_flask = (combine['flask_del14C'])
y_flask = y_flask.dropna()
lapse = (combine['delta_measure_mins_collect_days'])
lapse = lapse.dropna()
wind = (combine['Wind Direction'])
wind = wind.dropna()
# print(x)
# print(y_naoh)
#
"""
FIT THE DATA TO POLYNOMIALS OF VARYING DEGREES
"""

n = 4
empty_array = []  # pre-allocate an array where the for loop will put the coefficient outputs
cols = []  # empty array pre-allocated for the columns needed in new datafram
for i in range(0, n):
    p = np.polyfit(x, y_naoh, i, rcond=None, full=False, w=None, cov=False)  # multiple and linear polynomial fits
    empty_array.append(p)
    cols.append(i)
coeff = pd.DataFrame(empty_array, columns=cols)  # output the results from for loop into dataframe
# print(coeff)
# coeffs = pd.DataFrame(empty_array, columns=['0', '1', '2', '3', '4'])  # output the results from for loop into dataframe


# TODO write for-loop to simplify this block of code
degree0 = coeff.iloc[0]
degree1 = coeff.iloc[1]
degree2 = coeff.iloc[2]
degree3 = coeff.iloc[3]

# TODO write for-loop to simplify this block of code
y_guess_0th    = degree0[0]*x**0
y_guess_lin = degree1[0]*x**1 + degree1[1]*x**0
y_guess_2nd    = degree2[0]*x**2 + degree2[1]*x**1 + degree2[2]*x**0
y_guess_3rd    = degree3[0]*x**3 + degree3[1]*x**2 + degree3[2]*x**1 + degree3[3]*x**0
#
Degree_to_test = y_guess_3rd
# TODO write for-loop to simplify this block of code
residual = y_naoh - Degree_to_test


"""
MY VERSION OF THE CURVE FITTING PROGRAM
"""

# # TRANSFORM RESIDUAL
G = fft(residual)
G = abs(G)

# # CREATE LOW PASS FILTER
fs = 0.1 # sampling frequency
x_new = np.arange(0, len(G))
x_new = x_new*0.1  # setting the data to be measured once per second (10 Hz)
delta = 1/(len(G)*fs)  # parameter used to calculate the frequency
k = np.arange(0, len(G), 1) # list from 0 to 3952
freq = k*delta
cutoff = 667
f_c = 365 / cutoff
p = 4
ln2 = -.0693
H_f = np.exp(ln2*(freq/f_c)**p)

# MULTIPLY FUNCTION BY FILTER AND SMOOTH LINE
residual_forinv = G*H_f
G_new = ifft(residual_forinv)
G_new = np.real(G_new)
smoothed_trend = G_new + y_guess_3rd
#


"""
PLOT THE DATA 
"""

# PLOTTING: https://www.youtube.com/watch?v=fwZahTYfyxA&t=13s&ab_channel=TaylorSparks
# down sample data for plotting?
# Generate some nice colors:
colors = sns.color_palette("rocket", 3)
seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']
#            0sangre,   1neptune,  2pumpkin,  3clover,   4denim,    5cocoa,    6cumin,    7berry


# dflask_dtrend = y_flask - smoothed_trend
# fig = plt.figure(1, figsize=(5, 5))
# plt.scatter(x, y_naoh, linestyle='-', marker='o', label='Select NaOH Measured 14CO2 at BARING HEAD from RRL', color=colors[2]) # plot data
# plt.plot(x, Degree_to_test, linestyle='--', marker='' , label='Polynomial Fit', color='black') # plot data
# plt.plot(x, smoothed_trend, linestyle='-', marker='' , label='Smoothed Line of Select NaOH Data - 667 Day Cutoff', color=colors[1]) # plot data
# plt.scatter(x, y_flask, linestyle='-', marker='^' , label='Flask Measurement', color=colors[0]) # plot data
# # plt.scatter(date, Del14C_flask, linestyle='-', marker='^', label='Select FLASK Measurements from BARING HEAD', color=colors[0]) # plot data
# # create a legend
# plt.legend(fontsize=6)
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('14CO2', fontsize=14)  # label the y axis
# plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
# plt.savefig(r'G:/My Drive/Work/GNS Radiocarbon Scientist/The Science/Stats and Data Analysis/Matlab and Python Files/FlaskvNaOH_667cutoff_3rdDegree.png', dpi=300, bbox_inches="tight")


"""
IS THE DATA IMPACTED BY THE TIME FLASK MEASUREMENTS WERE WAITING IN THE FLASK??
"""

# Calculate Difference Between Flask and NaOH
dflask_dtrend = y_flask - smoothed_trend
dflask_dnaoh = y_flask - y_naoh
linear = np.polyfit(lapse, dflask_dtrend, 1)
y_guess_lin = linear[0]*lapse + linear[1]

# fig = plt.figure(2, figsize=(5, 5))
# plt.scatter(lapse, dflask_dnaoh, linestyle='-', marker='o', label='Del14C Flask - raw NaOH', color=colors[0]) # plot data
# plt.scatter(lapse, dflask_dtrend, linestyle='-', marker='X', label='Del14C Flask - smoothed NaOH', color=colors[1]) # plot data
# plt.plot(lapse, y_guess_lin, linestyle='-', marker='', label='Linear fit', color='black') # plot data
# # create a legend
# plt.legend(fontsize=6)
# plt.xlabel('Days between collection and measurement', fontsize=14)
# plt.ylabel('Flask - Smoothed NaOH Trend', fontsize=14)  # label the y axis
# plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
# plt.savefig(r'G:/My Drive/Work/GNS Radiocarbon Scientist/The Science/Stats and Data Analysis/Matlab and Python Files/TimeOffset', dpi=300, bbox_inches="tight")

"""
WHAT ABOUT WIND DIRECTION? 
"""
# Plotting the wind direction
# need to adjust the length of Wind so it fits the other value i'm plotting (the difference between flask and smoothed trend)
wind = wind[0:len(dflask_dtrend)]

linear_2 = np.polyfit(wind, dflask_dtrend, 1)
y_guess_lin_2 = (linear_2[0]*wind) + linear_2[1]


# fig = plt.figure(3)
# plt.scatter(wind, dflask_dnaoh, linestyle='-', marker='o', label='Del14C Flask - raw NaOH', color=colors[0]) # plot data
# plt.scatter(wind, dflask_dtrend, linestyle='-', marker='X', label='Del14C Flask - smoothed NaOH', color=colors[1]) # plot data
# plt.plot(wind, y_guess_lin_2, linestyle='-', marker='', label='Linear fit', color='black') # plot data
# # create a legend
# plt.legend(fontsize=6)
# plt.xlabel('Wind direction', fontsize=14)
# plt.ylabel('Difference between flask and NaOH del14CO2', fontsize=14)  # label the y axis
# plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
# plt.savefig(r'G:/My Drive/Work/GNS Radiocarbon Scientist/The Science/Stats and Data Analysis/Matlab and Python Files/Winddirection', dpi=300, bbox_inches="tight")


"""
STATS -> a simple T-test 
"""
resid_1 = y_naoh - smoothed_trend
resid_2 = y_flask - smoothed_trend

fig = plt.figure(4)
plt.scatter(x, resid_1, linestyle='-', marker='o', label='Residual of NaOH - smoothed line', color=colors[0]) # plot data
plt.scatter(x, resid_2, linestyle='-', marker='X', label='Residual of flask - smoothed line', color=colors[1]) # plot data
plt.legend(fontsize=6)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Residual', fontsize=14)  # label the y axis
plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
plt.savefig(r'G:/My Drive/Work/GNS Radiocarbon Scientist/The Science/Stats and Data Analysis/Matlab and Python Files/NaOH_v_Flask_Residual', dpi=300, bbox_inches="tight")
d_mean = np.abs(np.average(resid_1) - np.average(resid_2))
print(d_mean)
d_of_f = (len(resid_1) + len(resid_2)) - 2
print("Degrees of freedom = " + str(d_of_f))
var_a = np.var(resid_1)
var_b = np.var(resid_2)
c = (np.sqrt((var_a / len(resid_1)) + (var_b / len(resid_2))))
X = d_mean / c
print(X)  # t-value =  -2.26199631876107
# critical value at 98% confidence = 2.390, if crit val > t-value, no difference.



