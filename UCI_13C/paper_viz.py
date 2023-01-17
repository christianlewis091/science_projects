import doctest

from data_cleaning import *

from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec




"""

The first results figure of the paper

"""
s = df.loc[df['SorD'] == 'Surface']
d = df.loc[df['SorD'] == 'Deep']

# https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3
# Skyblue to distant mountain green

c1, c2, c3 = '#d73027', '#fdae61', '#1c9099'

fig = plt.figure(1, figsize=(10, 8))
gs = gridspec.GridSpec(3, 4)
gs.update(wspace=.25, hspace=.35)

cruises = ['P16', 'P18', 'IO7']
colors = [c1, c2, c3 ]
symbol = ['o','x','^']

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
for i in range(0, 3):
    curr = s.loc[s['Cruise'] == cruises[i]]
    color = colors[i]
    symbols = symbol[i]
    plt.errorbar(curr['Latitude'], curr['13C_corr'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)
    plt.scatter(curr['Latitude'], curr['13C_corr'], color=color, label=str(cruises[i]), marker=symbols)
    # plt.errorbar(curr['Latitude'], curr['Raw d13C'], yerr=0.2, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.25)

plt.ylim(-24, -21.75)
plt.xlim(-60, 60)
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
plt.title('Deep (2000-4000 m)', fontsize=14)
plt.yticks([], [])
plt.xlabel('Latitude (N)', fontsize=14)
plt.xlim(-60, 60)


p18 = p18[['LATITUDE','DEPTH']].drop_duplicates(keep='first').reset_index(drop=True).astype(float)
p18['DEPTH'] = p18['DEPTH']*-1
xtr_subsplot = fig.add_subplot(gs[2:3, 0:2])
plt.plot(p18['LATITUDE'], p18['DEPTH'], color=color, label='P18 Bottom Depth')
plt.xlim(-60, 60)
xtr_subsplot = fig.add_subplot(gs[2:3, 2:4])
plt.plot(p18['LATITUDE'], p18['DEPTH'], color=color, label='P18 Bottom Depth')
plt.legend()
plt.xlim(-60, 60)
plt.yticks([], [])

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results1.png', dpi=95, bbox_inches="tight")
plt.close()

"""

SPE 13C vs 14C

"""

fig = plt.figure(1, figsize=(10, 5))
gs = gridspec.GridSpec(2, 4)
gs.update(wspace=.1, hspace=.35)

cruises = ['P16', 'P18', 'IO7']
colors = [c1, c2, c3 ]
symbol = ['o','x','^']

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
for i in range(0, 3):
    curr = s.loc[s['Cruise'] == cruises[i]]
    color = colors[i]
    symbols = symbol[i]
    plt.errorbar(curr['Corrected 14C with duplicates averaged'], curr['13C_corr'], xerr=curr['Unnamed: 52'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)


plt.ylim(-24, -21.75)
plt.ylabel('SPE-DOC \u03B4$^1$$^3$C (\u2030)', fontsize=14)
plt.title('Surface (0-200 m)', fontsize=14)
plt.xlabel('SPE-DOC \u0394$^1$$^4$C (\u2030)', fontsize=14)


xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
for i in range(0, 3):
    curr = d.loc[d['Cruise'] == cruises[i]]
    color = colors[i]
    symbols = symbol[i]
    plt.errorbar(curr['Corrected 14C with duplicates averaged'], curr['13C_corr'], xerr=curr['Unnamed: 52'], yerr=0.2, fmt=symbols, color=color, ecolor=color, elinewidth=1, capsize=2, alpha = 1)
    plt.scatter(curr['Corrected 14C with duplicates averaged'], curr['13C_corr'], color=color, label=str(cruises[i]), marker=symbols)
    # plt.errorbar(curr['Latitude'], curr['Raw d13C'], yerr=0.2, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.25)
plt.legend()
plt.ylim(-24, -21.75)
plt.title('Deep (2000-4000 m)', fontsize=14)
plt.yticks([], [])
plt.xlabel('SPE-DOC \u0394$^1$$^4$C (\u2030)', fontsize=14)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results2.png', dpi=95, bbox_inches="tight")
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
names = np.unique(doc['Ocean Region'])
print(len(names))
print(doc.columns)
colors = ['#d73027','#fc8d59','#91bfdb','#4575b4']
markers = ['o','x','^','D','s']

for i in range(0, len(names)):
    cruise = doc.loc[doc['Ocean Region'] == names[i]]
    plt.scatter(cruise['Value'], (cruise['Depth']*-1), color=colors[i], marker=markers[i], label=str(names[i] + ' Total DOC'))
plt.scatter(df[['13C_corr']], df['Weighted Average Depth'] * -1, color='black', label='SPE-DOC')
plt.legend()

# next subplot is just the P18 data
xtr_subsplot = fig.add_subplot(gs[0:2, 3:5])
plt.title('P18, 2016')
p18_doc = doc.loc[doc['Ocean Region'] == 'P18']
p18_spe = df.loc[(df['Cruise'] == 'P18')]

plt.errorbar(p18_doc['Value'], (p18_doc['Depth']*-1), yerr=p18_doc['±'], fmt=markers[3], color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_doc['Value'], p18_doc['Depth']*-1, marker=markers[3], color=colors[3], label='Total DOC')
plt.errorbar(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']*-1), yerr=p18_spe['Unnamed: 52'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']*-1), marker='o', color='black', label='SPE-DOC')



xtr_subsplot = fig.add_subplot(gs[2:4, 3:5])
plt.title('P16N, 2015')
p18_doc = doc.loc[doc['Ocean Region'] == 'P16N']
p18_spe = df.loc[(df['Cruise'] == 'P16')]

plt.errorbar(p18_doc['Value'], (p18_doc['Depth']*-1), yerr=p18_doc['±'], fmt=markers[2], color=colors[2], ecolor=colors[2], elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_doc['Value'], p18_doc['Depth']*-1, marker=markers[2], color=colors[2], label='Total DOC')
plt.errorbar(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']*-1), yerr=p18_spe['Unnamed: 52'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']*-1), marker='o', color='black', label='SPE-DOC')


xtr_subsplot = fig.add_subplot(gs[4:6, 3:5])
plt.title('IO7N, 2018')
p18_doc = doc.loc[doc['Ocean Region'] == 'I7N']
p18_spe = df.loc[(df['Cruise'] == 'IO7')]

plt.errorbar(p18_doc['Value'], (p18_doc['Depth']*-1), yerr=p18_doc['±'], fmt=markers[0], color=colors[0], ecolor=colors[0], elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_doc['Value'], p18_doc['Depth']*-1, marker=markers[0], color=colors[0], label='Total DOC')
plt.errorbar(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']*-1), yerr=p18_spe['Unnamed: 52'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 1)
plt.scatter(p18_spe['13C_corr'], (p18_spe['Weighted Average Depth']*-1), marker='o', color='black', label='SPE-DOC')





plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results3.png', dpi=95, bbox_inches="tight")








