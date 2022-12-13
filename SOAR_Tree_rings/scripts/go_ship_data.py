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

df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/test_all.csv')

indexes = np.unique(df['Cat4Index'])

for i in range(0, len(indexes)):
    print(indexes[i])

    thiscruise = df.loc[df['Cat4Index'] == indexes[i]]
    print(thiscruise)
    #
    fig = plt.figure(figsize=(15, 12))
    gs = gridspec.GridSpec(20, 20)
    gs.update(wspace=.5, hspace=.5)

    xtr_subsplot = fig.add_subplot(gs[0:9, 0:9])

    minlat = min((thiscruise['LATITUDE']))
    minlon = min((thiscruise['LONGITUDE']))
    maxlat = max((thiscruise['LATITUDE']))
    maxlon = max((thiscruise['LONGITUDE']))

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
    x, y = map(thiscruise['LATITUDE'], (thiscruise['LONGITUDE']))
    map.scatter(y, x, marker='D',color='black', s= 10)
    plt.title(f'{indexes[i]}')


    # create the next subplot\
    try:
        xtr_subsplot = fig.add_subplot(gs[0:4, 10:19])
        pltname = 'Dissolved Oxygen (UMOL/KG)'
        plt.xlabel('Latitude')
        plt.ylabel('Depth (CTD Pressure)')
        df1 = thiscruise.loc[(thiscruise['OXYGEN'] > -998) & (thiscruise['CTDPRS'] > -998) & (thiscruise['LATITUDE'] > -998)]

        plt.scatter(df1['LATITUDE'], df1['CTDPRS'], c=df1['OXYGEN'], cmap='magma')
        plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))
    except ValueError:
        x = 1

    # create the next subplot\
    try:
        xtr_subsplot = fig.add_subplot(gs[5:9, 10:19])
        plt.xlabel('Latitude')
        plt.title('NITRATE')
        plt.ylabel('Depth (CTD Pressure)')
        df1 = thiscruise.loc[(thiscruise['NITRAT'] > -998) & (thiscruise['CTDPRS'] > -998) & (thiscruise['LATITUDE'] > -998)]

        plt.scatter(df1['LATITUDE'], df1['CTDPRS'], c=df1['NITRAT'], cmap='magma')
        plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))
    except ValueError:
        x = 1

    try:
        xtr_subsplot = fig.add_subplot(gs[10:14, 10:19])
        plt.xlabel('Latitude')
        plt.title('DELC14')
        plt.ylabel('Depth (CTD Pressure)')
        df1 = thiscruise.loc[(thiscruise['DELC14'] > -998) & (thiscruise['CTDPRS'] > -998) & (thiscruise['LATITUDE'] > -998)]

        plt.scatter(df1['LATITUDE'], df1['CTDPRS'], c=df1['DELC14'], cmap='magma')
        plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))
    except ValueError:
        x = 1

    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Hydrography/{indexes[i]}',
            dpi=300, bbox_inches="tight")
    plt.close()







#     # need to adujst the data because it's reading in strangely as strings...
    #     cols = list(df.columns)
    #
    #     if 'OXYGEN' in cols:
    #         pltname = 'Dissolved Oxygen (UMOL/KG)'
    #         oxy = np.array(df['OXYGEN'], dtype=np.float32)
    #         lat = np.array(df['LATITUDE'], dtype=np.float32)
    #         ctdprs = np.array(df['CTDPRS'], dtype=np.float32)
    #         df1 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, "OXYGEN":oxy})
    #
    #         plt.title(f'{pltname}')
    #         plt.xlabel('Latitude')
    #         plt.ylabel('Depth (CTD Pressure)')
    #         df1 = df1.loc[df1['OXYGEN'] > -998]
    #         plt.scatter(df1['LATITUDE'], df1['CTDPRS'], c=df1['OXYGEN'], cmap='magma')
    #         plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))
    #
    #     if 'NITRAT' in cols:
    #         xtr_subsplot = fig.add_subplot(gs[5:9, 10:19])
    #         pltname = 'NITRATE (UMOL/KG)'
    #         nitrate = np.array(df['NITRAT'], dtype=np.float32)
    #         lat = np.array(df['LATITUDE'], dtype=np.float32)
    #         ctdprs = np.array(df['CTDPRS'], dtype=np.float32)
    #         df2 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, 'NITRAT':nitrate})
    #
    #         plt.title(f'{pltname}')
    #         plt.xlabel('Latitude')
    #         plt.ylabel('Depth (CTD Pressure)')
    #         df2 = df2.loc[df2['NITRAT'] > -998]
    #         plt.scatter(df2['LATITUDE'], df2['CTDPRS'], c=df2['NITRAT'], cmap='magma')
    #         plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))
    #
    #     if 'DELC14' in cols:
    #         xtr_subsplot = fig.add_subplot(gs[10:14, 10:19])
    #         pltname = 'DELC14 (/mille)'
    #         d14c = np.array(df['DELC14'], dtype=np.float32)
    #         lat = np.array(df['LATITUDE'], dtype=np.float32)
    #         ctdprs = np.array(df['CTDPRS'], dtype=np.float32)
    #         df3 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, 'DELC14':d14c})
    #
    #         plt.title(f'{pltname}')
    #         plt.xlabel('Latitude')
    #         plt.ylabel('Depth (CTD Pressure)')
    #         df3 = df3.loc[df3['DELC14'] > -998]
    #         plt.scatter(df3['LATITUDE'], df3['CTDPRS'], c=df3['DELC14'], cmap='magma')
    #         plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))
    #         x = 1
    #
    #     if 'TCARBN' in cols:
    #         xtr_subsplot = fig.add_subplot(gs[15:19, 10:19])
    #         pltname = 'TCARBN'
    #         tcarbn = np.array(df['TCARBN'], dtype=np.float32)
    #         lat = np.array(df['LATITUDE'], dtype=np.float32)
    #         ctdprs = np.array(df['CTDPRS'], dtype=np.float32)
    #         df4 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, 'TCARBN':tcarbn})
    #
    #         plt.title(f'{pltname}')
    #         plt.xlabel('Latitude')
    #         plt.ylabel('Depth (CTD Pressure)')
    #         df4 = df4.loc[df4['TCARBN'] > -998]
    #         plt.scatter(df4['LATITUDE'], df4['CTDPRS'], c=df4['TCARBN'], cmap='magma')
    #         plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))
    #
    #     print(cols)
    #     try:
    #         if 'CTDSAL' and 'CTDTMP' and 'CTDPRS' in cols:
    #             print("I have all three")
    #             xtr_subsplot = fig.add_subplot(gs[10:19, 0:9])
    #             pltname = 'TvS'
    #             temp = np.array(df['CTDTMP'], dtype=np.float32)
    #             sal = np.array(df['CTDSAL'], dtype=np.float32)
    #             ctdprs = np.array(df['CTDPRS'], dtype=np.float32)
    #             df5 = pd.DataFrame({"CTDTMP": temp, "CTDPRS": ctdprs, 'SALNTY': sal})
    #
    #             plt.title(f'{pltname}')
    #             plt.ylabel('CTDTMP')
    #             plt.xlabel('SALINITY')
    #             df5 = df5.loc[df5['SALNTY'] > -998]
    #             plt.scatter(df5['CTDTMP'], df5['SALNTY'], c=df5['CTDPRS'], cmap='magma')
    #             plt.colorbar()
    #     except KeyError:
    #         continue
    #
    #     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Hydrography/{expocode}',
    #                 dpi=300, bbox_inches="tight")
    #     plt.close()
    # except ValueError or TypeError:
    #     continue
    #


