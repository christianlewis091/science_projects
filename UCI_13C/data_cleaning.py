"""
Lets clean up the 13C data
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from scipy import stats

df = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\Cleaned_data.xlsx')
print(df.columns)
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
# print('SPE-DOC')
# print(np.average(df['13C_corr']))
# print(np.std(df['13C_corr']))
# print(len(df))
# print()
# print('Total DOC')
# print(np.average(doc['Value']))
# print(np.std(doc['Value']))
# print(len(doc))
# print()
# print('Difference')
# print(np.average(df['13C_corr']) - (np.average(doc['Value'])))
# print(np.sqrt((np.std(df['13C_corr']))**2 + (np.std(doc['Value']))**2))
# print()


names = ['P18', 'P16N','I7N']
names2 = ['P18', 'P16','IO7']

# Initialize some arrays to store data later
bulk_av = []
bulk_std = []
SPE_av = []
SPE_std = []
descrip_doc = []
descrip_spe = []
nonret = []
nonret_error = []
ppl_rec = []
ppl_rec_err = []
count  = []
for i in range(0, len(names)):

    # grab the DOC from each cruise
    a = doc.loc[doc['Ocean Region'] == names[i]]
    # break up into surface and deep
    a_s = a.loc[(a['Depth'] < 200)]
    a_d = a.loc[(a['Depth'] < 4000) & (a['Depth'] > 2000)]

    bulk_av.append(np.average(a_s['Value']))
    bulk_std.append(np.std(a_s['Value']))
    descrip_doc.append(f'Surface {names[i]}')

    bulk_av.append(np.average(a_d['Value']))
    bulk_std.append(np.std(a_d['Value']))
    descrip_doc.append(f'Deep {names[i]}')


    # grab the SPE-DOC from each cruise
    b = df.loc[(df['Cruise'] == names2[i])]
    # break up into surface and deep
    b_s = b.loc[b['SorD'] == 'Surface']
    print(b_s)
    count.append(len(b_s))
    b_d = b.loc[b['SorD'] == 'Deep']
    print(b_d)
    count.append(len(b_d))

    SPE_av.append(np.average(b_s['13C_corr']))
    SPE_std.append(np.std(b_s['13C_corr']))
    # descrip_spe.append(f'Surface, SPE-DOC {names2[i]}')

    SPE_av.append(np.average(b_d['13C_corr']))
    SPE_std.append(np.std(b_d['13C_corr']))
    # descrip_spe.append(f'Deep, SPE-DOC {names2[i]}')

    # calculate non-retained's (surface)
    rec = (np.nanmean(b_s['PPL % Recovery']))/100
    rec_err = (np.nanstd(b_s['PPL % Recovery']))/100
    ppl_rec.append(rec)
    ppl_rec_err.append(rec_err)

    nonretained_surface = (np.nanmean(a_s['Value']) - (np.nanmean(b_s['13C_corr'])*rec)) / (1-rec)
    nonret.append(nonretained_surface)

    # propogate the error
    a = np.sqrt((np.nanmean(b_s['13C_corr_err'])/np.nanmean(b_s['13C_corr'])**2) + (np.nanmean(b_s['±.12'])/np.nanmean(b_s['PPL % Recovery'])**2))
    b = np.sqrt(a**2 + np.nanmean(a_s['±']**2))
    value = np.nanmean(a_s['Value']) - (np.nanmean(b_s['13C_corr'])*rec)
    nonret_error_fin = -1*nonretained_surface*(np.sqrt((b/value)**2 + (np.nanmean(b_s['±.12'])/np.nanmean(b_s['PPL % Recovery'])**2)))
    print(nonret_error_fin)
    nonret_error.append(np.nanmean(nonret_error_fin))
# #
    # calculate non-retained's (deep)
    rec = (np.nanmean(b_d['PPL % Recovery']))/100
    rec_err = (np.nanstd(b_d['PPL % Recovery']))/100
    ppl_rec.append(rec)
    ppl_rec_err.append(rec_err)
    nonretained_deep = (np.nanmean(a_d['Value']) - (np.nanmean(b_d['13C_corr'])*rec)) / (1-rec)
    nonret.append(nonretained_deep)
    # propogate the error
    a = np.sqrt((np.nanmean(b_d['13C_corr_err'])/np.nanmean(b_d['13C_corr'])**2) + (np.nanmean(b_d['±.12'])/np.nanmean(b_d['PPL % Recovery'])**2))
    b = np.sqrt(a**2 + np.nanmean(a_d['±']**2))
    value = np.nanmean(a_d['Value']) - (np.nanmean(b_d['13C_corr'])*rec)
    nonret_error_fin = -1*nonretained_deep*(np.sqrt((b/value)**2 + (np.nanmean(b_d['±.12'])/np.nanmean(b_d['PPL % Recovery'])**2)))
    print(nonret_error_fin)
    nonret_error.append(np.nanmean(nonret_error_fin))


results = pd.DataFrame({"Description": descrip_doc, 'DOC 13C': bulk_av, 'error1': bulk_std,
                        'SPE-DOC 13C': SPE_av, "error2": SPE_std, "PPL % Recovery": ppl_rec, "error3": ppl_rec_err,
                        "Nonretained 13C": nonret, "error4": nonret_error, "N": count})
#results.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\UCI_13C\output\results_table.xlsx')
plt.close()


# plot the new model data
colors = ['#d73027','#fc8d59','#91bfdb','#4575b4']
markers = ['o','x','^','D','s']

plt.errorbar(results['Description'], results['DOC 13C'], yerr=results['error1'], fmt=markers[0], color=colors[0], capsize=4)
plt.scatter(results['Description'], results['DOC 13C'], color=colors[0], marker=markers[0], label='DOC')

plt.errorbar(results['Description'], results['SPE-DOC 13C'], yerr=results['error2'], fmt=markers[1], color=colors[1], capsize=4)
plt.scatter(results['Description'], results['SPE-DOC 13C'], color=colors[1], marker=markers[1], label='SPE-DOC')

plt.errorbar(results['Description'], results['Nonretained 13C'], yerr=results['error4'], fmt=markers[2], color=colors[2], capsize=4)
plt.scatter(results['Description'], results['Nonretained 13C'], color=colors[2], marker=markers[2], label='Nonretained')
plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Discussion1.png', dpi=95, bbox_inches="tight")








    # c = stats.ttest_ind(a['Value'], b[['13C_corr']])
    # print(f'Independent t-test for {names[i]} result is {c}')


# Calculate the mass balance for the discussion:

# s = df.loc[df['SorD'] == 'Surface']
# d = df.loc[df['SorD'] == 'Deep']
#
# s_doc = doc.loc[(doc['Depth'] < 200)]
# d_doc = doc.loc[(doc['Depth'] < 4000) & (doc['Depth'] > 2000)]
#












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