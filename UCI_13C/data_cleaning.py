"""
Lets clean up the 13C data
"""
import numpy as np
import pandas as pd
from scipy import stats

df = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\Cleaned_data.xlsx')

df = df[['SPEDOC split UCID', 'Cruise', 'SorD', 'Latitude',
          'Weighted Average Depth', 'Seawater Volume', 'Seawater Volume PM',
          'Empty mass of round-bottom 60 mL vial (mg) ', '±2',
          'Mass of round bottom 60 mL vial after elution', '±2.1',
          'Difference (mg) ', '±', 'Total Methanol Volume (mL) ', '±.1',
          'SPE-Split Vial Pre-Weight (mg) ', '±.2',
          'SPE-split vial post-weight (mg) ', '±.3', 'difference (mg) ', '±.4',
          'Methanol Volume (mL)', '±.5', 'Fraction of whole',
          '±.6', 'ug C', '±.7',
          'mass SPE-DOC in full extract (ug) 1', '±.8', '[SPE-DOC] micromols C',
          '±.9', '[SPE-DOC] uM', '±.10', 'Taking out PPL Split dups', '±.11',
          'Closest DOC depth', 'DOC Concentration from closest depth',
          'PPL % Recovery', '±.12', 'DO13C from closest depth', 'Raw d13C',
          '±.13', 'Corrected 14C with duplicates averaged', 'Unnamed: 52', 'X_sample', 'X_sample_err','X_blank','X_blank_err']].dropna(subset='Raw d13C')

# write the sheet to excel for later if you want to view it offline
# df.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\UCI_13C\output\test.xlsx')

# need to calculate the mass-balance corrected 13C value for the small contribution from the PPL cartridge
# the relative abundances of Cex vs sample is defined from 9 ug Cex contribution from my first paper.

# now the mass balance
# define a number for the 13C of Cex
cex_13C = -30  # typical value for petroleum 13C
df['13C_corr'] = (df['Raw d13C'] - (cex_13C*df['X_blank']) ) / df['X_sample']

# and now the error propogation for the 13C correction
# for the multiplied term
a = np.sqrt((0.2/cex_13C)**2 + (df['X_blank_err']/df['X_blank'])**2)

# and now the whole numerator
b = np.sqrt(a**2 + df['±.13']**2)
value = (df['Raw d13C'] - (cex_13C*df['X_blank']) )

# and now the whole thing
df['13C_corr_err'] = np.sqrt((b/value)**2 + (df['X_sample_err']/df['X_sample'])**2)
# in the end, the error propogation makes the errors too small, so I'm putting the 0.2 back in

# how much does the mass balance actually change the value? What is the percent change?
df['pct_ch'] = ((df['Raw d13C'] - df['13C_corr']) / df['Raw d13C']) * 100
# print(max(df['pct_ch']))


"""

Some quick calculations to help my writing process

"""

check = df.loc[(df['Cruise'] == 'P18')]
# print(np.average(check[['13C_corr']]))
# print(np.std(check[['13C_corr']]))
# print(len(check))
#
#
# print(min(check['13C_corr']))
# print(max(check['13C_corr']))





"""

Checking how the 13C and 14C values match with bottom depth / seamounts

"""

p18 = pd.read_csv('H:\Science\Datasets\Hydrographic\P18_2016.csv', skiprows=174).dropna(subset='DATE')



"""

total DOC data

"""

doc = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\bulkDOCdatabase.xlsx').dropna(subset='Value')
doc = doc.replace('P16N.2', 'P16N')


"""

Comparing total DOC and SPE-DOC 

"""
print('SPE-DOC')
print(np.average(df['13C_corr']))
print(np.std(df['13C_corr']))
print(len(df))
print()
print('Total DOC')
print(np.average(doc['Value']))
print(np.std(doc['Value']))
print(len(doc))
print()
print('Difference')
print(np.average(df['13C_corr']) - (np.average(doc['Value'])))
print(np.sqrt((np.std(df['13C_corr']))**2 + (np.std(doc['Value']))**2))
print()


names = ['P18', 'P16N','I7N']
names2 = ['P18', 'P16','IO7']
for i in range(0, len(names)):

    a = doc.loc[doc['Ocean Region'] == names[i]]
    print(len(a))
    b = df.loc[(df['Cruise'] == names2[i])]
    print(len(b))
    c = stats.ttest_ind(a['Value'], b[['13C_corr']])
    print(f'Independent t-test for {names[i]} result is {c}')


















# # Let's recreate Figure 4.2 from my thesis, with this newly cleaned dataset
# s = df.loc[df['SorD'] == 'Surface']
# d = df.loc[df['SorD'] == 'Deep']
#
# # https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3
# # Skyblue to distant mountain green
#
# c1, c2, c3 = '#d73027', '#fdae61', '#1c9099'
#
# fig = plt.figure(1, figsize=(15, 5))
# gs = gridspec.GridSpec(2, 4)
# gs.update(wspace=.35, hspace=.35)
#
# cruises = ['P16', 'P18', 'IO7']
# colors = [c1, c2, c3 ]
# symbol = ['o','x','^']
#
# xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
# for i in range(0, 3):
#     curr = s.loc[s['Cruise'] == cruises[i]]
#     color = colors[i]
#     symbols = symbol[i]
#     plt.errorbar(curr['Latitude'], curr['13C_corr'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)
#     plt.scatter(curr['Latitude'], curr['13C_corr'], color=color, label=str(cruises[i]), marker=symbols)
#     # plt.errorbar(curr['Latitude'], curr['Raw d13C'], yerr=0.2, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.25)
# plt.legend()
# plt.ylim(-24, -21.75)
# plt.title('Surface (0-200 m)')
#
# xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
# for i in range(0, 3):
#     curr = d.loc[d['Cruise'] == cruises[i]]
#     color = colors[i]
#     symbols = symbol[i]
#     plt.errorbar(curr['Latitude'], curr['13C_corr'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)
#     plt.scatter(curr['Latitude'], curr['13C_corr'], color=color, label=str(cruises[i]), marker=symbols)
#     # plt.errorbar(curr['Latitude'], curr['Raw d13C'], yerr=0.2, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.25)
# plt.legend()
# plt.ylim(-24, -21.75)
# plt.title('Deep (2-4 km)')
# plt.show()