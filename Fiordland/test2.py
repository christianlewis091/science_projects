import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import pandas as pd
import numpy as np

df = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/02_SPEDOC/SPE_Processing_and_Data.xlsx', sheet_name='Cruise_Data_Sheet_ALL', comment='#')
df = df.loc[df['Qflag'] != '.X.']
uci = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/02_SPEDOC/UCI_wheels/Summary.xlsx', comment='#')
# TODO CONCENSUS VALUES HAVEN"T HAD STD MULTIPLIER! FIX
"""
Read in some of the parameters for my GNS secondary SPE standards
"""
bulk_tannic_GNS = df.loc[(df['STD_ONLY_type'] == 'tannic acid') & (df['STD_ONLY_Process'] == 'bulk combustion')]
bulk_sa_GNS = df.loc[(df['STD_ONLY_type'] == 'salicylic acid') & (df['STD_ONLY_Process'] == 'bulk combustion')]

spe_tannic_GNS = df.loc[(df['STD_ONLY_type'] == 'tannic acid') & (df['STD_ONLY_Process'] == 'spe')]
spe_sa_GNS = df.loc[(df['STD_ONLY_type'] == 'salicylic acid') & (df['STD_ONLY_Process'] == 'spe')]

spes = pd.concat([spe_tannic_GNS, spe_sa_GNS]).reset_index(drop=True)
spes = spes[['STD_ONLY_type','processing mg C','Ratio to Standard']].rename(columns={'processing mg C':'mg C', "STD_ONLY_type":'ID'})
spes['Site'] = 'GNS'
uci['Site'] = 'UCI'
df = pd.concat([spes, uci])


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


# add some parameters required for the calculations
df['STD_MULT'] = 1.04
df['MCC'] = -999 # placeholder
df['MCCerr'] = -999
df['DCC'] = -999 # placeholder
df['DCCerr'] = -999

DCCs = [0, .1, 1, 3, 5, 10, 15, 30, 50]
MCCs = [0, .1, 1, 3, 5, 10, 15, 30, 50]
for i in range(0, len(MCCs)):

    # set MCC values...change later
    df.loc[(df['Site'] == 'GNS'), 'MCC'] = 1
    df.loc[(df['Site'] == 'GNS'), 'MCCerr'] = .5
    df.loc[(df['Site'] == 'GNS'), 'DCC'] = DCCs[i]
    df.loc[(df['Site'] == 'GNS'), 'DCCerr'] = .5

    df.loc[(df['Site'] == 'UCI'), 'MCC'] = 1.5
    df.loc[(df['Site'] == 'UCI'), 'MCCerr'] = .5
    df.loc[(df['Site'] == 'UCI'), 'DCC'] = DCCs[i]
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
    The below code will essentially copy UCI complete files. 
    """

    # Create a figure with two horizontal subplots
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns

    # PARAMETERIZE THE FIGURES
    ax[0].set_xscale('log')  # Logarithmic scale for x-axis
    ax[0].axhline(y=np.mean(bulk_tannic_GNS['Ratio to Standard']), label='GNS Tannic Acid Concensus', color='red',alpha=0.5)
    ax[0].axhline(y=np.mean(bulk_tannic_UCI), label='UCI Tannic Acid Concensus', color='blue',alpha=0.5)

    ax[1].set_xscale('log')  # Logarithmic scale for x-axis
    ax[1].axhline(y=np.mean(bulk_sa_GNS['Ratio to Standard']), label='GNS Salicylic Acid Concensus', color='red',alpha=0.5)
    ax[1].axhline(y=np.mean(bulk_sa_UCI), label='UCI Salicylic Acid Concensus', color='blue',alpha=0.5)

    ax[0].grid(True, which="both", ls="--")
    ax[1].grid(True, which="both", ls="--")

    ax[0].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
    ax[1].set_xticks(ticks=[0.001, 0.01, 0.1, 1, 10], labels=['0.001', '0.01', '0.1', '1','10'])
    ax[0].set_xlim(.001, 10)
    ax[1].set_xlim(.001, 10)
    ax[0].set_ylim(.75, 1.3)
    ax[1].set_ylim(.075, .2)

    ax[0].set_title('Tannic Acid Indirect Blank Analysis')
    ax[1].set_title('Salicylic Acid Indirect Blank Analysis')

    ax[0].set_xlabel('Sample size (mg C)')
    ax[1].set_xlabel('Sample size (mg C)')
    ax[0].set_ylabel('Fraction Modern')


    # NOW WE CAN POPULATE IT WITH DATA
    df = df.loc[df['FM'] < 2]
    uci_tannic6 = df.loc[(df['ID'] == 'Tannic acid (6 mL)')].dropna(subset='FM')
    uci_tannic30 = df.loc[(df['ID'] == 'Tannic acid (30 mL)')].dropna(subset='FM')

    ax[0].scatter(uci_tannic6 ['mg C'], uci_tannic6 ['FM'], label='UCI Tannic Acid, 6mL, Corrected', color='yellow', edgecolor='blue', s= 60)
    ax[0].scatter(uci_tannic6 ['mg C'], uci_tannic6 ['Ratio to Standard'], color='white', edgecolor='black', s= 60)


    ax[0].scatter(uci_tannic30 ['mg C'], uci_tannic30 ['FM'], label='UCI Tannic Acid, 30mL, Corrected', color='blue', edgecolor='yellow', s= 60)
    ax[0].scatter(uci_tannic30 ['mg C'], uci_tannic30 ['Ratio to Standard'], color='white', edgecolor='black', s= 60)

    gns_tannic = df.loc[(df['Site'] == 'GNS') & (df['ID'] == 'tannic acid')].dropna(subset='FM')
    ax[0].scatter(gns_tannic['mg C'], gns_tannic['FM'], label='GNS Tannic Acid, Corrected', color='red', edgecolor='black', s= 60)
    ax[0].scatter(gns_tannic['mg C'], gns_tannic['Ratio to Standard'], color='white', edgecolor='black', s= 60)

    """
    XXXXXXXXXXXXXXXXXXXX
    """

    uci_sa6 = df.loc[(df['ID'] == 'Salicylic acid (6 mL)')].dropna(subset='FM')
    uci_sa30 = df.loc[(df['ID'] == 'Salicylic acid (30 mL)')].dropna(subset='FM')

    ax[1].scatter(uci_sa6['mg C'], uci_sa6 ['FM'], label='UCI Salicylic Acid, 6mL, Corrected', color='yellow', edgecolor='blue', s= 60)
    ax[1].scatter(uci_sa6['mg C'], uci_sa6 ['Ratio to Standard'], color='white', edgecolor='black', s= 60)

    ax[1].scatter(uci_sa30 ['mg C'], uci_sa30 ['FM'], label='UCI Salicylic Acid, 30mL, Corrected', color='blue', edgecolor='yellow', s= 60)
    ax[1].scatter(uci_sa30 ['mg C'], uci_sa30 ['Ratio to Standard'], color='white', edgecolor='black', s= 60)

    gns_sa = df.loc[(df['Site'] == 'GNS') & (df['ID'] == 'salicylic acid')].dropna(subset='FM')
    ax[1].scatter(gns_sa['mg C'], gns_sa['FM'], label='GNS Salicylic Acid, Corrected', color='red', edgecolor='black', s= 60)
    ax[1].scatter(gns_sa['mg C'], gns_sa['Ratio to Standard'], color='white', edgecolor='black', s= 60)
    ax[1].legend()
    plt.title(f"DCC = {int(DCCs[i])}")
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Blank_analysis_plots/animation/Figure1_{int(DCCs[i])}.png', dpi=300, bbox_inches="tight")

plt.close()






















