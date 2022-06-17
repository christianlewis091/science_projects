"""
Purpose:

Harmonize the offset-corrected Cape Grim data with the Baring Head data.

"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5
"""

Because I’ll need a harmonized dataset as a reference to understand the
tree-rings, I’m going to create a python file to do dataset harmonization.
I know we may change the corrections for the later half of the available
data; however, I can at least get the code ready so we can quickly
run it later and get the answer.

"""

capegrim = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\CapeGrim_offset.xlsx')
neumayer = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\Neumayer_offset.xlsx')
mcq      = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\MCQ_offset.xlsx')

baringhead = pd.read_excel(r'H:\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')
baringhead = baringhead.dropna(subset=['DELTA14C'])
# snip out 1995 - 2005, and 2009 - 2012 from Baring Head Record
snip = baringhead.loc[(baringhead['DEC_DECAY_CORR'] < 1994)]
snip2 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2006) & (baringhead['DEC_DECAY_CORR'] < 2009)]
snip3 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2012)]
snip = pd.merge(snip, snip2, how='outer')
snip = pd.merge(snip, snip3, how='outer')
baringhead = snip.reset_index(drop=True)
baringhead = baringhead.drop(columns=['SITE', 'NZPREFIX', 'NZ', 'DATE_ST', 'DATE_END', 'DAYS_EXP',
                                      'DATE_COLL', 'date_as_number', 'DELTA13C_IRMS',
                                      'FLAG', 'METH_VESSEL',
                                      'METH_COLL'])
baringhead = baringhead.rename(columns={"DEC_DECAY_CORR": "Decimal_date"})
baringhead = baringhead.rename(columns={"DELTA14C": "D14C"})
baringhead = baringhead.rename(columns={"DELTA14C_ERR": "D14C_err"})
baringhead = baringhead.rename(columns={"F14C_ERR": "F14C_err"})
capegrim['key'] = np.ones(len(capegrim))
baringhead['key'] = np.zeros(len(baringhead))

"""Add FM values to Cape Grim by back-calculating"""
# I realized that I was missing FM from the Heidelberg dataset, so I'm going to add that here...
# age_corr = exp((1950 - sample year)/8267)
# D14C = 1000*(FM-1)
# Del14C = 1000*(FM*age_corr-1)
capegrim['D14C_offsetcorrected'] = capegrim['D14C_1']
capegrim['D14C_offsetcorrected_err'] = capegrim['D14C_1_err']
baringhead['D14C_offsetcorrected'] = baringhead['D14C']
baringhead['D14C_offsetcorrected_err'] = baringhead['D14C_err']

x = capegrim['Decimal_date']
y = capegrim['D14C_offsetcorrected_err']                  # make sure to use the correct / offset corrected data for this!
age_corr = np.exp((1950 - x) / 8267)
fm = ((y / 1000) + 1) / age_corr
fm_err = capegrim['D14C_1_err'] / 1000
x = np.float_(x)                                         # in order to create dictionary, first change briefly to array
fm = np.float_(fm)
new_frame = pd.DataFrame({"Decimal_date": x, "F14C": fm, "F14C_err": fm_err})  # create dictionary with common column to merge on.

capegrim = pd.merge(capegrim, new_frame, how = 'outer')  # merge the dataframes.

harmonized = pd.merge(baringhead, capegrim, how='outer')  # have to merge in stages but it's all good.
harmonized.sort_values(by=['Decimal_date'], inplace=True)
harmonized = harmonized[['key','Decimal_date', 'D14C_offsetcorrected', 'D14C_offsetcorrected_err', 'F14C','F14C_err']]
harmonized = harmonized.reset_index(drop=True)
harmonized.to_excel('harmonized_dataset.xlsx')

"""
In Rachel's thesis, she talks about comparing the tree-ring values to the BHD data, but only using the data from the
growing season, which is November to February. The following code slices the harmonized data to ONLY INCLUDE data from
during the growing season. While this code took ~ 1 hour to write, I don't know how to get from here to a yearly
average because the SH summer crosses the year-line (January). Can come back to this later.
The following code retains only the summer months.
"""

L = np.linspace(0, 1, 365)
# add the number that is 1/2 of the previous month plus the current month
Jan = 31 / 365
Feb = ((28 / 2) + 31) / 365
Mar = ((31 / 2) + 31 + 28) / 365
Apr = ((30 / 2) + 31 + 28 + 31)/ 365
May = ((31 / 2) + 31 + 28 + 31 + 30)/ 365
June = ((30 / 2) + 31 + 28 + 31 + 30 + 31)/ 365
July = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30)/ 365
August = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31)/ 365
Sep = ((30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31)/ 365
Oct = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30)/ 365
Nov = ((30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30)/ 365
Dec = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30 + 30)/ 365
# print(Nov)
# print(Dec)
# print(Jan)
# print(Feb)
# harmonized['Summer_index'] = harmonized['Decimal_date']  # makes a copy of the DecimalDate column
mt_array = []                                    # initialize an empty array to dump sliced date-data
harmonized = harmonized.reset_index(drop=True)   # re-index the harmonized dataset to avoid confusion
for i in range(0, len(harmonized)):
    row = harmonized.iloc[i]                     # grab i'th row
    element = row['Decimal_date']                # extract the date
    element = str(element)                       # convert to a string so it is indexable
    element = element[4:9:1]                     # index the decimal portion
    element = np.float_(element)                 # convert back to float for indexing a few lines later
    mt_array.append(element)                     # append to the new array
indexed = pd.DataFrame({"decimals": mt_array, "Decimal_date": harmonized['Decimal_date']})                 # put the array into a DataFrame format

harmonized_summer = pd.merge(harmonized, indexed)   # merge the datasets

# print(harmonized_summer)
harmonized_summer = harmonized_summer.loc[((harmonized_summer['decimals']) < .124) | ((harmonized_summer['decimals']) > .870)]   # grab data only in the months that I want
harmonized_summer.to_excel('harmonized_summer.xlsx')
# print(harmonized.columns)
# print(harmonized_summer.columns)
# test the dates fall into the bounds that I want using a histogram
x = harmonized_summer['decimals']
plt.hist(x, bins=12)
# plt.show()
#
plt.close()
# plt.scatter(harmonized['Decimal_date'], harmonized['F14C'])
# plt.show()




















































"""
What is the difference between these two offset types? 
"""
# heidelberg_ds = heidelberg.iloc[::10, :]  # downsample every 10th point
# # plt.errorbar(heidelberg_ds['Decimal_date'], heidelberg_ds['smoothed_offset'], label='Trended Offset, mean of "n" error simulations', yerr=heidelberg_ds['smoothed_offset_error'], fmt='o', color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2)
# # plt.errorbar(heidelberg_ds['Decimal_date'], heidelberg_ds['pre-postAMS_offset'], label='Fixed Pre and Post XCAMS Offset', yerr=heidelberg_ds['pre-postAMS_offset_err'], fmt='o', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
# plt.scatter(heidelberg['Decimal_date'], heidelberg['smoothed_offset'], marker='o', label='Trended Offset, mean of "n" error simulations', color=colors[3], s=size1, alpha = 0.5)
# plt.scatter(heidelberg['Decimal_date'], heidelberg['pre-postAMS_offset'], marker='o', label='Fixed Pre and Post XCAMS Offset', color=colors2[3], s=size1, alpha = 0.5)
# plt.legend()
# # plt.title('All available data after 1980')
# # plt.xlim([1980, 2020])
# plt.ylim([-1, 2.5])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('Applied offset to Uni Heidelberg Data (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Two_offset_types2.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
# plt.errorbar(heidelberg['Decimal_date'], heidelberg['D14C_2'], label='Trended Offset, mean of "n" error simulations', yerr=heidelberg['weightedstderr_D14C_2'], fmt='o', color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2, alpha = 0.3)
# plt.errorbar(heidelberg['Decimal_date'], heidelberg['D14C_1'], label='Fixed Pre and Post XCAMS Offset', yerr=heidelberg['weightedstderr_D14C_1'], fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2, alpha=0.3)
# plt.legend()
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Two_offset_types3.png',
#             dpi=300, bbox_inches="tight")
# plt.close()


# """ STEP 4: MERGE OFFSET CORRECTED CAPE GRIM DATA WITH BARING HEAD RECORD TO MAKE HARMONIZED BACKGROUND """
# for simplicity (and because I'm indexing the Heidelberg dataset much
# more than the Baring Head dataset right now, I'm going to change the
# baringhead column names to match those of the Heidelberg dataset
# print(baringhead.columns)
# # print(h1.columns)
# df2_dates = df2_dates.rename(columns={"NZ/NZA": "NZ"})
# baringhead = baringhead.rename(columns={"DEC_DECAY_CORR": "Decimal_date"})
# baringhead = baringhead.rename(columns={"DELTA14C": "D14C"})
# baringhead = baringhead.rename(columns={"DELTA14C_ERR": "D14C_err"})
#
# harmonized = pd.merge(baringhead, heidelberg, how='outer')  # have to merge in stages but it's all good.

"""
A few of the data have errors of -1000 and this is throwing everything off
in later calculations...
I need to get rid of these...
"""
# harmonized = harmonized.loc[(harmonized['weightedstderr_D14C'] > 0)]
# harmonized = harmonized.drop(columns=['index'], axis=1)
# harmonized = harmonized.dropna()
# harmonized.sort_values(by=['Decimal_date'], inplace=True)
# # harmonized.to_excel('harmonized_dataset.xlsx')
# harm1 = harmonized.loc[(harmonized['key'] == 0)]
# harm2 = harmonized.loc[(harmonized['key'] == 1)]
# x_bars = harm1['Decimal_date']
# y_bars = harm1['D14C']
# x_heids = harm2['Decimal_date']
# y_heids = harm2['D14C']
# colors = sns.color_palette("rocket", 6)
# colors2 = sns.color_palette("mako", 6)
# mpl.rcParams['pdf.fonttype'] = 42
# mpl.rcParams['font.size'] = 10
# size1 = 5

# """
# Figure 1. All the data together
# """
# fig = plt.figure(1)
# plt.scatter(x_bars, y_bars, marker='o', label='Data from Baring Head (RRL)', color=colors[3], s=size1, alpha = 0.5)
# plt.scatter(x_heids, y_heids, marker='o', label='Data from CGO (Heidelberg)', color=colors2[3], s=size1, alpha = 0.5)
# plt.legend()
# # plt.title('All available data after 1980')
# # plt.xlim([1980, 2020])
# # plt.ylim([0, 300])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Harmonized_dataset.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# In Rachel's thesis, she talks about comparing the tree-ring values to the BHD data, but only using the data from the
# growing season, which is November to February. The following code slices the harmonized data to ONLY INCLUDE data from
# during the growing season. While this code took ~ 1 hour to write, I don't know how to get from here to a yearly
# average because the SH summer crosses the year-line (January). Can come back to this later.
# The following code retains only the summer months.
# """
#
# L = np.linspace(0, 1, 365)
# # add the number that is 1/2 of the previous month plus the current month
# Jan = 31 / 365
# Feb = ((28 / 2) + 31) / 365
# Mar = ((31 / 2) + 31 + 28) / 365
# Apr = ((30 / 2) + 31 + 28 + 31)/ 365
# May = ((31 / 2) + 31 + 28 + 31 + 30)/ 365
# June = ((30 / 2) + 31 + 28 + 31 + 30 + 31)/ 365
# July = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30)/ 365
# August = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31)/ 365
# Sep = ((30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31)/ 365
# Oct = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30)/ 365
# Nov = ((30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30)/ 365
# Dec = ((31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30 + 30)/ 365
# # print(Nov)
# # print(Dec)
# # print(Jan)
# # print(Feb)
# # harmonized['Summer_index'] = harmonized['Decimal_date']  # makes a copy of the DecimalDate column
# mt_array = []                                    # initialize an empty array to dump sliced date-data
# harmonized = harmonized.reset_index(drop=True)   # re-index the harmonized dataset to avoid confusion
# for i in range(0, len(harmonized)):
#     row = harmonized.iloc[i]                     # grab i'th row
#     element = row['Decimal_date']                # extract the date
#     element = str(element)                       # convert to a string so it is indexable
#     element = element[4:9:1]                     # index the decimal portion
#     element = np.float_(element)                 # convert back to float for indexing a few lines later
#     mt_array.append(element)                     # append to the new array
# indexed = pd.DataFrame({"decimals": mt_array, "Decimal_date": harmonized['Decimal_date']})                 # put the array into a DataFrame format
#
# harmonized_summer = pd.merge(harmonized, indexed)   # merge the datasets
#
# # print(harmonized_summer)
# harmonized_summer = harmonized_summer.loc[((harmonized_summer['decimals']) < .124) | ((harmonized_summer['decimals']) > .870)]   # grab data only in the months that I want
# # harmonized_summer.to_excel('test.xlsx')
# # print(harmonized.columns)
# # print(harmonized_summer.columns)
# # test the dates fall into the bounds that I want using a histogram
# x = harmonized_summer['decimals']
# plt.hist(x, bins=12)
# # plt.show()
# #
# plt.close()
# # plt.scatter(harmonized['Decimal_date'], harmonized['F14C'])
# # plt.show()
#
