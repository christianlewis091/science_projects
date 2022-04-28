import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dataset_harmonization import harmonized
from miller_curve_algorithm import ccgFilter
from heidelberg_intercomparison import monte_carlo_randomization_Trend
from heidelberg_intercomparison import monte_carlo_randomization_Smooth
"""
In the previous iteration of this file, I tried indexing and cleaning the 
tree ring file BEFORE doing the math. 
This led to many errors and NaN outputs due to problems with the actual indexing
rather than any errors or bad data. 

For example, all Chilean values need to be changed to NEGATIVE longitude, right now 
its in the same hemisphere as new zealand values. 
And there are a lot of missing data. 

In this iteration, I'm going to do all the math FIRST, and then index the data
after. 
"""
"""Omitted lines re-create the SOAR excel file without missing 14C values (there were a lot)"""
# df = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
#                    r'\SOARTreeRingData2022-02-01.xlsx')
# df = df.dropna(subset = '∆14C').reset_index()
# df.to_excel('adjusted_SOAR.xlsx')

df = pd.read_excel(r'C:\Users\lewis\venv\python310'
                   r'\python-masterclass-remaster-shared'
                   r'\radiocarbon_intercomparison2\interlab_comparison'
                   r'\adjusted_SOAR.xlsx')

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

# Smooth the harmonized data using CCGCRV and have the ouput at the same time as tree ring x's
# input is: 1) x data, 2) y data that you want smoothed, then, 3) x-values at which you want y's output
harmonized_trend = ccgFilter(harm_xs, harm_ys, cutoff).getTrendValue(sample_xs2)
# put the ouput into a dataframe
harmonized_trend = pd.DataFrame({'harmonized_data_trended': np.concatenate(harmonized_trend)})

# error estimate on the harmonized data trended using CCGCRV
n = 10  # TODO change back to 10,000
errors = monte_carlo_randomization_Trend(harm_xs, sample_xs2, harm_ys, harm_y_errs, cutoff, n)
errors_fin = errors[2]  # extract the summary dataframe
errors_fin = errors_fin['stdevs']

# add this new exciting data onto the original dataframe
df['harmonized_dataset_trended'] = harmonized_trend
df['harmonized_dataset_errors'] = errors_fin
print(np.shape(df))
print(df)

""" 
I think NOW I have to finally drop the NAN's beacause the math has trouble
When there are missing values
"""
df = df.dropna(subset = 'harmonized_dataset_trended')
# df.to_excel('df.xlsx')

# re-extract the values from the cleaned dataframe to calculate offsets
sample_xs = df['DecimalDate']
sample_ys = df['∆14C']
sample_y_err = df['∆14Cerr']
harm_ys = df['harmonized_dataset_trended']
harm_y_err = df['harmonized_dataset_errors']

df['offset'] = sample_ys - harm_ys
df['offset_err_prop'] = np.sqrt((sample_y_err**2) + (harm_y_err**2))
print(df)

# plt.scatter(sample_xs, df['offset'])
plt.errorbar(sample_xs, df['offset'], label='Tree Rings offset from background', yerr=df['offset_err_prop'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.15)
plt.show()


""" Later, when I need to adjust the Chilean values to negative lon, here is the code"""
# df['Lon'] = df['Lon'].fillna(-999)  # fill all missing values with -999
# df['Lat'] = df['Lat'].fillna(-999)  # fill all missing values with -999
# df.drop(df[df['C14Flag'] == -999].index, inplace=True)
#
# # baringhead = baringhead.iloc[::5, :]  # if I want to downsample the data
# xtot_bhd = baringhead['DEC_DECAY_CORR']             # entire dataset x-values
# ytot_bhd = baringhead['DELTA14C']                   # entire dataset y-values
#
# """ First order of tidying, adjust the Western Hemisphere longitude values (should be negative) """
# # From POKEMON.PY file
# # df.loc[(df['Type 1'] == 'Grass') | (df['Type 2'] == 'Poison')] # filtering based on two types of data OR
# nz = df.loc[(df['Lon'] > 100) | (df['Lon'] == -999)].reset_index()  # split up the data
# chile = df.loc[(df['Lon'] < 100) & (df['Lon'] > 0)].reset_index()  # split up the data
# chile['new_lon'] = np.multiply(chile['Lon'], -1)  # address the bad longitude
# nz['new_lon'] = nz['Lon']  # need this new column to be the same for concatenation
#
# frames = [chile, nz]  # TODO: figure out: why I need to put these two DataFrames into an array before concat
# df = pd.concat(frames)  # put the data back together
# # df.to_excel('adjusted_SOAR2.xlsx')

""" And later, when i want to index by location, see this block of code: """
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