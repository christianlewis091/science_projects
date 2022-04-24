import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dataset_harmonization import harmonized
from miller_curve_algorithm import ccgFilter
from heidelberg_intercomparison import monte_carlo_randomization_Trend
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

""" 
I have run lines 8 - 15 and saved the file, while I import for future use on line 17
!!! This file subsequently had flags of -999 manually added for some values of Monte Tarn !!! 
"""
# df = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
#                    r'\SOARTreeRingData2022-02-01.xlsx')
# df = df.dropna(subset = '∆14C').reset_index()
# df['Lon'] = df['Lon'].fillna(-999)  # fill all missing values with -999
# df['Lat'] = df['Lat'].fillna(-999)  # fill all missing values with -999
# df.to_excel('SOAR_dropna_subset14C.xlsx')
# # print(np.shape(df))
# # print(df.columns)

df = pd.read_excel(r'C:\Users\lewis\venv\python310\python-masterclass-remaster-shared'
                   r'\radiocarbon_intercomparison2\data\SOAR_dropna_subset14C.xlsx')
print(df.columns)
# df = df.drop(['C14Flag'] == -999)
df.drop(df[df['C14Flag'] == -999].index, inplace=True)

# importing baring head record for background visual reference
baringhead = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')
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
result = pd.concat(frames)  # put the data back together


"""
#######################################################################
#######################################################################
#######################################################################
#######################################################################
INDEX THE DATA BY SITE, LATITUDE, quick check on Monte Tarn data
#######################################################################
#######################################################################
#######################################################################
#######################################################################

I want to, in as simplest lines as possible, index the DataFrame according
to every unique site-name (so I can plot each one individually). I could do
this in as many lines as there are sites; but I want to try this.
On second thought, it's likely simpler to just write it out...

['19 Nikau St, Eastbourne, NZ' '23 Nikau St, Eastbourne, NZ'
 'Bahia San Pedro, Chile' 'Baja Rosales, Isla Navarino' 'Baring Head, NZ'
 'Haast Beach, paddock near beach' "Mason's Bay Homestead"
 'Monte Tarn, Punta Arenas' 'Muriwai Beach Surf Club' 'Oreti Beach'
 'Puerto Navarino, Isla Navarino' 'Raul Marin Balmaceda' 'Seno Skyring'
 'Tortel island' 'Tortel river'
 "World's Loneliest Tree, Camp Cove, Campbell island"
 'near Kapuni school field, NZ']

"""
# names = np.unique(df['StudySites::Site name'])
# print(names)
eastbourne1 = df.loc[(df['Site'] == '19 Nikau St, Eastbourne, NZ')]
eastbourne2 = df.loc[(df['Site'] == '23 Nikau St, Eastbourne, NZ')]
san_pedro = df.loc[(df['Site'] == 'Bahia San Pedro, Chile')]
navarino1 = df.loc[(df['Site'] == 'Baja Rosales, Isla Navarino')]
bhd = df.loc[(df['Site'] == 'Baring Head, NZ')]
haast_paddock = df.loc[(df['Site'] == 'Haast Beach, paddock near beach')]
mason_bay = df.loc[(df['Site'] == "Mason's Bay Homestead")]
monte_tarn = df.loc[(df['Site'] == 'Monte Tarn, Punta Arenas')]
muriwai_beach = df.loc[(df['Site'] == 'Muriwai Beach Surf Club')]
oreti_beach = df.loc[(df['Site'] == 'Oreti Beach')]
navarino2 = df.loc[(df['Site'] == 'Puerto Navarino, Isla Navarino')]
balmaceda = df.loc[(df['Site'] == 'Raul Marin Balmaceda')]
seno = df.loc[(df['Site'] == 'Seno Skyring')]
tortel_island = df.loc[(df['Site'] == 'Tortel island')]
tortel_river = df.loc[(df['Site'] == 'Tortel river')]
lonely_tree = df.loc[(df['Site'] == "World's Loneliest Tree, Camp Cove, Campbell island")]
kapuni_field = df.loc[(df['Site'] == 'near Kapuni school field, NZ')]

"""
Jocelyn sent me a seperate data file from Chile with Monte Tarn data.
Is it the same as the data that is already in the SOAR file?

NO. THE DATA IS DIFFERENT. BUT CAN QUICKLY COMPARE THEM...
There is some overlap in the data post 1980, but mostly the DePol Holz record 
exists post 1980, and the Baring Head dataset is in the early part of the bomb peak.
See Figure below. 
"""
df2 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\Jocelyn Chile tree data 1980-2016(2).xlsx')

# print(df2.columns)
# print(monte_tarn.columns)
monte_tarn_x = monte_tarn['DecimalDate']
monte_tarn_y = monte_tarn['∆14C']
df2_x = df2['Year of Growth']
df2_y = df2['D14C']
# print(df2_x)
# print(df2_y)
"""
CODE FOR PLOTS
"""
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
size1 = 5
fig = plt.figure(1)
plt.plot(xtot_bhd, ytot_bhd, label='Baring Head Atmospheric CO2 Record', color='black', alpha = 0.15)
plt.scatter(df2_x, df2_y, marker='o', label='De Pol Holz Tree Ring Data', color=colors2[3], s=20)
plt.scatter(monte_tarn_x, monte_tarn_y, marker='o', label='SOAR Tree Ring Data', color=colors[3], s=20)
plt.legend()
plt.xlabel('Year of Growth', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison2/interlab_comparison/plots/chile_compare.png',
            dpi=300, bbox_inches="tight")
plt.close()
# plt.show()
# changes test

"""
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
Compare Tree Rings with harmonized data: 
to actually USE the harmonized dataset, we need x-values that directly 
correspond to the data that we're trying to compare. Therefore, all I have to do 
is put my sample's x-values in the final section of the method-call
###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
harm_xs = harmonized['Decimal_date'] # see dataset_harmonization.py
harm_ys = harmonized['D14C']  # see dataset_harmonization.py
sample_xs = (df['DecimalDate'])
sample_ys = (df['∆14C'])
cutoff = 667
n = 10
# input is: 1) x data, 2) y data that you want smoothed, then, 3) x-values at which you want y's output
harmonized_trend = ccgFilter(harmonized['Decimal_date'], harmonized['D14C'], cutoff).getTrendValue(sample_xs)
# to input below(x_init, fake_x, y_init, y_error, cutoff, n):
# x_init and y_init come from the harmonized dataset, while the "fake_x" is where
# I select what x-output values are, and this is my sample x's!!!!
errors = monte_carlo_randomization_Trend(harm_xs, sample_xs, sample_ys, harmonized['weightedstderr_D14C'], cutoff, n)

# What does this function return?
# summary = pd.DataFrame({"Means": mean_array,
#                         "stdevs": stdev_array,
#                         "error_upperbound": upper_array,
#                         "error_lowerbound": lower_array,
#                         "my_xs": fake_x_for_dataframe})
#
# return randomized_dataframe, smoothed_dataframe, summary
final_errors = errors[1]  # extract the real data I want out of the summary array.
print(final_errors)
"""
We can quickly see differences in a rough way by taking the offset between the output directly above, 
and the y-values from our samples...
"""
offsets = sample_ys - harmonized_trend
"""
But none of this means anything without some quality error propagation...
Actually, I need to do a Monte Carlo analysis on this new CCGCRV in order to get
error bars that I can use to propogate...
"""



























# fig = plt.figure(2)
# plt.scatter(sample_xs, offsets, label='Tree Rings Data offset from Harmonized Background', color='black', alpha = 0.15)
# plt.legend()
# plt.xlabel('Year of Growth', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.ylim([-50, 50])
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison2/interlab_comparison/plots/tree_ring_offsets2.png',
#             dpi=300, bbox_inches="tight")
# plt.close()

























# fig = plt.figure(2)
# plt.scatter(sample_xs, harmonized_trend, label='Baring Head Atmospheric CO2 Record', color='black', alpha = 0.15)
# plt.legend()
# plt.xlabel('Year of Growth', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# # plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
# #             'radiocarbon_intercomparison2/interlab_comparison/plots/harmonized_trended.png',
# #             dpi=300, bbox_inches="tight")
# plt.show()
