"""
August 21, 2024
Jack sent me some cnv files of cruise data from DBT. Lets see if I can get it into a readable file...

"""

"""
First step is to convert the .cnv files with the data to python readable files
"""
import matplotlib.pyplot as plt
import os
import glob
import shutil
import csv
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
"""
STEP1. Change to txt
"""

input_directory = r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\CTD_CNVFiles'
out_directory = r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP1'
#
# def copy_and_rename_files(source_directory, destination_directory):
#     # Change the current working directory to the source directory
#     os.chdir(source_directory)
#
#     # Find all files with the .asc extension in the source directory
#     for file in glob.glob("*.cnv"):
#         # Change the file extension from .asc to .csv
#         new_name = os.path.splitext(file)[0] + ".txt"
#         # Construct the full path for the destination file
#         destination_path = os.path.join(destination_directory, new_name)
#         # Copy the file with the new extension to the destination directory
#         shutil.copy(file, destination_path)
#         print(f"Copied {file} to {destination_path}")
#
# # Call the function to rename the files
# copy_and_rename_files(input_directory, out_directory)

"""
STEP2. Dealwith Preamble
"""

# # read in the data that was created above, this line finds the directory
# files = os.listdir(r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP1')
#
# # make a list with all the file names
# file_list = np.unique(files)
#
# # create a dummy dataframe to store the data later
# final_dataframe = pd.DataFrame()
#
# # loop through each of the CTD files that we're going to alter in format
# for i in range(0, len(file_list)):
#
#     # open the file
#     with open(f'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP1/{file_list[i]}', 'r') as fp:
#
#         """
#         This whole subsection below is to find where the preable ENDS and the data begins
#         """
#
#         # set columns for later
#         column_name = ['DepSM', 'bpos', 'T090C', 'Sal00', 'Sbeox0Mg/L', 'sbeox0PS','fls','prdM','flag']
#
#         # attach these set columns to the dummy dataframe
#         dataframe1 = pd.DataFrame(columns=column_name)
#
#         # read all lines using readline()
#         lines = fp.readlines()
#
#         """
#         This for loop reads in each ROW of the file that we're currently looking at. If it finds that its NOT
#         the pre-amble, it will strip the whitespace from the data and attach it to a dataframe.
#         """
#         for row in lines:
#             # check if these characters exist in the data
#             word = '#'
#             word2 = '*'
#             #print(row.find(word))
#             # find() method returns -1 if the value is not found
#             # if found it returns index of the first occurrence of the substring
#             if row.find(word) != -1:  # we found the character
#                 x = 1
#             elif row.find(word2) != -1:  # we found the character
#                 x = 1
#             elif row == '\n':
#                 x = 1
#             else:
#                 data = [row.strip().split()]
#                 data = pd.DataFrame(data, columns=column_name)
#                 dataframe1 = pd.concat([dataframe1, data]).reset_index(drop=True)
#
#         filename = file_list[i].replace(".txt", "")
#         dataframe1['FileName'] = filename
#
#         # these casts seem to incude the downcast AND the upcast.
#         # I want to only include the downcast.
#
#         dataframe1.to_excel(f'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP2/{filename}.xlsx')


"""
Now we'll run the concat STEP3
"""

# files = os.listdir(r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP2/')
#
# # make a list with all the file names
# file_list = np.unique(files)
#
# # create a dummy dataframe to store the data later
# concat_df = pd.DataFrame()
#
# for i in range(0, len(file_list)):
#     sub_df = pd.read_excel(f'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP2/{file_list[i]}')
#     concat_df = pd.concat([concat_df, sub_df]).reset_index(drop=True)
#
# concat_df.to_excel(f'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP3/Concatonated_Data.xlsx')
#


"""
Check the CTD data I was given matches where we were
"""
# # first a rough check I was sent the propoer profiles. Do they aligm on the maP?
# mets = pd.read_excel(r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\metadata.xlsx')
# mets = mets.dropna(subset='My Station Name')
# df = pd.read_excel('C:/2024_Polaris_II/Sampling_Log.xlsx')
# stns = np.unique(df['My Station Name'])
#
# plt.figure(figsize=(10, 8))
# maxlat = -45.0
# minlat = -46
# nz_max_lon = 167.25
# nz_min_lon = 166.25
# map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h')
# map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.1)
# map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.1)
# map.fillcontinents(color="mediumaquamarine", lake_color='#DDEEFF')
# map.drawmapboundary(fill_color="#DDEEFF")
# map.drawcoastlines()
# size2 = 50
#
# plt.text(167.1, -45.5, 'Doubtful S.', fontsize=12)
# plt.text(167, -45.75, 'Dusky S.', fontsize=12)
#
# lat = df['Latitude_N_decimal']
# lon = df['Longitude_E_decimal']
# x, y = map(lon, lat)
# map.scatter(x, y, color='red', edgecolor='black', label='CBL Sheet lat lons', s=size2, marker='^', zorder=2, alpha=0.5)
#
# lat = mets['Lat']
# lon = mets['Lon']
# x, y = map(lon, lat)
# map.scatter(x, y, color='blue', edgecolor='black', label='Otago Lat lons', s=60, marker='o')
# plt.legend()
#
# plt.savefig('H:\Science\Datasets\Fiordland\SFCS2405_CTD/Spothceck.png',
#             dpi=300, bbox_inches="tight")


"""
Add lat lons
"""
# mets = pd.read_excel(r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\metadata.xlsx')
# df = pd.read_excel(f'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP3/Concatonated_Data.xlsx')
#
# df = df.merge(mets, on='FileName')
# df.to_excel(r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4\merge_all.xlsx')
#
# df = df.dropna(subset='My Station Name')
# df.to_excel(r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4\mystations.xlsx')
#
#
# """
# Edit the file to read only one transect each so its easier to deal with in ODV
# """
#
# df = pd.read_excel(r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4\merge_all.xlsx')
# names = np.unique(df['FileName'])
#
# dbt_stn =['DBT001_01CTD','DBT002_01CTD', 'DBT003_01CTD','DBT004_01CTD', 'DBT006_01CTD', 'DBT007_01CTD', 'DBT008_01CTD' , 'DBT031_01CTD']
# dus_stn =['DUS019_01CTD','DUS020_01CTD','DUS022_01CTD', 'DUS023_01CTD', 'DUS056_01CTD','DBT011_02CTD', 'DBT012_01CTD','DBT017_01CTD', 'DBT010_02CTD']
# dbt = df.loc[df['FileName'].isin(dbt_stn)]
# dus = df.loc[df['FileName'].isin(dus_stn)]
#
# dbt = dbt[['DepSM', 'bpos', 'T090C', 'Sal00', 'Sbeox0Mg/L', 'sbeox0PS', 'FileName', 'Lat', 'Lon']]
# dus = dus[['DepSM', 'bpos', 'T090C', 'Sal00', 'Sbeox0Mg/L', 'sbeox0PS', 'FileName', 'Lat', 'Lon']]
#
# dbt.to_excel(r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4\edited_files_for_ODV\DBT.xlsx')
# dus.to_excel(r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4\edited_files_for_ODV\dus.xlsx')

# # check on a map that they're right
# plt.figure(figsize=(10, 8))
# maxlat = -45.0
# minlat = -46
# nz_max_lon = 167.25
# nz_min_lon = 166.25
# map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h')
# map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
# map.drawmapboundary(fill_color="#DDEEFF")
# map.drawcoastlines()
# plt.text(167.1, -45.5, 'Doubtful S.', fontsize=12)
# plt.text(167, -45.75, 'Dusky S.', fontsize=12)
#
# lat_dbt = dbt['Lat']
# lon_dbt = dbt['Lon']
# x_dbt, y_dbt = map(lon_dbt, lat_dbt)
# map.scatter(x_dbt, y_dbt, edgecolor='black', zorder=2, s=50, color='blue', marker='o', label='Existing')
#
# lat_dus = dus['Lat']
# lon_dus = dus['Lon']
# x_dus, y_dus = map(lon_dus, lat_dus)
# map.scatter(x_dus, y_dus, edgecolor='red', zorder=2, s=50, color='red', marker='o', label='Existing')
#
# plt.show()





