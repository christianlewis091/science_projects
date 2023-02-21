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
import matplotlib.patches as mpatches

# read in the SPE-DOC data, called "df" for DataFrame
df = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\Cleaned_data.xlsx').dropna(subset='Raw d13C')

# read in the total DOC data, called "doc" for dissloved organic carbon
doc = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\bulkDOCdatabase.xlsx', sheet_name='ForMerge').dropna(
    subset='del13C')
doc = doc.loc[doc['Flag'] != 'X']

# make sure all the cruise names are the same for both the DOC and SPE-DOC databases.
# In SPE-DOC data, its 'P16', 'P18', and 'IO7'.
# doc = doc.replace('I7N', 'IO7N')

# read in the hydrographic data
p18 = pd.read_csv('H:\Science\Datasets\Hydrographic\P18_2016.csv', skiprows=174).dropna(subset='DATE')
P18 = pd.read_csv('H:\Science\Datasets\Hydrographic\P18_2016.csv', skiprows=174).dropna(subset='DATE')
P16N = pd.read_csv('H:\Science\Datasets\Hydrographic\P16N_2015.csv', skiprows=119).dropna(subset='DATE')
IO7N = pd.read_csv('H:\Science\Datasets\Hydrographic\IO7N_2018.csv', skiprows=131).dropna(subset='DATE')
P18_1994 = pd.read_csv('H:\Science\Datasets\Hydrographic\P18_1994.csv', skiprows=10).dropna(subset='DATE')

# Lets concat all the cruises together into one file...
P18['Cruise'] = 'P18'
P16N['Cruise'] = 'P16N'
IO7N['Cruise'] = 'IO7N'
go_ship = pd.concat([P18, P16N, IO7N]).reset_index(drop=True)

# And merge the DOC data into it.
merged1 = pd.merge(go_ship, doc, how='outer')
merged2 = pd.merge(go_ship, doc)

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
cleaned_df = cleaned_df.dropna(subset='SPE 13C')


"""
As of this point the data has been associated with total DOC data, and the GO-SHIP data. We will still add a few changes
to the data, so we will re-publish the final excel sheet at the end of the file. For now we'll carry on with some analysis,
using the "cleaned_df" as the data from here on out. 

"""

"""
First order of business: do the mass-balance calculation to remove Cex
"""
# need to calculate the mass-balance corrected 13C value for the small contribution from the PPL cartridge
# the relative abundances of Cex vs sample is defined from 9 ug Cex contribution from my first paper.

# now the mass balance
# define a number for the 13C of Cex
cex_13C = -30  # typical value for petroleum 13C
cleaned_df['SPE 13C Corrected'] = (cleaned_df['SPE 13C'] - (cex_13C*cleaned_df['X_blank']) ) / cleaned_df['X_sample']

# and now the error propogation for the 13C correction
# for the multiplied term
a = np.sqrt((0.2/cex_13C)**2 + (cleaned_df['X_blank_err']/cleaned_df['X_blank'])**2)

# and now the whole numerator
b = np.sqrt(a**2 + cleaned_df['SPE 13C err']**2)
value = (cleaned_df['SPE 13C'] - (cex_13C*cleaned_df['X_blank']))

# and now the whole thing
cleaned_df['SPE 13C Corrected Err'] = np.sqrt((b/value)**2 + (cleaned_df['X_sample_err']/cleaned_df['X_sample'])**2)
# in the end, the error propogation makes the errors too small, so I'm putting the 0.2 back in

# how much does the mass balance actually change the value? What is the percent change?
cleaned_df['pct_ch'] = ((cleaned_df['SPE 13C'] - cleaned_df['SPE 13C Corrected']) / cleaned_df['SPE 13C']) * 100
# print(max(df['pct_ch']))


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
cruise = []
dep = []
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
    cruise.append(names[i])
    dep.append('S')
    descrip_doc.append(f'Surface {names[i]}')

    bulk_av.append(np.average(a_d['del13C']))
    bulk_std.append(np.std(a_d['del13C']))
    cruise.append(names[i])
    dep.append('D')
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
                        "Nonretained 13C": nonret, "error4": nonret_error, "N": count, "Cruise": cruise, "Dep": dep})


"""
Ellen asked me to recreate her Figure S6 from her 2021 paper, which is a plot of DOC vs He from the 1994 P18 cruise. 
I'll see if I can associate my SPE data with the closest stations and depths where there is He data from the 1994 P18 cruise
"""

# we only want to see the P18 data for this section...
cleaned_df_chop = cleaned_df.loc[cleaned_df['Cruise'] == 'P18']

# grab only where there's real data (remove fillers (-999))
P18_1994 = P18_1994.loc[P18_1994['DELHE3'] != '-999']

#we'll have to do a similar thing where I create a station index / merge index, based on the closest values.
station_index = []
depth_index = []
final_string = []
# while looping through the SPE data, what's the closest station from P18 1994 where there's He data?
for i in range(0, len(cleaned_df_chop)):
    row = cleaned_df_chop.iloc[i]
    lat = row['LATITUDE']
    spe_depth = row['Weighted Average Depth'].astype(float)


    # what's the closest station from P18 1994?
    B = np.asarray(P18_1994['LATITUDE'])
    idx_station = (np.abs(B - lat)).argmin()
    # what's the closest depth from this station on the weighted average depth?
    # first, isolate all data with the latitudes we just found above
    D = P18_1994.loc[P18_1994['LATITUDE'] == B[idx_station]]
    # now grab the depth data
    D_2 = D['CTDPRS'].astype(float)
    D_2 = np.asarray(D_2)
    idx_depth = (np.abs(D_2 - spe_depth)).argmin()

    station_index.append(B[idx_station])
    depth_index.append(D_2[idx_depth])
    stringies = f"{B[idx_station]}+{D_2[idx_depth]}"
    final_string.append(stringies)

# Now I'll add these values from the P18 1994 cruise to my SPE-DOC data
cleaned_df_chop['P18 1994 Latitude'] = station_index
cleaned_df_chop['P19 1994 Depth'] = depth_index
cleaned_df_chop['Helium Merge String'] = final_string

# I have to also add a similar merge string onto the P18 1994 data, and then I can merge
final_string2 = []
for i in range(0, len(P18_1994)):
    row = P18_1994.iloc[i]
    lat = row['LATITUDE']
    ctdprs = row['CTDPRS']
    stringies = f"{lat}+{ctdprs}"
    final_string2.append(stringies)

P18_1994['Helium Merge String'] = final_string2
HeliumMerge = pd.merge(P18_1994, cleaned_df_chop, on='Helium Merge String')
# only take data where the difference in depths is less than X
x = 150
# HeliumMerge['DeltaDepths'] = np.abs(HeliumMerge['CTDPRS_x'].astype(float) - HeliumMerge['CTDPRS_y'].astype(float))
# HeliumMerge = HeliumMerge.loc[HeliumMerge['DeltaDepths'] < x]



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
    plt.scatter(curr['SPE-14C'], curr['SPE 13C Corrected'], color=color, label=str(cruises[i]), marker=symbols)
# specify the location of (left,bottom),width,height
rect=mpatches.Rectangle((-620, -23.75), 140, 0.72,
                        fill = False,
                        color = "black",
                        linewidth = 0.5, alpha=0.5)
plt.gca().add_patch(rect)
plt.ylim(-24, -21.75)
plt.ylabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)', fontsize=14)
plt.title('Surface (0-200 m)', fontsize=14)
plt.xlabel('SPE-DOC \u0394$^1$$^4$C (\u2030)', fontsize=14)
plt.legend()

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
for i in range(0, 3):
    curr = d.loc[d['Cruise'] == cruises[i]]
    color = colors[i]
    symbols = symbol[i]
    plt.errorbar(curr['SPE-14C'], curr['SPE 13C Corrected'], xerr=curr['SPE-14C err'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)
    # plt.scatter(curr['SPE-14C'], curr['SPE 13C Corrected'], color=color, label=str(cruises[i]), marker=symbols)
    # plt.errorbar(curr['Latitude'], curr['Raw d13C'], yerr=0.2, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.25)
rect=mpatches.Rectangle((-610, -24), 72, 0.4,
                            fill = False,
                            color = "black",
                            linewidth = 0.5, alpha=0.5)
plt.gca().add_patch(rect)
rect1=mpatches.Rectangle((-680, -23.3), 120, 0.5,
                        fill = False,
                        color = "black",
                        linewidth = 0.5, alpha=0.5)
plt.gca().add_patch(rect1)
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
"""
# set up the figure
fig = plt.figure(1, figsize=(8, 8))
gs = gridspec.GridSpec(6, 5)
gs.update(wspace=1, hspace=1)

# first subplot is all the data together.
xtr_subsplot = fig.add_subplot(gs[0:6, 0:3])
names = np.unique(doc['Cruise'])
colors = ['#d73027','#fc8d59','#4575b4']
markers = ['o','^','D','s']
#
for i in range(0, len(names)):
    cruise = doc.loc[doc['Cruise'] == names[i]]
    plt.scatter(cruise['del13C'], (cruise['Depth']), color=colors[i], marker=markers[i], label=str(names[i] + ' Total DOC'))
plt.scatter(cleaned_df['SPE 13C Corrected'], cleaned_df['Weighted Average Depth'], color='black', label='SPE-DOC', marker='s')
plt.ylim(max(cruise['Depth']), min(cruise['Depth']))
plt.ylabel('Depth (m)', fontsize=12)
plt.xlabel('\u03B4$^1$$^3$C (\u2030)', fontsize=12)
plt.legend()

# next subplot is just the P18 data
xtr_subsplot = fig.add_subplot(gs[0:2, 3:5])
plt.title('P18, 2016')
p18_doc = doc.loc[doc['Cruise'] == 'P18']
p18_spe = cleaned_df.loc[(cleaned_df['Cruise'] == 'P18')]
#
plt.errorbar(p18_doc['del13C'], (p18_doc['Depth']), yerr=p18_doc['del13C_err'], fmt=markers[2], color=colors[2], ecolor=colors[2], elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_doc['del13C'], p18_doc['Depth'], marker=markers[2], color=colors[2], label='Total DOC')
plt.errorbar(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), yerr=p18_spe['SPE 13C Corrected Err'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), marker='s', color='black', label='SPE-DOC')
plt.ylim(max(cruise['Depth']), min(cruise['Depth']))
plt.xlim(-24, -20)


xtr_subsplot = fig.add_subplot(gs[2:4, 3:5])
plt.title('P16N, 2015')
p18_doc = doc.loc[doc['Cruise'] == 'P16N']
p18_spe = cleaned_df.loc[(cleaned_df['Cruise'] == 'P16N')]
#
plt.errorbar(p18_doc['del13C'], (p18_doc['Depth']), yerr=p18_doc['del13C_err'], fmt=markers[1], color=colors[1], ecolor=colors[1], elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_doc['del13C'], p18_doc['Depth'], marker=markers[1], color=colors[1], label='Total DOC')
plt.errorbar(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), yerr=p18_spe['SPE 13C Corrected Err'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), marker='s', color='black', label='SPE-DOC')
plt.ylim(max(cruise['Depth']), min(cruise['Depth']))
plt.xlim(-24, -20)

xtr_subsplot = fig.add_subplot(gs[4:6, 3:5])
plt.title('IO7N, 2018')
p18_doc = doc.loc[doc['Cruise'] == 'IO7N']
p18_spe = cleaned_df.loc[(cleaned_df['Cruise'] == 'IO7N')]
#
plt.errorbar(p18_doc['del13C'], (p18_doc['Depth']), yerr=p18_doc['del13C_err'], fmt=markers[0], color=colors[0], ecolor=colors[0], elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_doc['del13C'], p18_doc['Depth'], marker=markers[0], color=colors[0], label='Total DOC')
plt.errorbar(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), yerr=p18_spe['SPE 13C Corrected Err'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_spe['SPE 13C Corrected'], (p18_spe['Weighted Average Depth']), marker='s', color='black', label='SPE-DOC')
plt.ylim(max(cruise['Depth']), min(cruise['Depth']))
plt.xlabel('\u03B4$^1$$^3$C (\u2030)', fontsize=12)
plt.xlim(-24, -20)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results3.png', dpi=300, bbox_inches="tight")
plt.close()


#
"""
Based on my conversation with Ellen and Brett on 9/2/23, how does total DOC change with latitude? Do we see progressive reworking?
"""
#
#
names = ['IO7N', 'P18','P16N']

cruise = []
means = []
stds = []
depths_int = []
for i in range(0, len(names)):

    # grab the DOC from each cruise

    a = merged2.loc[merged2['Cruise'] == names[i]]
    print(len(a))
    a['CTDPRS'] = a['CTDPRS'].astype(float)


    # grab only the deep ocean
    b = a.loc[(a['CTDPRS'] <= 4000) & (a['CTDPRS'] >= 2000)]
    print(len(b))
    means.append(np.nanmean(b['del13C']))
    stds.append(np.nanstd(b['del13C']))
    cruise.append(names[i])
    depths_int.append('Deep')

    # grab mid depths ocean
    c = a.loc[(a['CTDPRS'] <= 2000) & (a['CTDPRS'] >= 500)]
    print(c)
    means.append(np.nanmean(c['del13C']))
    stds.append(np.nanstd(c['del13C']))
    cruise.append(names[i])
    depths_int.append('Middepth')
    #
    # grab surface
    d = a.loc[(a['CTDPRS'] <= 500) & (a['CTDPRS'] >= 0)]
    print(d)
    means.append(np.nanmean(d['del13C']))
    stds.append(np.nanstd(d['del13C']))
    cruise.append(names[i])
    depths_int.append('Surface')

#
dfnew = pd.DataFrame({"Cruise": cruise, "Mean": means, "STD": stds, "Depth Call": depths_int})
print(dfnew)

words = ['Surface','Middepth','Deep']
for word in words:
    df_inuse = dfnew.loc[dfnew["Depth Call"] == word]
    cruise = df_inuse['Cruise']
    means = df_inuse['Mean']
    stds = df_inuse['STD']
    name1 = df_inuse['Depth Call']
    for i in range(0, 3):
        plt.errorbar(cruise, means, yerr=stds)
        plt.scatter(cruise, means, label=name1)


plt.title('Mean DOC 13C <1500 m; progressive reworking of DOM?')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results4.png', dpi=300, bbox_inches="tight")
# plt.show()
plt.close()
#
#
"""
Trying to plot individual sites of interest, DOC vs SPE
"""

# set up the figure
fig = plt.figure(1, figsize=(8, 8))
gs = gridspec.GridSpec(2, 6)
gs.update(wspace=1, hspace=1)
#
xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
data = cleaned_df.loc[cleaned_df['STNNBR'] == 205].reset_index(drop=True)
plt.scatter(data['SPE 13C Corrected'], data['Weighted Average Depth'], color=c2, label='SPE-DOC')

doc2 = doc.loc[doc['STNNBR'] == 206].reset_index(drop=True)
plt.scatter(doc2['del13C'], doc2['Depth'], color=c1, label='Total DOC')
plt.title('P18 Stn. 205-206')
plt.ylim(4000, 0)
plt.ylabel('Depth (m)', fontsize=12)
plt.legend()
#
xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
data = cleaned_df.loc[cleaned_df['STNNBR'] == 116].reset_index(drop=True)
plt.scatter(data['SPE 13C Corrected'], data['Weighted Average Depth'], color=c2, label='SPE-DOC')

doc2 = doc.loc[doc['STNNBR'] == 117].reset_index(drop=True)
plt.scatter(doc2['del13C'], doc2['Depth'], color=c1, label='Total DOC')
plt.title('P18 Stn. 116-117')
plt.ylim(4000, 0)

xtr_subsplot = fig.add_subplot(gs[0:2, 4:6])
data = cleaned_df.loc[cleaned_df['STNNBR'] == 150].reset_index(drop=True)
plt.scatter(data['SPE 13C Corrected'], data['Weighted Average Depth'], color=c2, label='SPE-DOC')
doc2 = doc.loc[doc['STNNBR'] == 151].reset_index(drop=True)
plt.scatter(doc2['del13C'], doc2['Depth'], color=c1, label='Total DOC')
plt.title('P18 Stn. 150-151')
plt.ylim(4000, 0)
plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Supp2.png', dpi=300, bbox_inches="tight")
plt.close()

"""
Do SPE-DOC and total DOC change with temperature? 
"""

s = cleaned_df.loc[cleaned_df['SorD'] == 'Surface']
d = cleaned_df.loc[cleaned_df['SorD'] == 'Deep']

plt.errorbar(s['CTDTMP'], s['SPE 13C Corrected'], label='Surface SPE-DOC', yerr=s['SPE 13C Corrected Err'],  fmt=markers[0], color=colors[0], ecolor=colors[0], elinewidth=1, capsize=2, alpha = 1)
plt.errorbar(d['CTDTMP'], d['SPE 13C Corrected'], label='Deep SPE-DOC', yerr=d['SPE 13C Corrected Err'],  fmt=markers[1], color=colors[1], ecolor=colors[1], elinewidth=1, capsize=2, alpha = 1)
plt.legend()
plt.xlabel('CTD Temperature (C)')
plt.ylabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Supp3.png', dpi=300, bbox_inches="tight")
plt.close()


"""
Does Helium data track with SPE? 
"""

# # fig = plt.figure(1, figsize=(8, 8))
s = HeliumMerge.loc[HeliumMerge['SorD'] == 'Surface']
d = HeliumMerge.loc[HeliumMerge['SorD'] == 'Deep']
# plt.errorbar(s['DELHE3'].astype(float), s['SPE 13C Corrected'].astype(float))
# plt.errorbar(d['DELHE3'].astype(float), d['SPE 13C Corrected'].astype(float))

plt.xlabel('CTD Temperature (C)')
plt.ylabel('SPE-DOC 13C')
plt.errorbar(s['DELHE3'].astype(float), s['SPE 13C Corrected'].astype(float), label='Surface SPE-DOC',yerr=s['SPE 13C Corrected Err'],  fmt=markers[0], color=colors[0], ecolor=colors[0], elinewidth=1, capsize=2, alpha = 1)
plt.errorbar(d['DELHE3'].astype(float), d['SPE 13C Corrected'].astype(float), label='Deep SPE-DOC', yerr=d['SPE 13C Corrected Err'],  fmt=markers[1], color=colors[2], ecolor=colors[2], elinewidth=1, capsize=2, alpha = 1)
plt.legend()
plt.xlabel('\u03B4He3')
# plt.xticks(s['DELHE3'], s['SPE 13C Corrected'], rotation='vertical')
plt.ylabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Supp4.png', dpi=300, bbox_inches="tight")
plt.close()


"""
Does Bulk DOC13C also increase toward the OMZ?  
"""

df_1 = merged2.loc[merged2['SECT_ID'] == 'IO7N']
df_1 = df_1.loc[df_1['CTDPRS'].astype(float) < 200]

cleaned_df_1 = cleaned_df.loc[cleaned_df['Cruise'] == 'IO7N']
cleaned_df_1 = cleaned_df_1.loc[cleaned_df_1['SorD'] == 'Surface']

plt.errorbar(cleaned_df_1['LATITUDE'], cleaned_df_1['SPE 13C Corrected'], label='Surface SPE-DOC', yerr=0.2,  fmt=markers[0], color=colors[0], ecolor=colors[0], elinewidth=1, capsize=2, alpha = 1)
plt.errorbar(df_1['LATITUDE'], df_1['del13C'], label='Total DOC', yerr=df_1['del13C_err'],  fmt=markers[1], color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
plt.legend()
plt.xlabel('Latitude')
plt.ylabel('\u03B4$^1$$^3$C (\u2030)')

plt.title('Does total DOC 13C increase toward the Indian Ocean OMZ as well/')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Supp5.png', dpi=300, bbox_inches="tight")
plt.close()


"""
testing a new plot
"""
letter = ['S','D']
x = ['Surface','Deep']
a = [1, 0.5]

for i in range(0, len(letter)):
    mp1 = results.loc[results['Dep'] == letter[i]]
    plt.errorbar(mp1['Cruise'], mp1['SPE-DOC 13C'], yerr=mp1['error2'], alpha=a[i], fmt='s', color='black', ecolor='black', elinewidth=1, capsize=2)
    plt.scatter(mp1['Cruise'], mp1['SPE-DOC 13C'], alpha=a[i], color='black', label=f'SPE-DOC {x[i]}', marker='s')
    plt.plot(mp1['Cruise'], mp1['SPE-DOC 13C'], alpha=a[i], color='black')

    plt.errorbar(mp1['Cruise'], mp1['DOC 13C'], yerr=mp1['error2'], alpha = a[i], fmt='D', color='black', ecolor='black', elinewidth=1, capsize=2)
    plt.scatter(mp1['Cruise'], mp1['DOC 13C'], alpha = a[i], color='black', label=f'Total DOC {x[i]}', marker='D')
    plt.plot(mp1['Cruise'], mp1['DOC 13C'], alpha=a[i], color='black')
plt.xlabel('GO-SHIP Transect')
plt.ylabel('Mean \u03B4$^1$$^3$C (\u2030)')
plt.title('')
plt.legend()
plt.title('Mean \u03B4$^1$$^3$C (\u2030) by Basin')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Supp6.png', dpi=300, bbox_inches="tight")
plt.close()
#
# with pd.ExcelWriter(r'C:\Users\clewis\IdeaProjects\GNS\UCI_13C\output\output.xlsx') as writer:
#     cleaned_df.to_excel(writer, sheet_name='SPE Data')
#     results.to_excel(writer, sheet_name='SPE Results Summary')
#     HeliumMerge.to_excel(writer, sheet_name='SPEvP18 1994 He')
#     merged2.to_excel(writer, sheet_name='DOC Data')
#     dfnew.to_excel(writer, sheet_name='DOC Results')
#



