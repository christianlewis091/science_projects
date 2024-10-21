"""
What happened to TW3537?
see  I:\XCAMS\4_maintenance\October_2024_Beam_Spreading

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
#
# # # data below was exported by simply grabbing category of Primary Std Oxalic I
# df = pd.read_excel(r'I:\XCAMS\4_maintenance\October_2024_Beam_Spreading\oxalic_analysis.xlsx')
# df = df.loc[df['Quality Flag'] == '...']  # remove flags
# df = df.loc[df['wtgraph'] > 0.35]  # remove smalls
# df = df.loc[(df['TP'] > 60000) & (df['TP'] < 89400)]  # remove smalls
#

#
# data = df['F_corrected_normed']
#
# # Calculate the mean and standard deviation
# mean = np.mean(data)
# print(mean)
# std_dev = np.std(data)
#
# # TP 89244 has FM 1.03520 for Mode 5
# extraline = 1.03520
#
# # Create the histogram
# plt.figure(figsize=(10, 6))
#
# plt.axvline(mean, color='gray', linestyle='--')
# plt.axvline(mean + std_dev, color='gray', linestyle='--')
# plt.axvline(mean - std_dev, color='gray', linestyle='--')
# plt.axvline(mean + 2 * std_dev, color='gray', linestyle='--')
# plt.axvline(mean - 2 * std_dev, color='gray', linestyle='--')
# plt.axvline(mean + 3 * std_dev, color='gray', linestyle='--')
# plt.axvline(mean - 3 * std_dev, color='gray', linestyle='--')
# plt.axvline(1.03520, color='red', linestyle='-', label='TP89244')
# plt.axvline(1.03724, color='orange', linestyle='-', label='TP89220')
#
# sns.histplot(data, bins=150, kde=False, color='lightblue', stat='density', label='Data histogram', zorder=0)
#
#
# # Plot the normal distribution curve
# xmin, xmax = plt.xlim()
# x = np.linspace(xmin, xmax, 100)
# p = norm.pdf(x, mean, std_dev)
# plt.plot(x, p, 'k', linewidth=2, label='Normal distribution fit')
#
# plt.xlim(1.0325, 1.0475)
# # Labeling
# plt.title('Distribution of Primary Std OX-I')
# plt.xlabel('F_corrected_normed')
# plt.ylabel('Density')
# plt.legend()
#
# # Show the plot
# plt.savefig(r'I:\XCAMS\4_maintenance\October_2024_Beam_Spreading\ox_distribution.png', dpi=300, bbox_inches="tight")
# #

"""
Lets make the same plots for JCT's standards
"""

df = pd.read_excel(r'I:\C14Data\C14_blank_corrections_NEW\import_from_RLIMS\historical_data\TW3537standards_mode5.xlsx')
df = df.loc[df['Quality Flag'] == '...']  # remove flags
df = df.loc[df['wtgraph'] > 0.35]  # remove smalls
df = df.loc[(df['TP'] > 60000) & (df['TP'] < 89400)]  # remove smalls

df['R_number'] = df['R_number'].replace('/', '_', regex=True)
df = df.loc[(df['R_number'] == '40430_1') | (df['R_number'] == '40430_2')]

# BELOW CHUNK TAKEN FROM DATA QUALITY PAPER
# we're only gong to look at "FLASK" oxalics...
# September 12, merge with STD prep type: We only want air secondaries run with Flask OX
spt = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_4_output/flask_ox_label.xlsx')
tp_for_spt = np.unique(df['TP'])
spt = spt.loc[spt['TP'].isin(tp_for_spt)].drop_duplicates()
df = df.merge(spt, on='TP', how='outer')
df = df.dropna(subset='Ratio to standard')
df = df[['R_number','TP','Ratio to standard','preptype','TW']]

df = df.loc[df['preptype'] == 'FLASK']

# df.to_excel(r'I:\XCAMS\4_maintenance\October_2024_Beam_Spreading\air_secondaries.xlsx')
rs = ['40430_1','40430_2']
labels = ['BHDamb','BHDspike']

subdf1 = df.loc[(df['R_number'] == '40430_1') & (df['Ratio to standard'] <1.010)]
data = subdf1['Ratio to standard']

# Calculate the mean and standard deviation
mean = np.mean(data)
print(mean)
std_dev = np.std(data)

# Create the histogram
plt.figure(figsize=(10, 6))

plt.axvline(mean, color='gray', linestyle='--')
plt.axvline(mean + std_dev, color='gray', linestyle='--')
plt.axvline(mean - std_dev, color='gray', linestyle='--')
plt.axvline(mean + 2 * std_dev, color='gray', linestyle='--')
plt.axvline(mean - 2 * std_dev, color='gray', linestyle='--')
plt.axvline(mean + 3 * std_dev, color='gray', linestyle='--')
plt.axvline(mean - 3 * std_dev, color='gray', linestyle='--')
plt.axvline(.99737, color='red', linestyle='--', label='BHDamb TW3537.1')

sns.histplot(data, bins=100, kde=False, color='lightblue', stat='density', label='Data histogram', zorder=0)


# Plot the normal distribution curve
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mean, std_dev)
plt.plot(x, p, 'k', linewidth=2, label='Normal distribution fit')

plt.title('Distribution of BHDamb')
plt.xlabel('F_corrected_normed')
plt.ylabel('Density')
plt.legend()
plt.savefig(r'I:\XCAMS\4_maintenance\October_2024_Beam_Spreading\BHDamb.png', dpi=300, bbox_inches="tight")

"""
NEXT SECONARY

"""
subdf2 = df.loc[(df['R_number'] == '40430_2') & (df['Ratio to standard'] > 0.1)]
data = subdf2['Ratio to standard']
print(len(data))
print(min(data))
# Calculate the mean and standard deviation
mean = np.mean(data)
print(mean)
std_dev = np.std(data)

# Create the histogram
plt.figure(figsize=(10, 6))

plt.axvline(mean, color='gray', linestyle='--')
plt.axvline(mean + std_dev, color='gray', linestyle='--')
plt.axvline(mean - std_dev, color='gray', linestyle='--')
plt.axvline(mean + 2 * std_dev, color='gray', linestyle='--')
plt.axvline(mean - 2 * std_dev, color='gray', linestyle='--')
plt.axvline(mean + 3 * std_dev, color='gray', linestyle='--')
plt.axvline(mean - 3 * std_dev, color='gray', linestyle='--')
plt.axvline(.89726, color='red', linestyle='--', label='BHDspike TW3537.1')
plt.axvline(.8941, color='red', linestyle='--', label='BHDspike #2 TW3537.1')
sns.histplot(data, bins=100, kde=False, color='lightblue', stat='density', label='Data histogram', zorder=0)


# Plot the normal distribution curve
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mean, std_dev)
plt.plot(x, p, 'k', linewidth=2, label='Normal distribution fit')

plt.title('Distribution of BHDspike')
plt.xlabel('F_corrected_normed')
plt.ylabel('Density')
plt.legend()
plt.savefig(r'I:\XCAMS\4_maintenance\October_2024_Beam_Spreading\BHDspike.png', dpi=300, bbox_inches="tight")
















