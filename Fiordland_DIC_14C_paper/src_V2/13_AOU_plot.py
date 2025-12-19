"""
First I need a reproducable way to assing T,S,and O data for every 14C point.
Then I can calculae AOU for every 14C point.

I think I can do something like in script 8...
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nzgeom.coastlines
from cmcrameri import cm
import gsw
import matplotlib.cm as mpl_cm
cmap = mpl_cm.viridis
import matplotlib.gridspec as gridspec
from scipy.stats import linregress




# df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\05_concatonate_DIC_data/DIC_JOINED_FINAL_V2_edited.xlsx', comment='#')
# ctds = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\04_concatonate_CTD_data\ctd_cat.xlsx")
#
# groups = np.unique(df['helper column group'])
# siz=50
#
# c1 = "#0072B2"
# c2 = "#D55E00"
# c3 = "#009E73"
#
# d_arr = []
# t_arr = []
# s_arr = []
# o_arr = []
#
# for i in range(0,len(df)):
#     row_i = df.iloc[i]
#     filename = row_i['FileName']
#     depth = row_i['Depth']
#     lat = row_i['Lat N']
#     lon = row_i['Lon E']
#
#     # use row iloc to grab CTD profile for each 14C point
#     ctd_data = ctds.loc[ctds['FileName'] == filename]
#
#     # find profile that is closest in depth to each point
#     idx = (ctd_data['depSM'] - depth).abs().idxmin()
#     closest_row = ctd_data.loc[idx]
#
#     # grab data from that ctd depth
#     sal = closest_row['sal00']
#     temp = closest_row['t090C']
#     ox = closest_row['sbox0Mm/Kg']
#     depid = closest_row['depSM']
#
#     d_arr.append(depid)
#     t_arr.append(temp)
#     s_arr.append(sal)
#     o_arr.append(ox)
#
#     # make a figure to check each one...
#     fig, axs = plt.subplots(1, 5, figsize=(25, 8))  # 3 rows, 1 column
#     c =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.8, 167.2, -45.2))
#     c.plot(ax=axs[0], color="lightgray")
#
#     axs[0].scatter(row_i['Lon E'],row_i['Lat N'],color=c1,marker='o',label=f'{i}',alpha=0.2,s=siz)
#     axs[1].errorbar(row_i['DELTA14C'], row_i['Depth'], xerr=row_i['DELTA14C_Error'], marker='s', label=f'{i}', capsize=5)
#     axs[2].scatter(ctd_data['t090C'], ctd_data['depSM'],color=c1)
#     axs[3].scatter(ctd_data['sal00'], ctd_data['depSM'],color=c1)
#     axs[4].scatter(ctd_data['sbox0Mm/Kg'], ctd_data['depSM'],color=c1)
#
#     axs[2].scatter(temp, depid,color='red',s=siz*1.5)
#     axs[3].scatter(sal, depid,color='red',s=siz*1.5)
#     axs[4].scatter(ox, depid,color='red',s=siz*1.5)
#
#     axs[1].set_ylim(300,0)
#     axs[2].set_ylim(300,0)
#     axs[3].set_ylim(300,0)
#     axs[4].set_ylim(300,0)
#     plt.savefig(f"C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/13_AOU_plot/{i}.png",
#                 dpi=300, bbox_inches="tight")
#
# p_resultsss = pd.DataFrame({"CTD chosen depth": d_arr, "Temp": t_arr, "Sal": s_arr, "Oxygen": o_arr })
#
# df = pd.concat([df.reset_index(drop=True),p_resultsss.reset_index(drop=True)],axis=1)
#

"""
https://www.ncei.noaa.gov/access/ocean-carbon-acidification-data-system/oceans/ndp_065/3e.html
HOW TO CALCULATE AOU

The Apparent Oxygen Utilization (AOU) value was obtained by subtracting the measured value from the 
saturation value computed at the potential temperature of water and 1 atm total pressure using the 
following expression based on the data of Murray and Riley (1969):
"""

df = pd.read_excel(r"C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/13_AOU_plot/results.xlsx")

# STEP 1, calculate potential tempeaure
df['SA'] = gsw.SA_from_SP(df['Sal'],df['CTD chosen depth'],df['Lon E'],df['Lat N'])
df['pot_temp'] = gsw.pt_from_t(df['SA'],df['Temp'],df['CTD chosen depth'],0)

# STEP 2: calculate oxygen saturation
df['02sol_umolkg'] = gsw.O2sol_SP_pt(df['Sal'],df['pot_temp']) # https://www.teos-10.org/pubs/gsw/html/gsw_O2sol_SP_pt.html
# df['O2sol_mmolkg'] = df['02sol_umolkg']/1000
# print(df['02sol_umolkg']) # TODO having unit problems again with oxygen!

# STEP 3: compare with measured oxygen value
df['AOU'] = df['02sol_umolkg'] - df['Oxygen']
print(df['AOU'])

# Subset datasets
s2405_dbt = df.loc[(df['EXPOCODE'] == 'SFCS2405') & (df['Site'] == 'Doubtful')]
s2505_dbt = df.loc[(df['EXPOCODE'] == 'SFCS2505') & (df['Site'] == 'Doubtful')]

s2405_dus = df.loc[(df['EXPOCODE'] == 'SFCS2405') & (df['Site'] == 'Dusky')]
s2505_dus = df.loc[(df['EXPOCODE'] == 'SFCS2505') & (df['Site'] == 'Dusky')]

s309_dbt = df.loc[(df['EXPOCODE'] == 'S309') & (df['Site'] == 'Doubtful')]
s309_dus = df.loc[(df['EXPOCODE'] == 'S309') & (df['Site'] == 'Dusky')]

slope1, intercept1, r1, p1, stderr1 = linregress(s2405_dbt['AOU'], s2405_dbt['DELTA14C'])
slope2, intercept2, r2, p2, stderr2 = linregress(s2505_dbt['AOU'], s2505_dbt['DELTA14C'])
slope3, intercept3, r3, p3, stderr3 = linregress(s2405_dus['AOU'], s2405_dus['DELTA14C'])
slope4, intercept4, r4, p4, stderr4 = linregress(s2505_dus['AOU'], s2505_dus['DELTA14C'])
slope5, intercept5, r5, p5, stderr5 = linregress(s309_dbt['AOU'], s309_dbt['DELTA14C'])
slope6, intercept6, r6, p6, stderr6 = linregress(s309_dus['AOU'], s309_dus['DELTA14C'])

print(f'SFCS2405 DBT AOU vs D14C: y = {slope1:.2f}x + {intercept1:.2f}, r2 = {r1**2:.2f}')
print(f'SFCS2505 DBT AOU vs D14C: y = {slope2:.2f}x + {intercept2:.2f}, r2 = {r2**2:.2f}')
print(f'SFCS2405 DUS AOU vs D14C: y = {slope3:.2f}x + {intercept3:.2f}, r2 = {r3**2:.2f}')
print(f'SFCS2505 DUS AOU vs D14C: y = {slope4:.2f}x + {intercept4:.2f}, r2 = {r4**2:.2f}')
print(f'S309 DBT AOU vs D14C: y = {slope5:.2f}x + {intercept5:.2f}, r2 = {r5**2:.2f}')
print(f'S309 DUS AOU vs D14C: y = {slope6:.2f}x + {intercept6:.2f}, r2 = {r6**2:.2f}')

fig, axs = plt.subplots(3, 2, figsize=(16,16))  # 3 rows, 1 column

sc = axs[0,0].scatter(s2405_dbt['AOU'], s2405_dbt['DELTA14C'], c=s2405_dbt['Depth'], cmap=cmap, s=60, zorder=3, label='SFCS2405, Doubtful Sound')
axs[0,0].errorbar(s2405_dbt['AOU'], s2405_dbt['DELTA14C'], yerr=s2405_dbt['DELTA14C_Error'], fmt='none', ecolor='k', elinewidth=0.8, alpha=0.5, zorder=2)

sc = axs[1,0].scatter(s309_dbt['AOU'], s309_dbt['DELTA14C'], c=s309_dbt['Depth'], cmap=cmap, s=60, zorder=3, label='S309, Doubtful Sound')
axs[1,0].errorbar(s309_dbt['AOU'], s309_dbt['DELTA14C'], yerr=s309_dbt['DELTA14C_Error'], fmt='none', ecolor='k', elinewidth=0.8, alpha=0.5, zorder=2)

sc = axs[2,0].scatter(s2505_dbt['AOU'], s2505_dbt['DELTA14C'], c=s2505_dbt['Depth'], cmap=cmap, s=60, zorder=3, label='SFCS2505, Doubtful Sound')
axs[2,0].errorbar(s2505_dbt['AOU'], s2505_dbt['DELTA14C'], yerr=s2505_dbt['DELTA14C_Error'], fmt='none', ecolor='k', elinewidth=0.8, alpha=0.5, zorder=2)

sc = axs[0,1].scatter(s2405_dus['AOU'], s2405_dus['DELTA14C'], c=s2405_dus['Depth'], cmap=cmap, s=60, zorder=3, label='SFCS2405, Dusky Sound')
axs[0,1].errorbar(s2405_dus['AOU'], s2405_dus['DELTA14C'], yerr=s2405_dus['DELTA14C_Error'], fmt='none', ecolor='k', elinewidth=0.8, alpha=0.5, zorder=2)

sc = axs[1,1].scatter(s309_dus['AOU'], s309_dus['DELTA14C'], c=s309_dus['Depth'], cmap=cmap, s=60, zorder=3, label='S309, Dusky Sound')
axs[1,1].errorbar(s309_dus['AOU'],s309_dus['DELTA14C'], yerr=s309_dus['DELTA14C_Error'], fmt='none', ecolor='k', elinewidth=0.8, alpha=0.5, zorder=2)

sc = axs[2,1].scatter(s2505_dus['AOU'], s2505_dus['DELTA14C'], c=s2505_dus['Depth'], cmap=cmap, s=60, zorder=3, label='SFCS2505, Dusky Sound')
axs[2,1].errorbar(s2505_dus['AOU'],s2505_dus['DELTA14C'], yerr=s2505_dus['DELTA14C_Error'], fmt='none', ecolor='k', elinewidth=0.8, alpha=0.5, zorder=2)


# ADD TRENDLINES
# Trendline
x1 = s2405_dbt['AOU']; y_fit1 = slope1 * x1 + intercept1
x2 = s2505_dbt['AOU']; y_fit2 = slope2 * x2 + intercept2
x3 = s2405_dus['AOU']; y_fit3 = slope3 * x3 + intercept3
x4 = s2505_dus['AOU']; y_fit4 = slope4 * x4 + intercept4
x5 = s309_dbt['AOU']; y_fit5 = slope5 * x5 + intercept5
x6 = s309_dus['AOU']; y_fit6= slope6 * x6 + intercept6

axs[0,0].plot(x1, y_fit1 ,color='k',linestyle='--', label=f'Fit: r = {r1:.2f}, DBT SFCS2405', alpha=0.5)
axs[1,0].plot(x5, y_fit5 ,color='k',linestyle='--', label=f'Fit: r = {r5:.2f}, DBT S309', alpha=0.5)
axs[2,0].plot(x2, y_fit2 ,color='k',linestyle='--', label=f'Fit: r = {r2:.2f}, DBT SFCS2505', alpha=0.5)

axs[0,1].plot(x3, y_fit3 ,color='k',linestyle='--', label=f'Fit: r = {r3:.2f}, DUS, SFCS2405', alpha=0.5)
axs[1,1].plot(x6, y_fit6 ,color='k',linestyle='--', label=f'Fit: r = {r6:.2f}, DUS, S309', alpha=0.5)
axs[2,1].plot(x4, y_fit4 ,color='k',linestyle='--', label=f'Fit: r = {r4:.2f}, DUS, SFCS2505', alpha=0.5)

axs[0,0].legend()
axs[1,0].legend()
axs[2,0].legend()

axs[0,1].legend()
axs[1,1].legend()
axs[2,1].legend()

cbar = plt.colorbar(sc, ax=axs[0,1]); cbar.set_label('Depth')
cbar = plt.colorbar(sc, ax=axs[1,1]); cbar.set_label('Depth')
cbar = plt.colorbar(sc, ax=axs[2,1]); cbar.set_label('Depth')

axs[0,0].set_title('Patea/Doubtful Sound')
axs[0,1].set_title('Tamatea/Dusky Sound')

axs[1,0].set_xlabel('AOU (µmol kg$^{-1}$)')
axs[1,1].set_xlabel('AOU (µmol kg$^{-1}$)')
axs[0,0].set_ylabel(r'$\Delta^{14}$C')
axs[1,0].set_ylabel(r'$\Delta^{14}$C')

axs[0,0].set_ylim(15, 35)
axs[1,0].set_ylim(15, 35)
axs[2,0].set_ylim(15, 35)

axs[0,1].set_ylim(15, 35)
axs[1,1].set_ylim(15, 35)
axs[2,1].set_ylim(15, 35)

axs[0,0].set_xlim(0,275)
axs[1,0].set_xlim(0,275)
axs[2,0].set_xlim(0,275)

axs[0,1].set_xlim(0,275)
axs[1,1].set_xlim(0,275)
axs[2,1].set_xlim(0,275)

plt.savefig(f"C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/13_AOU_plot/AOU.png", dpi=300, bbox_inches="tight")

