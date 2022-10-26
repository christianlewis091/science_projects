import pandas as pd
import numpy as np
from soar_analysis1 import df_2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

site_array = []
for i in range(0, len(df_2)):
    current_row = df_2.iloc[i]
    if str(current_row['#location']) == 'nan':
        site_array.append(current_row['Site'])
    elif str(current_row['Site']) == 'nan':
        site_array.append(current_row['#location'])
df_2['SiteNew'] = site_array
df_2 = df_2.sort_values(by=['Decimal_date'], ascending=False).reset_index(drop=True)
locs = np.unique(df_2['SiteNew'])
print(locs)

chile = df_2.loc[df_2['Country'] == 0].reset_index(drop=True)
nz = df_2.loc[df_2['Country'] == 1].reset_index(drop=True)
ant = df_2.loc[df_2['Country'] == 2].reset_index(drop=True)

locs1 = np.unique(chile['SiteNew'])
locs2 = np.unique(nz['SiteNew'])
locs3 = np.unique(ant['SiteNew'])
a1, a2, a3, a4, a5, a6 = '#253494', '#7fcdbb', '#2c7fb8', '#c7e9b4', '#41b6c4', '#ffffcc'
c1, c2, c3 = '#ece2f0', '#a6bddb', '#1c9099'
d1, d2 = '#ef8a62', '#67a9cf'
colors = [a1, a2, a3, a4, a5, a6, c1, c2, c3, d1, d2]


fig = plt.figure(figsize=(12, 12))
gs = gridspec.GridSpec(6, 2)
gs.update(wspace=.35, hspace=.25)
xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])

for i in range(0, len(locs1)):
    col = colors[i]
    slice = chile.loc[chile['SiteNew'] == str(locs1[i])]  # grab the first data to plot, based on location
    plt.plot(slice['Decimal_date'], slice['r2_diff_trend'], label='{}'.format(str(locs1[i])), color=col)
    plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], fmt='o', elinewidth=1, capsize=2, alpha=1, label='{}'.format(str(locs1[i])), color=col)
    plt.legend()
    plt.ylim(-25, 15)

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
for i in range(0, len(locs2)):
    col = colors[i]
    slice = nz.loc[nz['SiteNew'] == str(locs2[i])]  # grab the first data to plot, based on location
    plt.plot(slice['Decimal_date'], slice['r2_diff_trend'], label='{}'.format(str(locs2[i])), color=col)
    plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], fmt='o', elinewidth=1, capsize=2, alpha=1, label='{}'.format(str(locs2[i])), color=col)
    plt.legend()
    plt.ylim(-25, 15)

xtr_subsplot = fig.add_subplot(gs[4:6, 0:2])
for i in range(0, len(locs3)):
    col = colors[i]
    slice = ant.loc[ant['SiteNew'] == str(locs3[i])]  # grab the first data to plot, based on location
    plt.plot(slice['Decimal_date'], slice['r2_diff_trend'], label='{}'.format(str(locs3[i])), color=col)
    plt.errorbar(slice['Decimal_date'], slice['r2_diff_trend'], slice['r2_diff_trend_errprop'], fmt='o', elinewidth=1, capsize=2, alpha=1, label='{}'.format(str(locs3[i])), color=col)
    plt.legend()
    plt.ylim(-25, 15)
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot6.png',
            dpi=300, bbox_inches="tight")
plt.close()




















