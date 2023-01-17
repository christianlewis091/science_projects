"""
Trying to understand how Jacob's first small samples worked in the new reactors
TW:3450

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


ox = pd.read_csv(r'C:\Users\clewis\IdeaProjects\GNS\smalls_at_GNS\data\ox_1_hist.csv').dropna(subset='Ratio to standard').reset_index(drop=True)
kap = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\smalls_at_GNS\data\kapuni_hist.xlsx').dropna(subset='Ratio to standard').reset_index(drop=True)

# only take data from the last 100 wheels, and less than 0.5 mg
wheel_min = 100
size_max = 0.6
ox = ox.loc[(ox['TW'] > (3450-wheel_min)) & (ox['wtgraph'] < size_max)]
kap = kap.loc[kap['TW'] > (3450-wheel_min)]

# I have to adjust the output from RLIMS, because it comes out as 87665.0, instead of 87765, and leads to problems
tp_as_str = []
for i in range(0, len(ox)):
    row = ox.iloc[i]
    tp_as_str.append(int(row['TP']))
ox['TP_adjusted'] = tp_as_str

tp_as_str = []
for i in range(0, len(kap)):
    row = kap.iloc[i]
    tp_as_str.append(int(row['TP']))
kap['TP_adjusted'] = tp_as_str


ox_average, ox_std = np.average(ox['Ratio to standard']), np.std(ox['Ratio to standard'])
kap_average, kap_std = np.average(kap['Ratio to standard']), np.std(kap['Ratio to standard'])


# make a Dataframe for just the test data
ox_result = ox.loc[ox['TP_adjusted'].isin([85758, 85748, 85776])]
kap_result = kap.loc[kap['TP_adjusted'].isin([85791, 85792, 85793])]


# Make a plot

fig = plt.figure(4, figsize=(10, 5))
gs = gridspec.GridSpec(2, 4)
gs.update(wspace=.5, hspace=.25)

# plot the OX-1
xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.axhline(ox_average)
plt.scatter(ox['TW'], ox['Ratio to standard'])
plt.scatter(ox_result['TW'], ox_result['Ratio to standard'], color='red')
plt.fill_between(ox['TW'], ox_average+ox_std, ox_average-ox_std, color='black', alpha=.15, edgecolor=None)
plt.fill_between(ox['TW'], ox_average+2*ox_std, ox_average-2*ox_std, color='black', alpha=.1, edgecolor=None)
plt.xlabel('TW (Wheel Number)')
plt.ylabel('Ratio to Standard')
plt.title('OX1 CO2 Flask')

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.axhline(kap_average)
plt.scatter(kap['TW'], kap['Ratio to standard'])
plt.scatter(kap_result['TW'], kap_result['Ratio to standard'], color='red')
plt.fill_between(kap['TW'], kap_average+kap_std, kap_average-kap_std, color='black', alpha=.15, edgecolor=None)
plt.fill_between(kap['TW'], kap_average+2*kap_std, kap_average-2*kap_std, color='black', alpha=.1, edgecolor=None)
plt.xlabel('TW (Wheel Number)')
plt.title('Kapuni')

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/smalls_at_GNS/output/test1.png',
            dpi=300, bbox_inches="tight")
plt.close()

# Make a plot

fig = plt.figure(4, figsize=(10, 5))
gs = gridspec.GridSpec(2, 4)
gs.update(wspace=.5, hspace=.25)

# plot the OX-1
xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.axhline(ox_average)
plt.scatter(ox['wtgraph'], ox['Ratio to standard'])
plt.scatter(ox_result['wtgraph'], ox_result['Ratio to standard'], color='red')
plt.fill_between(ox['TW'], ox_average+ox_std, ox_average-ox_std, color='black', alpha=.15, edgecolor=None)
plt.fill_between(ox['TW'], ox_average+2*ox_std, ox_average-2*ox_std, color='black', alpha=.1, edgecolor=None)
plt.xlabel('TW (Wheel Number)')
plt.ylabel('Ratio to Standard')
plt.title('OX1 CO2 Flask')

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.axhline(kap_average)
plt.scatter(kap['wtgraph'], kap['Ratio to standard'])
plt.scatter(kap_result['wtgraph'], kap_result['Ratio to standard'], color='red')
plt.fill_between(kap['TW'], kap_average+kap_std, kap_average-kap_std, color='black', alpha=.15, edgecolor=None)
plt.fill_between(kap['TW'], kap_average+2*kap_std, kap_average-2*kap_std, color='black', alpha=.1, edgecolor=None)
plt.xlabel('TW (Wheel Number)')
plt.title('Kapuni')

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/smalls_at_GNS/output/test2.png',
            dpi=300, bbox_inches="tight")
plt.close()

