"""
April 8, 2025
This short script will merge the sampling log (lat, lon, notes) with the 14C data (output from RLIMS)
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw/Sampling_Log.xlsx')

# just keep the important columns
df = df[['My Station Name', 'Cruise Station Name','Latitude_N_decimal','Longitude_E_decimal','Bottom Depth (m)','Depth','Sample','ID']]
# retain just the DIC samples for now (not thinking about SPE-DOC or DOC)
dic = df.loc[((df['Sample'] == 'DIC') | (df['Sample'] == 'DIC Duplicate'))]

tw3530 = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw//TW3530_export.xlsx')
tw3530 = tw3530.loc[tw3530['Samples::Sample Description'] == 'Fiordland DIC samples from SFCS2405'] # remove oxalics, kapunis, etc
print(tw3530.columns)
print(dic.columns)

df = dic.merge(tw3530, on='ID')
df.to_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2405_DIC_14C_FINAL.xlsx')


"""
# Dave Mucciarone's DIC 13C data was manually added to this sheet on 5/5/25
 # here are some plots of the data. How do they compare?
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# Read and filter the data
df = pd.read_excel(
    'C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/data/processed/SFCS2405_DIC_14C_FINAL.xlsx',
    sheet_name='13C_comparison', comment='#').dropna(subset=['Cruise Station Name'])

# Get unique stations
stns = np.unique(df['Sort Number'].astype(str))

# Set up subplot grid
fig = plt.figure(figsize=(15, 12))
gs = gridspec.GridSpec(3, 3, wspace=0.2, hspace=0.3)  # 3x3 grid

for i, stn in enumerate(stns):
    df_i = df[df['Sort Number'].astype(str) == stn]
    descrip = df_i['Site Description'].iloc[0]
    code = df_i['Cruise Station Name'].iloc[0]
    ax = fig.add_subplot(gs[i])
    ax.errorbar(df_i['Mean of duplicates'], df_i['Depth'], xerr=0.02, label='Stanford', marker='o', color='red')
    ax.errorbar(df_i['delta13C_IRMS'], df_i['Depth'], xerr=0.3, label='RLL', marker='o', color='blue')
    ax.set_xlim(-5, 5)
    ax.set_ylim(300, 0)
    ax.set_title(f'{code}_{descrip}', fontsize=10)
    ax.set_xlabel('δ13C')
    ax.set_ylabel('Depth (m)')
    ax.legend(fontsize=8)

plt.suptitle('δ13C Comparison by Station', fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Leave room for the suptitle
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/data/processed/13C_comparison.png', dpi=300, bbox_inches="tight")
plt.close()
