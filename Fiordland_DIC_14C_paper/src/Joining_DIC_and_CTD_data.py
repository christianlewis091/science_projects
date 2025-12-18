"""
Now join all data files together:
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# edited some column names to match up better
df1= pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2405_DIC_14C_FINAL.xlsx', comment='#')
df2= pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/S309_DIC_14C_FINAL.xlsx', comment='#', sheet_name='Cleaner')
df3= pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2505_DIC_14C_FINAL.xlsx', comment='#')

print(df1.columns)
print(df2.columns)
print(df3.columns)

df1 = df1[['Cruise Station Name',
           'Latitude_N_decimal', 'Longitude_E_decimal', 'Bottom Depth (m)',
           'Depth', 'Sample', 'ID', 'R_number', 'Job', 'wtgraph', 'TW',
           'TP',
           'Collection Decimal Date', 'Date Run', 'F_corrected_normed',
           'F_corrected_normed_error', 'Samples::Sample Description', 'DELTA14C',
           'DELTA14C_Error', 'delta13C_IRMS', 'delta13C_IRMS_Error']]

df1 = df1.rename(columns={"Latitude_N_decimal": "Lat N",
                          "Longitude_E_decimal": "Lon E",
                          'Bottom Depth (m)':"Bottom Depth",
                          'Depth':"Depth",
                          'Cruise Station Name':'Station',
                          })

df2 = df2[['Station', 'Site', 'Date (UTC)', 'Time (UTC)',
           'Lat N', 'Lon E', 'Niskin', 'Depth', 'Notes ', 'Sound',
           'Samples::Sample Description', 'TW', 'Date Run',
           'Description', 'Fraction dated', 'R_number', 'NZA', 'CRA', 'CRA error',
           'delta13C_IRMS', 'delta13C_IRMS_Error', 'd13C source',
           'F_corrected_normed', 'F_corrected_normed_error', 'Lab comments',
           'Pretreatment description', 'DELTA14C', 'DELTA14C_Error',
           'Collection date']]

df2 = df2.rename(columns={"NZA":"TP"})

df3 = df3[['delta13C_IRMS', 'delta13C_IRMS_Error', 'DELTA14C',
           'DELTA14C_Error', 'F_corrected_normed', 'F_corrected_normed_error',
           'ID', 'TP', 'TW', 'wtgraph', 'Samples::Sample ID', 'expedAcronym',
           'siteCode', 'siteNumber', 'dropNumber', 'dropLongitude',
           'dropLatitude', 'dropWaterDepth',
           'bottleDepth','Job::R']]
#
df3 = df3.rename(columns={"bottleDepth":"Depth",
                          "dropWaterDepth":"Bottom Depth",
                          'Samples::Sample ID':'Samples::Sample Description',
                          'Job::R':'R_number',
                          'dropLatitude':'Lat N',
                          'dropLongitude':'Lon E'})
#
df = pd.concat([df1, df2, df3], ignore_index=True)
df.to_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/DIC_JOINED_FINAL.xlsx')


"""
Draw some maps using TIM's packing to make sure data is all labelled properly
"""
import nzgeom.coastlines
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


df = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/DIC_JOINED_FINAL_EDITED.xlsx', sheet_name='for_paper')
print(df.columns)
a = df.loc[(df['Expedition'] == 'SFCS2405') & (df['Site'] == 'Doubtful') ]
b = df.loc[(df['Expedition'] == 'S309') & (df['Site'] == 'Doubtful') ]
d = df.loc[(df['Expedition'] == 'SFCS2505') & (df['Site'] == 'Doubtful') ]

a2 = df.loc[(df['Expedition'] == 'SFCS2405') & (df['Site'] == 'Dusky') ]
b2 = df.loc[(df['Expedition'] == 'S309') & (df['Site'] == 'Dusky') ]
d2 = df.loc[(df['Expedition'] == 'SFCS2505') & (df['Site'] == 'Dusky') ]


c =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.8, 167.2, -45.2))
ax = c.plot(color="lightgray", figsize=(6,8))
siz = 50
ax.scatter(a['Lon E'], a['Lat N'], color='#0072B2', marker='o', label='SFCS2405, May 2024', alpha=0.2, s=siz)
ax.scatter(b['Lon E'], b['Lat N'], color='#0072B2', marker='s', label='S309, January 2025', alpha=0.2, s=siz)
ax.scatter(d['Lon E'], d['Lat N'], color='#0072B2', marker='D', label='SFCS2505, May 2025', alpha=0.2, s=siz)

ax.scatter(a2['Lon E'], a2['Lat N'], color='#D55E00', marker='o', label='SFCS2405, May 2024', alpha=0.2, s=siz)
ax.scatter(b2['Lon E'], b2['Lat N'], color='#D55E00', marker='s', label='S309, January 2025', alpha=0.2, s=siz)
ax.scatter(d2['Lon E'], d2['Lat N'], color='#D55E00', marker='D', label='SFCS2505, May 2025', alpha=0.2, s=siz)


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



