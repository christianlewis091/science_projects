"""
Cleaning and redoing some of the math for the 13C paper, as well as redrawing some of the plots.
The contents of this sheet were also contained on paper_viz.py and data_cleaning.py, but got messed up. Makes sense
because I was doing that workup in quite a hurry, and I'll try to keep this more tidy.

Currently as of line (X), the data is in a form that I am willing to submit to the journal in the open data access
stuff. From this new, complete database, which includes the GO-SHIP data, the Do14C data, and SPE-DOC data, I can
go ahead with re-doing the data processing in a way that will be more readable to another audiance or Future Christian.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# read in the SPE-DOC data, called "df" for DataFrame
df = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\Cleaned_data.xlsx').dropna(subset='Raw d13C')

# read in the total DOC data, called "doc" for dissloved organic carbon
doc = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\bulkDOCdatabase.xlsx', sheet_name='ForMerge').dropna(
    subset='del13C')

# make sure all the cruise names are the same for both the DOC and SPE-DOC databases.
# In SPE-DOC data, its 'P16', 'P18', and 'IO7'.
# doc = doc.replace('I7N', 'IO7N')

# read in the hydrographic data
p18 = pd.read_csv('H:\Science\Datasets\Hydrographic\P18_2016.csv', skiprows=174).dropna(subset='DATE')
P18 = pd.read_csv('H:\Science\Datasets\Hydrographic\P18_2016.csv', skiprows=174).dropna(subset='DATE')
P16N = pd.read_csv('H:\Science\Datasets\Hydrographic\P16N_2015.csv', skiprows=119).dropna(subset='DATE')
IO7N = pd.read_csv('H:\Science\Datasets\Hydrographic\IO7N_2018.csv', skiprows=131).dropna(subset='DATE')

# Lets concat all the cruises together into one file...
P18['Cruise'] = 'P18'
P16N['Cruise'] = 'P16N'
IO7N['Cruise'] = 'IO7N'
go_ship = pd.concat([P18, P16N, IO7N]).reset_index(drop=True)

# And merge the DOC data into it.
merged1 = pd.merge(go_ship, doc, how='outer')

# I also want to add the SPE-DOC into there, but need the depths are weighted averages.
# I want to stick the SPE-DOC data in the bottle with the closest depth to the weighted average (for loop required)
# I've had some issues with the mergeing of these data, so I'm going to try to add a Niskin Index on which to merge
# after the "closest sampling depths" have been found
new_index = []
for i in range(0, len(merged1)):
    row = merged1.iloc[i]
    cruise = row['Cruise']
    station = row['STNNBR']
    bottle = row['SAMPNO']
    string = f'{cruise}+{station}+{bottle}'
    new_index.append(string)

merged1['Merging_Index'] = new_index

"""
"""
# Now I'll try to associate the closest sampling depths to the SPE weighted average depths
# initialize an array for the merging indexes to be added as strings
new_index2 = []

# initialize an array for the CTDPRS of the closest depths to the WAD (weighted average depths)
new_depths = []

# this array = when I index the data and create mergeing index, it gets scrambled, this is a workaround by
# reassembling the data alongside its mergeing index.
redoing_data = []

for c in ['P16N', 'P18', 'IO7N']:
    # for the first cruise (locate the first cruise for both main datasets and spe datasets)
    cruise_spe = df.loc[df['Cruise'] == c]
    cruise_main = go_ship.loc[go_ship['Cruise'] == c]

    # for the stations that we sampled for SPE
    stations = np.unique(cruise_spe['STNNBR'])

    # extract both stations from the data (my SPE station data, and the same station in the merged file with the
    # depths we want to allocate
    for i in range(0, len(stations)):
        spe_stn = cruise_spe.loc[cruise_spe['STNNBR'] == stations[i]].reset_index(drop=True)
        main_stn = cruise_main.loc[cruise_main['STNNBR'] == stations[i]]

        for j in range(0, len(spe_stn)):
            this_row = spe_stn.iloc[j]

            # grab the weighted average depth from this row of SPE data
            A = this_row['Weighted Average Depth'].astype(float)

            # meanwhile, grab the sample No and the CTDPRS from the go-ship data
            B = main_stn['CTDPRS'].astype(float).reset_index(drop=True)
            C = main_stn['SAMPNO'].astype(float).reset_index(drop=True)

            # find the closest depths from GO-SHIP to the WAD.
            try:
                B = np.asarray(B)
                # find the index where the differences is the least between the Go-SHIP data CTDPRS and the weighted average depth
                idx = (np.abs(B - A)).argmin()
                string = f'{c}+{stations[i].astype(float)}+{C[idx]}'

                # append this string to the array, for mergeing index
                new_index2.append(string)
                # re-append this row's data to a new dataframe.
                redoing_data.append(this_row)
                # re-append this row's data to a new dataframe.
                new_depths.append(B[idx])

            except ValueError:
                string = 'BADMERGE'

                # append this string to the array, for mergeing index
                new_index2.append(string)
                # re-append this row's data to a new dataframe.
                redoing_data.append(this_row)
                # re-append this row's data to a new dataframe.
                new_depths.append(-999)

new_df = pd.DataFrame(redoing_data)
new_df['Merging_Index'] = new_index2
new_df['CTDPRS'] = new_depths
new_df = new_df[['SPEDOC split UCID', 'Cruise','SorD','STNNBR','Weighted Average Depth',
                 'Raw d13C','13cerr','Corrected 14C with duplicates averaged','14cerr','Merging_Index','CTDPRS','X_sample',
                 'X_sample_err', 'X_blank', 'X_blank_err','PPL % Recovery','±.12']]
new_df = new_df.rename(columns={"SPEDOC split UCID": "SPE_ID",
                                "Raw d13C": "SPE 13C",
                                "13cerr": "SPE 13C err",
                       "Corrected 14C with duplicates averaged": "SPE-14C",
                                "14cerr": "SPE-14C err"})

merged1 = merged1[['EXPOCODE','SECT_ID','STNNBR','SAMPNO','CTDPRS','CTDTMP','Merging_Index','UCID','del13C','del13C_err','LATITUDE','LONGITUDE']]
merged1 = merged1.rename(columns={"del13C": "Total DOC 13C", "del13C_err": "Total DOC 13C err"})
new_df['STNNBR'] = new_df['STNNBR'].astype(float)
merged1['CTDPRS'] = merged1['CTDPRS'].astype(float)

cleaned_df = pd.merge(new_df, merged1, how='outer')
full_df = cleaned_df
cleaned_df = cleaned_df.dropna(subset='SPE 13C')

# cleaned_df.to_excel('test1.xlsx')

"""
As of this point the data has been associated with total DOC data, and the GO-SHIP data. We will still add a few changes
to the data, so we will re-publish the final excel sheet at the end of the file. For now we'll carry on with some analysis,
using the "cleaned_df" as the data from here on out. 

Next thing I'm going to do is write a function to deal with the mass-balance eqn and error propogation. 
I need to do these equations all the time for radiocarbon, and I need to finally write a function for it. 

"""

def mass_balance_plus_err_prop(M_14C, M14C_err, B_14C, X_blank, X_blank_err, X_sample, X_sample_err, route=None, **kwargs):
    # where:
    # M_14C = measured value
    # M_14C_err = measured value's error
    # S_14C = sample 14C (what we're usually solving for)
    # S_14C_err = sample 14C error
    # B_14C = blank 14C
    # B_14C_err = blank 14C error
    # X_sample = fraction of sample
    # X_blank = fraction of blank

    # mass balance first
    S_14C = M_14C - (np.nanmean(B_14C)*np.nanmean(X_blank)) / X_sample

    # now the error prop
    # first the multiplied term in parentheses
    a = np.sqrt((0.2/B_14C)**2 + (X_blank_err/X_blank)**2)

    # and now the whole numerator
    b = np.sqrt(a**2 + M14C_err**2)
    value = (M_14C - (B_14C*X_blank))

    # and now the whole thing
    S_14C_err = np.sqrt((b/value)**2 + (X_sample_err/X_sample)**2)
    return S_14C, S_14C_err

"""
Lets apply the mass balance function to the 13C data
"""

x = mass_balance_plus_err_prop(cleaned_df['SPE 13C'], cleaned_df['SPE 13C err'], -30, cleaned_df['X_blank'], cleaned_df['X_blank_err'], cleaned_df['X_sample'], cleaned_df['X_sample_err'])
cleaned_df['SPE 13C Corrected'] = x[0]
cleaned_df['SPE 13C Corrected Err'] = x[1]


"""
Now, I'll compare total DOC to SPE-DOC
"""

names = ['P18', 'P16N','IO7N']
# names2 = ['P18', 'P16','IO7']

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
    a = doc.loc[doc['Cruise'] == names[i]]
    # break up into surface and deep
    a_s = a.loc[(a['Depth'] < 200)]
    a_d = a.loc[(a['Depth'] < 4000) & (a['Depth'] > 2000)]

    bulk_av.append(np.average(a_s['del13C']))
    bulk_std.append(np.std(a_s['del13C']))
    descrip_doc.append(f'Surface {names[i]}')

    bulk_av.append(np.average(a_d['del13C']))
    bulk_std.append(np.std(a_d['del13C']))
    descrip_doc.append(f'Deep {names[i]}')

    # grab the SPE-DOC from each cruise
    b = cleaned_df.loc[(cleaned_df['Cruise'] == names[i])]
    # break up into surface and deep
    b_s = b.loc[b['SorD'] == 'Surface']
    count.append(len(b_s))

    b_d = b.loc[b['SorD'] == 'Deep']
    count.append(len(b_d))

    SPE_av.append(np.average(b_s['SPE 13C Corrected']))
    SPE_std.append(np.std(b_s['SPE 13C Corrected']))
    # descrip_spe.append(f'Surface, SPE-DOC {names2[i]}')

    SPE_av.append(np.average(b_d['SPE 13C Corrected']))
    SPE_std.append(np.std(b_d['SPE 13C Corrected']))
    # descrip_spe.append(f'Deep, SPE-DOC {names2[i]}')

    # calculate non-retained's (surface)
    rec = (np.nanmean(b_s['PPL % Recovery']))/100
    rec_err = (np.nanstd(b_s['PPL % Recovery']))/100
    ppl_rec.append(rec)
    ppl_rec_err.append(rec_err)

    nonretained_surface = (np.nanmean(a_s['del13C']) - (np.nanmean(b_s['SPE 13C Corrected'])*rec)) / (1-rec)
    nonret.append(nonretained_surface)

    # propogate the error
    a = np.sqrt((np.nanmean(b_s['SPE 13C Corrected Err'])/np.nanmean(b_s['SPE 13C Corrected'])**2) + (np.nanmean(b_s['±.12'])/np.nanmean(b_s['PPL % Recovery'])**2))
    b = np.sqrt(a**2 + np.nanmean(a_s['del13C_err']**2))
    value = np.nanmean(a_s['del13C']) - (np.nanmean(b_s['SPE 13C Corrected'])*rec)
    nonret_error_fin = -1*nonretained_surface*(np.sqrt((b/value)**2 + (np.nanmean(b_s['±.12'])/np.nanmean(b_s['PPL % Recovery'])**2)))

    nonret_error.append(np.nanmean(nonret_error_fin))
    # #


    # calculate non-retained's (deep)
    rec = (np.nanmean(b_d['PPL % Recovery']))/100
    rec_err = (np.nanstd(b_d['PPL % Recovery']))/100
    ppl_rec.append(rec)
    ppl_rec_err.append(rec_err)
    nonretained_deep = (np.nanmean(a_d['del13C']) - (np.nanmean(b_d['SPE 13C Corrected'])*rec)) / (1-rec)
    nonret.append(nonretained_deep)
    # propogate the error
    a = np.sqrt((np.nanmean(b_d['SPE 13C Corrected Err'])/np.nanmean(b_d['SPE 13C Corrected'])**2) + (np.nanmean(b_d['±.12'])/np.nanmean(b_d['PPL % Recovery'])**2))
    b = np.sqrt(a**2 + np.nanmean(a_d['del13C_err']**2))
    value = np.nanmean(a_d['del13C']) - (np.nanmean(b_d['SPE 13C Corrected'])*rec)
    nonret_error_fin = -1*nonretained_deep*(np.sqrt((b/value)**2 + (np.nanmean(b_d['±.12'])/np.nanmean(b_d['PPL % Recovery'])**2)))

    nonret_error.append(np.nanmean(nonret_error_fin))

results = pd.DataFrame({"Description": descrip_doc, 'DOC 13C': bulk_av, 'error1': bulk_std,
                        'SPE-DOC 13C': SPE_av, "error2": SPE_std, "PPL % Recovery": ppl_rec, "error3": ppl_rec_err,
                        "Nonretained 13C": nonret, "error4": nonret_error, "N": count})
# with pd.ExcelWriter(r'C:\Users\clewis\IdeaProjects\GNS\UCI_13C\output\output.xlsx') as writer:
#     cleaned_df.to_excel(writer, sheet_name='Complete_Data')
#     results.to_excel(writer, sheet_name='Results_Summary')
#     full_df.to_excel(writer, sheet_name='WithDOC')
#

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
s = cleaned_df.loc[cleaned_df['SorD'] == 'Surface']
d = cleaned_df.loc[cleaned_df['SorD'] == 'Deep']

# https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3
# Skyblue to distant mountain green

c1, c2, c3 = '#d73027', '#fdae61', '#1c9099'

fig = plt.figure(1, figsize=(10, 8))
gs = gridspec.GridSpec(3, 4)
gs.update(wspace=.1, hspace=0)

cruises = ['P16N', 'P18', 'IO7N']
colors = [c2, c1, c3]
symbol = ['x','o','^']

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
for i in range(0, 3):
    curr = s.loc[s['Cruise'] == cruises[i]]
    color = colors[i]
    symbols = symbol[i]
    plt.errorbar(curr['LATITUDE'], curr['SPE 13C Corrected'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)
    plt.scatter(curr['LATITUDE'], curr['SPE 13C Corrected'], color=color, label=str(cruises[i]), marker=symbols)
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
    plt.errorbar(curr['LATITUDE'], curr['SPE 13C Corrected'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)
    plt.scatter(curr['LATITUDE'], curr['SPE 13C Corrected'], color=color, label=str(cruises[i]), marker=symbols)
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

cruises = ['P16N', 'P18', 'IO7N']
colors = [c2, c1, c3 ]
symbol = ['x','o','^']

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
for i in range(0, 3):
    curr = s.loc[s['Cruise'] == cruises[i]]
    color = colors[i]
    symbols = symbol[i]
    plt.errorbar(curr['SPE-14C'], curr['SPE 13C Corrected'], xerr=curr['SPE-14C err'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)


plt.ylim(-24, -21.75)
plt.ylabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)', fontsize=14)
plt.title('Surface (0-200 m)', fontsize=14)
plt.xlabel('SPE-DOC \u0394$^1$$^4$C (\u2030)', fontsize=14)


xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
for i in range(0, 3):
    curr = d.loc[d['Cruise'] == cruises[i]]
    color = colors[i]
    symbols = symbol[i]
    plt.errorbar(curr['SPE-14C'], curr['SPE 13C Corrected'], xerr=curr['SPE-14C err'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)
    plt.scatter(curr['SPE-14C'], curr['SPE 13C Corrected'], color=color, label=str(cruises[i]), marker=symbols)
    # plt.errorbar(curr['Latitude'], curr['Raw d13C'], yerr=0.2, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.25)
plt.legend()
plt.ylim(-24, -21.75)
plt.title('Deep (2000-4000 m)', fontsize=14)
plt.yticks([], [])
plt.xlabel('SPE-DOC \u0394$^1$$^4$C (\u2030)', fontsize=14)
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results2.png', dpi=300, bbox_inches="tight")
plt.close()
#
#
"""

SPE v total DOC

# """
# reading in the sheet that has the P06 data.
# set up the figure

full_df = full_df.dropna(subset='Total DOC 13C')
fig = plt.figure(1, figsize=(8, 8))
gs = gridspec.GridSpec(6, 5)
gs.update(wspace=1, hspace=1)

# first subplot is all the data together.
xtr_subsplot = fig.add_subplot(gs[0:6, 0:3])
names = np.unique(full_df['SECT_ID'])
colors = ['#d73027','#fc8d59','#91bfdb','#4575b4']
markers = ['o','x','^','D','s']

for i in range(0, len(names)):
    cruise = doc.loc[doc['Cruise'] == names[i]]
    plt.scatter(cruise['Total DOC 13C'], (cruise['CTDPRS']), color=colors[i], marker=markers[i], label=str(names[i] + ' Total DOC'))
plt.scatter(df[['SPE 13C Corrected']], df['Weighted Average Depth'], color='black', label='SPE-DOC')
plt.ylim(max(cruise['CTDPRS']), min(cruise['CTDPRS']))
plt.ylabel('Depth (m)', fontsize=12)
plt.xlabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)', fontsize=12)
plt.legend()

# # next subplot is just the P18 data
# xtr_subsplot = fig.add_subplot(gs[0:2, 3:5])
# plt.title('P18, 2016')
# p18_doc = doc.loc[doc['Cruise'] == 'P18']
# p18_spe = cleaned_df.loc[(cleaned_df['Cruise'] == 'P18')]
#
# plt.errorbar(p18_doc['del13C'], (p18_doc['Depth']), yerr=p18_doc['del13C_err'], fmt=markers[3], color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2, alpha = 1)
# plt.scatter(p18_doc['del13C'], p18_doc['Depth'], marker=markers[3], color=colors[3], label='Total DOC')
# plt.errorbar(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), yerr=p18_spe['SPE 13C Corrected Err'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
# plt.scatter(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), marker='o', color='black', label='SPE-DOC')
# plt.ylim(max(cruise['Depth']), min(cruise['Depth']))
#
#
# xtr_subsplot = fig.add_subplot(gs[2:4, 3:5])
# plt.title('P16N, 2015')
# p18_doc = doc.loc[doc['Cruise'] == 'P16N']
# p18_spe = cleaned_df.loc[(cleaned_df['Cruise'] == 'P16')]
#
# plt.errorbar(p18_doc['del13C'], (p18_doc['Depth']), yerr=p18_doc['del13C_err'], fmt=markers[2], color=colors[2], ecolor=colors[2], elinewidth=1, capsize=2, alpha = 1)
# plt.scatter(p18_doc['del13C'], p18_doc['Depth'], marker=markers[2], color=colors[2], label='Total DOC')
# plt.errorbar(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), yerr=p18_spe['SPE 13C Corrected Err'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
# plt.scatter(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), marker='o', color='black', label='SPE-DOC')
# plt.ylim(max(cruise['Depth']), min(cruise['Depth']))
#
# xtr_subsplot = fig.add_subplot(gs[4:6, 3:5])
# plt.title('IO7N, 2018')
# p18_doc = doc.loc[doc['Cruise'] == 'I7N']
# p18_spe = cleaned_df.loc[(cleaned_df['Cruise'] == 'IO7')]
#
# plt.errorbar(p18_doc['del13C'], (p18_doc['Depth']), yerr=p18_doc['del13C_err'], fmt=markers[0], color=colors[0], ecolor=colors[0], elinewidth=1, capsize=2, alpha = 1)
# plt.scatter(p18_doc['del13C'], p18_doc['Depth'], marker=markers[0], color=colors[0], label='Total DOC')
# plt.errorbar(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), yerr=p18_spe['SPE 13C Corrected Err'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
# plt.scatter(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), marker='o', color='black', label='SPE-DOC')
# plt.ylim(max(cruise['Depth']), min(cruise['Depth']))
# plt.xlabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)', fontsize=12)
# plt.show()

# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results3.png', dpi=300, bbox_inches="tight")
# plt.close()

#
#
# """
# Based on my conversation with Ellen and Brett on 9/2/23, how does total DOC change with latitude? Do we see progressive reworking?
# """
#
# doc2 = doc2.loc[doc2['Flag'] != 'X']
# plt.close()
#
# names = ['I7N', 'P18','P16N']
#
# cruise = []
# means = []
# stds = []
# for i in range(0, len(names)):
#
#     # grab the DOC from each cruise
#     a = doc.loc[doc['Ocean Region'] == names[i]]
#
#     # grab only the deep ocean
#     a = a.loc[a['Depth'] >= 1500]
#     means.append(np.nanmean(a['Value']))
#     stds.append(np.nanstd(a['Value']))
#     cruise.append(names[i])
#
#     # plt.scatter(a['corr DEL 14C'], a['Value'])
#     # plt.show()
#
# dfnew = pd.DataFrame({"Cruise": cruise, "Mean": means, "STD": stds})
# plt.errorbar(cruise, means, yerr=stds)
# plt.plot(cruise, means)
# plt.scatter(cruise, means)
# plt.title('Mean DOC 13C <1500 m; progressive reworking of DOM?')
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results4.png', dpi=300, bbox_inches="tight")
# plt.close()
#
#
# """
# Trying to plot individual sites of interest, DOC vs SPE
# """
# doc = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\bulkDOCdatabase.xlsx').dropna(subset='Value')
# doc = doc.replace('P16N.2', 'P16N')
# # set up the figure
# fig = plt.figure(1, figsize=(8, 8))
# gs = gridspec.GridSpec(2, 6)
# gs.update(wspace=1, hspace=1)
#
# xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
# doc2 = df.loc[df['Station'] == 205]
# plt.scatter(doc2['13C_corr'], doc2['Weighted Average Depth'], color=c2, label='SPE-DOC')
# doc2 = doc.loc[doc['Station'] == 206]
# plt.scatter(doc2['Value'], doc2['Depth'], color=c1, label='Total DOC')
# plt.plot(doc2['Value'], doc2['Depth'], color=c1)
# plt.title('P18 Stn. 205-206')
# plt.ylim(4000, 0)
# plt.ylabel('Depth (m)', fontsize=12)
#
# xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
# doc2 = df.loc[df['Station'] == 116]
# plt.scatter(doc2['13C_corr'], doc2['Weighted Average Depth'], color=c2, label='SPE-DOC')
# doc2 = doc.loc[doc['Station'] == 117]
# plt.scatter(doc2['Value'], doc2['Depth'], color=c1, label='Total DOC')
# plt.plot(doc2['Value'], doc2['Depth'], color=c1)
# plt.ylim(max(doc2['Depth'])+50, min(doc2['Depth'])-50)
# plt.title('P18 Stn. 116-117')
# plt.ylim(4000, 0)
# plt.xlabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)', fontsize=12)
#
#
# xtr_subsplot = fig.add_subplot(gs[0:2, 4:6])
# doc2 = df.loc[df['Station'] == 150]
# plt.scatter(doc2['13C_corr'], doc2['Weighted Average Depth'], color=c2, label='SPE-DOC')
# doc2 = doc.loc[doc['Station'] == 151]
# plt.scatter(doc2['Value'], doc2['Depth'], color=c1, label='Total DOC')
# plt.plot(doc2['Value'], doc2['Depth'], color=c1)
# plt.title('P18 Stn. 150-151')
# plt.ylim(4000, 0)
# plt.legend()
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Supp2.png', dpi=300, bbox_inches="tight")
#
#
# """
# I want to plot total DOC and SPE-DOC 13C vs temp, but to do so, I need to associate the weighted average depth with the CTDTMP. I'll
# try to write a quick code to do this, rather than plug them into the data sheets.
#
# First, I'm going to reimport the bulk DOC data from the DOC database, sheet New, which contains the data from Ellen's lab
# that also resides in my Google Drive from UCI/Field Work/each cruise name/Hydrography
# """
#
# doc = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\bulkDOCdatabase.xlsx', sheet_name='New').dropna(subset='Value')
# doc = doc.loc[doc['Flag'] != 'X']
#
# #
