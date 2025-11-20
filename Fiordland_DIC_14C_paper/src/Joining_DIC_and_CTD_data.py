"""
Now join all data files together:
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# # edited some column names to match up better
# df1= pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2405_DIC_14C_FINAL.xlsx', comment='#')
# df2= pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/S309_DIC_14C_FINAL.xlsx', comment='#', sheet_name='Cleaner')
# df3= pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2505_DIC_14C_FINAL.xlsx', comment='#')
#
# print(df1.columns)
# print(df2.columns)
# print(df3.columns)
#
# df1 = df1[['Cruise Station Name',
#            'Latitude_N_decimal', 'Longitude_E_decimal', 'Bottom Depth (m)',
#            'Depth', 'Sample', 'ID', 'R_number', 'Job', 'wtgraph', 'TW',
#            'TP',
#            'Collection Decimal Date', 'Date Run', 'F_corrected_normed',
#            'F_corrected_normed_error', 'Samples::Sample Description', 'DELTA14C',
#            'DELTA14C_Error', 'delta13C_IRMS', 'delta13C_IRMS_Error']]
#
# df1 = df1.rename(columns={"Latitude_N_decimal": "Lat N",
#                           "Longitude_E_decimal": "Lon E",
#                           'Bottom Depth (m)':"Bottom Depth",
#                           'Depth':"Depth",
#                           'Cruise Station Name':'Station',
#                           })
#
# df2 = df2[['Station', 'Site', 'Date (UTC)', 'Time (UTC)',
#            'Lat N', 'Lon E', 'Niskin', 'Depth', 'Notes ', 'Sound',
#            'Samples::Sample Description', 'TW', 'Date Run',
#            'Description', 'Fraction dated', 'R_number', 'NZA', 'CRA', 'CRA error',
#            'delta13C_IRMS', 'delta13C_IRMS_Error', 'd13C source',
#            'F_corrected_normed', 'F_corrected_normed_error', 'Lab comments',
#            'Pretreatment description', 'DELTA14C', 'DELTA14C_Error',
#            'Collection date']]
#
# df2 = df2.rename(columns={"NZA":"TP"})
#
# df3 = df3[['delta13C_IRMS', 'delta13C_IRMS_Error', 'DELTA14C',
#            'DELTA14C_Error', 'F_corrected_normed', 'F_corrected_normed_error',
#            'ID', 'TP', 'TW', 'wtgraph', 'Samples::Sample ID', 'expedAcronym',
#            'siteCode', 'siteNumber', 'dropNumber', 'dropLongitude',
#            'dropLatitude', 'dropWaterDepth',
#            'bottleDepth','Job::R']]
# #
# df3 = df3.rename(columns={"bottleDepth":"Depth",
#                           "dropWaterDepth":"Bottom Depth",
#                           'Samples::Sample ID':'Samples::Sample Description',
#                           'Job::R':'R_number',
#                           'dropLatitude':'Lat N',
#                           'dropLongitude':'Lon E'})
# #
# df = pd.concat([df1, df2, df3], ignore_index=True)
# df.to_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/DIC_JOINED_FINAL.xlsx')
#

"""
Draw some maps using TIM's packing to make sure data is all labelled properly
"""
import nzgeom.coastlines
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/DIC_JOINED_FINAL_EDITED.xlsx', sheet_name='for_paper')
print(df.columns)
a = df.loc[(df['Expedition'] == 'SFCS2405')]
b = df.loc[(df['Expedition'] == 'S309')]
d = df.loc[(df['Expedition'] == 'SFCS2505')]


c =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.8, 167.2, -45.2))
ax = c.plot(color="lightgray", figsize=(6,8))
siz = 50
ax.scatter(a['Lon E'], a['Lat N'], color='blue', marker='o', label='SFCS2405, May 2024', alpha=0.2, s=siz)
ax.scatter(b['Lon E'], b['Lat N'], color='red', marker='o', label='S309, January 2025', alpha=0.2, s=siz)
ax.scatter(d['Lon E'], d['Lat N'], color='green', marker='o', label='SFCS2505, May 2025', alpha=0.2, s=siz)
plt.legend()
# Show the map
plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/MAP1.png", dpi=300, bbox_inches="tight")
plt.close()


"""
I assigned groups to stations to plot them better for comparison, check for mistakes
"""
grps = np.unique(df['group'])
for i in range(0,len(grps)):
    subset = df.loc[df['group'] == grps[i]]

    c =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.8, 167.2, -45.2))
    ax = c.plot(color="lightgray", figsize=(6,8))
    siz = 50
    ax.scatter(subset['Lon E'], subset['Lat N'], color='blue', marker='o', label=f'{i+1}', alpha=0.2, s=siz)
    plt.legend()
    # plt.show()
    # Show the map
    plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/groupchecks/{i+1}.png", dpi=300, bbox_inches="tight")
    plt.close()

"""
Main figures
"""
"""
Dusky Figure
I'm not sure the best way to go about this but it may be to extract each station title and plot manually to avoid bs 
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(2, 4, figure=fig)  # 2 rows, 4 columns

# Top row: map spans all 4 columns
ax_map = fig.add_subplot(gs[0, :])
c = nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.25, 167.2, -45.5))
c.plot(ax=ax_map, color="lightgray")  # plot directly on existing ax_map


"""
Group 1
"""
g1_1 = df.loc[(df['Station'] == 'DBT001') & (df['Expedition'] == 'SFCS2405')]
ax_map.scatter(g1_1['Lon E'], g1_1['Lat N'], color='black', marker='o', label=f'{i+1}', alpha=0.2, s=siz)

g1_2 = df.loc[(df['Station'] == 'DBT021') & (df['Expedition'] == 'SFCS2505')]
ax_map.scatter(g1_2['Lon E'], g1_2['Lat N'], color='gray', marker='o', label=f'{i+1}', alpha=0.2, s=siz)

# Bottom row: 4 individual subplots
ax1 = fig.add_subplot(gs[1, 0])
ax2 = fig.add_subplot(gs[1, 1])
ax3 = fig.add_subplot(gs[1, 2])
ax4 = fig.add_subplot(gs[1, 3])

ax4.plot(g1_1['∆14C'], g1_1['Depth'], color='black', marker='o') ##### black FOR SFCS2405
ax4.plot(g1_2['∆14C'], g1_2['Depth'], color='gray', marker='o') ##### gray for SFCS2505
ax4.set_ylim(250,-5)

plt.tight_layout()
plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/ongoing.png", dpi=300, bbox_inches="tight")
plt.close()





















