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

df = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\13_AOU_plot\JOINED_DATA_wAOU.xlsx")
# df = df.loc[df['Depth'] >= 6]

s2405_dbt = df.loc[(df['EXPOCODE'] == 'SFCS2405') & (df['Lat N'] > -45.6)]
s309_dbt = df.loc[(df['EXPOCODE'] == 'S309') & (df['Lat N'] > -45.6)]
s2505_dbt = df.loc[(df['EXPOCODE'] == 'SFCS2505') & (df['Lat N'] > -45.6)]

s2405_dus = df.loc[(df['EXPOCODE'] == 'SFCS2405') & (df['Lat N'] < -45.6)]
s309_dus = df.loc[(df['EXPOCODE'] == 'S309') & (df['Lat N'] < -45.6)]
s2505_dus = df.loc[(df['EXPOCODE'] == 'SFCS2505') & (df['Lat N'] < -45.6)]

# fig, axs = plt.subplots(1, 2, figsize=(9,5.5))

# """
# DOUBTFUL
# """

# # stns = np.unique(s2405_dbt['FileName_ctd'])
# # for i in range(0, len(stns)):
# #     subdf = s2405_dbt.loc[s2405_dbt['FileName_ctd'] == stns[i]]
# #     axs[0].errorbar(subdf['DELTA14C'], subdf['Depth'], xerr=subdf['DELTA14C_Error'], linestyle='-', marker='o', color=c1)

# # stns = np.unique(s309_dbt['FileName_ctd'])
# # for i in range(0, len(stns)):
# #     subdf = s309_dbt.loc[s309_dbt['FileName_ctd'] == stns[i]]
# #     axs[0].errorbar(subdf['DELTA14C'], subdf['Depth'], xerr=subdf['DELTA14C_Error'], linestyle='-', marker='o', color=c2)

# stns = np.unique(s2505_dbt['FileName_ctd'])
# for i in range(0, len(stns)):
#     subdf = s2505_dbt.loc[s2505_dbt['FileName_ctd'] == stns[i]]
#     axs[0].errorbar(subdf['DELTA14C'], subdf['Depth'], xerr=subdf['DELTA14C_Error'], linestyle='-', marker='o', color=c3)

# """
# DUSKY
# """

# # stns = np.unique(s2405_dus['FileName_ctd'])
# # for i in range(0, len(stns)):
# #     subdf = s2405_dus.loc[s2405_dus['FileName_ctd'] == stns[i]]
# #     axs[1].errorbar(subdf['DELTA14C'], subdf['Depth'], xerr=subdf['DELTA14C_Error'], linestyle='-', marker='o', color=c1)

# # stns = np.unique(s309_dus['FileName_ctd'])
# # for i in range(0, len(stns)):
# #     subdf = s309_dus.loc[s309_dus['FileName_ctd'] == stns[i]]
# #     axs[1].errorbar(subdf['DELTA14C'], subdf['Depth'], xerr=subdf['DELTA14C_Error'], linestyle='-', marker='o', color=c2)

# stns = np.unique(s2505_dus['FileName_ctd'])
# for i in range(0, len(stns)):
#     subdf = s2505_dus.loc[s2505_dus['FileName_ctd'] == stns[i]]
#     axs[1].errorbar(subdf['DELTA14C'], subdf['Depth'], xerr=subdf['DELTA14C_Error'], linestyle='-', marker='o', color=c3)
# axs[0].set_ylim(450,0)
# axs[1].set_ylim(450,0)
# axs[0].set_xlim(20,35)
# axs[1].set_xlim(20,35)
# axs[0].set_title('Patea/Doubtful Sound')
# axs[1].set_title('Tamatea/Dusky Sound')
# axs[0].set_xlabel('Δ$^{14}$C (‰)')
# axs[1].set_xlabel('Δ$^{14}$C (‰)')
# axs[0].set_ylabel('Depth (m)')

# plt.show()
# # plt.savefig(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\07_LSL_Figure/deep_14Cd_2505.png",
# #             dpi=300, bbox_inches="tight")
# plt.close()

"""
Making some extra plots to prepare for my meeting with Stanford Team, comparing each station, which will help vizualize through the messy data
"""
dbt_stns = ['Doubtful Mouth', 'Malaspina Reach','Deep Cove','Ferguson Is.']
dusky_stns = ['Dusky Mouth','Sportsmans Cove','S. of Cooper Is.','Outside Duck Cove','Girlies Basin']

spots = np.unique(df['Loc']) # make a list of unique locations
for i in range(0, len(spots)):
    fig, axs = plt.subplots(1, 2, figsize=(9,5.5))

    spot_i = df.loc[df['Loc'] == spots[i]] # grab the first spot

    filenames = np.unique(spot_i['FileName_ctd']) # grab each set of data within the spot to plot...
    for j in range(0, len(filenames)):
        name_j = spot_i.loc[spot_i['FileName_ctd'] == filenames[j]].sort_values(by='Depth') # grab the individual station

        expocode = name_j['EXPOCODE'].iloc[0] # find which expedition this filename was on

        if expocode == 'SFCS2405':
            color = c1
        elif expocode == 'S309':
            color = c2
        elif expocode == 'SFCS2505':
            color = c3

        if spots[i] in dbt_stns:
            axs[0].errorbar(name_j['DELTA14C'], name_j['Depth'], xerr=name_j['DELTA14C_Error'], linestyle='-', marker='o', color=color)
            axs[0].set_title(f'{spots[i]}')
        else:
            axs[1].errorbar(name_j['DELTA14C'], name_j['Depth'], xerr=name_j['DELTA14C_Error'], linestyle='-', marker='o', color=color)
            axs[1].set_title(f'{spots[i]}')

    axs[0].axhline(y=5, color="black", alpha=0.2)
    axs[1].axhline(y=5, color="black", alpha=0.2)
    axs[0].set_ylim(450,0)
    axs[1].set_ylim(450,0)
    axs[0].set_xlim(16,35)
    axs[1].set_xlim(16,35)
    axs[0].set_xlabel('Δ$^{14}$C (‰)')
    axs[1].set_xlabel('Δ$^{14}$C (‰)')
    axs[0].set_ylabel('Depth (m)')
    plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output_V2/DeepFigure/{spots[i]}.png",
            dpi=300, bbox_inches="tight")

