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
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

# read in the data
df = pd.read_excel(f'H:\Science\Datasets\Fiordland\Digitized_Data\Fiordland_Digitization_Database.xlsx')

# fill all empty gaps with -999 for later
df = df.fillna(-999)

# I want to add a flag. I began digitization with Stanton 1986, which included reproductions of data from the other
# two papers, whihc I added later. Therefore, I want to FLAG, and REMOVE, anything from Stanton 1986 that is duplicated
# from a previous work
df['Flag'] = -999
df.loc[(df['Year'] != 1983) & (df['Citation'] == 'Stanton 1986'), 'Flag'] = 'Dont use, use data from original paper'

df.to_excel(f'H:\Science\Datasets\Fiordland\Digitized_Data\Fiordland_Digitization_Database2.xlsx')

# read in the data
df = pd.read_excel(f'H:\Science\Datasets\Fiordland\Digitized_Data\Fiordland_Digitization_Database2.xlsx')

# first, lets interpolate the gaps within the data for ease of future use. For example, I cant make T/S plot
# if the depths arent exact beacuse of my coarse digitization in Automatis
stations = np.unique(df['Station'])

columns = ['Temperature','Salinity','Density','Oxygen']
combined = pd.DataFrame()
for i in range(0, len(stations)):
#
    # this next bit of code is going to isolate each batch of data
    this_stn_df = pd.DataFrame()
    for j in range(0, len(columns)):
#
        this_one = df.loc[(df['Station'] == stations[i]) & (df[f'{columns[j]}'] > -999)].reset_index(drop=True)
        if this_one.empty:
            poop = 1
        else:
            x = this_one[f'{columns[j]}']
            y = this_one['Depth']


            # quickly set the metadata via a loop
            metadatas = ['Citation','Figure','Day','Month','Year','Date','Expedition','Lat','Lon','Location_1','Location_2','Flag']
            mt_array = []
            for k in range(0, len(metadatas)):
                citation = this_one[f'{metadatas[k]}'].reset_index(drop=True)
                citation = citation[0]
                mt_array.append(citation)

            new_depth = np.arange(0, max(y), 5)  # Generate new depth values at every 5-meter depth
            interpd = interp1d(y, x, kind='linear', fill_value='extrapolate')
            interpd_data = interpd(new_depth)  # Interpolate temperature values at every 5-meter depth
    #
            # add this new data on as a dataframe
            interpd_data = pd.DataFrame({"Station": stations[i], "Depth": new_depth, f"{columns[j]}": interpd_data})

            # add this data onto the STATION dataframe
            this_stn_df = pd.concat([this_stn_df, interpd_data]) # accumulate the interpolated data from this station
            this_stn_df['Origin'] = 'Interpolated'
            # add the metadata we got earlier
            for l in range(0, len(metadatas)):
                this_stn_df[f'{metadatas[l]}'] = mt_array[l]

    # # organize the data properly.
    fixed_interpd = this_stn_df.groupby('Depth').apply(lambda group: group.fillna(method='ffill')).reset_index(drop=True).dropna()


    combined = pd.concat([combined, fixed_interpd]).reset_index(drop=True)


# concatonate the original data back on
df_full = pd.concat([combined, df]).reset_index(drop=True)
df_full['Sill_Depth'] = -999
df_full.loc[(df_full['Location_1'] == 'Milford Sound'), 'Sill_Depth'] = 64
df_full.loc[(df_full['Location_1'] == 'George'), 'Sill_Depth'] = 47
df_full.loc[(df_full['Location_1'] == 'Thompson'), 'Sill_Depth'] = 145
df_full.loc[(df_full['Location_1'] == 'Doubtful'), 'Sill_Depth'] = 101
df_full.loc[(df_full['Location_1'] == 'Dusky'), 'Sill_Depth'] = 65
df_full.loc[(df_full['Location_1'] == 'Preservation Inlet'), 'Sill_Depth'] = 30

df_full.to_excel(f'H:\Science\Datasets\Fiordland\Digitized_plus_interpolated_Data\InterpolatedData.xlsx')


"""
4 plots horizontal
"""
fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=0.1, hspace=0.35)

stations = np.unique(df_full['Station'])

xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
for i in range(0, len(stations)):
    stn1 = df_full.loc[(df_full['Station'] == stations[i]) & (df_full['Temperature'] > -999)]
    digitized = stn1.loc[df_full['Origin'] == 'Digitized']
    interpolated = stn1.loc[df_full['Origin'] == 'Interpolated']
    location = np.unique(stn1['Location_2'])

    plt.scatter(digitized['Temperature'], digitized['Depth'], label=f'{stations[i]}_{location}')
    plt.plot(interpolated['Temperature'], interpolated['Depth'])
plt.ylim(400,0)
plt.xlim(5,16)
plt.xlabel('Temperature (C)')
plt.ylabel('Depth (m)')
# plt.legend()

xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
for i in range(0, len(stations)):
    stn1 = df_full.loc[(df_full['Station'] == stations[i]) & (df_full['Salinity'] > -999)]
    digitized = stn1.loc[df_full['Origin'] == 'Digitized']
    interpolated = stn1.loc[df_full['Origin'] == 'Interpolated']
    location = np.unique(stn1['Location_2'])

    plt.scatter(digitized['Salinity'], digitized['Depth'], label=f'{stations[i]}_{location}')
    plt.plot(interpolated['Salinity'], interpolated['Depth'])
plt.ylim(400,0)
plt.xlim(0, 40)
plt.yticks([])
plt.xlabel('Salinity')
# plt.legend()

xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])
for i in range(0, len(stations)):
    stn1 = df_full.loc[(df_full['Station'] == stations[i]) & (df_full['Oxygen'] > -999)]
    digitized = stn1.loc[df_full['Origin'] == 'Digitized']
    interpolated = stn1.loc[df_full['Origin'] == 'Interpolated']
    location = np.unique(stn1['Location_2'])

    plt.scatter(digitized['Oxygen'], digitized['Depth'], label=f'{stations[i]}_{location}')
    plt.plot(interpolated['Oxygen'], interpolated['Depth'])
plt.ylim(400,0)
plt.xlim(0, 10)
plt.yticks([])
plt.xlabel('Oxygen')
# plt.legend()

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Fiordland_output/blueskyview_nolegend.png',
            dpi=300, bbox_inches="tight")
plt.close()






# # find where I have sill depths
# sills = df_full.loc[df_full['Sill_Depth'] > -999]
# print(sills)
# locs = np.unique(sills['Location_1'])
# arr1 = []
# arr2 = []
# arr3 = []
# for i in range(0, len(locs)):
#     loc1 = sills.loc[(sills['Location_1'] == locs[i]) & (sills['Oxygen'] > -999)]
#     if loc1.empty:
#         poop = 2
#     else:
#         arr1.append(min(loc1['Oxygen']))
#         arr2.append(min(loc1['Sill_Depth']))
#         arr3.append(locs[i])
#
# print(arr1)
# print(arr2)
# plt.scatter(arr2, arr1)
# plt.show()
#


#
# """
# XXXXXXXX
# XXXXXXXXX
# XXXXXXXXXXX
# XXXXXXXX
# """
#
# """
# 3x2 plots horizontal
# """
# fig = plt.figure(figsize=(12,12))
# gs = gridspec.GridSpec(2, 3)
# gs.update(wspace=0.1, hspace=0.15)
#
# stations_6a = ['S533', 'S517','S508','S483']
# labels_6a = ['Milford','George','Thompson','Preservation']
# stations_6b = ['S467','S469','S479','S483']
# labels_6b = ['Outer Sill','Cavern Head','Revolver Basin','Long Sound']
#
# # TOP ROW
# # plot structure
# xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
# for i in range(0, len(stations_6a)):
#
#     # grab the first location
#     loci = df_full.loc[df_full['Station'] == stations_6a[i]]
#     # split into original and integrated
#     og = loci.loc[loci['Origin'] == 'Digitized']
#     intergrated = loci.loc[loci['Origin'] == 'Interpolated']
#
#     plt.scatter(og['Temperature'], og['Depth'])
#     plt.plot(intergrated['Temperature'], intergrated['Depth'])
#
# plt.ylim(400,0)
# plt.xlim(9,13)
# plt.xlabel('Temperature')
# plt.ylabel('Depth (m)')
#
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# for i in range(0, len(stations_6a)):
#
#     # grab the first location
#     loci = df_full.loc[df_full['Station'] == stations_6a[i]]
#     # split into original and integrated
#     og = loci.loc[loci['Origin'] == 'Digitized']
#     print(og)
#     intergrated = loci.loc[loci['Origin'] == 'Interpolated']
#
#     plt.scatter(og['Salinity'], og['Depth'])
#     plt.plot(intergrated['Salinity'], intergrated['Depth'])
# plt.xlim(33,36)
# plt.xlabel('Salinity')
# plt.ylim(400,0)
# plt.yticks([])
#
#
# xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])
# for i in range(0, len(stations_6a)):
#
#     # grab the first location
#     loci = df_full.loc[df_full['Station'] == stations_6a[i]]
#     # split into original and integrated
#     og = loci.loc[loci['Origin'] == 'Digitized']
#     intergrated = loci.loc[loci['Origin'] == 'Interpolated']
#
#     plt.scatter(og['Density'], og['Depth'], label=f'{stations_6a[i]}_{labels_6a[i]}')
#     plt.plot(intergrated['Density'], intergrated['Depth'])
# plt.xlabel('Density')
# plt.ylim(400,0)
# plt.xlim(24,27)
# plt.yticks([])
# plt.legend()
#
# xtr_subsplot = fig.add_subplot(gs[1:2, 0:1])
# for i in range(0, len(stations_6b)):
#
#     # grab the first location
#     loci = df_full.loc[df_full['Station'] == stations_6b[i]]
#     # split into original and integrated
#     og = loci.loc[loci['Origin'] == 'Digitized']
#     intergrated = loci.loc[loci['Origin'] == 'Interpolated']
#
#     plt.scatter(og['Temperature'], og['Depth'])
#     plt.plot(intergrated['Temperature'], intergrated['Depth'])
# plt.ylim(400,0)
# plt.xlim(9,13)
# plt.xlabel('Temperature')
# plt.ylabel('Depth (m)')
#
# xtr_subsplot = fig.add_subplot(gs[1:2, 1:2])
# for i in range(0, len(stations_6b)):
#
#     # grab the first location
#     loci = df_full.loc[df_full['Station'] == stations_6b[i]]
#     # split into original and integrated
#     og = loci.loc[loci['Origin'] == 'Digitized']
#     intergrated = loci.loc[loci['Origin'] == 'Interpolated']
#
#     plt.scatter(og['Salinity'], og['Depth'])
#     plt.plot(intergrated['Salinity'], intergrated['Depth'])
# plt.xlim(33,36)
# plt.xlabel('Salinity')
# plt.ylim(400,0)
# plt.yticks([])
#
#
# xtr_subsplot = fig.add_subplot(gs[1:2, 2:3])
# for i in range(0, len(stations_6b)):
#
#     # grab the first location
#     loci = df_full.loc[df_full['Station'] == stations_6b[i]]
#     # split into original and integrated
#     og = loci.loc[loci['Origin'] == 'Digitized']
#     intergrated = loci.loc[loci['Origin'] == 'Interpolated']
#
#     plt.scatter(og['Density'], og['Depth'], label=f'{stations_6b[i]}_{labels_6b[i]}')
#     plt.plot(intergrated['Density'], intergrated['Depth'])
# plt.xlabel('Density')
# plt.ylim(400,0)
# plt.xlim(24,27)
# plt.yticks([])
# plt.legend()
#
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Fiordland_output/test2.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
#
# """
# NEW TS PLOTS
# """
#
# for i in range(0, len(stations_6a)):
#     loci = df_full.loc[df_full['Station'] == stations_6a[i]]
#     scatter
#
