import pandas as pd
import numpy as np
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

df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP1_reboot/STEP1_GLODAP_C14.csv')
print(df.columns)
print(len(df))

# rename certain fields to match the previous iteration of this work, and to get rid of the G2's:
df = df.rename(columns={'G2expocode': "EXPOCODE",
                        'G2salinity': "SALNTY",
                        'G2temperature':'CTDTMP',
                        'G2pressure':'CTDPRS',
                        'G2latitude':'LATITUDE',
                        'G2longitude':'LONGITUDE',
                        'G2c14':'DELC14',
                        'G2sigma0':'Pot_density_anomaly'})

"""
This next block of code assigns each row of data an "ocean label"
"""

df['OCEAN_LABEL'] = -999 # add initial value for this column
df['OCEAN_LABEL_2'] = -999 # add initial value for this column
df.loc[(df['LONGITUDE'] > 20) & (df['LONGITUDE'] <= 120), 'OCEAN_LABEL'] = 'Indian'

df.loc[(df['LONGITUDE'] > 120) & (df['LONGITUDE'] <= 180) & (df['LATITUDE'] > 0), 'OCEAN_LABEL'] = 'North Pacific'
df.loc[(df['LONGITUDE'] > -180) & (df['LONGITUDE'] <= -80) & (df['LATITUDE'] > 0), 'OCEAN_LABEL'] = 'North Pacific'

df.loc[(df['LONGITUDE'] > 120) & (df['LONGITUDE'] <= 180) & (df['LATITUDE'] <= 0), 'OCEAN_LABEL'] = 'South Pacific'
df.loc[(df['LONGITUDE'] > -180) & (df['LONGITUDE'] <= -80) & (df['LATITUDE'] <= 0), 'OCEAN_LABEL'] = 'South Pacific'

df.loc[(df['LONGITUDE'] > -80) & (df['LONGITUDE'] <= 20) & (df['LATITUDE'] > 0), 'OCEAN_LABEL'] = 'North Atlantic'
df.loc[(df['LONGITUDE'] > -60) & (df['LONGITUDE'] <= 20) & (df['LATITUDE'] <= 0), 'OCEAN_LABEL'] = 'South Atlantic'

df.loc[(df['LATITUDE'] <= -30), 'OCEAN_LABEL'] = 'Southern'

# all data above 55 will be RELABELED as Arctic.
df.loc[(df['LATITUDE'] >= 55), 'OCEAN_LABEL'] = 'Arctic'  # This is put into the second label beacuse there is no categorization for Arctic in Talley 08


df.loc[(df['LONGITUDE'] > -180) & (df['LONGITUDE'] <= -80) & (df['LATITUDE'] <= -30), 'OCEAN_LABEL_2'] = 'Southern - Pacific Sector'  # THIS IS ONLY ADDED SO I CAN INDEX UPON IT LATER DOING STATS
df.loc[(df['LONGITUDE'] > 120) & (df['LONGITUDE'] <= 180) & (df['LATITUDE'] <= 0-30), 'OCEAN_LABEL_2'] = 'Southern - Pacific Sector'
df.loc[(df['LONGITUDE'] > -60) & (df['LONGITUDE'] <= 20) & (df['LATITUDE'] <= -30), 'OCEAN_LABEL_2'] = 'Southern - Atlantic Sector'  # THIS IS ONLY ADDED SO I CAN INDEX UPON IT LATER DOING STATS
df.loc[(df['LONGITUDE'] > 20) & (df['LONGITUDE'] <= 120) & (df['LATITUDE'] <= -30), 'OCEAN_LABEL_2'] = 'Southern - Indian Sector'  # THIS IS ONLY ADDED SO I CAN INDEX UPON IT LATER DOING STATS

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

df = df.loc[df['Pot_density_anomaly'] > 0]
df.to_excel(r'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP2_assign_masses/STEP2_WATER_MASSES_ASSIGNED.xlsx')

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

    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP2_assign_masses/Spot_checks/{oceans[i]}.jpg', dpi=300, bbox_inches="tight")
    plt.close()

"""
Some final checks
"""

# how many bottles are not assigned a water mass?
nans = df.loc[df['Tally_assigned'] == -999]
# nans seems to include a potential density calculated of -1000. Lets remove that.
nans = nans.loc[nans['Pot_density_anomaly'] > 0]

assigned = df.loc[df['Tally_assigned'] != -999]
print(f'I ran step 2. Of the total dataset {len(df)}, {len(nans)} are NOT characterized. These are all samples that are in the Arctic')
actics = df.loc[df['OCEAN_LABEL'] == 'Arctic']
print(len(actics))





