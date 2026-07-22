"""
February 2, 2025
I want to make a nice map that shows the overlap between my Polaris II trip (SFCS2405) and the samples Helen took
on the RV Sonne S309 to choose which samples I want to prioritize measuring
"""
from xcams.OLD_MISC.chi2 import subset

"""
HIGH RES COASTLINE!
https://ctroupin.github.io/posts/2019-09-02-fine-coast/
"""
# resolutions = {"c": "crude",
#                "l": "low",
#                "i": "intermediate",
#                "h": "high",
#                "f": "full"}
#
from cmcrameri import cm
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import numpy as np
import cartopy.feature as cf
import matplotlib.gridspec as gridspec
#
# # cmap=cm.batlow
# # color_sfcs = cm.batlow(0.2)  # Lighter shade from batlow
# # color_s309 = cm.batlow(0.8)  # Darker shade from batlow
#
# colors = getattr(cm, 'davos')(np.linspace(1, 0, 5))
#
# df = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/01_Fiordland/01_May_2024_Cruise/2024_Polaris_II/Sampling_Log.xlsx', skiprows=1)
# sonne = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/S309_RV_Sonne_DIC/14C_samples_for_Christian_Lewis_GNS.xlsx', comment='#')
#
# sounds = np.unique(sonne['Sound'])
# print(sounds)
#
# fig = plt.figure(figsize=(16, 8))
# gs = gridspec.GridSpec(1, 2)
# gs.update(wspace=.15, hspace=0.1)
#
# ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())
# ax2 = fig.add_subplot(gs[0, 1])
#
# ax1.set_extent((166.3, 168.25, -46.0, -44))
# coast = cf.GSHHSFeature(scale="full")
# ax1.add_feature(coast)
#
# for i in range(0, len(sounds)):
#
#     sonne1 = sonne.loc[sonne['Sound'] == sounds[i]]
#     df1 = df.loc[df['Sound'] == sounds[i]]
#
#     sc = ax1.scatter(df1['Longitude_E_decimal'].values, df1['Latitude_N_decimal'].values, color='blue', transform=ccrs.PlateCarree(), label='SFCS2405', marker='o')
#     sc2 = ax1.scatter(sonne1['Lon'].values, sonne1['Lat_corrected'].values, color='red', transform=ccrs.PlateCarree(), label='S309', marker='D')
#
#     sc = ax2.scatter(df1['Latitude_N_decimal'].values, df1['Depth'].values, color='blue', label='SFCS2405', marker='o')
#     sc2 = ax2.scatter(sonne1['Lat_corrected'].values, sonne1['Water depth (m)'].values, color='red', label='S309', marker='D')
#     ax2.set_ylim(2100,0)
#
# plt.savefig(f'H:/Science/Current_Projects/03_CCE_24_25/S309_RV_Sonne_DIC/SFCS2405_vs_S309SonneLocations.png',
#                 dpi=300, bbox_inches="tight")
#

"""
I'm drawing functions from my SFCS2405_CTD_dataworkup.py to analyze the CTD data
"""

from SFCS2405_CTD_dataworkup import copy_and_rename_files
import os

# input_directory1 = r'H:\Science\Datasets\Fiordland\RVSONNE'
# out_directory1 = r'H:\Science\Datasets\Fiordland\RVSONNE\STEP1'
#
# copy_and_rename_files(input_directory1, out_directory1)


"""
STEP2. Dealwith Preamble
"""

# # read in the data that was created above, this line finds the directory
# files = os.listdir(r'H:\Science\Datasets\Fiordland\RVSONNE\STEP1')
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
#     with open(f'H:\Science\Datasets\Fiordland\RVSONNE\STEP1/{file_list[i]}', 'r') as fp:
#
#         """
#         This whole subsection below is to find where the preable ENDS and the data begins
#         """
#
#         # set columns for later
#         column_name = ['depSM', 'prDM', 'timeJ', 'timeH', 'timeM', 'timeM','nbf','latitude','longitude','t090C','t190C','pottempt090C','potemp190C','COSm','C1sm','sal00','sal11','sigma00','sigma11','sbox0Mm/Kg','sbox1Mm/kg','sbeox0PS','sboeox1PS','f1ECO-AFL','turbWETntu0','par','svCM','sbeox0MLL','altM','flag']
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
#         dataframe1.to_excel(f'H:\Science\Datasets\Fiordland\RVSONNE\STEP2/{filename}.xlsx')

"""
Now we'll run the concat STEP3
"""

# files = os.listdir(r'H:\Science\Datasets\Fiordland\RVSONNE\STEP2/')
#
# # make a list with all the file names
# file_list = np.unique(files)
#
# # create a dummy dataframe to store the data later
# concat_df = pd.DataFrame()
#
# for i in range(0, len(file_list)):
#     sub_df = pd.read_excel(f'H:\Science\Datasets\Fiordland\RVSONNE\STEP2/{file_list[i]}')
#     concat_df = pd.concat([concat_df, sub_df]).reset_index(drop=True)
#
# concat_df.to_excel(f'H:\Science\Datasets\Fiordland\RVSONNE\STEP3/Concatonated_CTD_SONNE.xlsx')

"""
Check they match the right locations on the map
"""

# concat_df = pd.read_excel(f'H:\Science\Datasets\Fiordland\RVSONNE\STEP3/Concatonated_CTD_SONNE.xlsx')
# print(concat_df.columns)
#
# fig = plt.figure(figsize=(16, 8))
# ax = plt.axes(projection=ccrs.PlateCarree())
# ax.set_extent((166.3, 168.25, -46.0, -44))
# coast = cf.GSHHSFeature(scale="l")
# ax.add_feature(coast)
#
# filenames = np.unique(concat_df['FileName'])
#
# for i in range(0, len(filenames)):
#     sub1 = concat_df.loc[concat_df['FileName'] == filenames[i]].reset_index()
#     lat1 = sub1['latitude']
#     lat1 = lat1[0]
#     lon1 = sub1['longitude']
#     lon1 = lon1[0]
#
#     sc = ax.scatter(lon1, lat1, color='black', transform=ccrs.PlateCarree(), label='RVSONNE', marker='o')
#
# plt.show()

"""
LOCATIONS ON MAP LOOK GOOD! 
"""

# ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())
# ax2 = fig.add_subplot(gs[0, 1])
#
# ax1.set_extent((166.3, 168.25, -46.0, -44))
# coast = cf.GSHHSFeature(scale="full")
# ax1.add_feature(coast)
#
# for i in range(0, len(sounds)):
#
#     sonne1 = sonne.loc[sonne['Sound'] == sounds[i]]
#     df1 = df.loc[df['Sound'] == sounds[i]]
#
#     sc = ax1.scatter(df1['Longitude_E_decimal'].values, df1['Latitude_N_decimal'].values, color='blue', transform=ccrs.PlateCarree(), label='SFCS2405', marker='o')
#     sc2 = ax1.scatter(sonne1['Lon'].values, sonne1['Lat_corrected'].values, color='red', transform=ccrs.PlateCarree(), label='S309', marker='D')
#
#     sc = ax2.scatter(df1['Latitude_N_decimal'].values, df1['Depth'].values, color='blue', label='SFCS2405', marker='o')
#     sc2 = ax2.scatter(sonne1['Lat_corrected'].values, sonne1['Water depth (m)'].values, color='red', label='S309', marker='D')
#     ax2.set_ylim(2100,0)
#
# plt.savefig(f'H:/Science/Current_Projects/03_CCE_24_25/S309_RV_Sonne_DIC/SFCS2405_vs_S309SonneLocations.png',
#                 dpi=300, bbox_inches="tight")

"""
I only want to compare specific locations, so from now on I need to be a bit more precise. 
I want to compare SO309-59-18 (Dusky) with my station there, DUS023_01CTD
I want to compare SO309-53-1 (mouth of DBT) with my DBT008_01CTD
I want to compare SO309-46-17 (within DBT) with DBT006_01CTD

# for stations I sampled on SFCS2405, we'll look at H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4/mystations.xlsx
SOnne data lives at (f'H:\Science\Datasets\Fiordland\RVSONNE\STEP3/Concatonated_CTD_SONNE.xlsx')
"""

import pandas as pd
import gsw

sun = pd.read_excel(f'H:\Science\Datasets\Fiordland\RVSONNE\STEP3/Concatonated_CTD_SONNE.xlsx')
moy = pd.read_excel('H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4/mystations.xlsx')

sun['pt'] = gsw.conversions.pt_from_t(sun['sal00'],sun['t090C'], sun['depSM'],0)
moy['pt'] = gsw.conversions.pt_from_t(moy['Sal00'],moy['T090C'], moy['DepSM'],0)

interest1_sun = sun.loc[sun['FileName'] == 'SO309-59-13_by_depth_1_m']
interest2_sun = sun.loc[sun['FileName'] == 'SO309-53-1_by_depth_1_m']
interest3_sun = sun.loc[sun['FileName'] == 'SO309-46-17_by_depth_1_m']

interest1_moy = moy.loc[moy['FileName'] == 'DUS023_01CTD']
interest2_moy = moy.loc[moy['FileName'] == 'DBT008_01CTD']
interest3_moy = moy.loc[moy['FileName'] == 'DBT006_01CTD']

sites_of_interest = [interest1_moy, interest2_moy, interest3_moy]
sites_of_interest2 = [interest1_sun, interest2_sun, interest3_sun]
labels = ['DUS023', 'DBT008', 'DBT006']


import matplotlib.pyplot as plt
import numpy as np

# Create figure and axes
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 6), sharey=False)

# Plot a) Temperature-Salinity diagram
ax1.set_title("a)")
ax1.set_xlabel("Salinity")
ax1.set_ylabel("Potential Temperature [°C]")
# ax1.set_xlim(33.5, 35.5)
# ax1.set_ylim(5, 25)

# Example contour lines (isopycnals placeholder)
# for sigma in np.arange(23, 29, 1):
#     ax1.plot(salinity, 1000 + 0 * salinity - sigma, 'k--', linewidth=0.5)  # Replace with actual isopycnals
ax1.plot(interest1_sun['sal00'], interest1_sun['pt'], label='Your Label', color='red')
ax1.plot(interest1_moy['Sal00'], interest1_moy['pt'], label='Your Label', color='red', alpha=0.5)
ax1.plot(interest2_sun['sal00'], interest2_sun['pt'], label='Your Label', color='blue')
ax1.plot(interest2_moy['Sal00'], interest2_moy['pt'], label='Your Label', color='blue', alpha=0.5)
ax1.plot(interest3_sun['sal00'], interest3_sun['pt'], label='Your Label', color='green')
ax1.plot(interest3_moy['Sal00'], interest3_moy['pt'], label='Your Label', color='green', alpha=0.5)

# Plot b) Oxygen vs Depth
ax2.set_title("b)")
ax2.set_xlabel("Oxygen [μmol/kg]")
ax2.set_ylabel("Depth [m]")
# ax2.set_xlim(0, 300)
ax2.set_ylim(250, 0)
ax2.plot(interest1_sun['sbeox0MLL'], interest1_sun['depSM'], label='Your Label', color='red')
ax2.plot(interest1_moy['Sbeox0Mg/L'], interest1_moy['DepSM'], label='Your Label', color='red', alpha=0.5)
ax2.plot(interest2_sun['sbeox0MLL'], interest2_sun['depSM'], label='Your Label', color='blue')
ax2.plot(interest2_moy['Sbeox0Mg/L'], interest2_moy['DepSM'], label='Your Label', color='blue', alpha=0.5)
ax2.plot(interest3_sun['sbeox0MLL'], interest3_sun['depSM'], label='Your Label', color='green')
ax2.plot(interest3_moy['Sbeox0Mg/L'], interest3_moy['DepSM'], label='Your Label', color='green', alpha=0.5)

plt.tight_layout()
plt.savefig(f'H:\Science\Datasets\Fiordland\RVSONNE/CTD_comparison_.png', dpi=300, bbox_inches="tight")











