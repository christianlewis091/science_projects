import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
from dataset_harmonization import harmonized
from miller_curve_algorithm import ccgFilter
from heidelberg_intercomparison import monte_carlo_randomization_Trend
from heidelberg_intercomparison import monte_carlo_randomization_Smooth
"""
#######################################################################
#######################################################################
#######################################################################
#######################################################################
Import and tidy the data
#######################################################################
#######################################################################
#######################################################################
#######################################################################
"""

"""Omitted lines re-create the SOAR excel file without missing 14C values (there were a lot)"""
# df = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
#                    r'\SOARTreeRingData2022-02-01.xlsx')
# df = df.dropna(subset = '∆14C').reset_index()
# df.to_excel('adjusted_SOAR.xlsx')

# importing baring head record for background visual reference
baringhead = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')
df = pd.read_excel(r'C:\Users\lewis\venv\python310'
                   r'\python-masterclass-remaster-shared'
                   r'\radiocarbon_intercomparison2\interlab_comparison'
                   r'\adjusted_SOAR.xlsx')





























df.sort_values(by=['DecimalDate'], inplace=True)

# The following line of code removes items before 1954 beacuse, for an unknown reason,
# the CCGCRV (ccgFilter Trend) ouput in a few lines returned NaN for those years, and it threw
# off the rest of the code/ plotting. Need to figure this outn in the future but need to move on at the moment.
# df = df.loc[(df['DecimalDate'] > 1955)]


df['Lon'] = df['Lon'].fillna(-999)  # fill all missing values with -999
df['Lat'] = df['Lat'].fillna(-999)  # fill all missing values with -999
df.drop(df[df['C14Flag'] == -999].index, inplace=True)

# baringhead = baringhead.iloc[::5, :]  # if I want to downsample the data
xtot_bhd = baringhead['DEC_DECAY_CORR']             # entire dataset x-values
ytot_bhd = baringhead['DELTA14C']                   # entire dataset y-values

""" First order of tidying, adjust the Western Hemisphere longitude values (should be negative) """
# From POKEMON.PY file
# df.loc[(df['Type 1'] == 'Grass') | (df['Type 2'] == 'Poison')] # filtering based on two types of data OR
nz = df.loc[(df['Lon'] > 100) | (df['Lon'] == -999)].reset_index()  # split up the data
chile = df.loc[(df['Lon'] < 100) & (df['Lon'] > 0)].reset_index()  # split up the data
chile['new_lon'] = np.multiply(chile['Lon'], -1)  # address the bad longitude
nz['new_lon'] = nz['Lon']  # need this new column to be the same for concatenation

frames = [chile, nz]  # TODO: figure out: why I need to put these two DataFrames into an array before concat
df = pd.concat(frames)  # put the data back together
# df.to_excel('adjusted_SOAR2.xlsx')

"""
MAIN STEPS FROM HERE: 

1. I'm going to use the HARMONIZED DATASET (harm_xs, harm_ys) to create a smoothed trend, and extract y-values (output_ys) specific x-values that correspond 
to my SAMPLE DATA (sample_xs, sample_ys). 

2. Need to do a monte carlo to get error estimates on the smoothed trend in step 1. 

3. I'm going to write all the data to an excel file: sample_xs (sample_xs = output_xs), output_ys, sample_ys, sample_y_errs. 
 
4. Calcualte the offset between sample_ys and output_ys. 

5. Propagate the errors from the offset calculation. 


SIDE "QUEST" 

1. Is our Monte Tarn data the same as De Pol Holz Monte Tarn data? 

"""

""" EXECUTING STEP 1"""

harm_xs = harmonized['Decimal_date']  # see dataset_harmonization.py
harm_ys = harmonized['D14C']  # see dataset_harmonization.py
harm_y_errs = harmonized['weightedstderr_D14C']
sample_xs = (df['DecimalDate'])
sample_ys = (df['∆14C'])
sample_y_err = (df['∆14Cerr'])

# to appease the code, I have to adjust the format of the sample x's.
# the original monte carlo code had to extract a column ['x'] from a dataframe
# and its bugging because it doesn't see that here. So I'll just create one versus
# changing the function and risking ruining the other code.
sample_xs2 = pd.DataFrame({'x': sample_xs})
cutoff = 667
n = 10  # TODO change back to 10,000
# input is: 1) x data, 2) y data that you want smoothed, then, 3) x-values at which you want y's output
harmonized_trend = ccgFilter(harm_xs, harm_ys, cutoff).getTrendValue(sample_xs2)
print(harmonized_trend)
# TODO This line of code above causes some NaN's in the output, and I really don't know why.



# testingNans = pd.DataFrame({'sample_xs': sample_xs,
#                            'harmonized_trend': harmonized_trend})
# testingNans.to_excel('testingNaNs.xlsx')
# # print(harmonized_trend)
# # NANs appear between 1948 and 1954, for unknown reasons.
#
# smooth_trend = ccgFilter(harm_xs, harm_ys, cutoff).getSmoothValue(sample_xs2)
#
# """ EXECUTE STEP 2 """
# # def monte_carlo_randomization_Smooth(x_init, fake_x, y_init, y_error, cutoff, n):
# # errors = monte_carlo_randomization_Trend(harm_xs, sample_xs2, harm_ys, sample_y_err, cutoff, n)
# errors = monte_carlo_randomization_Trend(harm_xs, sample_xs2, harm_ys, harm_y_errs, cutoff, n)
# errors_fin = errors[2]  # extract the summary dataframe
# errors_fin = errors_fin['stdevs']
#
# errors2 = monte_carlo_randomization_Smooth(harm_xs, sample_xs2, harm_ys, harm_y_errs, cutoff, n)
# errors_fin2 = errors2[2]  # extract the summary dataframe
# errors_fin2 = errors_fin2['stdevs']
#
#
# """ EXECUTING STEP 3: Append a few final items to DataFrame that already includes all the data. """
#
# df['CCGCRV_Trend_D14C'] = harmonized_trend
# df['CCGCRV_Trend_D14C_errors'] = errors_fin
# df['CCGCRV_Smooth_D14C'] = smooth_trend
# df['CCGCRV_Smooth_D14C_errors'] = errors_fin2
# df.sort_values(by=['DecimalDate'], inplace=True)
# df.to_excel('Tree_Ring_Analysis_Part1.xlsx')
#
# """
# It may seem strange at first that the data is so evenly spaced in time  but remember these are TREE RINGS, and each one
# corresponds to 1 year. Hence the even spacing in plot below (have to remind myself).
#
# Why the large errors in 1984- 1986?
# """
print(np.amax(sample_xs, axis=0))
print(np.amax(sample_xs2, axis=0))
# print(np.amax(harmonized_trend, axis=0))
# print(np.amax(sample_ys, axis=0))
# Harmonized Trend has an NaN value.
# # TODO Why do I get an error when running this plot?
# plt.errorbar(sample_xs, harmonized_trend, label='Error of Harmonized Data, including Tree Ring x-values' , yerr=errors_fin, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.15)
# plt.errorbar(sample_xs, sample_ys, label = 'Tree Ring Samples and Errors', yerr = sample_y_err, fmt='x', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.15)
# plt.scatter(sample_xs, harmonized_trend)
# plt.legend()
# plt.xlabel('Year of Growth', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# # plt.xlim([1983, 1995])
# # plt.ylim([70, 270])
# # plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
# #             'radiocarbon_intercomparison2/interlab_comparison/plots/harmonized_background_werrors_wTreeRings_x_vals.png',
# #             dpi=300, bbox_inches="tight")
# plt.show()
# plt.close()


































# # to input below(x_init, fake_x, y_init, y_error, cutoff, n):
# # x_init and y_init come from the harmonized dataset, while the "fake_x" is where
# # I select what x-output values are, and this is my sample x's!!!!
# # print(np.shape(harmonized['weightedstderr_D14C']))
# # print(harmonized['weightedstderr_D14C'])

#

# """
# #######################################################################
# #######################################################################
# #######################################################################
# #######################################################################
# INDEX THE DATA BY SITE, LATITUDE, quick check on Monte Tarn data
# #######################################################################
# #######################################################################
# #######################################################################
# #######################################################################
#
# I want to, in as simplest lines as possible, index the DataFrame according
# to every unique site-name (so I can plot each one individually). I could do
# this in as many lines as there are sites; but I want to try this.
# On second thought, it's likely simpler to just write it out...
#
# ['19 Nikau St, Eastbourne, NZ' '23 Nikau St, Eastbourne, NZ'
#  'Bahia San Pedro, Chile' 'Baja Rosales, Isla Navarino' 'Baring Head, NZ'
#  'Haast Beach, paddock near beach' "Mason's Bay Homestead"
#  'Monte Tarn, Punta Arenas' 'Muriwai Beach Surf Club' 'Oreti Beach'
#  'Puerto Navarino, Isla Navarino' 'Raul Marin Balmaceda' 'Seno Skyring'
#  'Tortel island' 'Tortel river'
#  "World's Loneliest Tree, Camp Cove, Campbell island"
#  'near Kapuni school field, NZ']
#
# """
# # names = np.unique(df['StudySites::Site name'])
# # print(names)
# eastbourne1 = df.loc[(df['Site'] == '19 Nikau St, Eastbourne, NZ')]
# eastbourne2 = df.loc[(df['Site'] == '23 Nikau St, Eastbourne, NZ')]
# san_pedro = df.loc[(df['Site'] == 'Bahia San Pedro, Chile')]
# navarino1 = df.loc[(df['Site'] == 'Baja Rosales, Isla Navarino')]
# bhd = df.loc[(df['Site'] == 'Baring Head, NZ')]
# haast_paddock = df.loc[(df['Site'] == 'Haast Beach, paddock near beach')]
# mason_bay = df.loc[(df['Site'] == "Mason's Bay Homestead")]
# monte_tarn = df.loc[(df['Site'] == 'Monte Tarn, Punta Arenas')]
# muriwai_beach = df.loc[(df['Site'] == 'Muriwai Beach Surf Club')]
# oreti_beach = df.loc[(df['Site'] == 'Oreti Beach')]
# navarino2 = df.loc[(df['Site'] == 'Puerto Navarino, Isla Navarino')]
# balmaceda = df.loc[(df['Site'] == 'Raul Marin Balmaceda')]
# seno = df.loc[(df['Site'] == 'Seno Skyring')]
# tortel_island = df.loc[(df['Site'] == 'Tortel island')]
# tortel_river = df.loc[(df['Site'] == 'Tortel river')]
# lonely_tree = df.loc[(df['Site'] == "World's Loneliest Tree, Camp Cove, Campbell island")]
# kapuni_field = df.loc[(df['Site'] == 'near Kapuni school field, NZ')]
#
# """
# Jocelyn sent me a separate data file from Chile with Monte Tarn data.
# Is it the same as the data that is already in the SOAR file?
#
# NO. THE DATA IS DIFFERENT. BUT CAN QUICKLY COMPARE THEM...
# There is some overlap in the data post 1980, but mostly the DePol Holz record
# exists post 1980, and the Baring Head dataset is in the early part of the bomb peak.
# See Figure below.
# """
#
# df2 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
#                     r'\Jocelyn Chile tree data 1980-2016(2).xlsx')
# monte_tarn_x = monte_tarn['DecimalDate']
# monte_tarn_y = monte_tarn['∆14C']
# df2_x = df2['Year of Growth']
# df2_y = df2['D14C']
#
# colors = sns.color_palette("rocket", 6)
# colors2 = sns.color_palette("mako", 6)
# size1 = 5
# fig = plt.figure(1)
# plt.plot(xtot_bhd, ytot_bhd, label='Baring Head Atmospheric CO2 Record', color='black', alpha = 0.15)
# plt.scatter(df2_x, df2_y, marker='o', label='De Pol Holz Tree Ring Data', color=colors2[3], s=20)
# plt.scatter(monte_tarn_x, monte_tarn_y, marker='o', label='SOAR Tree Ring Data', color=colors[3], s=20)
# plt.legend()
# plt.xlabel('Year of Growth', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison2/interlab_comparison/plots/chile_compare.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# ###############################################################################
# ###############################################################################
# ###############################################################################
# ###############################################################################
# ###############################################################################
# Compare Tree Rings with harmonized data:
# Use CCGCRV Trend to get Trend Values for Harmonized Dataset at the exact x-values
# we need to compare with our samples.
# THen, use Monte Carlo to get errors on those Harmonized Dataset values.
# Then, we can calculate offsets and propogate errors.
#
# ###############################################################################
# ###############################################################################
# ###############################################################################
# ###############################################################################
# """
# harm_xs = harmonized['Decimal_date']  # see dataset_harmonization.py
# harm_ys = harmonized['D14C']  # see dataset_harmonization.py
# sample_xs = (df['DecimalDate'])
# sample_ys = (df['∆14C'])
# # to appease the code, I have to adjust the format of the sample x's.
# # the original monte carlo code had to extract a column ['x'] from a dataframe
# # and its bugging because it doesn't see that here. So I'll just create one versus
# # changing the function and risking ruining the other code.
# fake_x = {'x': sample_xs}
# fake_x = pd.DataFrame(data=fake_x)
#
# cutoff = 667
# n = 10000
# # input is: 1) x data, 2) y data that you want smoothed, then, 3) x-values at which you want y's output
# harmonized_trend = ccgFilter(harmonized['Decimal_date'], harmonized['D14C'], cutoff).getTrendValue(sample_xs)
# # to input below(x_init, fake_x, y_init, y_error, cutoff, n):
# # x_init and y_init come from the harmonized dataset, while the "fake_x" is where
# # I select what x-output values are, and this is my sample x's!!!!
# # print(np.shape(harmonized['weightedstderr_D14C']))
# # print(harmonized['weightedstderr_D14C'])
# errors = monte_carlo_randomization_Trend(harm_xs, fake_x, harm_ys, harmonized['weightedstderr_D14C'], cutoff, n)
#
# # What does this function return?
# # summary = pd.DataFrame({"Means": mean_array,
# #                         "stdevs": stdev_array,
# #                         "error_upperbound": upper_array,
# #                         "error_lowerbound": lower_array,
# #                         "my_xs": fake_x_for_dataframe})
# #
# # return randomized_dataframe, smoothed_dataframe, summary
# harmonized_dataset_errors = errors[2]  # extract the summary dataframe
# harmonized_dataset_errors = harmonized_dataset_errors['stdevs']
# # print(harmonized_dataset_errors)
# """
# We can quickly see differences in a rough way by taking the offset between the output directly above,
# and the y-values from our samples...
# """
# offsets = sample_ys - harmonized_trend
# print(max(offsets))
# """
# But none of this means anything without some quality error propagation...
# Actually, I need to do a Monte Carlo analysis on this new CCGCRV in order to get
# error bars that I can use to propogate...
# """
#
# offset_error_prop = np.sqrt(df['∆14Cerr']**2) + (harmonized_dataset_errors**2) # error prop between the tree ring 14C error, and background error from MOnte Carlo
#
#
#
# # TODO There are some problems with the dataset, including really low offset values, and some extremely high errors (>1000, see index 2)
# # TODO See how error prop produces extremely large errors across the board, see my plot files
# #
# fig = plt.figure(2)
# plt.errorbar(sample_xs, offsets, label='Tree Rings offset from background' , yerr=offset_error_prop, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.15)
# # plt.scatter(sample_xs, offsets, label='Tree Rings Data offset from Harmonized Background', color='black', alpha = 0.15)
# plt.legend()
# plt.xlabel('Year of Growth', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# # plt.ylim([-50, 50])
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison2/interlab_comparison/plots/tree_ring_offsets_errorprop_10000.png',
#             dpi=300, bbox_inches="tight")
# # plt.show()
# plt.close()
#
# data = pd.DataFrame({"tree_ring_xs": sample_xs,
#                      "tree-ring14C": df['∆14C'],
#                      "tree-ring14C_errors": df['∆14Cerr'],
#                      "harmonized_14C": harmonized_trend,
#                      "harmonized_14C_errors": harmonized_dataset_errors,
#                      "offset": offsets,
#                      "offset_errors": offset_error_prop})
# data.to_excel('offset_10000.xlsx')
#
#
#
#

















# fig = plt.figure(2)
# plt.scatter(sample_xs, harmonized_trend, label='Baring Head Atmospheric CO2 Record', color='black', alpha = 0.15)
# plt.legend()
# plt.xlabel('Year of Growth', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# # plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
# #             'radiocarbon_intercomparison2/interlab_comparison/plots/harmonized_trended.png',
# #             dpi=300, bbox_inches="tight")
# plt.show()

# fig = plt.figure(2)
# plt.scatter(df['DecimalDate'], df['∆14C'], label='Whole SOAR Tree Ring Record', color='black', alpha = 0.15)
#
# plt.legend()
# plt.xlabel('Year of Growth', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# # plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
# #             'radiocarbon_intercomparison2/interlab_comparison/plots/chile_compare.png',
# #             dpi=300, bbox_inches="tight")
# plt.show()
# plt.close()