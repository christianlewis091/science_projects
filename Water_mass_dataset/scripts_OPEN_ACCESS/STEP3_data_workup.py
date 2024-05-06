"""
This script assigns each Niskin bottle a watermass based on the ocean its in,
and the potential densities by comparing them to Talley 08

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

# read in the sheet that was written in the above section of the code.
df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\Water_mass_dataset\output_OPEN_ACCESS\STEP2_clean_data\raw_data_watermassproject.xlsx')

"""
Potential density needs to be added to the data in order to filter based on Talley's tables. 

This will be done according to :
McDougall T. J. and P. M. Barker, 2011: Getting started with TEOS-10 and the Gibbs Seawater (GSW)
Oceanographic Toolbox, 28pp., SCOR/IAPSO WG127, ISBN 978-0-646-55621-5.

Followed steps on bottom of page 2. 
"""

df['fake_ref'] = 0 # create a column with zeroes to allow functions to continue in pandas (0 = reference pressure)
df['SA'] = gsw.conversions.SA_from_SP(df['SALNTY'], df['CTDPRS'], df['LONGITUDE'], df['LATITUDE'])
df['CT'] = gsw.conversions.CT_from_t(df['SA'], df['CTDTMP'], df['CTDPRS'])
df['Pot_density'] = gsw.pot_rho_t_exact(df['SA'], df['CTDTMP'], df['CTDPRS'], df['fake_ref'])
df['Pot_density_anomaly'] = gsw.sigma0(df['SA'], df['CT'])

# some rows/cruises are missing because they don't include SALTY or CTDTMP. We will drop those
# row by dropping NANs on the Pot_density_anomaly
df = df.dropna(subset=['Pot_density_anomaly'])
# df.to_excel(r'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP3_data_workup/STEP3_data_watermassproject.xlsx')

"""
6/5/24
I find it helpful when exact numbers that are found in the publication can be found in a line in PYTHON. 
Therefore I'll be writing some special print lines that I can traceback later to avoid mini panics if I dont know 
where the data is coming from.  
"""
go_ship = df.loc[df['Project Name'] == 'GO-SHIP']
glodap = df.loc[df['Project Name'] == 'GLODAP']
x = len(np.unique(go_ship['EXPOCODE'].astype(str)))
y = len(np.unique(glodap['EXPOCODE'].astype(str)))

print(f'The total length of data is {len(df)}. After filtering out all NaNs after calculating potential density, there is {x} cruises from GoSHIP and {y} cruises from GLODAP ')


"""
This next block of code assigns each row of data an "ocean label"
"""

df['OCEAN_LABEL'] = -999 # add initial value for this column
df.loc[(df['LONGITUDE'] > 20) & (df['LONGITUDE'] <= 120), 'OCEAN_LABEL'] = 'Indian'

df.loc[(df['LONGITUDE'] > 120) & (df['LONGITUDE'] <= 180) & (df['LATITUDE'] > 0), 'OCEAN_LABEL'] = 'North Pacific'
df.loc[(df['LONGITUDE'] > -180) & (df['LONGITUDE'] <= -80) & (df['LATITUDE'] > 0), 'OCEAN_LABEL'] = 'North Pacific'

df.loc[(df['LONGITUDE'] > 120) & (df['LONGITUDE'] <= 180) & (df['LATITUDE'] <= 0), 'OCEAN_LABEL'] = 'South Pacific'
df.loc[(df['LONGITUDE'] > -180) & (df['LONGITUDE'] <= -80) & (df['LATITUDE'] <= 0), 'OCEAN_LABEL'] = 'South Pacific'

df.loc[(df['LONGITUDE'] > -80) & (df['LONGITUDE'] <= 20) & (df['LATITUDE'] > 0), 'OCEAN_LABEL'] = 'North Atlantic'
df.loc[(df['LONGITUDE'] > -80) & (df['LONGITUDE'] <= 20) & (df['LATITUDE'] <= 0), 'OCEAN_LABEL'] = 'South Atlantic'

df.loc[(df['LATITUDE'] >= 66.6), 'OCEAN_LABEL'] = 'Arctic'
df.loc[(df['LATITUDE'] <= -30), 'OCEAN_LABEL'] = 'Southern'

"""
THIS BLOCK ASSIGNS THE WATER MASSES!
"""

df['Tally_assigned'] = -999 # assign a dummy column name to the Talley Water Masses
wmc_Talley = pd.read_excel(f'H:\Science\Datasets\Water_Mass_Characteristics.xlsx',sheet_name='Talley', skiprows=1, comment='#')
for i in range(0, len(wmc_Talley)):
    row = wmc_Talley.iloc[i]
    water_mass = row['Name']
    # assign the new water mass using pandas
    df.loc[(df['OCEAN_LABEL'] == row['Talley Label']) & (df['Pot_density_anomaly'] >= row['roe min']) & (df['Pot_density_anomaly'] < row['roe max']), 'Tally_assigned'] = water_mass


df.to_excel(r'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP3_data_workup/STEP3_WATER_MASSES_ASSIGNED.xlsx')

"""
THIS BLOCK CHECKS THE OCEANS ARE LABELLED CORRECTLY - are they in the right spot on the map? 
"""

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

    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP3_data_workup/Spot_checks/{oceans[i]}.jpg', dpi=300, bbox_inches="tight")
    plt.close()





