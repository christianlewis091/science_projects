
"""
Main figures
Re starting (kind of) after I realized my CTD means are NOT working...
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nzgeom.coastlines
from cmcrameri import cm
import gsw
import matplotlib.gridspec as gridspec

from zzz_old_but_dont_delete.Interlab_Comparison.scripts.colors_set import c2_line, c3_line

df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\05_concatonate_DIC_data/DIC_JOINED_FINAL_V2_edited.xlsx', comment='#')
ctds = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\04_concatonate_CTD_data\ctd_cat.xlsx")

groups = np.unique(df['helper column group'])
siz=50

c1 = "#0072B2"
c2 = "#D55E00"
c3 = "#009E73"


for i in range(0,len(groups)):

    # make a new figure for each group
    fig, axs = plt.subplots(1, 5, figsize=(25, 8))  # 3 rows, 1 column
    c =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.8, 167.2, -45.2))
    c.plot(ax=axs[0], color="lightgray")

    subdf = df.loc[df['helper column group'] == groups[i]].reset_index(drop=True)

    s2405 = subdf.loc[subdf['EXPOCODE'] == 'SFCS2405']
    s309 = subdf.loc[subdf['EXPOCODE'] == 'S309']
    s2505 = subdf.loc[subdf['EXPOCODE'] == 'SFCS2505']

    axs[1].errorbar(s2405['DELTA14C'], s2405['Depth'], xerr=s2405['DELTA14C_Error'], marker='o', label='SFCS2405', color=c1, capsize=5)
    axs[1].errorbar(s309['DELTA14C'], s309['Depth'], xerr=s309['DELTA14C_Error'], marker='D', label='s309', color=c2, capsize=5)
    axs[1].errorbar(s2505['DELTA14C'], s2505['Depth'], xerr=s2505['DELTA14C_Error'], marker='s', label='SFCS2505', color=c3, capsize=5)

    files = np.unique(subdf['FileName'])

    # find the row for each filename
    for j in range(0,len(files)):

        row = subdf.loc[subdf['FileName'] == files[j]].reset_index(drop=True)
        ctd_data = ctds.loc[ctds['FileName'] == files[j]]

        cruise = row['EXPOCODE'].iloc[0]

        if cruise == 'SFCS2405':
            axs[0].scatter(row['Lon E'],row['Lat N'],color=c1,marker='o',label=f'{cruise}',alpha=0.2,s=siz)
            axs[2].scatter(ctd_data['t090C'], ctd_data['depSM'],color=c1)
            axs[3].scatter(ctd_data['sal00'], ctd_data['depSM'],color=c1)
            axs[4].scatter(ctd_data['sbox0Mm/Kg'], ctd_data['depSM'],color=c1)

        elif cruise == 'S309':
            axs[0].scatter(row['Lon E'],row['Lat N'],color=c2,marker='D',label=f'{cruise}',alpha=0.2,s=siz)
            axs[2].scatter(ctd_data['t090C'], ctd_data['depSM'],color=c2)
            axs[3].scatter(ctd_data['sal00'], ctd_data['depSM'],color=c2)
            axs[4].scatter(ctd_data['sbox0Mm/Kg'], ctd_data['depSM'],color=c2)

        elif cruise == 'SFCS2505':
            axs[0].scatter(row['Lon E'],row['Lat N'],color=c3,marker='s',label=f'{cruise}',alpha=0.2,s=siz)
            axs[2].scatter(ctd_data['t090C'], ctd_data['depSM'],color=c3)
            axs[3].scatter(ctd_data['sal00'], ctd_data['depSM'],color=c3)
            axs[4].scatter(ctd_data['sbox0Mm/Kg'], ctd_data['depSM'],color=c3)

    axs[1].set_xlim(16,34)
    axs[2].set_xlim(0,25)
    axs[3].set_xlim(30,40)
    axs[4].set_xlim(0,300)

    axs[2].set_xlabel('Temperature')
    axs[3].set_xlabel('Salinity')
    axs[4].set_xlabel('Oxygen')

    axs[1].set_ylim(300,0)
    axs[2].set_ylim(300,0)
    axs[3].set_ylim(300,0)
    axs[4].set_ylim(300,0)

    axs[0].legend()
    axs[1].legend()

    plt.savefig(f"C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/08_exploratory_large_figure/{groups[i]}.png",
                dpi=300, bbox_inches="tight")




