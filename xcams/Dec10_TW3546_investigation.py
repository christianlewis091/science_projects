# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# from cmcrameri import cm
# from os import listdir
# from os.path import isfile, join


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from cmcrameri import cm
from os import listdir
from os.path import isfile, join
from matplotlib.colors import Normalize

mypath = 'C:/Users/clewis/IdeaProjects/GNS/xcams/Dec_10_2024/outfiles/subset'

"""
17/1/25. Is RTS related to transmission, and/or beam current? 
"""
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

std_pos_reg = [0, 7, 14, 21, 28, 35]
std_pos_air = [0, 5, 10, 15, 20, 25, 30]

# Set up the figure
fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(3, 1)
gs.update(wspace=.15, hspace=0.4)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[2, 0])

# Define colormap and normalization
colormap = cm.roma  # Choose a colormap from cmcrameri
normalize = Normalize(vmin=0, vmax=1)  # Calibration values are already normalized (0-1)

for i in range(0, len(onlyfiles)):
    df = pd.read_csv(f'{mypath}/{onlyfiles[i]}', skiprows=2, sep='\t')
    print(df.columns)
    # Define standards and calibration for each file
    if onlyfiles[i] == 'TW3549_1.out':
        stds = std_pos_reg
        calib = 90.0 / 100  # Normalize to 0-1
    elif onlyfiles[i] == 'TW3547_p1.out':
        stds = std_pos_reg
        calib = 2.6 / 100
    elif onlyfiles[i] == 'TW3546_p2.out':
        stds = std_pos_reg
        calib = 0.1 / 100
    elif onlyfiles[i] == 'TW3545_p1.out':
        stds = [3, 9, 13, 26, 29, 32]
        calib = 11.2 / 100
    elif onlyfiles[i] == 'TW3544_p1.out':
        stds = [0, 8, 16, 20, 24, 28]
        calib = 13.9 / 100
    elif onlyfiles[i] == 'TW3543_1.out':
        stds = std_pos_reg
        calib = 29.7 / 100
    elif onlyfiles[i] == 'TW3542_1.out':
        stds = std_pos_reg
        calib = 40.4 / 100
    elif onlyfiles[i] == 'TW3541_1.out':
        stds = std_pos_reg
        calib = 21.1 / 100
    elif onlyfiles[i] == 'TW3550_p1.out':
        stds = [0,6,12,18,24,30,35]
        calib = 52 / 100

    # Get only standards (interested in calibration)
    df = df.loc[df['position'].isin(stds)]
    color = colormap(normalize(calib))  # Map calibration to color

    # Calculate RTS roughly
    c14c12 = df['14Ccnts'] / df['12Ccurr']
    c13c12 = df['13Ccurr'] / df['12Ccurr']
    trans = df['12Ccurr'] / df['12CLEcurr']
    az = df['14Ccnts']*df['12Ccurr'] / (df['13Ccurr'])**2

    # Scatter plots with color
    ax1.scatter(df['12CLEcurr'], az, label=f'{onlyfiles[i]}',color=color) # add color=color for calibration based colors
    ax2.scatter(c13c12, az, label=f'{onlyfiles[i]}',color=color)# add color=color for calibration based colors
    ax3.scatter(trans, az, label=f'{onlyfiles[i]}',color=color)# add color=color for calibration based colors

# Add colorbar for context (uncomment if you want colors back in based on calibration!
sm = plt.cm.ScalarMappable(cmap=colormap, norm=normalize)
sm.set_array([])  # Required for the colorbar
cbar = plt.colorbar(sm, ax=[ax1, ax2, ax3], orientation='vertical', pad=0.05)
cbar.set_label('Calibration (Normalized)', rotation=270, labelpad=15)

# Add legends
ax1.legend()

ax1.set_ylabel("14Ccnts*12Ccurr / (13Ccurr)**2")
ax2.set_ylabel("14Ccnts*12Ccurr / (13Ccurr)**2")
ax3.set_ylabel("14Ccnts*12Ccurr / (13Ccurr)**2")

ax1.set_xlabel("12C LE Curr")
ax2.set_xlabel("13CCurr/12CCurr")
ax3.set_xlabel("12CHe curr / 12C Le Curr (Transmission)")

plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Dec_10_2024/17_01_25_Fig1_colors_az.png', dpi=300, bbox_inches="tight")
plt.close()





#
# mypath = 'C:/Users/clewis/IdeaProjects/GNS/xcams/Dec_10_2024/outfiles/subset'
#
# """
# 17/1/25. Is RTS related to transmission, and/or beam current?
# """
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#
#
# std_pos_reg = [0,7,14,21,28,35]
# std_pos_air = [0,5,10,15,20,25,30]
#
# fig = plt.figure(figsize=(8, 8))
# gs = gridspec.GridSpec(3, 1)
# gs.update(wspace=.15, hspace=0.25)
#
# ax1 = fig.add_subplot(gs[0, 0])
# ax2 = fig.add_subplot(gs[1, 0])
# ax3 = fig.add_subplot(gs[2, 0])
# for i in range(0, len(onlyfiles)):
#
#     df = pd.read_csv(f'{mypath}/{onlyfiles[i]}', skiprows=2, sep='\t')
#     # print(df.columns)
#     # where are the standards in each?
#     if onlyfiles[i] == 'TW3549_1.out':
#         stds = std_pos_reg
#         calib = 90.0/100 # normalize to make work with colors between 0-1
#     if onlyfiles[i] == 'TW3547_p1.out':
#         stds = std_pos_reg
#         calib = 2.6/100
#     if onlyfiles[i] == 'TW3546_p2.out':
#         stds = std_pos_reg
#         calib = 0.1/100
#     if onlyfiles[i] == 'TW3545_p1.out':
#         stds = [3,9,13,26,29,32]
#         calib = 11.2/100
#     if onlyfiles[i] == 'TW3544_p1.out':
#         stds = [0,8,16,20,24,28]
#         calib = 13.9/100
#     if onlyfiles[i] == 'TW3543_1.out':
#         stds = std_pos_reg
#         calib = 29.7/100
#     if onlyfiles[i] == 'TW3542_1.out':
#         stds = std_pos_reg
#         calib = 40.4/100
#     if onlyfiles[i] == 'TW3541_1.out':
#         stds = std_pos_reg
#         calib = 21.1/100
#
#     # get only standards above (I'm interested in the calibration)
#     df = df.loc[df['position'].isin(stds)]
#     df['c'] = calib
#     print(onlyfiles[i])
#     print(calib)
#
#     # calc RTS rougly
#     c14c12 = df['14Ccnts']/df['12Ccurr']
#     c13c12 = df['13Ccurr']/df['12Ccurr']
#     trans = df['12Ccurr']/df['12CLEcurr']
#     ax1.scatter(df['12CLEcurr'], c14c12, label=f'{onlyfiles[i]}')
#     ax1.legend()
#
#     ax2.scatter(c13c12, c14c12, label=f'{onlyfiles[i]}')
#     ax3.scatter(trans, c14c12, label=f'{onlyfiles[i]}')
#
#
#
#
#
# # plt.xlabel('12CLECurr')
# # plt.ylabel("14Ccnts/12Ccurr")
# # plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Dec_10_2024/17_01_25_Fig1.png', dpi=300, bbox_inches="tight")
# # plt.close()
# plt.show()
#
#     # print(df.columns)
#     # plt.scatter([1,2], [1,2])
#     # plt.show()
#









"""
Older code from december 2024
"""
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# print(onlyfiles)
#
# fig = plt.figure(figsize=(8,6))
# for i in range(0, len(onlyfiles)):
#
#     df = pd.read_csv(f'{mypath}/{onlyfiles[i]}', skiprows=2, sep='\t')
#     df['T']= df['12Ccurr']/df['12CLEcurr']
#
#     # calculate per cathode average trans
#     tmean = []
#     tstd = []
#
#     pos = np.unique(df['position'])
#     for j in range(0, len(pos)):
#         df_j= df.loc[df['position'] == pos[j]]
#         tmean.append(np.mean(df_j['T']))
#         tstd.append(np.std(df_j['T']))
#
#     result = pd.DataFrame({'position': pos, 'Trans': tmean, 'Trans_err': tstd})
#
#     plt.errorbar(result['position'], result['Trans'], result['Trans_err'], label=f'{onlyfiles[i]}', marker='o', linestyle='', alpha=0.7)
# plt.ylabel('AccelNet Output HE 12C/ LE 12C')
# plt.xlabel('Cathode Position')
# plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Dec_10_2024/Fig3.png', dpi=300, bbox_inches="tight")
# plt.close()
#
# # repeat with
# for i in range(0, len(onlyfiles)):
#
#     df = pd.read_csv(f'{mypath}/{onlyfiles[i]}', skiprows=2, sep='\t')
#     df['T']= df['12Ccurr']/df['12CLEcurr']
#     plt.scatter(df['run'], df['T'], label=f'{onlyfiles[i]}', marker='o', linestyle='', alpha=0.4)
# plt.ylabel('AccelNet Output HE 12C/ LE 12C')
# plt.xlabel('Run Number')
# plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Dec_10_2024/Fig4.png', dpi=300, bbox_inches="tight")
# plt.close()






# df3546 = pd.read_csv(r'I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3500-3549\TW3546\TW3546_p2.out', skiprows=2, sep='\t')
# df3545 = pd.read_csv(r'I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3500-3549\TW3545\TW3545_p1.out', skiprows=2, sep='\t')
# df3543 = pd.read_csv(r'I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3500-3549\TW3543\TW3543_p1.out', skiprows=2, sep='\t')
# df3521 = pd.read_csv(r'I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3500-3549\TW3521\TW3521_1.out', skiprows=2, sep='\t')
# # print(df.columns)
#
# df3546['trans'] = df3546['12Ccurr']/df3546['12CLEcurr']
# df3545['trans'] = df3545['12Ccurr']/df3545['12CLEcurr']
# df3543['trans'] = df3543['12Ccurr']/df3543['12CLEcurr']
# df3521['trans'] = df3521['12Ccurr']/df3521['12CLEcurr']
#
# plt.scatter(df3546['run'], df3546['trans'], label='3546')
# plt.scatter(df3545['run'], df3545['trans'], label='3545')
# plt.scatter(df3543['run'], df3543['trans'], label='3543')
# plt.scatter(df3521['run'], df3521['trans'], label='3521')
#
# plt.legend()
# plt.show()



"""
Seems like there is a trend in the standards between transmission and 14/12; f-val below is the final data
"""

# standards = [0,5,10,15,20,25,30,35]
# f_val = [1.00289, 1.00222, .99964, 1.00020,.99995, .99818, .99413, 1.00661] # data from 3546_2.out
#
# # stds = df.loc[df['position'].isin(standards)]
#
# mean_trans = []
# std_trans = []
# for i in range(0, len(standards)):
#     std1 = df.loc[df['position'] == standards[i]]
#     trans = std1['12Ccurr']/std1['12CLEcurr']
#     y = np.mean(trans)
#     yer = np.std(trans)
#     plt.errorbar(f_val[i], y, yerr=yer, marker='o', label=f'{standards[i]}') # plot transmission by the resulting 14C value
#     plt.legend()
#
# plt.xlabel('RTS value from final calibration')
# plt.ylabel('12Ccurr/12CLEcurr (Transmission)')
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Dec_10_2024/Fig1.png', dpi=300, bbox_inches="tight")
# plt.close()

"""
I'm finding it extremely difficult to reconstruct the actual DMAN output from raw collected data. See AMS notebook from Dec 12,2024
Two versions of 
descriptions of the calculatinos exist, one is Root/AccelNet/Manual2/man7/AMSformulae, and the other is a manual printout
that I found in the cabinet attached to an email between NEC and Albert. I need to dig thruogh Albert's old stuff to find it, 
but now we can use a proxy. 
"""

# df['13Civg'] = df['13Ccurr']/1800 # from /../../AMSFormulae
# df['12Civg'] = df['12Ccurr']/1800 #from /../../AMSFormulae
# df['13/12He'] = df['13Civg']/df['12Civg']
#
# df['CntRate'] = df['14Ccnts']/180
# df['Mode5'] = (df['12Ccurr']*df['CntRate']/df['13Ccurr']**2)*((1-19)/-1000) # this is WRONG but it matches CALAMS...
# print(max(df['Mode5']))
#
# position = np.unique(df['position'])
# pos = []
# mode5_res = []
# mode5_res_std = []
# trans = []
# trans_std = []
#
# for i in range(0, len(position)):
#     df_i = df.loc[df['position'] == position[i]]
#     pos.append(position[i])
#
#     mode5_res.append(np.mean(df_i['Mode5']))
#     mode5_res_std.append(np.std(df_i['Mode5']))
#
#     trans.append(np.mean(df_i['12Ccurr']/df_i['12CLEcurr']))
#     trans_std.append(np.std(df_i['12Ccurr']/df_i['12CLEcurr']))
#
# df_out = pd.DataFrame({'P':pos, 'M5':mode5_res, 'M5_err':mode5_res_std, 'T': trans, 'Terr': trans_std})
# print(df_out)
#
# plt.errorbar(df_out['T'], df_out['M5'], xerr=df_out['Terr'], yerr=df_out['M5_err'], marker='o', linestyle='', alpha=0.1)
#
# for i in range(0, len(standards)):
#     std1 = df_out.loc[df_out['P'] == standards[i]]
#     plt.errorbar(std1['T'], std1['M5'], xerr=std1['Terr'], yerr=std1['M5_err'], marker='o', linestyle='', label=f'{standards[i]}') # plot transmission by the resulting 14C value
# plt.legend()
# plt.ylim(0.24, 0.3)
# plt.xlim(1650, 1690)
# plt.xlabel('Transmission (CALAMS units)')
# plt.ylabel('Mode5 rough Calc')
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Dec_10_2024/Fig2.png', dpi=300, bbox_inches="tight")
# plt.close()


