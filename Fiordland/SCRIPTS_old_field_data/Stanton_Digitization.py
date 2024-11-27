"""
April 3, 2024
I'm trying to digitize old Fiordland papers to understand their circulation, and see if I can understand some context for
new biogeochemical research.

The following file contains digitizations of data from Stanton 1981, 1984, 1986.

Can I calculate AOU? What else can i tell from this data?
"""

# IMPORT MODULES
from os import listdir
from os.path import isfile, join
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np


# # read in the data
# df = pd.read_excel(f'H:\Science\Datasets\Fiordland\Digitized_Data\Fiordland_Digitization_Database.xlsx')
#
# # fill all empty gaps with -999 for later
# df = df.fillna(-999)
#
# # I want to add a flag. I began digitization with Stanton 1986, which included reproductions of data from the other
# # two papers, whihc I added later. Therefore, I want to FLAG, and REMOVE, anything from Stanton 1986 that is duplicated
# # from a previous work
# df['Flag'] = -999
# df.loc[(df['Year'] != 1983) & (df['Citation'] == 'Stanton 1986'), 'Flag'] = 'Dont use, use data from original paper'
#
# df.to_excel(f'H:\Science\Datasets\Fiordland\Digitized_Data\Fiordland_Digitization_Database2.xlsx')

# read in the data
df = pd.read_excel(f'H:\Science\Datasets\Fiordland\Digitized_Data\Fiordland_Digitization_Database2.xlsx')
df['Lat'] = df['Lat'].astype(float)
df['Lon'] = df['Lon'].astype(float)

# THERE ARE NO LAT LON'S! Have to add them myself...
#MILFORD (STANTON 1986)
df.loc[(df['Station'] == 'S528'), 'Lat'] = -44.56570
df.loc[(df['Station'] == 'S528'), 'Lon'] = 167.77623

df.loc[(df['Station'] == 'S529'), 'Lat'] = -44.57267053441642
df.loc[(df['Station'] == 'S529'), 'Lon'] = 167.80043134716897

df.loc[(df['Station'] == 'S530'), 'Lat'] = -44.606655786258834
df.loc[(df['Station'] == 'S530'), 'Lon'] = 167.8385401709526

df.loc[(df['Station'] == 'S533'), 'Lat'] = -44.63683464416311
df.loc[(df['Station'] == 'S533'), 'Lon'] = 167.894845099786

df.loc[(df['Station'] == 'S532'), 'Lat'] = -44.64110973160041
df.loc[(df['Station'] == 'S532'), 'Lon'] = 167.90308484546892

df.loc[(df['Station'] == 'S531'), 'Lat'] = -44.66272463588251
df.loc[(df['Station'] == 'S531'), 'Lon'] = 167.91492948141155

df.loc[(df['Station'] == 'S538'), 'Lat'] = -44.68030369924159
df.loc[(df['Station'] == 'S538'), 'Lon'] = 167.91801938604266

# GEORGE SOUND
df.loc[(df['Station'] == 'S515'), 'Lat'] = -44.80217708256035
df.loc[(df['Station'] == 'S515'), 'Lon'] = 167.36202848249488

df.loc[(df['Station'] == 'S516'), 'Lat'] = -44.841698532364376
df.loc[(df['Station'] == 'S516'), 'Lon'] = 167.34586134641097

df.loc[(df['Station'] == 'S517'), 'Lat'] = -44.880579195254114
df.loc[(df['Station'] == 'S517'), 'Lon'] = 167.36751376080906

df.loc[(df['Station'] == 'S518'), 'Lat'] = -44.92145578054669
df.loc[(df['Station'] == 'S518'), 'Lon'] = 167.38467932412988

df.loc[(df['Station'] == 'S519'), 'Lat'] = -44.94964827629692
df.loc[(df['Station'] == 'S519'), 'Lon'] = 167.40012884803866

df.loc[(df['Station'] == 'S525'), 'Lat'] = -44.96859751646111
df.loc[(df['Station'] == 'S525'), 'Lon'] = 167.41042853014235

df.loc[(df['Station'] == 'S526'), 'Lat'] = -44.9826839202443
df.loc[(df['Station'] == 'S526'), 'Lon'] = 167.39463568425003

# Doubtful Sound
df.loc[(df['Station'] == 'S503'), 'Lat'] = -45.12232351636135
df.loc[(df['Station'] == 'S503'), 'Lon'] = 166.92187830315575

df.loc[(df['Station'] == 'S504'), 'Lat'] = -45.14766230414688
df.loc[(df['Station'] == 'S504'), 'Lon'] = 166.96905797324186

df.loc[(df['Station'] == 'S505'), 'Lat'] = -45.19387252581384
df.loc[(df['Station'] == 'S505'), 'Lon'] = 166.95983287149974

df.loc[(df['Station'] == 'S506'), 'Lat'] = -45.24312210428567
df.loc[(df['Station'] == 'S506'), 'Lon'] = 166.9875081767261

df.loc[(df['Station'] == 'S507'), 'Lat'] = -45.289938008889905
df.loc[(df['Station'] == 'S507'), 'Lon'] = 167.0278073053891

df.loc[(df['Station'] == 'S508'), 'Lat'] = -45.2854972818323
df.loc[(df['Station'] == 'S508'), 'Lon'] = 167.07587494078228

df.loc[(df['Station'] == 'S512'), 'Lat'] = -45.268072610755816
df.loc[(df['Station'] == 'S512'), 'Lon'] = 167.14821915970742

df.loc[(df['Station'] == 'S510'), 'Lat'] =-45.28378921731642
df.loc[(df['Station'] == 'S510'), 'Lon'] = 167.14433490634232

df.loc[(df['Station'] == 'S511'), 'Lat'] =-45.316916490059526
df.loc[(df['Station'] == 'S511'), 'Lon'] = 167.1797787182989

# Long Sound
df.loc[(df['Station'] == 'S486'), 'Lat'] =-45.93432186211679
df.loc[(df['Station'] == 'S486'), 'Lon'] = 166.91107178393278

df.loc[(df['Station'] == 'S485'), 'Lat'] =-45.9527910064098
df.loc[(df['Station'] == 'S485'), 'Lon'] = 166.8735409323094

df.loc[(df['Station'] == 'S483'), 'Lat'] =-45.98449539726917
df.loc[(df['Station'] == 'S483'), 'Lon'] = 166.80309841080097

df.loc[(df['Station'] == 'S481'), 'Lat'] =-46.03863178620148
df.loc[(df['Station'] == 'S481'), 'Lon'] = 166.77134153635043

df.loc[(df['Station'] == 'S479'), 'Lat'] =-46.06668164522057
df.loc[(df['Station'] == 'S479'), 'Lon'] =166.72919150298887

df.loc[(df['Station'] == 'S471'), 'Lat'] =-46.0366276797024
df.loc[(df['Station'] == 'S471'), 'Lon'] =166.7101373783185

df.loc[(df['Station'] == 'S473'), 'Lat'] =-46.10232446656036
df.loc[(df['Station'] == 'S473'), 'Lon'] = 166.68473187875807

df.loc[(df['Station'] == 'S469'), 'Lat'] = -46.087109000438744
df.loc[(df['Station'] == 'S469'), 'Lon'] =  166.64315924311376

df.loc[(df['Station'] == 'S467'), 'Lat'] = -46.12473960699604
df.loc[(df['Station'] == 'S467'), 'Lon'] =  166.57156192617074

df = df.loc[df['Lat'] != -999] # only keep stations where we have lat lon data from Stanton
# df.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/1980s_Stanton_Digitization/Fiordland_Digitization_Database3.xlsx')
stations = np.unique(df['Station'])
print(stations)
# # read in the data
# df = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/1980s_Stanton_Digitization/Fiordland_Digitization_Database3.xlsx')
# """
# Trying to create a nice figure for my Marsden Fast Start EOI
# """
#
# # Set up the map projection centered around Doubtful Sound
# projection = ccrs.PlateCarree()
# fig, ax = plt.subplots(figsize=(10, 8),subplot_kw={"projection": projection})
#
# # Add features to the map
# ax.add_feature(cfeature.LAND, facecolor="lightgray")
# ax.add_feature(cfeature.OCEAN, facecolor="lightblue")
# ax.add_feature(cfeature.COASTLINE, edgecolor="black")
# ax.add_feature(cfeature.BORDERS, linestyle=':')
# ax.add_feature(cfeature.LAKES, facecolor="lightblue")
# ax.add_feature(cfeature.RIVERS)
#
# # Set map extent around Doubtful Sound
# latitude, longitude = -45.316667, 167.016667
# extent = [longitude - 1, longitude + 1, latitude - 1, latitude + 1]
# ax.set_extent(extent, crs=ccrs.PlateCarree())
#
# # Plot stations
# stations = np.unique(df['Station'])
# print(stations)
# for station in stations:
#     this_stn = df.loc[df['Station'] == station].reset_index(drop=True)  # Filter for the current station
#     lat = this_stn['Lat'].values[0]  # Extract the latitude
#     lon = this_stn['Lon'].values[0]  # Extract the longitude
#     print(f"Station: {station}, Lat: {lat}, Lon: {lon}")  # Debugging output
#     ax.plot(lon, lat, marker="o", color="red", markersize=5, transform=ccrs.PlateCarree())
#
# # Add labels and legend
# ax.set_title("Map Centered Around Doubtful Sound, New Zealand")
#
# # Display the map
# plt.show()
































# # first, lets interpolate the gaps within the data for ease of future use. For example, I cant make T/S plot
# # if the depths arent exact beacuse of my coarse digitization in Automatis
# stations = np.unique(df['Station'])
#
# columns = ['Temperature','Salinity','Density','Oxygen']
# combined = pd.DataFrame()
# for i in range(0, len(stations)):
# #
#     # this next bit of code is going to isolate each batch of data
#     this_stn_df = pd.DataFrame()
#     for j in range(0, len(columns)):
# #
#         this_one = df.loc[(df['Station'] == stations[i]) & (df[f'{columns[j]}'] > -999)].reset_index(drop=True)
#         if this_one.empty:
#             poop = 1
#         else:
#             x = this_one[f'{columns[j]}']
#             y = this_one['Depth']
#
#
#             # quickly set the metadata via a loop
#             metadatas = ['Citation','Figure','Day','Month','Year','Date','Expedition','Lat','Lon','Location_1','Location_2','Flag']
#             mt_array = []
#             for k in range(0, len(metadatas)):
#                 citation = this_one[f'{metadatas[k]}'].reset_index(drop=True)
#                 citation = citation[0]
#                 mt_array.append(citation)
#
#             new_depth = np.arange(0, max(y), 5)  # Generate new depth values at every 5-meter depth
#             interpd = interp1d(y, x, kind='linear', fill_value='extrapolate')
#             interpd_data = interpd(new_depth)  # Interpolate temperature values at every 5-meter depth
#     #
#             # add this new data on as a dataframe
#             interpd_data = pd.DataFrame({"Station": stations[i], "Depth": new_depth, f"{columns[j]}": interpd_data})
#
#             # add this data onto the STATION dataframe
#             this_stn_df = pd.concat([this_stn_df, interpd_data]) # accumulate the interpolated data from this station
#             this_stn_df['Origin'] = 'Interpolated'
#             # add the metadata we got earlier
#             for l in range(0, len(metadatas)):
#                 this_stn_df[f'{metadatas[l]}'] = mt_array[l]
#
#     # # organize the data properly.
#     fixed_interpd = this_stn_df.groupby('Depth').apply(lambda group: group.fillna(method='ffill')).reset_index(drop=True).dropna()
#
#
#     combined = pd.concat([combined, fixed_interpd]).reset_index(drop=True)
#
#
# # concatonate the original data back on
# df_full = pd.concat([combined, df]).reset_index(drop=True)
# df_full['Sill_Depth'] = -999
# df_full.loc[(df_full['Location_1'] == 'Milford Sound'), 'Sill_Depth'] = 64
# df_full.loc[(df_full['Location_1'] == 'George'), 'Sill_Depth'] = 47
# df_full.loc[(df_full['Location_1'] == 'Thompson'), 'Sill_Depth'] = 145
# df_full.loc[(df_full['Location_1'] == 'Doubtful'), 'Sill_Depth'] = 101
# df_full.loc[(df_full['Location_1'] == 'Dusky'), 'Sill_Depth'] = 65
# df_full.loc[(df_full['Location_1'] == 'Preservation Inlet'), 'Sill_Depth'] = 30
#
# df_full.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/1980s_Stanton_Digitization/InterpolatedData.xlsx')


# """
# 4 plots horizontal
# """
# fig = plt.figure(figsize=(16, 8))
# gs = gridspec.GridSpec(1, 3)
# gs.update(wspace=0.1, hspace=0.35)
#
# stations = np.unique(df_full['Station'])
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# for i in range(0, len(stations)):
#     stn1 = df_full.loc[(df_full['Station'] == stations[i]) & (df_full['Temperature'] > -999)]
#     digitized = stn1.loc[df_full['Origin'] == 'Digitized']
#     interpolated = stn1.loc[df_full['Origin'] == 'Interpolated']
#     location = np.unique(stn1['Location_2'])
#
#     plt.scatter(digitized['Temperature'], digitized['Depth'], label=f'{stations[i]}_{location}')
#     plt.plot(interpolated['Temperature'], interpolated['Depth'])
# plt.ylim(400,0)
# plt.xlim(5,16)
# plt.xlabel('Temperature (C)')
# plt.ylabel('Depth (m)')
# # plt.legend()
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# for i in range(0, len(stations)):
#     stn1 = df_full.loc[(df_full['Station'] == stations[i]) & (df_full['Salinity'] > -999)]
#     digitized = stn1.loc[df_full['Origin'] == 'Digitized']
#     interpolated = stn1.loc[df_full['Origin'] == 'Interpolated']
#     location = np.unique(stn1['Location_2'])
#
#     plt.scatter(digitized['Salinity'], digitized['Depth'], label=f'{stations[i]}_{location}')
#     plt.plot(interpolated['Salinity'], interpolated['Depth'])
# plt.ylim(400,0)
# plt.xlim(0, 40)
# plt.yticks([])
# plt.xlabel('Salinity')
# # plt.legend()
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])
# for i in range(0, len(stations)):
#     stn1 = df_full.loc[(df_full['Station'] == stations[i]) & (df_full['Oxygen'] > -999)]
#     digitized = stn1.loc[df_full['Origin'] == 'Digitized']
#     interpolated = stn1.loc[df_full['Origin'] == 'Interpolated']
#     location = np.unique(stn1['Location_2'])
#
#     plt.scatter(digitized['Oxygen'], digitized['Depth'], label=f'{stations[i]}_{location}')
#     plt.plot(interpolated['Oxygen'], interpolated['Depth'])
# plt.ylim(400,0)
# plt.xlim(0, 10)
# plt.yticks([])
# plt.xlabel('Oxygen')
# # plt.legend()
#
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/1980s_Stanton_Digitization/blueskyview_nolegend.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
#
#
#
#
# for i in range(0, len(stations)):
#     stn1 = df_full.loc[(df_full['Station'] == stations[i]) & (df_full['Oxygen'] > -999)]
#     digitized = stn1.loc[df_full['Origin'] == 'Digitized']
#     interpolated = stn1.loc[df_full['Origin'] == 'Interpolated']
#     location = np.unique(stn1['Location_2'])
#
#     plt.scatter(digitized['Oxygen'], digitized['Depth'], label=f'{stations[i]}_{location}')
#     plt.plot(interpolated['Oxygen'], interpolated['Depth'])
# plt.ylim(400,0)
# plt.xlim(0, 10)
# plt.yticks([])
# plt.xlabel('Oxygen')
# # plt.legend()
#
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/1980s_Stanton_Digitization/blueskyview_nolegend.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
