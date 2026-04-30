import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.cm as mpl_cm
cmap = mpl_cm.viridis
import nzgeom.coastlines
from scipy import stats
from scipy.stats import linregress

c1 = "#0072B2"
c2 = "#D55E00"
c3 = "#009E73"

df = pd.read_excel("C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/05part2_joinCTD_and_DIC14C/JOINED_DATA.xlsx")
df = df.loc[df['Depth'] <6]

# Subset datasets
# We ignore S309 beacuse their shallowest depth was below LSL!
s2405_dbt = df.loc[(df['EXPOCODE'] == 'SFCS2405') & (df['Lat N'] > -45.6)]
s2505_dbt = df.loc[(df['EXPOCODE'] == 'SFCS2505') & (df['Lat N'] > -45.6)]

s2405_dus = df.loc[(df['EXPOCODE'] == 'SFCS2405') & (df['Lat N'] < -45.6)]
s2505_dus = df.loc[(df['EXPOCODE'] == 'SFCS2505') & (df['Lat N'] < -45.6)]

"""
THIS BLOCK IS CHECKING THE FILTERING STEP HASN"T MISSED ANYTHING
"""
print(len(df))
print(np.sum([len(s2405_dbt), len(s2505_dbt), len(s2405_dus), len(s2505_dus)]))

c =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.8, 167.2, -45.2))
ax = c.plot(color="lightgray", figsize=(6,8))
siz = 50
ax.scatter(s2405_dbt['Lon E'], s2405_dbt['Lat N'], color='blue', marker='o', label='s2405_dbt', alpha=0.2, s=siz)
ax.scatter(s2505_dbt['Lon E'], s2505_dbt['Lat N'], color='blue', marker='D', label='s2505_dbt', alpha=0.2, s=siz)
ax.scatter(s2405_dus['Lon E'], s2405_dus['Lat N'], color='red', marker='o', label='s2405_dus', alpha=0.2, s=siz)
ax.scatter(s2505_dus['Lon E'], s2505_dus['Lat N'], color='red', marker='D', label='s2505_dus', alpha=0.2, s=siz)
plt.legend()
# plt.show()
plt.close()

"""
MAIN FIG I WANT FROM THIS SCRIPT
"""
fig = plt.subplots(figsize=(7.75, 5.5))
s2405_dus = s2405_dus.sort_values(by='Lon E')
plt.errorbar(s2405_dbt['Lon E'], s2405_dbt['DELTA14C'], yerr=s2405_dbt['DELTA14C_Error'], marker='o', label='SFCS2405, DBT', color=c1, capsize=5)
plt.errorbar(s2505_dbt['Lon E'], s2505_dbt['DELTA14C'], yerr=s2505_dbt['DELTA14C_Error'], marker='s', label='SFCS2505, DBT', color=c3, capsize=5)
plt.errorbar(s2405_dus['Lon E'], s2405_dus['DELTA14C'], yerr=s2405_dus['DELTA14C_Error'], marker='o', label='SFCS2405, DUS', color=c1, capsize=5)
plt.errorbar(s2505_dus['Lon E'], s2505_dus['DELTA14C'], yerr=s2505_dus['DELTA14C_Error'], marker='s', label='SFCS2505, DUS', color=c3, capsize=5)
plt.legend()
plt.ylabel('Δ$^{14}$C (‰)')
plt.xlabel('Longitude (E)')
plt.savefig(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\07_LSL_Figure/LSL_14Cd.png",
            dpi=300, bbox_inches="tight")
#
#
# print('')
# print('Is there a difference between DUSKY SFCS2024 and DUSKY SFCS2025?')
# c = stats.ttest_ind(s2405_dus['DELTA14C'], s2505_dus['DELTA14C'])
# print(c)
#
# print('')
# print('Is there a difference between DUSKY SFCS2024 and DUSKY SFCS2025?')
# c = stats.ttest_ind(s2405_dbt['DELTA14C'], s2505_dbt['DELTA14C'])
# print(c)
#
# plt.close()
# fig = plt.subplots(figsize=(12, 8))
# s2405_dus = s2405_dus.sort_values(by='Lon E')
# plt.errorbar(s2405_dbt['Distance from Fjord Head'], s2405_dbt['DELTA14C'], yerr=s2405_dbt['DELTA14C_Error'], marker='o', label='SFCS2405, DBT', color=c1, capsize=5)
# plt.errorbar(s2505_dbt['Distance from Fjord Head'], s2505_dbt['DELTA14C'], yerr=s2505_dbt['DELTA14C_Error'], marker='s', label='SFCS2505, DBT', color=c3, capsize=5)
# plt.errorbar(s2405_dus['Distance from Fjord Head'], s2405_dus['DELTA14C'], yerr=s2405_dus['DELTA14C_Error'], marker='o', label='SFCS2405, DUS', color=c1, capsize=5)
# plt.errorbar(s2505_dus['Distance from Fjord Head'], s2505_dus['DELTA14C'], yerr=s2505_dus['DELTA14C_Error'], marker='s', label='SFCS2505, DUS', color=c3, capsize=5)
# plt.legend()
# plt.ylabel('Δ$^{14}$C (‰)')
# plt.xlabel('Longitude (E)')
# plt.xlim(33,-2)
# plt.savefig(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\07_LSL_Figure/LSL_14Cd_distfromhead.png",
#             dpi=300, bbox_inches="tight")
#

