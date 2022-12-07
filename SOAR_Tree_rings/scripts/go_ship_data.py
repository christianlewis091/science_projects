"""
https://cchdo.ucsd.edu/cruise/33RR20160208
See above link for the data
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/4_33RR20160208_hy1.csv', skiprows=166).dropna(subset="DATE")

z = np.array(df['DELC14'], dtype=np.float32)
x = np.array(df['LATITUDE'], dtype=np.float32)
y = np.array(df['CTDPRS'], dtype=np.float32)
o = np.array(df['OXYGEN'], dtype=np.float32)
s = np.array(df['CTDSAL'], dtype=np.float32)

df = pd.DataFrame({"x": x, "y": y, "z": z, "o":o, "s": s})
df = df.loc[df['y'] < 2000]

fig = plt.figure(4, figsize=(7.5, 7.5))
gs = gridspec.GridSpec(9, 2)
gs.update(wspace=.15, hspace=2)

# make first plot
xtr_subsplot = fig.add_subplot(gs[0:3, 0:2])
plt.title('DIC 14C')
df_1 = df.loc[df['z'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['z'], cmap='magma')
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)


xtr_subsplot = fig.add_subplot(gs[3:6, 0:2])
plt.title('Oxygen')
df_1 = df.loc[df['o'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['o'], cmap='magma')
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)

xtr_subsplot = fig.add_subplot(gs[6:9, 0:2])
plt.title('Salinity')
df_1 = df.loc[df['s'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['s'], cmap='magma')
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)


plt.xlabel('Latitude', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/io8_Ctd.png',
            dpi=300, bbox_inches="tight")
plt.close()
#
df2 = df.loc[(df['z'] > -998) & (df['o'] > -998)]
plt.scatter(df2['o'], df2['z'], c=df2['y'], cmap='magma_r')
plt.xlabel('Oxygen')
plt.ylabel('DIC14C')
plt.colorbar()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/io8_Ctd_2.png',
            dpi=300, bbox_inches="tight")
plt.close()


"""
Take 2
"""
# read in all the data from previous IO8 cruises in the Southern Ocean
df_16 = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/4_33RR20160208_hy1.csv', skiprows=166).dropna(subset="DATE")
df_07 = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/33RR20070204_hy1.csv', skiprows=36).dropna(subset="DATE")
df_94 = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/316N145_5_hy1.csv', skiprows=16).dropna(subset="DATE")
# df_03 = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/09AR20030103_hy1.csv', skiprows=7).dropna(subset="DATE")  No DI14C data

xsize = 18
ysize = 9
fig = plt.figure(4, figsize=(7.5, 7.5))
gs = gridspec.GridSpec(ysize, xsize)
gs.update(wspace=.15, hspace=2)

"""
2016 data
"""
z = np.array(df_16['DELC14'], dtype=np.float32)
x = np.array(df_16['LATITUDE'], dtype=np.float32)
y = np.array(df_16['CTDPRS'], dtype=np.float32)
o = np.array(df_16['OXYGEN'], dtype=np.float32)
s = np.array(df_16['CTDSAL'], dtype=np.float32)

df_16 = pd.DataFrame({"x": x, "y": y, "z": z, "o":o, "s": s})
df_1 = df_16.loc[df_16['y'] < 2000]  # find all depths above 2000m

xtr_subsplot = fig.add_subplot(gs[6:9, 0:6])
df_1 = df_1.loc[df_1['z'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['z'], cmap='viridis', vmin=-300, vmax=100)
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)

xtr_subsplot = fig.add_subplot(gs[6:9, 6:12])
df_1 = df_1.loc[df_1['o'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['o'], cmap='magma')
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)

xtr_subsplot = fig.add_subplot(gs[6:9, 12:18])
df_1 = df_1.loc[df_1['s'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['s'], cmap='Blues')
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)

"""
2007 data
"""
z = np.array(df_07['DELC14'], dtype=np.float32)
x = np.array(df_07['LATITUDE'], dtype=np.float32)
y = np.array(df_07['CTDPRS'], dtype=np.float32)
o = np.array(df_07['OXYGEN'], dtype=np.float32)
s = np.array(df_07['CTDSAL'], dtype=np.float32)

df_07 = pd.DataFrame({"x": x, "y": y, "z": z, "o":o, "s": s})
df_1 = df_07.loc[df_07['y'] < 2000]  # find all depths above 2000m

xtr_subsplot = fig.add_subplot(gs[3:6, 0:6])
df_1 = df_1.loc[df_1['z'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['z'], cmap='viridis', vmin=-300, vmax=100)
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)

xtr_subsplot = fig.add_subplot(gs[3:6, 6:12])
df_1 = df_1.loc[df_1['o'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['o'], cmap='magma')
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)

xtr_subsplot = fig.add_subplot(gs[3:6, 12:18])
df_1 = df_1.loc[df_1['s'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['s'], cmap='Blues')
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)

"""
1994 data
"""
z = np.array(df_94['DELC14'], dtype=np.float32)
x = np.array(df_94['LATITUDE'], dtype=np.float32)
y = np.array(df_94['CTDPRS'], dtype=np.float32)
o = np.array(df_94['OXYGEN'], dtype=np.float32)
s = np.array(df_94['CTDSAL'], dtype=np.float32)

df_94 = pd.DataFrame({"x": x, "y": y, "z": z, "o":o, "s": s})
df_1 = df_94.loc[df_94['y'] < 2000]  # find all depths above 2000m

xtr_subsplot = fig.add_subplot(gs[0:3, 0:6])
df_1 = df_1.loc[df_1['z'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['z'], cmap='viridis', vmin=-300, vmax=100)
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)

xtr_subsplot = fig.add_subplot(gs[0:3, 6:12])
df_1 = df_1.loc[df_1['o'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['o'], cmap='magma')
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)

xtr_subsplot = fig.add_subplot(gs[0:3, 12:18])
df_1 = df_1.loc[df_1['s'] > -998]
plt.scatter(df_1['x'], df_1['y'], c=df_1['s'], cmap='Blues')
plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/io8_Ctd_3.png',
            dpi=300, bbox_inches="tight")
plt.close()






















