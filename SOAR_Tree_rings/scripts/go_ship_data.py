"""
https://cchdo.ucsd.edu/cruise/33RR20160208
See above link for the data
"""

from mpl_toolkits.basemap import Basemap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import csv
import pandas.errors


"""
These two lines identify and make a list of all the filenames in the specific directory of the computer
"""
all_files = os.listdir(r"H:\Science\Datasets\Hydrographic\BatchSOCeDownload_noheader")
csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
# these two lines above definitely are a level up...

"""
For each of the files in the list above, I'm going to generate a plot with a map, and DO, and DIC data, and maybe TS data
"""
len1 = 83
for i in range(0, len1):  # LEN set to 83 since I wanted to test the code before removing the rest of the headers by hand...
    name = csv_files[i]
    print(name)
    df = pd.read_csv(f"H:/Science/Datasets/Hydrographic/BatchSOCeDownload_noheader/{name}").dropna(subset='DATE').reset_index(drop=True)
    try:
        # Find EXPOCODE for MAP LABEL
        expocode = df['EXPOCODE']
        expocode = expocode[0]
        print(expocode)

        # FIND LATS AND LONS FOR MAP
        minlat, maxlat = min(np.unique(df['LATITUDE'])), max(np.unique(df['LATITUDE']))
        minlon, maxlon = min(np.unique(df['LONGITUDE'])), max(np.unique(df['LONGITUDE']))

        # make a map of the cruise and data using gridspec:
        fig = plt.figure(figsize=(15, 12))
        gs = gridspec.GridSpec(20, 20)
        gs.update(wspace=.5, hspace=.5)

        # create the first subplot
        xtr_subsplot = fig.add_subplot(gs[0:9, 0:9])
        try:
            dlat = 20  # adds a buffer to see around the map
            map = Basemap(llcrnrlat=minlat-dlat, urcrnrlat=maxlat+dlat, llcrnrlon=minlon-dlat, urcrnrlon=maxlon+dlat, resolution='i')
        except:  # this exists because sometimes the 20 is too much and it gets out of range and crashes the code
            dlat = 10  # adds a buffer to see around the map
            map = Basemap(llcrnrlat=minlat-dlat, urcrnrlat=maxlat+dlat, llcrnrlon=minlon-dlat, urcrnrlon=maxlon+dlat, resolution='i')
        # parameters to make the plot more beautiful
        map.drawcoastlines(linewidth=0.5)
        map.drawmapboundary(fill_color='paleturquoise', linewidth=0.5)
        map.fillcontinents(color='coral', lake_color='aqua')
        map.drawcountries()
        map.drawparallels(np.arange(-90, 90, 20), labels=[False, False, False, False], fontsize=7, linewidth=0.5)
        map.drawmeridians(np.arange(-180, 180, 20), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
        x, y = map(df['LATITUDE'], (df['LONGITUDE']))
        map.scatter(y, x, marker='D',color='black', s= 10)
        plt.title(f'{expocode}')

        # create the next subplot\
        xtr_subsplot = fig.add_subplot(gs[0:4, 10:19])
        # need to adujst the data because it's reading in strangely as strings...
        cols = list(df.columns)

        if 'OXYGEN' in cols:
            pltname = 'Dissolved Oxygen (UMOL/KG)'
            oxy = np.array(df['OXYGEN'], dtype=np.float32)
            lat = np.array(df['LATITUDE'], dtype=np.float32)
            ctdprs = np.array(df['CTDPRS'], dtype=np.float32)
            df1 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, "OXYGEN":oxy})

            plt.title(f'{pltname}')
            plt.xlabel('Latitude')
            plt.ylabel('Depth (CTD Pressure)')
            df1 = df1.loc[df1['OXYGEN'] > -998]
            plt.scatter(df1['LATITUDE'], df1['CTDPRS'], c=df1['OXYGEN'], cmap='magma')
            plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))

        if 'NITRAT' in cols:
            xtr_subsplot = fig.add_subplot(gs[5:9, 10:19])
            pltname = 'NITRATE (UMOL/KG)'
            nitrate = np.array(df['NITRAT'], dtype=np.float32)
            lat = np.array(df['LATITUDE'], dtype=np.float32)
            ctdprs = np.array(df['CTDPRS'], dtype=np.float32)
            df2 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, 'NITRAT':nitrate})

            plt.title(f'{pltname}')
            plt.xlabel('Latitude')
            plt.ylabel('Depth (CTD Pressure)')
            df2 = df2.loc[df2['NITRAT'] > -998]
            plt.scatter(df2['LATITUDE'], df2['CTDPRS'], c=df2['NITRAT'], cmap='magma')
            plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))

        if 'DELC14' in cols:
            xtr_subsplot = fig.add_subplot(gs[10:14, 10:19])
            pltname = 'DELC14 (/mille)'
            d14c = np.array(df['DELC14'], dtype=np.float32)
            lat = np.array(df['LATITUDE'], dtype=np.float32)
            ctdprs = np.array(df['CTDPRS'], dtype=np.float32)
            df3 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, 'DELC14':d14c})

            plt.title(f'{pltname}')
            plt.xlabel('Latitude')
            plt.ylabel('Depth (CTD Pressure)')
            df3 = df3.loc[df3['DELC14'] > -998]
            plt.scatter(df3['LATITUDE'], df3['CTDPRS'], c=df3['DELC14'], cmap='magma')
            plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))
            x = 1

        if 'TCARBN' in cols:
            xtr_subsplot = fig.add_subplot(gs[15:19, 10:19])
            pltname = 'TCARBN'
            tcarbn = np.array(df['TCARBN'], dtype=np.float32)
            lat = np.array(df['LATITUDE'], dtype=np.float32)
            ctdprs = np.array(df['CTDPRS'], dtype=np.float32)
            df4 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, 'TCARBN':tcarbn})

            plt.title(f'{pltname}')
            plt.xlabel('Latitude')
            plt.ylabel('Depth (CTD Pressure)')
            df4 = df4.loc[df4['TCARBN'] > -998]
            plt.scatter(df4['LATITUDE'], df4['CTDPRS'], c=df4['TCARBN'], cmap='magma')
            plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))

        print(cols)
        try:
            if 'CTDSAL' and 'CTDTMP' and 'CTDPRS' in cols:
                print("I have all three")
                xtr_subsplot = fig.add_subplot(gs[10:19, 0:9])
                pltname = 'TvS'
                temp = np.array(df['CTDTMP'], dtype=np.float32)
                sal = np.array(df['CTDSAL'], dtype=np.float32)
                ctdprs = np.array(df['CTDPRS'], dtype=np.float32)
                df5 = pd.DataFrame({"CTDTMP": temp, "CTDPRS": ctdprs, 'SALNTY': sal})

                plt.title(f'{pltname}')
                plt.ylabel('CTDTMP')
                plt.xlabel('SALINITY')
                df5 = df5.loc[df5['SALNTY'] > -998]
                plt.scatter(df5['CTDTMP'], df5['SALNTY'], c=df5['CTDPRS'], cmap='magma')
                plt.colorbar()
        except KeyError:
            continue

        plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Hydrography/{expocode}',
                    dpi=300, bbox_inches="tight")
        plt.close()
    except ValueError:
        continue


















    #
    #
    #
    #
    #
    #
    #
    #
    #     sal = np.array(df['CTDSAL'], dtype=np.float32)
    #     df = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, "OXYGEN":oxy, "SALNTY": sal})
    # # df = df.loc[df['y'] < 2000]
    #
    #
    #
    # plt.title('IO8: DIC 14C')
    # df = df.loc[df['OXYGEN'] > -998]
    # plt.scatter(df['LATITUDE'], df['CTDPRS'], c=df['OXYGEN'], cmap='magma')
    # plt.colorbar(), plt.ylim(max(df['CTDPRS']), min(df['CTDPRS'])), plt.xlim(-70, -25)
    #
    #
    # plt.show()
    #
    #
    #














    # ax.set_title('New Zealand Tree Ring Sampling Sites')





























#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/4_33RR20160208_hy1.csv', skiprows=166).dropna(subset="DATE")
#
# z = np.array(df['DELC14'], dtype=np.float32)
# x = np.array(df['LATITUDE'], dtype=np.float32)
# y = np.array(df['CTDPRS'], dtype=np.float32)
# o = np.array(df['OXYGEN'], dtype=np.float32)
# s = np.array(df['CTDSAL'], dtype=np.float32)
#
# df = pd.DataFrame({"x": x, "y": y, "z": z, "o":o, "s": s})
# # df = df.loc[df['y'] < 2000]
#
# fig = plt.figure(4, figsize=(7.5, 7.5))
# gs = gridspec.GridSpec(9, 2)
# gs.update(wspace=.15, hspace=2)
#
# # make first plot
# xtr_subsplot = fig.add_subplot(gs[0:3, 0:2])
# plt.title('IO8: DIC 14C')
# df_1 = df.loc[df['z'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['z'], cmap='magma')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
#
# xtr_subsplot = fig.add_subplot(gs[3:6, 0:2])
# plt.title('Oxygen')
# df_1 = df.loc[df['o'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['o'], cmap='magma')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# xtr_subsplot = fig.add_subplot(gs[6:9, 0:2])
# plt.title('Salinity')
# df_1 = df.loc[df['s'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['s'], cmap='magma')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
#
# plt.xlabel('Latitude', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/io8_Ctd.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
# #
# df2 = df.loc[(df['z'] > -998) & (df['o'] > -998)]
# plt.scatter(df2['o'], df2['z'], c=df2['y'], cmap='magma_r')
# plt.xlabel('Oxygen')
# plt.ylabel('DIC14C')
# plt.colorbar()
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/io8_Ctd_2.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
#
# """
# Take 2
# """
# # read in all the data from previous IO8 cruises in the Southern Ocean
# df_16 = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/4_33RR20160208_hy1.csv', skiprows=166).dropna(subset="DATE")
# df_07 = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/33RR20070204_hy1.csv', skiprows=36).dropna(subset="DATE")
# df_94 = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/316N145_5_hy1.csv', skiprows=16).dropna(subset="DATE")
# # df_03 = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/09AR20030103_hy1.csv', skiprows=7).dropna(subset="DATE")  No DI14C data
#
# xsize = 18
# ysize = 9
# fig = plt.figure(4, figsize=(7.5, 7.5))
# gs = gridspec.GridSpec(ysize, xsize)
# gs.update(wspace=.15, hspace=2)
#
# """
# 2016 data
# """
# z = np.array(df_16['DELC14'], dtype=np.float32)
# x = np.array(df_16['LATITUDE'], dtype=np.float32)
# y = np.array(df_16['CTDPRS'], dtype=np.float32)
# o = np.array(df_16['OXYGEN'], dtype=np.float32)
# s = np.array(df_16['CTDSAL'], dtype=np.float32)
#
# df_16 = pd.DataFrame({"x": x, "y": y, "z": z, "o":o, "s": s})
# df_1 = df_16.loc[df_16['y'] < 2000]  # find all depths above 2000m
#
# xtr_subsplot = fig.add_subplot(gs[6:9, 0:6])
# df_1 = df_1.loc[df_1['z'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['z'], cmap='viridis', vmin=-300, vmax=100)
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# xtr_subsplot = fig.add_subplot(gs[6:9, 6:12])
# df_1 = df_1.loc[df_1['o'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['o'], cmap='magma')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# xtr_subsplot = fig.add_subplot(gs[6:9, 12:18])
# df_1 = df_1.loc[df_1['s'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['s'], cmap='Blues')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# """
# 2007 data
# """
# z = np.array(df_07['DELC14'], dtype=np.float32)
# x = np.array(df_07['LATITUDE'], dtype=np.float32)
# y = np.array(df_07['CTDPRS'], dtype=np.float32)
# o = np.array(df_07['OXYGEN'], dtype=np.float32)
# s = np.array(df_07['CTDSAL'], dtype=np.float32)
#
# df_07 = pd.DataFrame({"x": x, "y": y, "z": z, "o":o, "s": s})
# df_1 = df_07.loc[df_07['y'] < 2000]  # find all depths above 2000m
#
# xtr_subsplot = fig.add_subplot(gs[3:6, 0:6])
# df_1 = df_1.loc[df_1['z'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['z'], cmap='viridis', vmin=-300, vmax=100)
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# xtr_subsplot = fig.add_subplot(gs[3:6, 6:12])
# df_1 = df_1.loc[df_1['o'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['o'], cmap='magma')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# xtr_subsplot = fig.add_subplot(gs[3:6, 12:18])
# df_1 = df_1.loc[df_1['s'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['s'], cmap='Blues')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# """
# 1994 data
# """
# z = np.array(df_94['DELC14'], dtype=np.float32)
# x = np.array(df_94['LATITUDE'], dtype=np.float32)
# y = np.array(df_94['CTDPRS'], dtype=np.float32)
# o = np.array(df_94['OXYGEN'], dtype=np.float32)
# s = np.array(df_94['CTDSAL'], dtype=np.float32)
#
# df_94 = pd.DataFrame({"x": x, "y": y, "z": z, "o":o, "s": s})
# df_1 = df_94.loc[df_94['y'] < 2000]  # find all depths above 2000m
#
# xtr_subsplot = fig.add_subplot(gs[0:3, 0:6])
# df_1 = df_1.loc[df_1['z'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['z'], cmap='viridis', vmin=-300, vmax=100)
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# xtr_subsplot = fig.add_subplot(gs[0:3, 6:12])
# df_1 = df_1.loc[df_1['o'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['o'], cmap='magma')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# xtr_subsplot = fig.add_subplot(gs[0:3, 12:18])
# df_1 = df_1.loc[df_1['s'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['s'], cmap='Blues')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/io8_Ctd_3.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
#
#
#
# """
# P18
# """
#
# df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/33RO20161119_hy1.csv', skiprows=174).dropna(subset="DATE")
#
# z = np.array(df['DELC14'], dtype=np.float32)
# x = np.array(df['LATITUDE'], dtype=np.float32)
# y = np.array(df['CTDPRS'], dtype=np.float32)
# o = np.array(df['OXYGEN'], dtype=np.float32)
# s = np.array(df['TCARBN'], dtype=np.float32)
#
# df = pd.DataFrame({"x": x, "y": y, "z": z, "o":o, "s": s})
# # df = df.loc[df['y'] < 2000]
#
# fig = plt.figure(4, figsize=(7.5, 7.5))
# gs = gridspec.GridSpec(9, 2)
# gs.update(wspace=.15, hspace=2)
#
# # make first plot
# xtr_subsplot = fig.add_subplot(gs[0:3, 0:2])
# plt.title('P18: DIC 14C')
# df_1 = df.loc[df['z'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['z'], cmap='viridis')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
#
# xtr_subsplot = fig.add_subplot(gs[3:6, 0:2])
# plt.title('OXYGEN')
# df_1 = df.loc[df['o'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['o'], cmap='viridis')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# xtr_subsplot = fig.add_subplot(gs[6:9, 0:2])
# plt.title('TCARBON')
# df_1 = df.loc[df['s'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['s'], cmap='viridis')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
#
# plt.xlabel('Latitude', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/P18_Ctd.png',
#             dpi=300, bbox_inches="tight")
#
#
# """
# P16
# """
#
# df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/33RR200501_hy1.csv', skiprows=93).dropna(subset="DATE")
#
# z = np.array(df['DELC14'], dtype=np.float32)
# x = np.array(df['LATITUDE'], dtype=np.float32)
# y = np.array(df['CTDPRS'], dtype=np.float32)
# o = np.array(df['OXYGEN'], dtype=np.float32)
# s = np.array(df['TCARBN'], dtype=np.float32)
#
# df = pd.DataFrame({"x": x, "y": y, "z": z, "o":o, "s": s})
# # df = df.loc[df['y'] < 2000]
#
# fig = plt.figure(4, figsize=(7.5, 7.5))
# gs = gridspec.GridSpec(9, 2)
# gs.update(wspace=.15, hspace=2)
#
# # make first plot
# xtr_subsplot = fig.add_subplot(gs[0:3, 0:2])
# plt.title('P16: DIC 14C')
# df_1 = df.loc[df['z'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['z'], cmap='viridis')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
#
# xtr_subsplot = fig.add_subplot(gs[3:6, 0:2])
# plt.title('OXYGEN')
# df_1 = df.loc[df['o'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['o'], cmap='viridis')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
# xtr_subsplot = fig.add_subplot(gs[6:9, 0:2])
# plt.title('TCARBON')
# df_1 = df.loc[df['s'] > -998]
# plt.scatter(df_1['x'], df_1['y'], c=df_1['s'], cmap='viridis')
# plt.colorbar(), plt.ylim(max(df_1['y']), min(df_1['y'])), plt.xlim(-70, -25)
#
#
# plt.xlabel('Latitude', fontsize=14)  # label the y axis
# plt.show()
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/P16_Ctd.png',
#             dpi=300, bbox_inches="tight")
# # plt.close()
# # #
# # df2 = df.loc[(df['z'] > -998) & (df['o'] > -998)]
# # plt.scatter(df2['o'], df2['z'], c=df2['y'], cmap='magma_r')
# # plt.xlabel('Oxygen')
# # plt.ylabel('DIC14C')
# # plt.colorbar()
# # # plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/io8_Ctd_2.png',
# # #             dpi=300, bbox_inches="tight")
# # # plt.close()
# #
# # plt.show()
#
#
#
#
#









