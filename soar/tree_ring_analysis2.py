import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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
INDEX THE DATA BY SITE, LATITUDE
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
"""
df2 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Datasets'
                    r'\Jocelyn Chile tree data 1980-2016(2).xlsx')

print(df2.columns)
# print(monte_tarn.columns)
monte_tarn_x = monte_tarn['DecimalDate']
monte_tarn_y = monte_tarn['∆14C']
df2_x = df2['Year of Growth']
df2_y = df2['D14C']
print(df2_x)
print(df2_y)
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
            'radiocarbon_intercomparison2/soar/plots/chile_compare.png',
            dpi=300, bbox_inches="tight")
plt.show()
# changes test

"""
To actually USE the harmonized dataset, we need x-values that directly 
correspond to the data that we're trying to compare. Therefore, I'm going to 
smooth the harmonized dataset using CCGCRV getTrendValue, and ensure that 
the tree ring x-values are in the output. 
"""
xs = np.linspace(min())
L = np.linspace(0, 1, 365)