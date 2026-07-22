"""
October12, 2023
Adding new TEOS fnuctions to try to help potneitla density calcuilation

Future:
Still a problem exists where some potential desnities are not being calculated...

August 28, 2023:
Whenever CTD temperatures are below 0, potential density cannot be calculated, at least with the python module I have.
I'm setting those cases = "Bottom Water"

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
import seawater
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec

#
# # Import water mass characterisitcs
# wmc = pd.read_excel(f'H:\Science\Datasets\Water_Mass_Characteristics.xlsx',sheet_name='Emery' ,skiprows=2, comment='#')
# wmc_Talley = pd.read_excel(f'H:\Science\Datasets\Water_Mass_Characteristics.xlsx',sheet_name='Talley', skiprows=1, comment='#')
# #
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
"""
This section takes a bulk download of all the available GO-SHIP data and GLODAP data and merges it into one giant file
than can be used to run the for-loop to assign water masses.
"""
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
"""
Now I'm adding on GLODAP data, see scrape_GLODAP.py
"""
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














# print(f"{goship_len}: GOSHIP length")
# print(f"{glodap_len}: GLODAP length")
#

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

This will be done according to :
McDougall T. J. and P. M. Barker, 2011: Getting started with TEOS-10 and the Gibbs Seawater (GSW)
Oceanographic Toolbox, 28pp., SCOR/IAPSO WG127, ISBN 978-0-646-55621-5.

Followed steps on bottom of page 2. 
"""

df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')

df['fake_ref'] = 0 # create a column with zeroes to allow functions to continue in pandas (0 = reference pressure)
df['SA'] = gsw.conversions.SA_from_SP(df['SALNTY'], df['CTDPRS'], df['LONGITUDE'], df['LATITUDE'])
df['CT'] = gsw.conversions.CT_from_t(df['SA'], df['CTDTMP'], df['CTDPRS'])
df['Pot_density'] = gsw.pot_rho_t_exact(df['SA'], df['CTDTMP'], df['CTDPRS'], df['fake_ref'])
df['Pot_density_anomaly'] = gsw.sigma0(df['SA'], df['CT'])

# some rows/cruises are missing because they don't include SALTY or CTDTMP. We will drop those
# row by dropping NANs on the Pot_density_anomaly
df = df.dropna(subset=['Pot_density_anomaly'])

"""
THIS BLOCK ASSIGNS THE WATER MASSES!, Rewritten on October 23, 2023 to make full use of PANDAS :)
"""
df['OCEAN_LABEL'] = -999 # add initial value for this column
df.loc[(df['LONGITUDE'] > 20) & (df['LONGITUDE'] <= 120), 'OCEAN_LABEL'] = 'Indian'
df.loc[(df['LONGITUDE'] > 120) & (df['LONGITUDE'] <= 180), 'OCEAN_LABEL'] = 'Pacific'
df.loc[(df['LONGITUDE'] > -180) & (df['LONGITUDE'] <= -80), 'OCEAN_LABEL'] = 'Pacific'
df.loc[(df['LONGITUDE'] > -80) & (df['LONGITUDE'] <= 20), 'OCEAN_LABEL'] = 'Atlantic'
df.loc[(df['LATITUDE'] <= -30), 'OCEAN_LABEL'] = 'Southern'

df['Tally_assigned'] = -999 # assign a dummy column name to the Talley Water Masses
wmc_Talley = pd.read_excel(f'H:\Science\Datasets\Water_Mass_Characteristics.xlsx',sheet_name='Talley', skiprows=1, comment='#')
for i in range(0, len(wmc_Talley)):
    row = wmc_Talley.iloc[i]
    name = row['Name']
    new_label = row['Talley Label']
    # assign the new water mass using pandas
    df.loc[(df['OCEAN_LABEL'] == row['Ocean']) & (df['Pot_density_anomaly'] >= row['roe min']) & (df['Pot_density_anomaly'] < row['roe max']), 'Tally_assigned'] = name

# By renaming these, I can connect Southern Ocean sectors of each basin to their northward counterparts for more
# continuity in the figures (if I don't do these lines) you get a SOce plot for AABW, and then Atlantic for instance
# and its better if its a continous blob
# TODO very important this step is exaplined well in methods. people will get confused
df.loc[(df['LONGITUDE'] > 20) & (df['LONGITUDE'] <= 120) & (df['LATITUDE'] <= -30), 'OCEAN_LABEL'] = 'Southern_Indian'
df.loc[(df['LONGITUDE'] > 120) & (df['LONGITUDE'] <= 180) & (df['LATITUDE'] <= -30), 'OCEAN_LABEL'] = 'Southern_Pacific'
df.loc[(df['LONGITUDE'] > -180) & (df['LONGITUDE'] <= -80) & (df['LATITUDE'] <= -30), 'OCEAN_LABEL'] = 'Southern_Pacific'
df.loc[(df['LONGITUDE'] > -80) & (df['LONGITUDE'] <= 20) & (df['LATITUDE'] <= -30), 'OCEAN_LABEL'] = 'Southern_Atlantic'

# df.to_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_assigned2.xlsx')
# df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_assigned2.xlsx')
# check the data makes sense on the map
# where are valuse not assigned?
missing = df.loc[df['OCEAN_LABEL'] == -999]
df = df.loc[df['OCEAN_LABEL'] != -999]
oceans = np.unique(df['OCEAN_LABEL'])
for i in range(0, len(oceans)):
    df1 = df.loc[df['OCEAN_LABEL'] == oceans[i]]

    maxlat = 90
    minlat = -90
    max_lon = 180
    min_lon = -180

    # res = 'i'  # todo switch to i for intermediate
    size1 = 50

    # initialize the figure and subplots.
    fig = plt.figure(1, figsize=(8, 8))

    map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=min_lon, urcrnrlon=max_lon)
    map.etopo()
    map.drawcoastlines()
    map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
    map.drawmeridians(np.arange(-180, 180, 40), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
    lats = df1['LATITUDE']
    lons = df1['LONGITUDE']

    z, a = map(lons,  lats)
    map.scatter(z, a, marker='o', s = 3.5, color='yellow', edgecolor='yellow')

    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output/Maps/POST_WATER_MASS_ASSIGNEMT_LOCATION_CHECK_{oceans[i]}.jpg', dpi=300, bbox_inches="tight")
    plt.close()

# df.to_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_assigned2.xlsx')














"""
UNCOMMENT ABOVE IF YOU NEED TO EDIT OR REBUILD THE DATABASE. CONTINUE DOWN IF YOU WANT PLOTS

For the plots, it seems easier to interpret the Ocean Sections when the Southern Sector is included with the northward
section. For instance, if you include the Southern Ocean Pacific with the general pacific, you get a complete picture. 
For this reason, for the plots, I'm going to make a new dataframe for each where I select those two sectors and then 
plot them
"""

# df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_assigned2.xlsx')

pac = df.loc[(df['OCEAN_LABEL'] == 'Pacific') | (df['OCEAN_LABEL'] == 'Southern_Pacific')]
atl = df.loc[(df['OCEAN_LABEL'] == 'Atlantic') | (df['OCEAN_LABEL'] == 'Southern_Atlantic')]
ind = df.loc[(df['OCEAN_LABEL'] == 'Indian') | (df['OCEAN_LABEL'] == 'Southern_Indian')]

# # I want to report a table of all the cruises that I have inlcuded in here. I'll output that here...
# x = df['EXPOCODE'].astype(str)
# expos = np.unique(x)
# expos = pd.DataFrame({"EXPOCODE": expos})
#
# # expos.to_excel(r'H:\Science\Datasets\Hydrographic\unique_expos.xlsx')

# loop through the different oceans
list1 = [pac, atl, ind]
names = ['Pacific','Atlantic','Indian']
for i in range(0, len(list1)):
    sub_df = list1[i]
#
    # loop through the water masses that exist in that ocean
    wm_labels = np.unique(sub_df['Tally_assigned'])
    for q in range(0, len(wm_labels)):

        # find the first water mass in this ocean
        subsub_df = sub_df.loc[sub_df['Tally_assigned'] == wm_labels[q]]

        fig = plt.figure(figsize=(12,6))
        gs = gridspec.GridSpec(2, 4)
        gs.update(wspace=.6, hspace=.6)
        xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])

        plt.scatter(subsub_df['LATITUDE'], subsub_df['CTDPRS'], c=subsub_df['DELC14'], cmap='magma')
        # plt.plot(subsub_df['LATITUDE'], subsub_df['DEPTH'], color='black')
        plt.ylim(4000, 0)
        plt.xlim(-70, 70)
        plt.clim(-200, 150)
        plt.title(f"{names[i]}, {wm_labels[q]}")
        plt.ylabel('Depth (CTD Pressure)')
        plt.xlabel('Latitude')

        xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
        import math
        # add the contours
        # Figure out boudaries (mins and maxs)
        smin = subsub_df['SA'].min() - (0.01 * subsub_df['SA'].min())
        smax = subsub_df['SA'].max() + (0.01 * subsub_df['SA'].max())
        tmin = subsub_df['CT'].min() - (0.1 * subsub_df['CT'].max())
        tmax = subsub_df['CT'].max() + (0.1 * subsub_df['CT'].max())

        # Calculate how many gridcells we need in the x and y dimensions
        xdim = ((smax - smin)/0.1)+1
        ydim = ((tmax - tmin)/0.1)+1
        xdim = int(round(xdim, 0))
        ydim = int(round(ydim, 0))

        # Create empty grid of zeros
        dens = np.zeros((ydim,xdim))

        # Create temp and salt vectors of appropiate dimensions
        ti = np.linspace(1,ydim-1,ydim)*0.1+tmin
        si = np.linspace(1,xdim-1,xdim)*0.1+smin

        # Loop to fill in grid with densities
        for j in range(0,int(ydim)):
            for p in range(0, int(xdim)):
                dens[j,p]=gsw.rho(si[p],ti[j],0)

        # Substract 1000 to convert to sigma-t
        dens = dens - 1000

        CS = plt.contour(si,ti,dens, linestyles='dashed', colors='k')
        plt.clabel(CS, fontsize=12, inline=1) # Label every second
        plt.scatter(subsub_df['SA'], subsub_df['CT'], c=subsub_df['DELC14'], cmap='magma')
        plt.colorbar().set_label('\u0394$^1$$^4$CO$_2$ (\u2030)', rotation=270, labelpad = 1)
        plt.clim(-200, 150)
        plt.ylabel('Conservative Temperature')
        plt.xlabel('Absolute Salinity')
        plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output/Talley_all/{names[i]}_{wm_labels[q]}.png')
        plt.close()



"""
I'm repeating a bunch of code because I want to run a case where I dont categorize anything according to Dr. Talley's SOce 
categories so they plots can appear more fluid. 
"""

df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')

df['fake_ref'] = 0 # create a column with zeroes to allow functions to continue in pandas (0 = reference pressure)
df['SA'] = gsw.conversions.SA_from_SP(df['SALNTY'], df['CTDPRS'], df['LONGITUDE'], df['LATITUDE'])
df['CT'] = gsw.conversions.CT_from_t(df['SA'], df['CTDTMP'], df['CTDPRS'])
df['Pot_density'] = gsw.pot_rho_t_exact(df['SA'], df['CTDTMP'], df['CTDPRS'], df['fake_ref'])
df['Pot_density_anomaly'] = gsw.sigma0(df['SA'], df['CT'])

# some rows/cruises are missing because they don't include SALTY or CTDTMP. We will drop those
# row by dropping NANs on the Pot_density_anomaly
df = df.dropna(subset=['Pot_density_anomaly'])

"""
THIS BLOCK ASSIGNS THE WATER MASSES!, Rewritten on October 23, 2023 to make full use of PANDAS :)
"""
df['OCEAN_LABEL'] = -999 # add initial value for this column
df.loc[(df['LONGITUDE'] > 20) & (df['LONGITUDE'] <= 120), 'OCEAN_LABEL'] = 'Indian'
df.loc[(df['LONGITUDE'] > 120) & (df['LONGITUDE'] <= 180), 'OCEAN_LABEL'] = 'Pacific'
df.loc[(df['LONGITUDE'] > -180) & (df['LONGITUDE'] <= -80), 'OCEAN_LABEL'] = 'Pacific'
df.loc[(df['LONGITUDE'] > -80) & (df['LONGITUDE'] <= 20), 'OCEAN_LABEL'] = 'Atlantic'


df['Tally_assigned'] = -999 # assign a dummy column name to the Talley Water Masses
wmc_Talley = pd.read_excel(f'H:\Science\Datasets\Water_Mass_Characteristics.xlsx',sheet_name='Talley_noSouthern', skiprows=1, comment='#')
for i in range(0, len(wmc_Talley)):
    row = wmc_Talley.iloc[i]
    name = row['Name']
    new_label = row['Talley Label']
    # assign the new water mass using pandas
    df.loc[(df['OCEAN_LABEL'] == row['Ocean']) & (df['Pot_density_anomaly'] >= row['roe min']) & (df['Pot_density_anomaly'] < row['roe max']), 'Tally_assigned'] = name

missing = df.loc[df['OCEAN_LABEL'] == -999]
df = df.loc[df['OCEAN_LABEL'] != -999]
oceans = np.unique(df['OCEAN_LABEL'])
for i in range(0, len(oceans)):
    df1 = df.loc[df['OCEAN_LABEL'] == oceans[i]]

    maxlat = 90
    minlat = -90
    max_lon = 180
    min_lon = -180

    # res = 'i'  # todo switch to i for intermediate
    size1 = 50

    # initialize the figure and subplots.
    fig = plt.figure(1, figsize=(8, 8))

    map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=min_lon, urcrnrlon=max_lon)
    map.etopo()
    map.drawcoastlines()
    map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
    map.drawmeridians(np.arange(-180, 180, 40), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
    lats = df1['LATITUDE']
    lons = df1['LONGITUDE']

    z, a = map(lons,  lats)
    map.scatter(z, a, marker='o', s = 3.5, color='yellow', edgecolor='yellow')

    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output/Maps/noSouthern_maps_{oceans[i]}.jpg', dpi=300, bbox_inches="tight")
    plt.close()

df.to_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject_assigned_noSouthern.xlsx')

pac = df.loc[(df['OCEAN_LABEL'] == 'Pacific')]
atl = df.loc[(df['OCEAN_LABEL'] == 'Atlantic')]
ind = df.loc[(df['OCEAN_LABEL'] == 'Indian')]

# # I want to report a table of all the cruises that I have inlcuded in here. I'll output that here...
# x = df['EXPOCODE'].astype(str)
# expos = np.unique(x)
# expos = pd.DataFrame({"EXPOCODE": expos})
#
# # expos.to_excel(r'H:\Science\Datasets\Hydrographic\unique_expos.xlsx')

# loop through the different oceans
list1 = [pac, atl, ind]
names = ['Pacific','Atlantic','Indian']
for i in range(0, len(list1)):
    sub_df = list1[i]
    #
    # loop through the water masses that exist in that ocean
    wm_labels = np.unique(sub_df['Tally_assigned'])
    for q in range(0, len(wm_labels)):

        # find the first water mass in this ocean
        subsub_df = sub_df.loc[sub_df['Tally_assigned'] == wm_labels[q]]

        fig = plt.figure(figsize=(12,6))
        gs = gridspec.GridSpec(2, 4)
        gs.update(wspace=.6, hspace=.6)
        xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])

        plt.scatter(subsub_df['LATITUDE'], subsub_df['CTDPRS'], c=subsub_df['DELC14'], cmap='magma')
        # plt.plot(subsub_df['LATITUDE'], subsub_df['DEPTH'], color='black')
        plt.ylim(4000, 0)
        plt.xlim(-70, 70)
        plt.title(f"{names[i]}, {wm_labels[q]}")
        plt.ylabel('Depth (CTD Pressure)')
        plt.xlabel('Latitude')
        plt.clim(-200, 150)

        xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
        import math
        # add the contours
        # Figure out boudaries (mins and maxs)
        smin = subsub_df['SA'].min() - (0.01 * subsub_df['SA'].min())
        smax = subsub_df['SA'].max() + (0.01 * subsub_df['SA'].max())
        tmin = subsub_df['CT'].min() - (0.1 * subsub_df['CT'].max())
        tmax = subsub_df['CT'].max() + (0.1 * subsub_df['CT'].max())

        # Calculate how many gridcells we need in the x and y dimensions
        xdim = ((smax - smin)/0.1)+1
        ydim = ((tmax - tmin)/0.1)+1
        xdim = int(round(xdim, 0))
        ydim = int(round(ydim, 0))

        # Create empty grid of zeros
        dens = np.zeros((ydim,xdim))

        # Create temp and salt vectors of appropiate dimensions
        ti = np.linspace(1,ydim-1,ydim)*0.1+tmin
        si = np.linspace(1,xdim-1,xdim)*0.1+smin

        # Loop to fill in grid with densities
        for j in range(0,int(ydim)):
            for p in range(0, int(xdim)):
                dens[j,p]=gsw.rho(si[p],ti[j],0)

        # Substract 1000 to convert to sigma-t
        dens = dens - 1000

        CS = plt.contour(si,ti,dens, linestyles='dashed', colors='k')
        plt.clabel(CS, fontsize=12, inline=1) # Label every second
        plt.scatter(subsub_df['SA'], subsub_df['CT'], c=subsub_df['DELC14'], cmap='magma')
        plt.colorbar().set_label('\u0394$^1$$^4$CO$_2$ (\u2030)', rotation=270, labelpad = 1)
        plt.clim(-200, 150)

        plt.ylabel('Conservative Temperature')
        plt.xlabel('Absolute Salinity')
        plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output/Talley_noSouthern/{names[i]}_{wm_labels[q]}.png')
        plt.close()
































"""
OLD MAYBE BAD
"""



#
#
# df = pd.read_excel(r'H:\Science\Datasets\Hydrographic\water_masses_assigned.xlsx')
# df = df.loc[df['DELC14'] > -999]
# df = df.loc[df['SALNTY'] > -999]
# df = df.loc[df['Water Mass Talley'] != 'Error: No Water Mass Assigned']
# # df.to_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/water_mass_database_cleaned.csv')
#
# df = df.dropna(subset='DELC14')
# df = df.dropna(subset='CTDPRS')
# df = df.dropna(subset='LATITUDE')
#
# pacific = df.loc[df['Ocean_Label'] == 'Pacific']
# names = np.unique(pacific['Water Mass Talley'])
#
# for i in range(0, len(names)):
#     this_wm = pacific.loc[pacific['Water Mass Talley'] == names[i]]
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
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output/Pacific_Ocean_{names[i]}.png')
#     plt.close()
#
#
# pacific = df.loc[df['Ocean_Label'] == 'Indian']
# names = np.unique(pacific['Water Mass Talley'])
#
# for i in range(0, len(names)):
#     this_wm = pacific.loc[pacific['Water Mass Talley'] == names[i]]
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
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output/Indian_Ocean_{names[i]}.png')
#     plt.close()
#
#
# pacific = df.loc[df['Ocean_Label'] == 'Atlantic']
# names = np.unique(pacific['Water Mass Talley'])
#
# for i in range(0, len(names)):
#     this_wm = pacific.loc[pacific['Water Mass Talley'] == names[i]]
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
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output/Atlantic_Ocean_{names[i]}.png')
#     plt.close()





# d Conservative Temperature from parametesr based on TEOS guidelines...
# https://www.teos-10.org/pubs/gsw/html/gsw_SA_from_SP.html
# https://teos-10.github.io/GSW-Python/conversions.html Calculates Conservative Temperature of seawater from in-situ temperature.
# calculate convservative temperature

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
# database.to_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')
# np.savetxt(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.txt', database.values, fmt='%d')
# TODO the above block has potential densities within a very fixed range, must have a problem...

"""
Calculate potential desnity with different module
"""
# database = pd.read_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')
#
# # get rid of all -999's
# database = database.loc[database['SALNTY'] != -999]
# database = database.loc[database['CTDTMP'] != -999]
# database = database.loc[database['CTDPRS'] != -999]
#
# roe_array = []
# for i in range(0, len(database)):
#     row = database.iloc[i]
#
#     # if temperature is negative, assign it "Bottom Waters"
#     if row['CTDTMP'] <= 0:
#         roe_array.append('Negative CTDTMP')
#
#     else:
#         # SA = gsw.gsw_SA_from_SP(row['SALNTY'], row['CTDPRS'], row['LONGITUDE'], row['LATITUDE'])
#         roe = seawater.eos80.pden(row['SALNTY'], row['CTDTMP'], row['CTDPRS'], pr=0)
#         roe = roe - 1000
#         roe_array.append(np.float(roe))
#
#
# database['Potential Density'] = roe_array
# database.to_excel(r'H:\Science\Datasets\Hydrographic\raw_data_watermassproject.xlsx')
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
