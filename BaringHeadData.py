"""
This file curve fits the Baring Head Data that Jocelyn sent to me
using Christian's curve fitting program

"""
from cbl_curve_fitting_algorithm import cbl_curve_fit
from miller_curve_algorithm import ccgFilter
from year_month_to_decimaldate import year_month_todecimaldate
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

""" Import all of the data and extract / name variables """

df = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist'
                   r'\The Science\Datasets\BHD_14CO2_datasets_20211013.xlsx',
                   sheet_name='bhd_final_screened_data2')

df = df[['DEC_DECAY_CORR','DELTA14C', 'METH_COLL']]  # print only the data I want to see # this duplicates line 15
meth_coll = (df['METH_COLL'])  # pull out the method collection data
date = (df['DEC_DECAY_CORR'])  # pull out the date data
D14C = (df['DELTA14C'])  # pull out the radiocarbon ata

# EXTRACT X AND Y VARIABLES THAT I WANT
naoh = df.loc[(df['METH_COLL'] == 'NaOH_static') & (df['DEC_DECAY_CORR'] > 1970)]
naoh = naoh.reset_index()

flask = df.loc[(df['METH_COLL'] == 'Whole_air') & (df['DEC_DECAY_CORR'] > 1970)]
flask = flask.reset_index()

naoh_x = (naoh['DEC_DECAY_CORR'])
naoh_y = (naoh['DELTA14C'])
flask_x = (flask['DEC_DECAY_CORR'])
flask_y = (flask['DELTA14C'])

""" Call in the smoothing functions """

# my function returns just the y-values, and I can plot with the x's I already have
naoh_smooth = cbl_curve_fit(naoh_x, naoh_y) # smooth the naOH sampled data using Christian's curve
flask_smooth = cbl_curve_fit(flask_x, flask_y)  # smooth the flask sampled data using Christian's curve

# miller code returns dataset that still needs extraction and a bit of cleaning
naoh_miller = ccgFilter(naoh_x, naoh_y).getMonthlyMeans() # returns a dataset with multiple columns [year, month, value, ..., ..., ...
# print(naoh_miller)  # [151 rows x 4 columns]
naoh_miller_x = year_month_todecimaldate(naoh_miller[0], naoh_miller[1]) # get the dates to be in decimal format
naoh_miller_y = naoh_miller[2]

flask_miller = ccgFilter(flask_x, flask_y).getMonthlyMeans() # returns a dataset with multiple columns [year, month, value, ..., ..., ...
# print(naoh_miller)  # [151 rows x 4 columns]
flask_miller_x = year_month_todecimaldate(flask_miller[0], flask_miller[1]) # get the dates to be in decimal format
flask_miller_y = flask_miller[2]


# PLOTTING: https://www.youtube.com/watch?v=fwZahTYfyxA&t=13s&ab_channel=TaylorSparks
# down sample data for plotting?
# Generate some nice colors:
colors = sns.color_palette("rocket", 6)
seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']
#            0sangre,   1neptune,  2pumpkin,  3clover,   4denim,    5cocoa,    6cumin,    7berry

plt.plot(flask_miller_x, flask_miller_y, linestyle='solid', marker='', label='Flask Data Smoothed (Miller Algorithm)', color= 'tab:blue')
plt.plot(naoh_miller_x, naoh_miller_y, linestyle='solid', marker='', label='NaOH Data Smoothed (Miller Algorithm)', color='tab:red')
# plt.plot(flask_x, flask_smooth, linestyle='dashed', marker='', label='Flask Data Smoothed (CBL Algorithm)', color= 'tab:blue')
# plt.plot(naoh_x, naoh_smooth, linestyle='dashed', marker='', label='NaOH Data Smoothed (CBL Algorithm)', color= 'tab:red')
plt.scatter(naoh_x, naoh_y, marker='^', label='NaOH Final Data', color='tab:red', edgecolors='black')
plt.scatter(flask_x, flask_y, marker='o', label='NaOH Final Data', color='tab:blue', edgecolors='black')
plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
plt.legend()
plt.xlim([2010, 2020])
plt.ylim([0, 60])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.savefig(r'C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/Radiocarbonintercomparison/plots/BaringHead_final_zoom_b.png', dpi=300, bbox_inches="tight")
























# Y = naoh_miller[2]                                        # extract the 'value' column from the dataset
# naoh_miller_x = year_month_todecimaldate(naoh_miller[0], naoh_miller[1]) # get the dates to be in decimal format
#
# print(Y)
# print(naoh_miller_x)
# plt.plot(naoh_x, Y)
# plt.show()

# flask_miller = ccgFilter(flask_x, flask_y).getMonthlyMeans()
# Y2 = flask_miller[2]
# flask_miller_x = year_month_todecimaldate(flask_miller[0], flask_miller[1])


# plt.plot(flask_x, flask_y)
# plt.plot(naoh_x, naoh_y)
# plt.plot(naoh_x, naoh_smooth) # christian's smooth curve
# plt.plot(naoh_miller_x, naoh_miller_y)
# plt.show()

#
#
#
#
#
#
#
#
#
#
#
#
# # PLOTTING: https://www.youtube.com/watch?v=fwZahTYfyxA&t=13s&ab_channel=TaylorSparks
# # down sample data for plotting?
# # set limits of the plot right away:
# xmin = 1970
# xmax = 2020
# ymin = 0
# ymax = 500
#
# # Generate some nice colors:
# colors = sns.color_palette("rocket", 3)
# seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']
# #            0sangre,   1neptune,  2pumpkin,  3clover,   4denim,    5cocoa,    6cumin,    7berry
#
#
# # plot data for left panel
# fig = plt.figure(1)
# plt.scatter(naoh_x, naoh_y, linestyle='-', marker='^', label='NaOH Measured 14CO2 at BARING HEAD from RRL', color=colors[2]) # plot data
# plt.plot(naoh_x, naoh_smooth, linestyle='-', label='Smoothed NaOH Curve, 80 day cutoff', color=colors[1]) # plot data
# plt.scatter(flask_x, flask_y, linestyle='-', marker='o', label='FLASK Measured 14CO2 at BARING HEAD from RRL', color=colors[0]) # plot data
# # create a legend
# plt.legend()
# # plot limits
# plt.xlim([min(naoh_x), max(naoh_x)])
# plt.ylim([min(naoh_y), max(naoh_y)])
# # create axis labels
# plt.ylabel('14CO2', fontsize=14)  # label the y axis
# plt.xlabel('date', fontsize=14)  # label the y axis
# plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
# plt.show()
#
# # Generate second panel
# fig = plt.figure(2)
# plt.plot(naoh_x, y_guess, linestyle='-', markersize=2, label='NaOH Y-Guess for 3rd Deg Polynomial Fit', color=colors[0]) # plot data
# plt.plot(naoh_x, smoothed_trend, linestyle='-', label='Smoothed NaOH Curve', color=colors[1]) # plot data
# # create a legend
# plt.legend()
# # plot limits
# plt.xlim([min(naoh_x), max(naoh_x)])
# plt.ylim([min(naoh_y), max(naoh_y)])
# # create axis labels
# plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
# plt.show()
