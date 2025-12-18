
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

df = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/DIC_JOINED_FINAL_EDITED.xlsx', sheet_name='for_paper')

# Sonne has sal00, t090C
sonne_ctd = pd.read_excel(f'H:\Science\Datasets\Fiordland\RVSONNE\STEP3/Concatonated_CTD_SONNE.xlsx')
sonne_ctd = sonne_ctd[['FileName', 'sal00','t090C', 'depSM']]

# 2405 has DepSM, Sal00, T090C
sfcs2405_ctd = pd.read_excel('H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4/mystations.xlsx')
sfcs2405_ctd = sfcs2405_ctd.rename(columns={'Sal00':'sal00', 'T090C':'t090C','DepSM':'depSM'})
sfcs2405_ctd = sfcs2405_ctd[['FileName', 'sal00','t090C','depSM']]

# 2505 has depSM, sal00, t090C
sfcs2505_ctd = pd.read_csv(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2505_CTD_DATA_FINAL.csv')
sfcs2505_ctd = sfcs2505_ctd[['FileName', 'sal00','t090C','depSM']]

# Join the CTD data together, after changing some column names

ctd_cat = pd.concat([sonne_ctd, sfcs2405_ctd, sfcs2505_ctd])

cruise1 = ['DBT001_01CTD','DBT003_01CTD', 'DBT006_01CTD', 'DBT008_01CTD',
           'DBT010_02CTD', 'DBT011_02CTD', 'DBT012_01CTD', 'DUS020_01CTD',
           'DUS023_01CTD']
cruise2 = ['SO309-35-1_by_depth_1_m', 'SO309-38-1_27_by_depth_1_m',
           'SO309-46-17_by_depth_1_m', 'SO309-53-1_by_depth_1_m',
           'SO309-55-1_by_depth_1_m', 'SO309-59-13_by_depth_1_m',
           'SO309-62-1_by_depth_1_m', 'SO309-65-1_by_depth_1_m']
cruise3 = ['sfcs2505_dbt019_01ctd','sfcs2505_dbt020_01ctd', 'sfcs2505_dbt021_01ctd',
            'sfcs2505_dus028_01ctd', 'sfcs2505_dus030_01ctd', 'sfcs2505_dus036_01ctd']

ctd_cat['EXPOCODE'] = -999
ctd_cat.loc[ctd_cat['FileName'].isin(cruise1), 'EXPOCODE'] = 'SFCS2405'
ctd_cat.loc[ctd_cat['FileName'].isin(cruise2), 'EXPOCODE'] = 'S309'
ctd_cat.loc[ctd_cat['FileName'].isin(cruise3), 'EXPOCODE'] = 'SFCS2505'
ctd_cat.to_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/ctd_cat.xlsx')
#
groups = np.unique(df['group'])

for i in range(0,len(groups)):

    subdf = df.loc[df['group'] == groups[i]]
    print(f'Group = {i+1}')
    # print(subdf)

    # make a new figure for each group
    fig, axs = plt.subplots(1, 3, figsize=(16, 8))  # 3 rows, 1 column

    groups_ctd = np.unique(subdf['CTD_Filename'])
    print(groups_ctd)


    for j in range(0, len(groups_ctd)):
        # go find the CTD data for that one
        ctd1 = ctd_cat.loc[ctd_cat['FileName'] == groups_ctd[j]].reset_index(drop=True)
        print(ctd1.columns)
        print(ctd1)
        print()
        # which cruise is it on
        expocode = np.unique(ctd1['EXPOCODE'])

        if expocode == 'SFCS2405':
            axs[0].scatter(ctd1['sal00'], ctd1['depSM'], color='black', marker='o', label='SFCS2405, May 2024')
            axs[1].scatter(ctd1['t090C'], ctd1['depSM'], color='black', marker='o')
        elif expocode == 'S309':
            axs[0].scatter(ctd1['sal00'], ctd1['depSM'], color='red', marker='s', label='S309, January 2025')
            axs[1].scatter(ctd1['t090C'], ctd1['depSM'], color='red', marker='s')
        elif expocode == 'SFCS2505':
            axs[0].scatter(ctd1['sal00'], ctd1['depSM'], color='blue', marker='D', label='SFCS2505, May 2025')
            axs[1].scatter(ctd1['t090C'], ctd1['depSM'], color='blue', marker='D')

    axs[0].set_ylim(10,0)
    axs[1].set_ylim(10,0)
    axs[0].set_xlim(np.min(ctd_cat['sal00']),np.max(ctd_cat['sal00']))
    axs[1].set_xlim(np.min(ctd_cat['t090C']),np.max(ctd_cat['t090C']))
    plt.title(f'Group {i+1}')
    axs[0].set_xlabel('Salinity')
    axs[1].set_xlabel('Temp')
    axs[0].legend()
    plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/groupchecks/Group{i+1}.png", dpi=300, bbox_inches="tight")
    plt.close()





