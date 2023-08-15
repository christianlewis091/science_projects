"""
August 9, 2023:
Cleaning up the code so future me can read it.

August 8, 2023:
Adding a potential density calculation through which I can assign water masses based on Talley 2008 potential density
thresholds of water masses sent to me by Joellen Russell.

Goal:
We want to align oceanographic D14C measurements with water-masses. The idea came about because I wanted to see
what canonical "ages" certain water masses have in the Southern Ocean, and such a database didn't exist. So here I'm
going to create it.
This file originally existed in SOAR Tree Rings folder but was moved when it was decided that this small work could
be publishable.

Original wmc for water mass characteristics from Emery:
https://curry.eas.gatech.edu/Courses/5225/ency/Chapter11/Ency_Oceans/Water_Types_Masses.pdf
When speaking to Joellen Russel at NIWA, she said I should look for Lynne Talley's inverse modeling paper
where she assigns water masses to T and S values. THIS is the data I should use to assign my water masses. Those publicaitons
are in the folder where the scripts are stored.
"""

# IMPORT MODULES
import gsw
import pandas.errors
from os import listdir
from os.path import isfile, join
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec

#
# # Import water mass characterisitcs
# wmc = pd.read_excel(f'H:\Science\Datasets\Water_Mass_Characteristics.xlsx',sheet_name='Emery' ,skiprows=2, comment='#')
# wmc_Talley = pd.read_excel(f'H:\Science\Datasets\Water_Mass_Characteristics.xlsx',sheet_name='Talley', skiprows=2, comment='#')
#
# #
# # A FUNCTION CREATED TO DEAL WITH SOME ISSUES IN GO-SHIP DATA: REMOVES SEPARATORS FROM A STRING
# def remove_separators(value):
#     if isinstance(value, str):
#         stripped_value = value.strip()
#         try:
#             return int(stripped_value)
#         except ValueError:
#             try:
#                 return float(stripped_value)
#             except ValueError:
#                 return stripped_value
#     else:
#         return value
#
#
# """
# This section takes a bulk download of all the available GO-SHIP data and GLODAP data and merges it into one giant file
# than can be used to run the for-loop to assign water masses.
# """
# results_names = []
# res_2 = []
# filename = []
# originname = []
# onlyfiles = [f for f in listdir(r'H:\Science\Datasets\Hydrographic\Bulk_Download') if isfile(join(r'H:\Science\Datasets\Hydrographic\Bulk_Download', f))]
# goship_len = len(onlyfiles)
#
# database = pd.DataFrame()
# # for i in range(0,2):
# for i in range(0, len(onlyfiles)):
#     try:
#         print(f'loop 1: {i/len(onlyfiles)}')
#         # Read in the data in the file directory. Skip the first uncommented line (skiprows = 2). remove commented lines.
#         data = pd.read_csv(f'H:\Science\Datasets\Hydrographic\Bulk_Download\{onlyfiles[i]}', skiprows=2, comment='#')
#         data['Project Name'] = 'GO-SHIP'
#         data = data.applymap(remove_separators)
#         if 'DELC14' in data.columns:
#             data['Origin'] = f'{onlyfiles[i]}'
#             database = pd.concat([database, data])
#             results_names.append(str(onlyfiles[i]))
#
#     except UnicodeDecodeError:
#         x = 1
#     except pandas.errors.ParserError:
#         x = 1
#
# """
# Now I'm adding on GLODAP data, see scrape_GLODAP.py
# """
# #
# onlyfiles = [f for f in listdir(r'H:\Science\Datasets\Hydrographic\GLODAP_scrape2') if isfile(join(r'H:\Science\Datasets\Hydrographic\GLODAP_scrape2', f))]
# glodap_len = len(onlyfiles)
# for i in range(0, len(onlyfiles)):
#     try:
#         print(f'loop 2: {i/len(onlyfiles)}')
#         # Read in the data in the file directory. Skip the first uncommented line (skiprows = 2). remove commented lines.
#         data = pd.read_csv(f'H:\Science\Datasets\Hydrographic\GLODAP_scrape2\{onlyfiles[i]}', skiprows=2, comment='#')
#         data['Project Name'] = 'GLODAP'
#         data = data.applymap(remove_separators)
#         if 'DELC14' in data.columns:
#             data['Origin'] = f'{onlyfiles[i]}'
#             database = pd.concat([database, data])
#             results_names.append(str(onlyfiles[i]))
#
#     except UnicodeDecodeError:
#         x = 1
#     except pandas.errors.ParserError:
#         x = 1
#
# database = database.dropna(subset='LONGITUDE')
# database = database.dropna(subset='DELC14')
# database = database.loc[database['DELC14'] != '/MILLE']
# # remove missing data
# database = database.loc[database['DELC14'].astype(int) > int(-998)]
# print(database.head(5))
# results = pd.DataFrame({"Filename": results_names})
#
# with pd.ExcelWriter(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx') as writer:
#     database.to_excel(writer, sheet_name='Database')
#     results.to_excel(writer, sheet_name='FileErrors')
#
#
# print(f"{goship_len}: GOSHIP length")
# print(f"{glodap_len}: GLODAP length")


"""
I want to see a map of all the 14C data that's out there, this will be Figure 1. 
"""
# read in the sheet that was written in the above section of the code.
# df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')

# maxlat = 90
# minlat = -90
# max_lon = 180
# min_lon = -180
#
# # res = 'i'  # todo switch to i for intermediate
# size1 = 50
#
# # initialize the figure and subplots.
# fig = plt.figure(1, figsize=(8, 8))
# gs = gridspec.GridSpec(8, 8)
# gs.update(wspace=.75, hspace=1)
#
# import matplotlib.gridspec as gridspec
# # initalize the map
# xtr_subsplot = fig.add_subplot(gs[0:4, 0:8])
# map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=min_lon, urcrnrlon=max_lon)
# map.etopo()
# map.drawcoastlines()
# map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
# map.drawmeridians(np.arange(-180, 180, 40), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
# df1 = df.loc[df['Project Name'] == "GO-SHIP"]
# expos = df1['EXPOCODE'].astype(str)
# names = np.unique(expos)
# print(len(names))
# for i in range(0, len(names)):
#     # grab the first cruise
#     thiscruise = df1.loc[df1['EXPOCODE'] == names[i]]
#
#     # grab its lats and lons
#     lats = thiscruise['LATITUDE']
#     lons = thiscruise['LONGITUDE']
#
#     z, a = map(lons,  lats)
#     map.scatter(z, a, marker='o', s = 3.5, color='crimson', edgecolor='crimson')
#
#
# xtr_subsplot = fig.add_subplot(gs[4:8, 0:8])
# map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=min_lon, urcrnrlon=max_lon)
# map.etopo()
# map.drawcoastlines()
# map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
# map.drawmeridians(np.arange(-180, 180, 40), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
# df2 = df.loc[df['Project Name'] == "GLODAP"]
# expos = df2['EXPOCODE'].astype(str)
# names = np.unique(expos)
# print(len(names))
# for i in range(0, len(names)):
#     # grab the first cruise
#     thiscruise = df2 .loc[df2 ['EXPOCODE'] == names[i]]
#
#     # grab its lats and lons
#     lats = thiscruise['LATITUDE']
#     lons = thiscruise['LONGITUDE']
#
#     z, a = map(lons,  lats)
#     map.scatter(z, a, marker='o', s = 3.5, color='yellow', edgecolor='yellow')
#
#
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output/Map.jpg', dpi=300, bbox_inches="tight")


"""
Add potential density to the data in order to filter based on Talley's tables. 
"""

database = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')

# calculate Absolute salinity and Conservative Temperature from parametesr based on TEOS guidelines...
# https://www.teos-10.org/pubs/gsw/html/gsw_SA_from_SP.html
# https://teos-10.github.io/GSW-Python/conversions.html Calculates Conservative Temperature of seawater from in-situ temperature.
# calculate convservative temperature

roe_array = []
for i in range(0, len(database)):
    row = database.iloc[i]
    # SA = gsw.gsw_SA_from_SP(row['SALNTY'], row['CTDPRS'], row['LONGITUDE'], row['LATITUDE'])
    SA = row['SALNTY']  # TODO use ABSOLUTE Salinity, not measure salinity (shouldn't make any real difference...)
    CT = gsw.conversions.CT_from_t(SA, row['CTDTMP'], row['CTDPRS'])  # https://teos-10.github.io/GSW-Python/conversions.html
    roe = gsw.density.sigma0(SA, CT)
    roe_array.append(np.float(roe))

database['Potential Density'] = roe_array
database.to_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')
# np.savetxt(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.txt', database.values, fmt='%d')

"""
THIS BLOCK ASSIGNS THE WATER MASSES!
"""
#
# # See Full list of column names
# # print(database.columns.tolist())
#
# ocean_array = []
# # Need to assign ocean-sector labels to the data: Pacific, Atlantic, or Indian. Southern not included in WMC, looped into each 3.
# # for i in range(0, len(database)):
# for i in range(0, len(database)):
#     row = database.iloc[i]
#     x = row['LONGITUDE']
#     y = row['LATITUDE']
#
#     if type(x) == str:
#         ocean_array.append('Type Error: Lon = String')
#     elif 30 < float(row['LONGITUDE']) < 150:
#         ocean_array.append('Indian')
#     elif 50 < float(row['LONGITUDE']) < 180:
#         ocean_array.append('Pacific')
#     elif -180 < float(row['LONGITUDE']) < -60:
#         ocean_array.append('Pacific')
#     elif -60 < float(row['LONGITUDE']) < 0:
#         ocean_array.append('Atlantic')
#     elif 0 < float(row['LONGITUDE']) < 30:
#         ocean_array.append('Atlantic')
#     else:
#         ocean_array.append('Outside Boundaries')
#
# database['Ocean_Label'] = ocean_array
# # test = database.loc[database['Ocean_Label'] == 'Type Error: Lon = String']
# # print(len(test))
# # print(len(database))
# # About 10% of all the data got flagged as bad beacuse the lon couldn't be converted to strings. These
# # Usually showed up as just empty cells but weren't dropped by nan. there's likely a spacebar that was hit in these places.
#
# database = database.loc[database['Ocean_Label'] != 'Type Error: Lon = String']
#
#
# # BLOCK FOR ASSIGNING WATER MASSES ACCORDING TO EMERY
# water_masses_emery = []
#
# for i in range(0, len(database)):
#     # grab the first row
#     row = database.iloc[i]
#     print(f"Emery {i}")
#     # set an escape label to avoid double labeling
#     escapeflag = 'N'
#
#     for k in range(0, len(wmc)):
#         # grab the first row of water mass characteristics
#         wmc_row = wmc.iloc[k]
#         name = wmc_row['Name']
#
# # including depth filtering
#         # if wmc_row['Ocean'] == row['Ocean_Label'] and float(wmc_row['CTDPRS MIN']) < float(row['CTDPRS']) < float(wmc_row['CTDPRS MAX']) and float(wmc_row['CTDTMP MIN']) < float(row['CTDTMP']) < float(wmc_row['CTDTMP MAX']) and float(wmc_row['SALNTY MIN']) < float(row['CTDSAL']) < float(wmc_row['SALNTY MAX']):
#         #     water_masses.append(name)
#         #     escapeflag = 'Y'
#         #     break
#  # not including CTDPRS filter
#         if wmc_row['Ocean'] == row['Ocean_Label'] and float(wmc_row['CTDTMP MIN']) <= float(row['CTDTMP']) <= float(wmc_row['CTDTMP MAX']) and float(wmc_row['SALNTY MIN']) <= float(row['CTDSAL']) <= float(wmc_row['SALNTY MAX']):
#             water_masses_emery.append(name)
#             escapeflag = 'Y'
#             break
#
#     if escapeflag == 'N':  # I still haven't found a match
#         water_masses_emery.append('Error: No Water Mass Assigned')
# database['Water Mass Emery'] = water_masses_emery
#
#
#
#
# # BLOCK FOR ASSIGNING WATER MASSES ACCORDING TO TALLEY
# water_masses_talley = []
# # Now I want to assign water masses based on the data in "WMC"
# for i in range(0, len(database)):
#     print(f"Talley {i}")
#     # grab the first row
#     row = database.iloc[i]
#
#     # set an escape label to avoid double labeling
#     escapeflag = 'N'
#
#     # BLOCK FOR ASSIGNING WATER MASSES ACCORDING TO EMERY
#     for k in range(0, len(wmc_Talley)):
#         # grab the first row of water mass characteristics
#         wmc_row = wmc_Talley.iloc[k]
#         name = wmc_row['Name']
#
#         # including depth filtering
#         # if wmc_row['Ocean'] == row['Ocean_Label'] and float(wmc_row['CTDPRS MIN']) < float(row['CTDPRS']) < float(wmc_row['CTDPRS MAX']) and float(wmc_row['CTDTMP MIN']) < float(row['CTDTMP']) < float(wmc_row['CTDTMP MAX']) and float(wmc_row['SALNTY MIN']) < float(row['CTDSAL']) < float(wmc_row['SALNTY MAX']):
#         #     water_masses.append(name)
#         #     escapeflag = 'Y'
#         #     break
#         # not including CTDPRS filter
#         if wmc_row['Ocean'] == row['Ocean_Label'] and float(wmc_row['roe min']) <= float(row['Potential Density']) <= float(wmc_row['roe max']):
#             water_masses_talley.append(name)
#             escapeflag = 'Y'
#             break
#
#     if escapeflag == 'N':  # I still haven't found a match
#         water_masses_talley.append('Error: No Water Mass Assigned')
# database['Water Mass Talley'] = water_masses_talley
#
#
# database2 = database[['Origin','EXPOCODE','SECT_ID','STNNBR','CASTNO','SAMPNO','BTLNBR',
# 'BTLNBR_FLAG_W',
# 'DATE',
# 'TIME',
# 'LATITUDE',
# 'LONGITUDE',
# 'DEPTH',
# 'CTDPRS',
# 'CTDTMP',
# 'CTDSAL',
# 'CTDSAL_FLAG_W',
# 'SALNTY',
# 'SALNTY_FLAG_W',
# 'OXYGEN',
# 'OXYGEN_FLAG_W',
# 'SILCAT',
# 'SILCAT_FLAG_W',
# 'NITRAT',
# 'NITRAT_FLAG_W',
# 'NITRIT',
# 'NITRIT_FLAG_W',
# 'PHSPHT',
# 'PHSPHT_FLAG_W',
# 'TCARBN',
# 'TCARBN_FLAG_W',
# 'FCO2',
# 'FCO2_FLAG_W',
# 'FCO2TMP',
# 'DELC14',
# 'DELC14_FLAG_W',
# 'C14ERR',
# 'DELC13',
# 'DELC13_FLAG_W','Ocean_Label','Water Mass Emery','Water Mass Talley']]
#
#
# with pd.ExcelWriter(r'H:\Science\Datasets\Hydrographic\water_masses_assigned.xlsx') as writer:
#     database.to_excel(writer, sheet_name='Database_FULL')
#     database2.to_excel(writer, sheet_name='Database_D14Cfocus')

#


#


# """
# UNCOMMENT ABOVE IF YOU NEED TO EDIT OR REBUILD THE DATABASE. CONTINUE DOWN IF YOU WANT PLOTS
# """
#
#
# df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/water_mass_database_full.csv')
# df = df.loc[df['DELC14'] > -999]
# df = df.loc[df['SALNTY'] > -999]
# df = df.loc[df['Water Mass'] != 'Error: No Water Mass Assigned']
# df.to_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/water_mass_database_cleaned.csv')
#
# df = df.dropna(subset='DELC14')
#
# pacific = df.loc[df['Ocean_Label'] == 'Pacific']
# names = np.unique(pacific['Water Mass'])
#
# for i in range(0, len(names)):
#     this_wm = pacific.loc[pacific['Water Mass'] == names[i]]
#
#     fig = plt.figure(figsize=(12,6))
#     gs = gridspec.GridSpec(2, 4)
#     gs.update(wspace=.6, hspace=.6)
#     xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
#
#     plt.scatter(this_wm['LATITUDE'], this_wm['CTDPRS'], c=this_wm['DELC14'], cmap='magma')
#     plt.ylim(4000, 0)
#     plt.xlim(-70, 70)
#     plt.title(f"Pacific -  {str(names[i])}")
#     plt.ylabel('Depth (CTD Pressure)')
#     plt.xlabel('Latitude')
#
#     xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
#     plt.scatter(this_wm['SALNTY'], this_wm['CTDTMP'], c=this_wm['DELC14'], cmap='magma')
#     plt.colorbar().set_label('\u0394$^1$$^4$CO$_2$ (\u2030)', rotation=270)
#     plt.title(f"Pacific -  {str(names[i])}")
#     plt.ylabel('CTD Temperature')
#     plt.xlabel('Salinity (PSU)')
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Hydrography/WaterMasses/Pacific_Ocean_{names[i]}.png')
#     plt.close()
#
#
# pacific = df.loc[df['Ocean_Label'] == 'Indian']
# names = np.unique(pacific['Water Mass'])
#
# for i in range(0, len(names)):
#     this_wm = pacific.loc[pacific['Water Mass'] == names[i]]
#
#     fig = plt.figure(figsize=(12,6))
#     gs = gridspec.GridSpec(2, 4)
#     gs.update(wspace=.6, hspace=.6)
#     xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
#
#     plt.scatter(this_wm['LATITUDE'], this_wm['CTDPRS'], c=this_wm['DELC14'], cmap='magma')
#     plt.ylim(4000, 0)
#     plt.xlim(-70, 70)
#     plt.title(f"Indian -  {str(names[i])}")
#     plt.ylabel('Depth (CTD Pressure)')
#     plt.xlabel('Latitude')
#
#     xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
#     plt.scatter(this_wm['SALNTY'], this_wm['CTDTMP'], c=this_wm['DELC14'], cmap='magma')
#     plt.colorbar().set_label('\u0394$^1$$^4$CO$_2$ (\u2030)', rotation=270)
#     plt.title(f"Indian -  {str(names[i])}")
#     plt.ylabel('CTD Temperature')
#     plt.xlabel('Salinity (PSU)')
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Hydrography/WaterMasses/Indian_Ocean_{names[i]}.png')
#     plt.close()
#
#
# pacific = df.loc[df['Ocean_Label'] == 'Atlantic']
# names = np.unique(pacific['Water Mass'])
#
# for i in range(0, len(names)):
#     this_wm = pacific.loc[pacific['Water Mass'] == names[i]]
#
#     fig = plt.figure(figsize=(12,6))
#     gs = gridspec.GridSpec(2, 4)
#     gs.update(wspace=.6, hspace=.6)
#     xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
#
#     plt.scatter(this_wm['LATITUDE'], this_wm['CTDPRS'], c=this_wm['DELC14'], cmap='magma')
#     plt.ylim(4000, 0)
#     plt.xlim(-70, 70)
#     plt.title(f"Atlantic -  {str(names[i])}")
#     plt.ylabel('Depth (CTD Pressure)')
#     plt.xlabel('Latitude')
#
#     xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
#     plt.scatter(this_wm['SALNTY'], this_wm['CTDTMP'], c=this_wm['DELC14'], cmap='magma')
#     plt.colorbar().set_label('\u0394$^1$$^4$CO$_2$ (\u2030)', rotation=270)
#     plt.title(f"Atlantic -  {str(names[i])}")
#     plt.ylabel('CTD Temperature')
#     plt.xlabel('Salinity (PSU)')
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Hydrography/WaterMasses/Atlantic_Ocean_{names[i]}.png')
#     plt.close()
#

