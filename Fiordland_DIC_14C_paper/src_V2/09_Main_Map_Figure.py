
"""
Draw some maps using TIM's packing to make sure data is all labelled properly
"""
import nzgeom.coastlines
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\05_concatonate_DIC_data/DIC_JOINED_FINAL_V2_edited.xlsx', comment='#')

c1 = "#0072B2"
c2 = "#D55E00"
c3 = "#009E73"

print(df.columns)
a = df.loc[(df['EXPOCODE'] == 'SFCS2405')]
b = df.loc[(df['EXPOCODE'] == 'S309')]
d = df.loc[(df['EXPOCODE'] == 'SFCS2505')]


c =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.8, 167.2, -45.2))
ax = c.plot(color="lightgray", figsize=(6,8))
siz = 50
ax.scatter(a['Lon E'], a['Lat N'], color=c1, marker='o', label='SFCS2405, May 2024', alpha=0.5, s=siz)
ax.scatter(b['Lon E'], b['Lat N'], color=c2, marker='D', label='S309, January 2025', alpha=0.5, s=siz)
ax.scatter(d['Lon E'], d['Lat N'], color=c3, marker='s', label='SFCS2505, May 2025', alpha=0.5, s=siz)

plt.legend()

# Show the map
plt.savefig(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\09_Main_Map_Figure/MAP1.png", dpi=300, bbox_inches="tight")
plt.close()
