"""
Cleaning and redoing some of the math for the 13C paper, as well as redrawing some of the plots.
The contents of this sheet were also contained on paper_viz.py and data_cleaning.py, but got messed up. Makes sense
because I was doing that workup in quite a hurry, and I'll try to keep this more tidy.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# read in the SPE-DOC data
df = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\Cleaned_data.xlsx')
df = df.dropna(subset='Raw d13C')

# read in the total DOC data
doc = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\bulkDOCdatabase.xlsx').dropna(subset='Value')
doc = doc.replace('P16N.2', 'P16N')
doc2 = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\bulkDOCdatabase.xlsx', sheet_name='New').dropna(subset='Value')

# read in the hydrographic data
p18 = pd.read_csv('H:\Science\Datasets\Hydrographic\P18_2016.csv', skiprows=174).dropna(subset='DATE')
p16 = pd.read_csv('H:\Science\Datasets\Hydrographic\P16N_2015.csv', skiprows=119).dropna(subset='DATE')
io7 = pd.read_csv('H:\Science\Datasets\Hydrographic\IO7N_2018.csv', skiprows=131).dropna(subset='DATE')



"""
First order of business: do the mass-balance calculation to remove Cex
"""
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
b = np.sqrt(a**2 + df['13cerr']**2)
value = (df['Raw d13C'] - (cex_13C*df['X_blank']) )

# and now the whole thing
df['13C_corr_err'] = np.sqrt((b/value)**2 + (df['X_sample_err']/df['X_sample'])**2)
# in the end, the error propogation makes the errors too small, so I'm putting the 0.2 back in

# how much does the mass balance actually change the value? What is the percent change?
df['pct_ch'] = ((df['Raw d13C'] - df['13C_corr']) / df['Raw d13C']) * 100
# print(max(df['pct_ch']))


"""
Now, I'll compare total DOC to SPE-DOC
"""

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

    count.append(len(b_s))
    b_d = b.loc[b['SorD'] == 'Deep']

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

    nonret_error.append(np.nanmean(nonret_error_fin))


results = pd.DataFrame({"Description": descrip_doc, 'DOC 13C': bulk_av, 'error1': bulk_std,
                        'SPE-DOC 13C': SPE_av, "error2": SPE_std, "PPL % Recovery": ppl_rec, "error3": ppl_rec_err,
                        "Nonretained 13C": nonret, "error4": nonret_error, "N": count})
results.to_excel('test.xlsx')
results.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\UCI_13C\output\results_table.xlsx')


"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLO
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


RESULTS 1

"""
s = df.loc[df['SorD'] == 'Surface']
d = df.loc[df['SorD'] == 'Deep']

# https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3
# Skyblue to distant mountain green

c1, c2, c3 = '#d73027', '#fdae61', '#1c9099'

fig = plt.figure(1, figsize=(10, 8))
gs = gridspec.GridSpec(3, 4)
gs.update(wspace=.1, hspace=0)

cruises = ['P16', 'P18', 'IO7']
colors = [c2, c1, c3 ]
symbol = ['x','o','^']

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
for i in range(0, 3):
    curr = s.loc[s['Cruise'] == cruises[i]]
    color = colors[i]
    symbols = symbol[i]
    plt.errorbar(curr['Latitude'], curr['13C_corr'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)
    plt.scatter(curr['Latitude'], curr['13C_corr'], color=color, label=str(cruises[i]), marker=symbols)
    # plt.errorbar(curr['Latitude'], curr['Raw d13C'], yerr=0.2, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.25)

plt.ylim(-24, -21.75)
plt.xlim(-70, 60)
plt.ylabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)', fontsize=14)
plt.title('Surface (0-200 m)', fontsize=14)
plt.xlabel('Latitude (N)', fontsize=14)

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
for i in range(0, 3):
    curr = d.loc[d['Cruise'] == cruises[i]]
    color = colors[i]
    symbols = symbol[i]
    plt.errorbar(curr['Latitude'], curr['13C_corr'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)
    plt.scatter(curr['Latitude'], curr['13C_corr'], color=color, label=str(cruises[i]), marker=symbols)
    # plt.errorbar(curr['Latitude'], curr['Raw d13C'], yerr=0.2, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.25)
plt.legend()
plt.ylim(-24, -21.75)
plt.title('Deep (2000-4000 m)', fontsize=12)
plt.xticks([], [])
plt.yticks([], [])
plt.xlabel('Latitude (N)', fontsize=12)
plt.xlim(-70, 60)


p18 = p18[['LATITUDE','DEPTH']].drop_duplicates(keep='first').reset_index(drop=True).astype(float)
xtr_subsplot = fig.add_subplot(gs[2:3, 2:4])
plt.plot(p18['LATITUDE'], p18['DEPTH'], color=c1, label='P18 Bottom Depth')
plt.legend()
plt.xlim(-70, 60)
plt.xlabel('Latitude (N)', fontsize=12)
plt.ylabel('Bottom Depth (m)', fontsize=12)
plt.ylim(max(p18['DEPTH']), min(p18['DEPTH']))

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results1.png', dpi=300, bbox_inches="tight")
plt.close()

"""

SPE 13C vs 14C

"""

fig = plt.figure(1, figsize=(10, 5))
gs = gridspec.GridSpec(2, 4)
gs.update(wspace=.1, hspace=.35)

cruises = ['P16', 'P18', 'IO7']
colors = [c2, c1, c3 ]
symbol = ['x','o','^']

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
for i in range(0, 3):
    curr = s.loc[s['Cruise'] == cruises[i]]
    color = colors[i]
    symbols = symbol[i]
    plt.errorbar(curr['Corrected 14C with duplicates averaged'], curr['13C_corr'], xerr=curr['14cerr'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)



plt.ylim(-24, -21.75)
plt.ylabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)', fontsize=14)
plt.title('Surface (0-200 m)', fontsize=14)
plt.xlabel('SPE-DOC \u0394$^1$$^4$C (\u2030)', fontsize=14)


xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
for i in range(0, 3):
    curr = d.loc[d['Cruise'] == cruises[i]]
    color = colors[i]
    symbols = symbol[i]
    plt.errorbar(curr['Corrected 14C with duplicates averaged'], curr['13C_corr'], xerr=curr['14cerr'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)
    plt.scatter(curr['Corrected 14C with duplicates averaged'], curr['13C_corr'], color=color, label=str(cruises[i]), marker=symbols)
    # plt.errorbar(curr['Latitude'], curr['Raw d13C'], yerr=0.2, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.25)
plt.legend()
plt.ylim(-24, -21.75)
plt.title('Deep (2000-4000 m)', fontsize=14)
plt.yticks([], [])
plt.xlabel('SPE-DOC \u0394$^1$$^4$C (\u2030)', fontsize=14)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results2.png', dpi=300, bbox_inches="tight")
plt.close()


"""

SPE v total DOC 

"""
# set up the figure
fig = plt.figure(1, figsize=(8, 8))
gs = gridspec.GridSpec(6, 5)
gs.update(wspace=1, hspace=1)

# first subplot is all the data together.
xtr_subsplot = fig.add_subplot(gs[0:6, 0:3])
# names = ['P18','P16N','I7N']
names = np.unique(doc['Ocean Region'])
colors = ['#d73027','#fc8d59','#91bfdb','#4575b4']
markers = ['o','x','^','D','s']

for i in range(0, len(names)):
    cruise = doc.loc[doc['Ocean Region'] == names[i]]
    plt.scatter(cruise['Value'], (cruise['Depth']), color=colors[i], marker=markers[i], label=str(names[i] + ' Total DOC'))
plt.scatter(df[['13C_corr']], df['Weighted Average Depth'], color='black', label='SPE-DOC')
plt.ylim(max(cruise['Depth']), min(cruise['Depth']))
plt.ylabel('Depth (m)', fontsize=12)
plt.xlabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)', fontsize=12)
plt.legend()

# next subplot is just the P18 data
xtr_subsplot = fig.add_subplot(gs[0:2, 3:5])
plt.title('P18, 2016')
p18_doc = doc.loc[doc['Ocean Region'] == 'P18']
p18_spe = df.loc[(df['Cruise'] == 'P18')]

plt.errorbar(p18_doc['Value'], (p18_doc['Depth']), yerr=p18_doc['±'], fmt=markers[3], color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_doc['Value'], p18_doc['Depth'], marker=markers[3], color=colors[3], label='Total DOC')
plt.errorbar(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']), yerr=p18_spe['13C_corr_err'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']), marker='o', color='black', label='SPE-DOC')
plt.ylim(max(cruise['Depth']), min(cruise['Depth']))


xtr_subsplot = fig.add_subplot(gs[2:4, 3:5])
plt.title('P16N, 2015')
p18_doc = doc.loc[doc['Ocean Region'] == 'P16N']
p18_spe = df.loc[(df['Cruise'] == 'P16')]

plt.errorbar(p18_doc['Value'], (p18_doc['Depth']), yerr=p18_doc['±'], fmt=markers[2], color=colors[2], ecolor=colors[2], elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_doc['Value'], p18_doc['Depth'], marker=markers[2], color=colors[2], label='Total DOC')
plt.errorbar(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']), yerr=p18_spe['13C_corr_err'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']), marker='o', color='black', label='SPE-DOC')
plt.ylim(max(cruise['Depth']), min(cruise['Depth']))

xtr_subsplot = fig.add_subplot(gs[4:6, 3:5])
plt.title('IO7N, 2018')
p18_doc = doc.loc[doc['Ocean Region'] == 'I7N']
p18_spe = df.loc[(df['Cruise'] == 'IO7')]

plt.errorbar(p18_doc['Value'], (p18_doc['Depth']), yerr=p18_doc['±'], fmt=markers[0], color=colors[0], ecolor=colors[0], elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_doc['Value'], p18_doc['Depth'], marker=markers[0], color=colors[0], label='Total DOC')
plt.errorbar(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']), yerr=p18_spe['13C_corr_err'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']), marker='o', color='black', label='SPE-DOC')
plt.ylim(max(cruise['Depth']), min(cruise['Depth']))
plt.xlabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)', fontsize=12)


plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results3.png', dpi=300, bbox_inches="tight")
plt.close()



"""
Based on my conversation with Ellen and Brett on 9/2/23, how does total DOC change with latitude? Do we see progressive reworking?
"""

doc2 = doc2.loc[doc2['Flag'] != 'X']
plt.close()

names = ['I7N', 'P18','P16N']

cruise = []
means = []
stds = []
for i in range(0, len(names)):

    # grab the DOC from each cruise
    a = doc.loc[doc['Ocean Region'] == names[i]]

    # grab only the deep ocean
    a = a.loc[a['Depth'] >= 1500]
    means.append(np.nanmean(a['Value']))
    stds.append(np.nanstd(a['Value']))
    cruise.append(names[i])

    # plt.scatter(a['corr DEL 14C'], a['Value'])
    # plt.show()

dfnew = pd.DataFrame({"Cruise": cruise, "Mean": means, "STD": stds})
plt.errorbar(cruise, means, yerr=stds)
plt.plot(cruise, means)
plt.scatter(cruise, means)
plt.title('Mean DOC 13C <1500 m; progressive reworking of DOM?')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results4.png', dpi=300, bbox_inches="tight")
plt.close()


"""
Trying to plot individual sites of interest, DOC vs SPE
"""
doc = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\bulkDOCdatabase.xlsx').dropna(subset='Value')
doc = doc.replace('P16N.2', 'P16N')
# set up the figure
fig = plt.figure(1, figsize=(8, 8))
gs = gridspec.GridSpec(2, 6)
gs.update(wspace=1, hspace=1)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
doc2 = df.loc[df['Station'] == 205]
plt.scatter(doc2['13C_corr'], doc2['Weighted Average Depth'], color=c2, label='SPE-DOC')
doc2 = doc.loc[doc['Station'] == 206]
plt.scatter(doc2['Value'], doc2['Depth'], color=c1, label='Total DOC')
plt.plot(doc2['Value'], doc2['Depth'], color=c1)
plt.title('P18 Stn. 205-206')
plt.ylim(4000, 0)
plt.ylabel('Depth (m)', fontsize=12)

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
doc2 = df.loc[df['Station'] == 116]
plt.scatter(doc2['13C_corr'], doc2['Weighted Average Depth'], color=c2, label='SPE-DOC')
doc2 = doc.loc[doc['Station'] == 117]
plt.scatter(doc2['Value'], doc2['Depth'], color=c1, label='Total DOC')
plt.plot(doc2['Value'], doc2['Depth'], color=c1)
plt.ylim(max(doc2['Depth'])+50, min(doc2['Depth'])-50)
plt.title('P18 Stn. 116-117')
plt.ylim(4000, 0)
plt.xlabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)', fontsize=12)


xtr_subsplot = fig.add_subplot(gs[0:2, 4:6])
doc2 = df.loc[df['Station'] == 150]
plt.scatter(doc2['13C_corr'], doc2['Weighted Average Depth'], color=c2, label='SPE-DOC')
doc2 = doc.loc[doc['Station'] == 151]
plt.scatter(doc2['Value'], doc2['Depth'], color=c1, label='Total DOC')
plt.plot(doc2['Value'], doc2['Depth'], color=c1)
plt.title('P18 Stn. 150-151')
plt.ylim(4000, 0)
plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Supp2.png', dpi=300, bbox_inches="tight")


