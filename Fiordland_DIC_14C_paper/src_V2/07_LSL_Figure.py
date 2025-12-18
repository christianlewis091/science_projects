import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.cm as mpl_cm
cmap = mpl_cm.viridis
from scipy import stats
from scipy.stats import linregress

c1 = "#0072B2"
c2 = "#D55E00"
c3 = "#009E73"

df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\05_concatonate_DIC_data/DIC_JOINED_FINAL_V2_edited.xlsx', comment='#')
df = df.loc[df['Depth'] <6]

# Subset datasets
s2405_dbt = df.loc[(df['EXPOCODE'] == 'SFCS2405') & (df['Site'] == 'Doubtful')]
s2505_dbt = df.loc[(df['EXPOCODE'] == 'SFCS2505') & (df['Site'] == 'Doubtful')]

s2405_dus = df.loc[(df['EXPOCODE'] == 'SFCS2405') & (df['Site'] == 'Dusky')]
s2505_dus = df.loc[(df['EXPOCODE'] == 'SFCS2505') & (df['Site'] == 'Dusky')]

plt.close()


fig = plt.subplots(figsize=(12, 8))
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


print('')
print('Is there a difference between DUSKY SFCS2024 and DUSKY SFCS2025?')
c = stats.ttest_ind(s2405_dus['DELTA14C'], s2505_dus['DELTA14C'])
print(c)

print('')
print('Is there a difference between DUSKY SFCS2024 and DUSKY SFCS2025?')
c = stats.ttest_ind(s2405_dbt['DELTA14C'], s2505_dbt['DELTA14C'])
print(c)

plt.close()
fig = plt.subplots(figsize=(12, 8))
s2405_dus = s2405_dus.sort_values(by='Lon E')
plt.errorbar(s2405_dbt['Distance from Fjord Head'], s2405_dbt['DELTA14C'], yerr=s2405_dbt['DELTA14C_Error'], marker='o', label='SFCS2405, DBT', color=c1, capsize=5)
plt.errorbar(s2505_dbt['Distance from Fjord Head'], s2505_dbt['DELTA14C'], yerr=s2505_dbt['DELTA14C_Error'], marker='s', label='SFCS2505, DBT', color=c3, capsize=5)
plt.errorbar(s2405_dus['Distance from Fjord Head'], s2405_dus['DELTA14C'], yerr=s2405_dus['DELTA14C_Error'], marker='o', label='SFCS2405, DUS', color=c1, capsize=5)
plt.errorbar(s2505_dus['Distance from Fjord Head'], s2505_dus['DELTA14C'], yerr=s2505_dus['DELTA14C_Error'], marker='s', label='SFCS2505, DUS', color=c3, capsize=5)
plt.legend()
plt.ylabel('Δ$^{14}$C (‰)')
plt.xlabel('Longitude (E)')
plt.xlim(33,-2)
plt.savefig(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\07_LSL_Figure/LSL_14Cd_distfromhead.png",
            dpi=300, bbox_inches="tight")


