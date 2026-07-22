import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_excel(r"H:\Science\Current_Projects\03_CCE_24_25\02_Solid_Phase_Extraction\DATA_PROCESSING_RAW.xlsx", sheet_name='Cruise_Data_Sheet_ALL', comment='#')
df = df.loc[df['Qflag'] != '.X.']

"""
PLOT SPE-DOC Yields
"""
sa_spe = df.loc[(df['STD_ONLY_type'] == 'salicylic acid') & (df['STD_ONLY_Process'] == 'spe')]
ta_spe = df.loc[(df['STD_ONLY_type'] == 'tannic acid') & (df['STD_ONLY_Process'] == 'spe')].dropna(subset='processing mg C')

# Create figure and axes (3 subplots in 1 row)
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(14, 6), constrained_layout=True)

# First subplot
ax[0].plot(sa_spe['STD_ONLY_mass_added (g)'], sa_spe['processing mg C'], color='gray', label='Salicylic Acid', marker = 'o', linestyle ='none')
ax[0].plot(ta_spe['STD_ONLY_mass_added (g)'], ta_spe['processing mg C'], color='black', label='Tannic Acid', marker = 'D', linestyle ='none')
ax[0].set_title("SPE Recovery Trends")
ax[0].set_xlabel("mass of standard stock solution added (g)")
ax[0].set_ylabel("C recovered in manometry (mg)")
slope, intercept, rvalue, pvalue, stderr = stats.linregress(sa_spe['STD_ONLY_mass_added (g)'], sa_spe['processing mg C'])
sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(ta_spe['STD_ONLY_mass_added (g)'], ta_spe['processing mg C'])
ax[0].plot(sa_spe['STD_ONLY_mass_added (g)'], slope*sa_spe['STD_ONLY_mass_added (g)']+intercept, color='gray')
ax[0].plot(ta_spe['STD_ONLY_mass_added (g)'], sslope*ta_spe['STD_ONLY_mass_added (g)']+sintercept, color='black')
print("Salicylic Acid y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2))
print("Tannic Acid: y=%.3fx+%.3f\R$^2$=%.3f"%(sslope, sintercept,srvalue**2))

ax[0].legend()


df = df.loc[df['Qflag'] != '.X.']
uci = pd.read_excel(r"H:\Science\Current_Projects\03_CCE_24_25\02_Solid_Phase_Extraction\UCI_wheels\Summary.xlsx", comment='#')

# """
# Read in some of the parameters for my GNS secondary SPE standards
# """
bulk_tannic_GNS = df.loc[(df['STD_ONLY_type'] == 'tannic acid') & (df['STD_ONLY_Process'] == 'bulk combustion')]
bulk_sa_GNS = df.loc[(df['STD_ONLY_type'] == 'salicylic acid') & (df['STD_ONLY_Process'] == 'bulk combustion')]

spe_tannic_GNS = df.loc[(df['STD_ONLY_type'] == 'tannic acid') & (df['STD_ONLY_Process'] == 'spe')]
spe_sa_GNS = df.loc[(df['STD_ONLY_type'] == 'salicylic acid') & (df['STD_ONLY_Process'] == 'spe')]

spes = pd.concat([spe_tannic_GNS, spe_sa_GNS]).reset_index(drop=True)
spes = spes[['STD_ONLY_type','processing mg C','Ratio to Standard']].rename(columns={'processing mg C':'mg C', "STD_ONLY_type":'ID'})
spes['Site'] = 'GNS'
uci['Site'] = 'UCI'
df = pd.concat([spes, uci])

# add some parameters required for the calculations
df['STD_MULT'] = 1.04
df['MCC'] = -999 # placeholder
df['MCCerr'] = -999
df['DCC'] = -999 # placeholder
df['DCCerr'] = -999

# set MCC values...change later
df.loc[(df['Site'] == 'GNS'), 'MCC'] = 1
df.loc[(df['Site'] == 'GNS'), 'MCCerr'] = .5
df.loc[(df['Site'] == 'GNS'), 'DCC'] = 65
df.loc[(df['Site'] == 'GNS'), 'DCCerr'] = .5

df.loc[(df['Site'] == 'UCI'), 'MCC'] = 1.5
df.loc[(df['Site'] == 'UCI'), 'MCCerr'] = .5
df.loc[(df['Site'] == 'UCI'), 'DCC'] = 5
df.loc[(df['Site'] == 'UCI'), 'DCCerr'] = .5

# For simplicity, I'm going to apply DCC (the small corrections) to everything for now.
df['BKGD'] = df['MCC']/(1000*df['mg C'])
df['BKGDerr'] = df['BKGD']*(df['MCCerr']/df['MCC'])

# STD_CORR in vein of UCI
df['STD_CORR'] = (df['DCC']/1000)*((1/df['mg C'])- (1/.89))  # approximate standards are 0.8 mg

# FM
df['FM'] = (df['STD_MULT']*(df['Ratio to Standard'] - df['BKGD']))/(1-df['STD_CORR']-df['BKGD'])
# df.to_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Blank_analysis_plots/out.xlsx')


"""
What are the concensus values?
"""
print(f"The mean consensus value (ratio to OX-1) for Tannic Acid (GNS) is {np.mean(bulk_tannic_GNS['Ratio to Standard'])}")
print(f"The mean consensus value (ratio to OX-1) for Salicylic Acid (GNS) is {np.mean(bulk_sa_GNS['Ratio to Standard'])}")

# April 18, 2018
bulk_tannic_UCI = 1.017 # roughly converted from the Del14C values found on AC37
bulk_sa_UCI = .14        # roughly converted from the Del14C values found on AC37
print()
print(f"The mean consensus value (ratio to OX-1) for Tannic Acid (UCI) is {bulk_tannic_UCI}")
print(f"The mean consensus value (ratio to OX-1) for Salicylic Acid (UCI) is {bulk_sa_UCI}")


# """
# The below code will essentially copy UCI complete files.
# """
#
# # Create a figure with two horizontal subplots
# fig, ax = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns

# PARAMETERIZE THE FIGURES
ax[1].set_xscale('log')  # Logarithmic scale for x-axis
ax[1].axhline(y=np.mean(bulk_tannic_GNS['Ratio to Standard']), label='GNS Tannic Acid Concensus', color='red',alpha=0.5)
ax[1].axhline(y=np.mean(bulk_tannic_UCI), label='UCI Tannic Acid Concensus', color='blue',alpha=0.5)

ax[2].set_xscale('log')  # Logarithmic scale for x-axis
ax[2].axhline(y=np.mean(bulk_sa_GNS['Ratio to Standard']), label='GNS Salicylic Acid Concensus', color='red',alpha=0.5)
ax[2].axhline(y=np.mean(bulk_sa_UCI), label='UCI Salicylic Acid Concensus', color='blue',alpha=0.5)

ax[1].grid(True, which="both", ls="--")
ax[2].grid(True, which="both", ls="--")

ax[1].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
ax[2].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
ax[1].set_xlim(.001, 10)
ax[2].set_xlim(.001, 10)
# ax[0].set_ylim(.75, 1.05)
# ax[1].set_ylim(.075, .2)

ax[1].set_title('Tannic Acid Indirect Blank Analysis')
ax[2].set_title('Salicylic Acid Indirect Blank Analysis')

ax[1].set_xlabel('Sample size (mg C)')
ax[2].set_xlabel('Sample size (mg C)')
ax[1].set_ylabel('Fraction Modern')

#
# NOW WE CAN POPULATE IT WITH DATA
df = df.loc[df['FM'] < 2]
uci_tannic6 = df.loc[(df['ID'] == 'Tannic acid (6 mL)')].dropna(subset='FM')
uci_tannic30 = df.loc[(df['ID'] == 'Tannic acid (30 mL)')].dropna(subset='FM')

ax[1].scatter(uci_tannic6 ['mg C'], uci_tannic6 ['FM'], label='UCI Tannic Acid, 6mL, Corrected', color='yellow', edgecolor='blue', s= 60)
# ax[1].scatter(uci_tannic6 ['mg C'], uci_tannic6 ['Ratio to Standard'], color='white', edgecolor='black', s= 60)


ax[1].scatter(uci_tannic30 ['mg C'], uci_tannic30 ['FM'], label='UCI Tannic Acid, 30mL, Corrected', color='blue', edgecolor='yellow', s= 60)
# ax[1].scatter(uci_tannic30 ['mg C'], uci_tannic30 ['Ratio to Standard'], color='white', edgecolor='black', s= 60)

gns_tannic = df.loc[(df['Site'] == 'GNS') & (df['ID'] == 'tannic acid')].dropna(subset='FM')
ax[1].scatter(gns_tannic['mg C'], gns_tannic['FM'], label='GNS Tannic Acid, Corrected', color='red', edgecolor='black', s= 60)
# ax[1].scatter(gns_tannic['mg C'], gns_tannic['Ratio to Standard'], color='white', edgecolor='black', s= 60)

# """
# XXXXXXXXXXXXXXXXXXXX
# """

uci_sa6 = df.loc[(df['ID'] == 'Salicylic acid (6 mL)')].dropna(subset='FM')
uci_sa30 = df.loc[(df['ID'] == 'Salicylic acid (30 mL)')].dropna(subset='FM')

ax[2].scatter(uci_sa6['mg C'], uci_sa6 ['FM'], label='UCI Salicylic Acid, 6mL, Corrected', color='yellow', edgecolor='blue', s= 60)
# ax[2].scatter(uci_sa6['mg C'], uci_sa6 ['Ratio to Standard'], color='white', edgecolor='black', s= 60)

ax[2].scatter(uci_sa30 ['mg C'], uci_sa30 ['FM'], label='UCI Salicylic Acid, 30mL, Corrected', color='blue', edgecolor='yellow', s= 60)
# ax[2].scatter(uci_sa30 ['mg C'], uci_sa30 ['Ratio to Standard'], color='white', edgecolor='black', s= 60)

gns_sa = df.loc[(df['Site'] == 'GNS') & (df['ID'] == 'salicylic acid')].dropna(subset='FM')
ax[2].scatter(gns_sa['mg C'], gns_sa['FM'], label='GNS Salicylic Acid, Corrected', color='red', edgecolor='black', s= 60)
# ax[2].scatter(gns_sa['mg C'], gns_sa['Ratio to Standard'], color='white', edgecolor='black', s= 60)
ax[2].legend()

plt.show()
# plt.savefig(r'H:\Science\Papers\In Prep Work\2025_Fiordland_SPE-DOC\Figures/SI_Figure2.png', dpi=300, bbox_inches="tight")
# plt.close()

"""
Diagonal blank plot
"""
# # Create a figure and a set of subplots
# fig, ax = plt.subplots()
#
# # Set the x and y scales to logarithmic
# ax.set_xscale('log')
# ax.set_yscale('log')
#
# # Set the limits for x and y axes
# ax.set_xlim(0.001, 10)
# ax.set_ylim(0.0001, 1)
#
# # Add labels to the axes
# ax.set_xlabel('Sample Size (mg)')
# ax.set_ylabel('Ratio to OX-1')
# ax.xaxis.set_major_formatter(ScalarFormatter())
# ax.yaxis.set_major_formatter(ScalarFormatter())
# ax.xaxis.get_major_formatter().set_scientific(False)
# ax.yaxis.get_major_formatter().set_scientific(False)
# # Add a grid for better readability
# ax.grid(True, which="both", ls="--")
#
# # add the diagonal lines
# x = [0.001, 10]
# y1 = [0.2, .00002]
# y2 = [0.3, .00003]
# y3 = [0.4, .00004]
# y4 = [0.5, .00005]
# y5 = [0.6, .00006]
# y6 = [0.8, .00008]
# y7 = [1, .0001]
# y8 = [2, .0002]
# y9 = [5, .0005]
# ys = [y1, y2, y3, y4, y5, y6, y7, y8, y9]
# labels = ['0.2','0.3','0.4','0.5','0.6','0.8','1','2','5']
# for i in range(0, len(ys)):
#     plt.plot(x, ys[i], label=f'{labels[i]}')
#
# # salicylic acid 6 mL elutions
# sa6 = uci.loc[uci['ID'] == 'Salicylic acid (6 mL)']
# # salicylic acid 30 mL elutions
# sa30 = uci.loc[uci['ID'] == 'Salicylic acid (30 mL)']
#
# plt.scatter(sa6['mg C'], sa6['Ratio to Standard'], label='UCI Salicylic Acid, 6 mL elution')
# plt.scatter(sa30['mg C'], sa30['Ratio to Standard'], label='UCI Salicylic Acid, 30 mL elution')
# plt.scatter(spe_sa_GNS['processing mg C'], spe_sa_GNS['F_corrected_normed'], label='GNS Salicylic Acid, 3 mL elution')
#
# plt.legend()
# # Show the plot
# # plt.show()
# plt.close()





















