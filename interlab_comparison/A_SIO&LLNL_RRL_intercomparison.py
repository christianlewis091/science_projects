"""
Purpose:


In this code, I will be doing an inter-comparison of the AMS system / 14C
results from LLNL and RRL. This will be done using data that Jocelyn sent to me on Feb. 14, 2022.
This is part of the larger radiocarbon inter-comparison work that
is required to create a harmonized Southern Hemisphere radiocarbon dataset.


Outcome:
This analysis got quite confusing. In the end,
some of the original 13C data I was using was not properly corrected for fractionation.
After using the correct data, I was able to perfectly reproduce the result for RRL / LLNL / SIO offset
that is found in Rachel's thesis.

To follow the record of these analyses, see The Science/Papers/Heidelberg_Intercomparison/Skeleton First Draft
and then bullet point "SIO / LLNL: OFFSET APPLIED". read this, and then find the power point description
in the file The Science/Current Projects/Lab Intercomparison Data/Radiocarbon Intercomparison Project Figures

In the end, we are going to leave this data out anyway beacuse it is too funny, and we have an entire filled record
using the Heidelberg and RRL data anyway
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns
from X_my_functions import basic_analysis, long_date_to_decimal_date
import matplotlib.gridspec as gridspec
from scipy import stats

# general plot parameters


# read in the data from the spreadsheets
# llnl = pd.read_excel(r'H:\The Science\Datasets\LLNL_NWT3and4.xlsx',
#                      sheet_name='NWT3.tab_clean')
llnl = pd.read_excel(r'H:\The Science\Datasets\LLNLwheelcomparisons.xlsx',
                     sheet_name='Data', skiprows=24)
rrl = pd.read_excel(r'H:\The Science\Datasets\NWT_FARI_RRL_2022-02-15.xlsx')
rrl = rrl.dropna(subset=['AMS Submission Results Complete::DELTA14C'])

# immediately slice off the following values from RRL data, Jocelyn deemed them not good, see excel sheet
rrl = rrl.iloc[0:202]
rrl = rrl.reset_index(drop=True)
rrl_date = rrl['AMS Submission Results Complete::Date Run']  # extract x-values from heidelberg dataset
rrl_date = long_date_to_decimal_date(rrl_date)  # convert the x-values to a decimal date
rrl['Decimal_date'] = rrl_date  # add these decimal dates onto the dataframe
# locate the data I'm after
rrl = rrl.rename(columns={'Samples::Sample ID': 'standard_type'})
nwt3_rrl = rrl.loc[(rrl['standard_type'] == "NWT3")]   # new dataset with only NWT3 values from rrl
nwt4_rrl = rrl.loc[(rrl['standard_type'] == "NWT4")]  # new dataset with only NWT4 values from rrl
nwt3_llnl = llnl.loc[(llnl['Comment'] == "NWT3")]
nwt4_llnl = llnl.loc[(llnl['Comment'] == "NWT4")]

# # extract the variables I'm interested in
y1 = nwt3_llnl['D14C']
y1_average = np.average(y1)
y1_1sigma = np.std(y1)

y2 = nwt4_llnl['D14C']
y2_average = np.average(y2)
y2_1sigma = np.std(y2)

y1_err = nwt3_llnl['D14C_Err']
y2_err = nwt4_llnl['D14C_Err']
y3 = nwt3_rrl['AMS Submission Results Complete::DELTA14C']
y3_average = np.average(y3)
y3_1sigma = np.std(y3)

y4 = nwt4_rrl['AMS Submission Results Complete::DELTA14C']
y4_average = np.average(y4)
y4_1sigma = np.std(y4)

y3_err = nwt3_rrl['AMS Submission Results Complete::DELTA14C_Error']
y4_err = nwt4_rrl['AMS Submission Results Complete::DELTA14C_Error']
date = nwt3_llnl['Wheel']
date2 = nwt4_llnl['Wheel']
date3 = nwt3_rrl['AMS Submission Results Complete::Date Run']
date4 = nwt4_rrl['AMS Submission Results Complete::Date Run']

X = stats.ttest_ind(y1, y3)
print(X)

X = stats.ttest_ind(y2, y4)
print(X)


nwt3= basic_analysis(y1, y3, 'LLNL', 'RRL')
print(nwt3)
nwt4 = basic_analysis(y2, y4, 'LLNL', 'RRL')
print(nwt4)
print()
NWT3_offset = (nwt3.iloc[0, 1]) - (nwt3.iloc[1, 1])  # row then column
NWT3_offset_error = np.sqrt( (nwt3.iloc[0, 2]) ** 2 - (nwt3.iloc[1, 2]) ** 2)
print('The final offset for NWT3 is: LLNL is ' + str(NWT3_offset) + ' \u00B1 ' + str(NWT3_offset_error) + ' offset from RRL')
print()
NWT4_offset = (nwt4.iloc[0, 1]) - (nwt4.iloc[1, 1])  # row then column
NWT4_offset_error = np.sqrt( (nwt4.iloc[0, 2]) ** 2 - (nwt3.iloc[1, 2]) ** 2)
print('The final offset for NWT4 is: LLNL is ' + str(NWT4_offset) + ' \u00B1 ' + str(NWT4_offset_error) + ' offset from RRL')
print()
average = (NWT3_offset + NWT4_offset) / 2
error = np.sqrt ( (NWT3_offset_error ** 2) + (NWT4_offset_error) ** 2)
print('The OFFSET FOR LLNL is ' + str(average) + ' \u00B1 ' + str(error) + ' , which is an average of NWT3 and NWT4 offsets')

# plot the data
#
# organize the plots
# https://seaborn.pydata.org/tutorial/color_palettes.html
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']

# changing the x-axis so I can plot them on top of each other more simply (LLNL data only comes in wheel #)
date_change = list(range(0, len(y1)))
date_change2 = list(range(0, len(y2)))
date_change3 = list(range(0, len(y3)))
date_change4 = list(range(0, len(y4)))
#
# fig = plt.figure(1)
# plt.errorbar(date_change, y1, yerr=y1_err, fmt='X', color=colors[3], ecolor='black', elinewidth=1, capsize=2, label='LLNL NWT3')
# plt.errorbar(date_change2, y2, yerr=y2_err, fmt='X', color=colors[4], ecolor='black', elinewidth=1, capsize=2, label='LLNL NWT4')
# plt.errorbar(date_change3, y3, yerr=y3_err, fmt='o', color=colors2[3], ecolor='black', elinewidth=1, capsize=2, label='RRL NWT3')
# plt.errorbar(date_change4, y4, yerr=y4_err, fmt='o', color=colors2[4], ecolor='black', elinewidth=1, capsize=2, label='RRL NWT4')
# plt.legend()  # add the legend (will default to 'best' location)
#
# plt.xlabel('Available Meas # - See note in code', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.show()

# fig = plt.figure(1)
# plt.errorbar(nwt3_rrl['Decimal_date'], y3, yerr=y3_err, fmt='o', color=colors2[3], ecolor='black', elinewidth=1, capsize=2, label='RRL NWT3')
# plt.errorbar(nwt4_rrl['Decimal_date'], y4, yerr=y4_err, fmt='o', color=colors2[4], ecolor='black', elinewidth=1, capsize=2, label='RRL NWT4')
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.show()


fig = plt.figure(4, figsize=(16.1, 10))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=.5, hspace=.5)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.errorbar(nwt3_rrl['Decimal_date'], y3, yerr=y3_err, fmt='o', color=colors2[3], ecolor='black', elinewidth=1, capsize=2, label='RRL NWT3')
plt.axhline(y=y3_average, color='black', linestyle='-')
plt.axhspan((y3_average-y3_1sigma), (y3_average+y3_1sigma), facecolor=colors2[4], alpha=0.3)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.xlabel('Date of Measurement', fontsize=14)  # label the y axis
plt.legend()

plt.ylim(30,55)

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.errorbar(nwt4_rrl['Decimal_date'], y4, yerr=y4_err, fmt='o', color=colors2[4], ecolor='black', elinewidth=1, capsize=2, label='RRL NWT4')
plt.axhline(y=y4_average, color='black', linestyle='-')
plt.axhspan((y4_average-y4_1sigma), (y4_average+y4_1sigma), facecolor=colors2[5], alpha=0.3)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.legend()
plt.ylim(-40,-24)
plt.xlabel('Date of Measurement', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.ylim(30,55)
# plt.axhline(y=y3_average, color='black', linestyle='-')
# plt.axhspan((y3_average-y3_1sigma), (y3_average+y3_1sigma), facecolor=colors2[4], alpha=0.3)
plt.errorbar(date_change, y1, yerr=y1_err, fmt='X', color=colors[3], ecolor='black', elinewidth=1, capsize=2, label='LLNL NWT3')
plt.axhline(y=y1_average, color='black', linestyle='--')
plt.axhspan((y1_average-y1_1sigma), (y1_average+y1_1sigma), facecolor=colors[4], alpha=0.3)
plt.xlabel('Measurement #', fontsize=14)  # label the y axis
plt.legend()


xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
plt.ylim(-40,-24)
# plt.axhline(y=y4_average, color='black', linestyle='-')
# plt.axhspan((y4_average-y4_1sigma), (y4_average+y4_1sigma), facecolor=colors2[5], alpha=0.3)
plt.errorbar(date_change2, y2, yerr=y2_err, fmt='X', color=colors[4], ecolor='black', elinewidth=1, capsize=2, label='LLNL NWT4')
plt.axhline(y=y2_average, color='black', linestyle='--')
plt.axhspan((y2_average-y2_1sigma), (y2_average+y2_1sigma), facecolor=colors[4], alpha=0.3)
plt.xlabel('Measurement #', fontsize=14)  # label the y axis
plt.legend()

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/reading_group_pres/SIOLLNLvRRL.png',
            dpi=300, bbox_inches="tight")
plt.close()