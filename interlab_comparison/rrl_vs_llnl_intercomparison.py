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
import numpy as np
import seaborn as sns
from my_functions import basic_analysis

plt.rcParams['font.size'] = 14

# read in the data from the spreadsheets
llnl = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist'
                     r'\The Science\Datasets\LLNL_NWT3and4.xlsx',
                     sheet_name='NWT3.tab_clean')
rrl = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist'
                    r'\The Science\Datasets\NWT_FARI_RRL_2022-02-15.xlsx')

# immediately slice off the following values, Jocelyn deemed them not good, see excel sheet
rrl = rrl.iloc[0:202]

# clean up the NaN's, clean names, drop columns, making sure to keep the values I care about
llnl = llnl.dropna(subset=['D14C'])
llnl = llnl.rename(columns={'Unnamed: 0': 'standard_type'})
llnl = llnl.rename(columns={'D14C Err': 'D14C_err'})
rrl = rrl.dropna(subset=['AMS Submission Results Complete::DELTA14C'])
rrl = rrl.rename(columns={'Samples::Sample ID': 'standard_type'})
rrl = rrl.rename(columns={'AMS Submission Results Complete::Date Run': 'Date'})

# locate the data I'm after and create new datasets for it
nwt3_llnl = llnl.loc[(llnl['standard_type'] == "NWT3") & (llnl['AMS 13C'] > -8.1)]  # new dataset with only NWT4 values from LLNL, corrected for AMS 13C
# only grabbing specific NWT4 Standards, see email thread with Jocelyn in March 8, 2022
nwt4_llnl = llnl.loc[(llnl['standard_type'] == "NWT4") & (llnl['AMS 13C'] == -10.43)]  # new dataset with only NWT4 values from LLNL, corrected for AMS 13C

nwt3_rrl = rrl.loc[rrl['standard_type'] == "NWT3"]  # new dataset with only NWT3 values from rrl
nwt4_rrl = rrl.loc[rrl['standard_type'] == "NWT4"]  # new dataset with only NWT4 values from rrl

# extract the variables I'm interested in
y1 = nwt3_llnl['D14C']
y2 = nwt4_llnl['D14C']
y1_err = nwt3_llnl['D14C_err']
y2_err = nwt4_llnl['D14C_err']
y3 = nwt3_rrl['AMS Submission Results Complete::DELTA14C']
y4 = nwt4_rrl['AMS Submission Results Complete::DELTA14C']
y3_err = nwt3_rrl['AMS Submission Results Complete::DELTA14C_Error']
y4_err = nwt4_rrl['AMS Submission Results Complete::DELTA14C_Error']
date = nwt3_llnl['WHEEL']
date2 = nwt4_llnl['WHEEL']
date3 = nwt3_rrl['Date']
date4 = nwt4_rrl['Date']

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

# organize the plots
# # https://seaborn.pydata.org/tutorial/color_palettes.html
# colors = sns.color_palette("rocket", 4)
# seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']
#
# # changing the x-axis so I can plot them on top of each other more simply (LLNL data only comes in wheel #)
# date_change = list(range(0, len(y1)))
# date_change2 = list(range(0, len(y2)))
# date_change3 = list(range(0, len(y3)))
# date_change4 = list(range(0, len(y4)))
#
# fig = plt.figure(1)
# plt.errorbar(date_change, y1, yerr=y1_err, fmt='X', color=colors[0], ecolor='black', elinewidth=1, capsize=2,
#              label='LLNL NWT3')
# plt.errorbar(date_change2, y2, yerr=y2_err, fmt='X', color=colors[1], ecolor='black', elinewidth=1, capsize=2,
#              label='LLNL NWT4')
# plt.errorbar(date_change3, y3, yerr=y3_err, fmt='o', color=colors[2], ecolor='black', elinewidth=1, capsize=2,
#              label='RRL NWT3')
# plt.errorbar(date_change4, y4, yerr=y4_err, fmt='o', color=colors[3], ecolor='black', elinewidth=1, capsize=2,
#              label='RRL NWT4')
# plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
# plt.legend()
# plt.xlabel('Available Meas # - See note in code', fontsize=14)
# plt.ylabel('Del14CO2', fontsize=14)  # label the y axis
