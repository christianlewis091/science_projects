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
import pandas as pd
import numpy as np


# Import water mass characterisitcs
wmc = pd.read_csv(f'H:\Science\Datasets\Water_Mass_Characteristics.csv',sheetname='Emery' ,skiprows=2, comment='#')
wmc_Talley = pd.read_csv(f'H:\Science\Datasets\Water_Mass_Characteristics.csv',sheetname='Talley', skiprows=2, comment='#')


# A FUNCTION CREATED TO DEAL WITH SOME ISSUES IN GO-SHIP DATA: REMOVES SEPARATORS FROM A STRING
def remove_separators(value):
    if isinstance(value, str):
        stripped_value = value.strip()
        try:
            return int(stripped_value)
        except ValueError:
            try:
                return float(stripped_value)
            except ValueError:
                return stripped_value
    else:
        return value


"""
This section takes a bulk download of all the available GO-SHIP data and GLODAP data and merges it into one giant file
than can be used to run the for-loop to assign water masses.  
"""
# results_names = []
# res_2 = []
# filename = []
# onlyfiles = [f for f in listdir(r'H:\Science\Datasets\Hydrographic\Bulk_Download') if isfile(join(r'H:\Science\Datasets\Hydrographic\Bulk_Download', f))]
#
#
# database = pd.DataFrame()
# # for i in range(0,2):
# for i in range(0, len(onlyfiles)):
#     try:
#         print(f'loop 1: {i/len(onlyfiles)}')
#         # Read in the data in the file directory. Skip the first uncommented line (skiprows = 2). remove commented lines.
#         data = pd.read_csv(f'H:\Science\Datasets\Hydrographic\Bulk_Download\{onlyfiles[i]}', skiprows=2, comment='#')
#         data = data.applymap(remove_separators)
#         if 'DELC14' in data.columns:
#             data['Origin'] = f'{onlyfiles[i]}'
#             database = pd.concat([database, data])
#             results_names.append(str(onlyfiles[i]))
#
#
#     except UnicodeDecodeError:
#         x = 1
#     except pandas.errors.ParserError:
#         x = 1
#
# # """
# # Now I'm adding on GLODAP data, see scrape_GLODAP.py
# # """
#
# onlyfiles = [f for f in listdir(r'H:\Science\Datasets\Hydrographic\GLODAP_scrape2') if isfile(join(r'H:\Science\Datasets\Hydrographic\GLODAP_scrape2', f))]
#
# for i in range(0, len(onlyfiles)):
#     try:
#         print(f'loop 2: {i/len(onlyfiles)}')
#         # Read in the data in the file directory. Skip the first uncommented line (skiprows = 2). remove commented lines.
#         data = pd.read_csv(f'H:\Science\Datasets\Hydrographic\GLODAP_scrape2\{onlyfiles[i]}', skiprows=2, comment='#')
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
# RERUN ABOVE IF ISSUES WITH GO-SHIP DATA
# database = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')
#



# # calculate Absolute salinity and Conservative Temperature from parametesr based on TEOS guidelines...
# # https://www.teos-10.org/pubs/gsw/html/gsw_SA_from_SP.html
# # https://teos-10.github.io/GSW-Python/conversions.html Calculates Conservative Temperature of seawater from in-situ temperature.
# # calculate convservative temperature
#
# roe_array = []
# for i in range(0, len(database)):
#     row = database.iloc[i]
#     # SA = gsw.gsw_SA_from_SP(row['SALNTY'], row['CTDPRS'], row['LONGITUDE'], row['LATITUDE'])
#     SA = row['SALNTY']  # TODO use ABSOLUTE Salinity, not measure salinity (shouldn't make any real difference...)
#     CT = gsw.conversions.CT_from_t(SA, row['CTDTMP'], row['CTDPRS'])  # https://teos-10.github.io/GSW-Python/conversions.html
#     roe = gsw.density.sigma0(SA, CT)
#     roe_array.append(np.float(roe))
#
# database['Potential Density'] = roe_array
#
# database.to_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')
# #



database = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')


# See Full list of column names
# print(database.columns.tolist())

# I ONLY CARE ABOUT 14C!!!
#
#
ocean_array = []
# Need to assign ocean-sector labels to the data: Pacific, Atlantic, or Indian. Southern not included in WMC, looped into each 3.
# for i in range(0, len(database)):
for i in range(0, len(database)):
    row = database.iloc[i]
    x = row['LONGITUDE']

    if type(x) == str:
        ocean_array.append('Type Error: Lon = String')

    elif 30 < float(row['LONGITUDE']) < 150:
        ocean_array.append('Indian')
    elif 50 < float(row['LONGITUDE']) < 180:
        ocean_array.append('Pacific')
    elif -180 < float(row['LONGITUDE']) < -60:
        ocean_array.append('Pacific')
    elif -60 < float(row['LONGITUDE']) < 0:
        ocean_array.append('Atlantic')
    elif 0 < float(row['LONGITUDE']) < 30:
        ocean_array.append('Atlantic')
    else:
        ocean_array.append('Outside Boundaries')

database['Ocean_Label'] = ocean_array
# test = database.loc[database['Ocean_Label'] == 'Type Error: Lon = String']
# print(len(test))
# print(len(database))
# About 10% of all the data got flagged as bad beacuse the lon couldn't be converted to strings. These
# Usually showed up as just empty cells but weren't dropped by nan. there's likely a spacebar that was hit in these places.

database = database.loc[database['Ocean_Label'] != 'Type Error: Lon = String']


water_masses = []
# Now I want to assign water masses based on the data in "WMC"
for i in range(0, len(database)):
    # grab the first row
    row = database.iloc[i]

    # set an escape label to avoid double labeling
    escapeflag = 'N'

    for k in range(0, len(wmc)):
        # grab the first row of water mass characteristics
        wmc_row = wmc.iloc[k]
        name = wmc_row['Name']

# including depth filtering
        # if wmc_row['Ocean'] == row['Ocean_Label'] and float(wmc_row['CTDPRS MIN']) < float(row['CTDPRS']) < float(wmc_row['CTDPRS MAX']) and float(wmc_row['CTDTMP MIN']) < float(row['CTDTMP']) < float(wmc_row['CTDTMP MAX']) and float(wmc_row['SALNTY MIN']) < float(row['CTDSAL']) < float(wmc_row['SALNTY MAX']):
        #     water_masses.append(name)
        #     escapeflag = 'Y'
        #     break
 # not including CTDPRS filter
        if wmc_row['Ocean'] == row['Ocean_Label'] and float(wmc_row['CTDTMP MIN']) < float(row['CTDTMP']) < float(wmc_row['CTDTMP MAX']) and float(wmc_row['SALNTY MIN']) < float(row['CTDSAL']) < float(wmc_row['SALNTY MAX']):
            water_masses.append(name)
            escapeflag = 'Y'
            break

    if escapeflag == 'N':  # I still haven't found a match
        water_masses.append('Error: No Water Mass Assigned')

database['Water Mass'] = water_masses
database2 = database[['Origin','EXPOCODE','SECT_ID','STNNBR','CASTNO','SAMPNO','BTLNBR',
'BTLNBR_FLAG_W',
'DATE',
'TIME',
'LATITUDE',
'LONGITUDE',
'DEPTH',
'CTDPRS',
'CTDTMP',
'CTDSAL',
'CTDSAL_FLAG_W',
'SALNTY',
'SALNTY_FLAG_W',
'OXYGEN',
'OXYGEN_FLAG_W',
'SILCAT',
'SILCAT_FLAG_W',
'NITRAT',
'NITRAT_FLAG_W',
'NITRIT',
'NITRIT_FLAG_W',
'PHSPHT',
'PHSPHT_FLAG_W',
'TCARBN',
'TCARBN_FLAG_W',
'FCO2',
'FCO2_FLAG_W',
'FCO2TMP',
'DELC14',
'DELC14_FLAG_W',
'C14ERR',
'DELC13',
'DELC13_FLAG_W','Ocean_Label','Water Mass']]


with pd.ExcelWriter(r'H:\Science\Datasets\Hydrographic\water_masses_assigned.xlsx') as writer:
    database.to_excel(writer, sheet_name='Database_FULL')
    database2.to_excel(writer, sheet_name='Database_D14Cfocus')

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

