"""
This is useless.
See C:\Users\clewis\IdeaProjects\GNS\Water_mass_dataset\scripts_OPEN_ACCESS; glodap file created by GLODAP people!
"""



# """
# https://cchdo.ucsd.edu/cruise/33RR20160208
# See above link for the data
#
# THIS FILE CREATES THE DATAFRAME FROM WHICH WE CAN MAKE THE PLOTS -> SEE GO_SHIP_DATA.PY
# """
#
# from mpl_toolkits.basemap import Basemap
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# import os
# import csv
# import pandas.errors
# import seawater
#
#
# """
# These two lines identify and make a list of all the filenames in the specific directory of the computer,
# and then the cpmouter runs through the list and concatenates all the files into one.
# The issue I keep running into is that the data are in strange data types, I want them all to be in the form of FLOAT
# except for the SECT_ID and EXPOCODE because those have a random amount of letters and numbers
#
# I've removed a few of the cruises due to bugs that would take too long to fix (random missing data or empty s
#
# """
# all_files = os.listdir(r"H:\Science\Datasets\Hydrographic\BatchSOCeDownload")
# csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
#
# # create an inital dataframe to append things onto
# df_all = pd.DataFrame()
# len1 = len(csv_files)
# index_flag = []
# for i in range(0, len1):
#     name = csv_files[i]
#     print(name)
#     # skipping the first row avoids dealing with the "BOTTLE" row.
#     # comment as # gets rid of the commented rows
#     df = pd.read_csv(f"H:/Science/Datasets/Hydrographic/BatchSOCeDownload/{name}", comment='#', skiprows=1).dropna(subset='DATE').reset_index(drop=True)
#     desired_cols_14C = ['DATE','LATITUDE','LONGITUDE','CTDPRS','OXYGEN','NITRAT', 'DELC14','CTDTMP','SALNTY']
#
#     # define a function to find the overlap between the columns we want, and the columns we have
#     def intersection(lst1, lst2):
#         lst3 = [value for value in lst1 if value in lst2]
#         return lst3
#
#     # use that function above to create a list of the overlapping columns
#     result = intersection(desired_cols_14C, df.columns)
#     df = df[result]
#     print(df.columns)
#
#     # add a flag that I can index on later
#
#
#     try:
#     # change the whole dataframe to the type FLOAT
#         df = df.astype(float)
#
#         # get rid of all the empty cells
#         cols = df.columns
#         for item in cols:
#             df = df.dropna(subset=item).reset_index(drop=True)
#
#
#         df['Cat4Index'] = int(i)
#
#
#         df_all = pd.concat([df_all, df])
#         index_flag.append(i)
#
#         print(len(df_all))
#
#
#
#
#     except ValueError:
#         print('Likely: ValueError: could not convert string to float: '' ')
#
#
#
# df_all.to_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/test_all.csv')
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
# #
# #
# #
# # df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hydrography_30_90S_files1_83.csv')
# # """
# # Clean up the data for the general hydrographic parameters plots (df2) and the delC14 plots (df3)
# # """
# # # clean up the data a bit
# # df2 = df[['SECT_ID','DATE','LATITUDE','LONGITUDE','CTDPRS','CTDSAL','OXYGEN','NITRAT','TCARBN','Cat4Index']]
# # df2_cc = []
# # for item in ['SECT_ID','DATE','LATITUDE','LONGITUDE','CTDPRS','CTDSAL','OXYGEN','NITRAT','TCARBN','Cat4Index']:
# #     df2 = df2.dropna(subset=item).reset_index(drop=True)
# #
# # df3 = df[['SECT_ID','DATE','LATITUDE','LONGITUDE','CTDPRS','CTDSAL','OXYGEN','NITRAT','TCARBN','Cat4Index','DELC14']]
# # for item in ['SECT_ID','DATE','LATITUDE','LONGITUDE','CTDPRS','CTDSAL','OXYGEN','NITRAT','TCARBN','Cat4Index','DELC14']:
# #     df3 = df3.dropna(subset=item).reset_index(drop=True)
# #
# # range_df2 = np.unique(df2['Cat4Index'])
# # range_df3 = np.unique(df3['Cat4Index'])
# #
# # # I'll have to iterate througb every row and change everything to a float..., then add the sec ID back on at the end
# #
# # df2 = df2.drop(columns='SECT_ID')
# # df3 = df3.drop(columns='SECT_ID')
# # newdf2 = pd.DataFrame()
# # for i in range(0, len(df2)):
# #     row = df2.iloc[i]
# #     row = row.astype('float64')
# #     newdf2 = pd.concat([newdf2, row])
# #
# # df2_index = ['DATE','LATITUDE','LONGITUDE','CTDPRS','CTDSAL','OXYGEN','NITRAT','TCARBN','Cat4Index','DELC14']
# # df2 = pd.DataFrame(data=newdf2, index=df2_index)
# # df2 = pd.to_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/df2.csv')
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
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
# #
# #
# # # only 87 cruises are left after we filter out all those with missing data.
# # # 44 cruises exist with the DELC14 data.
# # for i in range_df2:
# #     print(i)
# #     current_cruise = df2.loc[df2['Cat4Index'] == i].reset_index(drop=True)
# #     print(current_cruise['LATITUDE'])
# #     try:
# #         minlat = min((current_cruise['LATITUDE']))
# #         minlon = min((current_cruise['LONGITUDE']))
# #         maxlat = max((current_cruise['LATITUDE']))
# #         maxlon = max((current_cruise['LONGITUDE']))
# #
# #         # make a map of the cruise and data using gridspec:
# #         fig = plt.figure(figsize=(15, 12))
# #         gs = gridspec.GridSpec(20, 20)
# #         gs.update(wspace=.5, hspace=.5)
# #         xtr_subsplot = fig.add_subplot(gs[0:9, 0:9])
# #         try:
# #             dlat = 20  # adds a buffer to see around the map
# #             map = Basemap(llcrnrlat=minlat-dlat, urcrnrlat=maxlat+dlat, llcrnrlon=minlon-dlat, urcrnrlon=maxlon+dlat, resolution='i')
# #         except ValueError:
# #             dlat = 0  # adds a buffer to see around the map
# #             map = Basemap(llcrnrlat=minlat-dlat, urcrnrlat=maxlat+dlat, llcrnrlon=minlon-dlat, urcrnrlon=maxlon+dlat, resolution='i')
# #
# #         map.drawcoastlines(linewidth=0.5)
# #         map.drawmapboundary(fill_color='paleturquoise', linewidth=0.5)
# #         map.fillcontinents(color='coral', lake_color='aqua')
# #         map.drawcountries()
# #         map.drawparallels(np.arange(-90, 90, 20), labels=[False, False, False, False], fontsize=7, linewidth=0.5)
# #         map.drawmeridians(np.arange(-180, 180, 20), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
# #         x, y = map(current_cruise['LATITUDE'], (current_cruise['LONGITUDE']))
# #         map.scatter(y, x, marker='D',color='black', s= 10)
# #         plt.title(str(i))
# #
# #         # # DO plot
# #         # xtr_subsplot = fig.add_subplot(gs[0:4, 10:19])
# #         # pltname = 'Dissolved Oxygen (UMOL/KG)'
# #         # # oxy = np.array(current_cruise['OXYGEN'], dtype=np.float32)
# #         # # lat = np.array(current_cruise['LATITUDE'], dtype=np.float32)
# #         # # ctdprs = np.array(current_cruise['CTDPRS'], dtype=np.float32)
# #         # # df1 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, "OXYGEN":oxy})
# #         #
# #         # plt.title(f'{pltname}')
# #         # plt.xlabel('Latitude')
# #         # plt.ylabel('Depth (CTD Pressure)')
# #         # x = np.array(current_cruise['LATITUDE'])
# #         # y = np.array(current_cruise['CTDPRS'])
# #         # current_cruise = current_cruise.loc[current_cruise['OXYGEN'] > -998]
# #         # z = np.array(current_cruise['OXYGEN'])
# #         # plt.scatter(x, y, c=z, cmap='magma')
# #         # plt.colorbar()
# #
# #         # Nitrate plot
# #         xtr_subsplot = fig.add_subplot(gs[5:9, 10:19])
# #         pltname = 'NITRATE (UMOL/KG)'
# #         nitrate = np.array(current_cruise['NITRAT'], dtype=np.float32)
# #         lat = np.array(current_cruise['LATITUDE'], dtype=np.float32)
# #         ctdprs = np.array(current_cruise['CTDPRS'], dtype=np.float32)
# #         df2 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, 'NITRAT':nitrate})
# #
# #         plt.title(f'{pltname}')
# #         plt.xlabel('Latitude')
# #         plt.ylabel('Depth (CTD Pressure)')
# #         df2 = df2.loc[df2['NITRAT'] > -998]
# #         plt.scatter([1,2,3], [2,3,4], c=[8,9,10], cmap='magma')
# #         plt.colorbar(), plt.ylim(max(df2['CTDPRS']), min(df2['CTDPRS']))
# #
# #         # # DIC
# #         # xtr_subsplot = fig.add_subplot(gs[15:19, 10:19])
# #         # pltname = 'TCARBN'
# #         # tcarbn = np.array(df['TCARBN'], dtype=np.float32)
# #         # lat = np.array(df['LATITUDE'], dtype=np.float32)
# #         # ctdprs = np.array(df['CTDPRS'], dtype=np.float32)
# #         # df4 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, 'TCARBN':tcarbn})
# #         #
# #         # plt.title(f'{pltname}')
# #         # plt.xlabel('Latitude')
# #         # plt.ylabel('Depth (CTD Pressure)')
# #         # df4 = df4.loc[df4['TCARBN'] > -998]
# #         # plt.scatter(df4['LATITUDE'], df4['CTDPRS'], c=df4['TCARBN'], cmap='magma')
# #         # plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))
# #
# #         plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Hydrography/{i}',
# #                     dpi=300, bbox_inches="tight")
# #         plt.close()
# #
# #     except TypeError:
# #
# #
# #     # # DO plot
# #     # xtr_subsplot = fig.add_subplot(gs[0:4, 10:19])
# #     # pltname = 'Dissolved Oxygen (UMOL/KG)'
# #     # oxy = np.array(current_cruise['OXYGEN'], dtype=np.float32)
# #     # lat = np.array(current_cruise['LATITUDE'], dtype=np.float32)
# #     # ctdprs = np.array(current_cruise['CTDPRS'], dtype=np.float32)
# #     # df1 = pd.DataFrame({"LATITUDE": lat, "CTDPRS": ctdprs, "OXYGEN":oxy})
# #     #
# #     # plt.title(f'{pltname}')
# #     # plt.xlabel('Latitude')
# #     # plt.ylabel('Depth (CTD Pressure)')
# #     # df1 = df1.loc[df1['OXYGEN'] > -998]
# #     # plt.scatter(df1['LATITUDE'], df1['CTDPRS'], c=df1['OXYGEN'], cmap='magma')
# #     # plt.colorbar(), plt.ylim(max(df1['CTDPRS']), min(df1['CTDPRS']))
# #     #
# #         plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Hydrography/{i}',
# #                     dpi=300, bbox_inches="tight")
# #         plt.close()
# #
#
#
#
#
#
#
#
#
