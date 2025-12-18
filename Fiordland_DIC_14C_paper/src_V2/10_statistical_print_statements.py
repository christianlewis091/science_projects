import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.cm as mpl_cm
cmap = mpl_cm.viridis
from scipy import stats
from scipy.stats import linregress

df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\05_concatonate_DIC_data/DIC_JOINED_FINAL_V2_edited.xlsx', comment='#')
df = df.loc[df['Depth'] <6]

# Subset datasets
s2405_dbt = df.loc[(df['EXPOCODE'] == 'SFCS2405') & (df['Site'] == 'Doubtful')]
s2505_dbt = df.loc[(df['EXPOCODE'] == 'SFCS2505') & (df['Site'] == 'Doubtful')]

s2405_dus = df.loc[(df['EXPOCODE'] == 'SFCS2405') & (df['Site'] == 'Dusky')]
s2505_dus = df.loc[(df['EXPOCODE'] == 'SFCS2505') & (df['Site'] == 'Dusky')]

# DBT 2024
slope, intercept, r, p, stderr = linregress(s2405_dbt['Lon E'], s2405_dbt['DELTA14C'])
print(f"May 2024, Doubtful Sound: y = {slope:.1f}*x + {intercept:.1f}, r² = {r**2:.2f}")

# DBT 2025
slope, intercept, r, p, stderr = linregress(s2505_dbt['Lon E'], s2505_dbt['DELTA14C'])
print(f"May 2024, Doubtful Sound: y = {slope:.1f}*x + {intercept:.1f}, r² = {r**2:.2f}")


# m is measured value
# A is one end-member
# B is second end-member
def mass_balance(m, a, b):
    x_a = (m-b)/(a-b)
    print(x_a)
    print(1-x_a)

mass_balance(5, 35, 0)

print('')
print('Is there a difference between DUSKY SFCS2024 and DUSKY SFCS2025?')
c = stats.ttest_ind(s2405_dus['DELTA14C'], s2505_dus['DELTA14C'])
print(c)

print('')
print('Is there a difference between Doubtful SFCS2024 and Doubtful SFCS2025?')
c = stats.ttest_ind(s2405_dbt['DELTA14C'], s2505_dbt['DELTA14C'])
print(c)