"""
Updated: March 28, 2023

1. Adding a new time-axis to compare with Landschutzer data ('seconds since 2000-01-01' (dont ask me why))

Updated: 29 November 2022

This file does the following:
1. Assigns new BROADER latitude bands
2. Assigns time bands which can be made coarser or finer using the apply_time_bands function.

3. Finds means of each of those bands using the split apply combine method.
4. Creates plots 7 (decadal averages) and 8 (rolling mean).
"""

import datetime as dt  # Python standard library datetime  module
import numpy as np
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import pandas as pd
import numpy as np
from soar_analysis1 import df_2
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
pd.set_option('mode.chained_assignment', None)
from netcdf_example import ncdump


"""
In this file we want to explore how the data looks in terms of decadal means, 5 year means, and so on...
And try to compare our findings to the landschutzer plot...
"""

#update as of March 28, 2023 - adding a new time axis, see notes above.
conversion = 31540000
df_2['Landschutzer_time'] = (df_2['Decimal_date'] - 2000) * conversion

# break up the data by country based on previously existing flags from analysis2
chile = df_2.loc[df_2['Country'] == 0]
nz = df_2.loc[df_2['Country'] == 1]
ant = df_2.loc[df_2['Country'] == 2]

# we'll try doing this more cleanly than in the past by using categorical variables and split apply combine.
# just worry about chilean block for first try.

"""
Lets define bands of latitude: 
Band 1: -38 to -45
Band 2: -45 to -50
Band 3: -50 to -55
Band 4: < -60
"""

def apply_lat_bands(df):
    result_array = []

    for i in range(0, len(df)):
        current_row = df.iloc[i]

        if -45 < current_row['NewLat'] <= -38:
            result_array.append('Band1')
        elif -50 < current_row['NewLat'] <= -45:
            result_array.append('Band2')
        elif -55 < current_row['NewLat'] <= -50:
            result_array.append('Band3')
        elif current_row['NewLat'] < -60:
            result_array.append('Band4')
        else:
            result_array.append('error')
    return result_array

# space = np.linspace(1980, 2020, 9)
# print(space)


def apply_time_bands(df):
    result_array = []

    for i in range(0, len(df)):
        current_row = df.iloc[i]
        space = np.linspace(1980, 2025, 10)
        for k in range(0, len(space)-1):
            if space[k] < current_row['Decimal_date'] <= (space[k+1]):
                result_array.append(f"Interval_{space[k]}_{space[k+1]}")
    return result_array


for item in [chile, nz, ant]:
    item['Lat_Bands'] = apply_lat_bands(item)
    item['Time_Bands'] = apply_time_bands(item)


chile_band1 = chile.loc[chile['Lat_Bands'] == 'Band1']
chile_band2 = chile.loc[chile['Lat_Bands'] == 'Band2']
chile_band3 = chile.loc[chile['Lat_Bands'] == 'Band3']
nz_band1 = nz.loc[nz['Lat_Bands'] == 'Band1']
nz_band2 = nz.loc[nz['Lat_Bands'] == 'Band2']
nz_band3 = nz.loc[nz['Lat_Bands'] == 'Band3']
ant_band4 = ant.loc[ant['Lat_Bands'] == 'Band4']



# If you want to see the 5-year of 10-year average...
means_ch1 = chile_band1.groupby('Time_Bands').mean().reset_index()
means_ch2 = chile_band2.groupby('Time_Bands').mean().reset_index()
means_ch3 = chile_band3.groupby('Time_Bands').mean().reset_index()
means_nz1 = nz_band1.groupby('Time_Bands').mean().reset_index()
means_nz2 = nz_band2.groupby('Time_Bands').mean().reset_index()
means_nz3 = nz_band3.groupby('Time_Bands').mean().reset_index()
means_ant = ant_band4.groupby('Time_Bands').mean().reset_index()
# print(means_ch1.to_markdown())
# print(means_nz1.to_markdown())

stds_ch1 = chile_band1.groupby('Time_Bands').std().reset_index()
stds_ch2 = chile_band2.groupby('Time_Bands').std().reset_index()
stds_ch3 = chile_band3.groupby('Time_Bands').std().reset_index()
stds_nz1 = nz_band1.groupby('Time_Bands').std().reset_index()
stds_nz2 = nz_band2.groupby('Time_Bands').std().reset_index()
stds_nz3 = nz_band3.groupby('Time_Bands').std().reset_index()
stds_ant = ant_band4.groupby('Time_Bands').std().reset_index()

# If you want to do the running mean, it's really easy
dt = 5
chile_band1['Rolling_mean'] = chile_band1['r2_diff_trend'].rolling(dt).mean()
chile_band2['Rolling_mean'] = chile_band2['r2_diff_trend'].rolling(dt).mean()
chile_band3['Rolling_mean'] = chile_band3['r2_diff_trend'].rolling(dt).mean()
nz_band1['Rolling_mean'] = nz_band1['r2_diff_trend'].rolling(dt).mean()
nz_band2['Rolling_mean'] = nz_band2['r2_diff_trend'].rolling(dt).mean()
nz_band3['Rolling_mean'] = nz_band3['r2_diff_trend'].rolling(dt).mean()
ant_band4['Rolling_mean'] = ant_band4['r2_diff_trend'].rolling(dt).mean()
chile_band1['Rolling_std'] = chile_band1['r2_diff_trend'].rolling(dt).std()
chile_band2['Rolling_std'] = chile_band2['r2_diff_trend'].rolling(dt).std()
chile_band3['Rolling_std'] = chile_band3['r2_diff_trend'].rolling(dt).std()
nz_band1['Rolling_std'] = nz_band1['r2_diff_trend'].rolling(dt).std()
nz_band2['Rolling_std'] = nz_band2['r2_diff_trend'].rolling(dt).std()
nz_band3['Rolling_std'] = nz_band3['r2_diff_trend'].rolling(dt).std()
ant_band4['Rolling_std'] = ant_band4['r2_diff_trend'].rolling(dt).std()



"""
CREATE THE PLOT
"""
a1, a3, a5, a8 ='#d73027', '#fdae61', '#1c9099', '#4575b4' # testing
#landschutzer
# schutz_x = [1985, 1990, 1995, 2000, 2005, 2010, 2015]
# schutz_y = np.multiply([-1.5, -1.4, -1.2, -1, -1.5, -2, -2.2], -1)

# CREATES THE FIGURE
q = 6
fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(q, q*1.6180))

# NEXT LINE IS REQUIRED TO HOLD ON LANDSHCUTZER DATA
# ax4, ax5, ax6 = ax1.twinx(), ax2.twinx(), ax3.twinx()

# PLOTS THE ACTUAL DATA (MEANS FOR EACH TIME PERIOD, FOR EACH LATITUDE, SUBPLOTS 1, 2, 3, for AX1, AX2, AX3
ax1.plot(means_ch1['Decimal_date'], means_ch1['r2_diff_trend'], label='CH 38-45S', color = a1)
ax1.plot(means_ch2['Decimal_date'], means_ch2['r2_diff_trend'], label='CH 45-50S', color = a3)
ax1.plot(means_ch3['Decimal_date'], means_ch3['r2_diff_trend'], label='CH 50-55S', color = a5)
ax2.plot(means_nz1['Decimal_date'], means_nz1['r2_diff_trend'], label='NZ 38-45S', color = a1)
ax2.plot(means_nz2['Decimal_date'], means_nz2['r2_diff_trend'], label='NZ 45-50S', color = a3)
ax2.plot(means_nz3['Decimal_date'], means_nz3['r2_diff_trend'], label='NZ 50-55S', color = a5)
ax3.plot(means_ant['Decimal_date'], means_ant['r2_diff_trend'], label = 'NMW (70S)', color = a8)
# HOLDS ON THE LANDSCHUTZER DATA
# ax4.plot(schutz_x, schutz_y, label='Landschutzer', alpha = 0.3, linestyle='--', color='black')
# ax5.plot(schutz_x, schutz_y, label='Landschutzer', alpha = 0.3, linestyle='--', color='black')
# ax6.plot(schutz_x, schutz_y, label='Landschutzer', alpha = 0.3, linestyle='--', color='black')

#PLOTS THE BACKGROUND COLORS/ERROR RANGE

ax1.fill_between(means_ch1['Decimal_date'], (means_ch1['r2_diff_trend']+stds_ch1['r2_diff_trend']), (means_ch1['r2_diff_trend']-stds_ch1['r2_diff_trend']), alpha = 0.3, color = a1)
ax1.fill_between(means_ch2['Decimal_date'], (means_ch2['r2_diff_trend']+stds_ch2['r2_diff_trend']), (means_ch2['r2_diff_trend']-stds_ch2['r2_diff_trend']), alpha = 0.3, color = a3)
ax1.fill_between(means_ch3['Decimal_date'], (means_ch3['r2_diff_trend']+stds_ch3['r2_diff_trend']), (means_ch3['r2_diff_trend']-stds_ch3['r2_diff_trend']), alpha = 0.3, color = a5)
ax2.fill_between(means_nz1['Decimal_date'], (means_nz1['r2_diff_trend']+stds_nz1['r2_diff_trend']), (means_nz1['r2_diff_trend']-stds_nz1['r2_diff_trend']), alpha = 0.3, color = a1)
ax2.fill_between(means_nz2['Decimal_date'], (means_nz2['r2_diff_trend']+stds_nz2['r2_diff_trend']), (means_nz2['r2_diff_trend']-stds_nz2['r2_diff_trend']), alpha = 0.3, color = a3)
ax2.fill_between(means_nz3['Decimal_date'], (means_nz3['r2_diff_trend']+stds_nz3['r2_diff_trend']), (means_nz3['r2_diff_trend']-stds_nz3['r2_diff_trend']), alpha = 0.3, color = a5)
ax3.fill_between(means_ant['Decimal_date'], (means_ant['r2_diff_trend']+stds_ant['r2_diff_trend']), (means_ant['r2_diff_trend']-stds_ant['r2_diff_trend']), alpha = 0.3, color = a8)

ax2.set_ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - Reference]', color='black')

ax1.legend(), ax2.legend(), ax3.legend()
ymin = -10
ymax = 10
xmin = 1980
xmax = 2020
ax1.axis(ymin=ymin, ymax=ymax), ax2.axis(ymin=ymin, ymax=ymax), ax3.axis(ymin=ymin, ymax=ymax)
ax1.axis(xmin=xmin, xmax=xmax), ax2.axis(xmin=xmin, xmax=xmax), ax3.axis(xmin=xmin, xmax=xmax)
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot7.png',
            dpi=300, bbox_inches="tight")
plt.close()

# CREATES THE FIGURE
q = 6
fig, (ax1, ax2, ax3) = plt.subplots(3, figsize=(q, q*1.6180))

# NEXT LINE IS REQUIRED TO HOLD ON LANDSHCUTZER DATA
ax4, ax5, ax6 = ax1.twinx(), ax2.twinx(), ax3.twinx()

# PLOTS THE ACTUAL DATA (MEANS FOR EACH TIME PERIOD, FOR EACH LATITUDE, SUBPLOTS 1, 2, 3, for AX1, AX2, AX3
ax1.plot(chile_band1['Decimal_date'], chile_band1['Rolling_mean'], label='CH 38-45S', color = a1)
ax1.plot(chile_band2['Decimal_date'], chile_band2['Rolling_mean'], label='CH 45-50S', color = a3)
ax1.plot(chile_band3['Decimal_date'], chile_band3['Rolling_mean'], label='CH 50-55S', color = a5)
ax2.plot(nz_band1['Decimal_date'], nz_band1['Rolling_mean'], label='NZ 38-45S', color = a1)
ax2.plot(nz_band2['Decimal_date'], nz_band2['Rolling_mean'], label='NZ 45-50S', color = a3)
ax2.plot(nz_band3['Decimal_date'], nz_band3['Rolling_mean'], label='NZ 50-55S', color = a5)
ax3.plot(ant_band4['Decimal_date'], ant_band4['Rolling_mean'], label = 'NMW (70S)', color = a8)
# HOLDS ON THE LANDSCHUTZER DATA
# ax4.plot(schutz_x, schutz_y, label='Landschutzer', alpha = 0.3, linestyle='--', color='black')
# ax5.plot(schutz_x, schutz_y, label='Landschutzer', alpha = 0.3, linestyle='--', color='black')
# ax6.plot(schutz_x, schutz_y, label='Landschutzer', alpha = 0.3, linestyle='--', color='black')

#PLOTS THE BACKGROUND COLORS/ERROR RANGE

ax1.fill_between(chile_band1['Decimal_date'], (chile_band1['Rolling_mean']+chile_band1['Rolling_std']), (chile_band1['Rolling_mean']-chile_band1['Rolling_std']), alpha = 0.3, color = a1)
ax1.fill_between(chile_band2['Decimal_date'], (chile_band2['Rolling_mean']+chile_band2['Rolling_std']), (chile_band2['Rolling_mean']-chile_band2['Rolling_std']), alpha = 0.3, color = a3)
ax1.fill_between(chile_band3['Decimal_date'], (chile_band3['Rolling_mean']+chile_band3['Rolling_std']), (chile_band3['Rolling_mean']-chile_band3['Rolling_std']), alpha = 0.3, color = a5)
ax2.fill_between(nz_band1['Decimal_date'], (nz_band1['Rolling_mean']+nz_band1['Rolling_std']), (nz_band1['Rolling_mean']-nz_band1['Rolling_std']), alpha = 0.3, color = a1)
ax2.fill_between(nz_band2['Decimal_date'], (nz_band2['Rolling_mean']+nz_band2['Rolling_std']), (nz_band2['Rolling_mean']-nz_band2['Rolling_std']), alpha = 0.3, color = a3)
ax2.fill_between(nz_band3['Decimal_date'], (nz_band3['Rolling_mean']+nz_band3['Rolling_std']), (nz_band3['Rolling_mean']-nz_band3['Rolling_std']), alpha = 0.3, color = a5)
ax3.fill_between(ant_band4['Decimal_date'], (ant_band4['Rolling_mean']+ant_band4['Rolling_std']), (ant_band4['Rolling_mean']-ant_band4['Rolling_std']), alpha = 0.3, color = a8)


ax2.set_ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Tree Ring - Baring head]', color='black')
# ax2.set_ylabel('SOAR Residuals', color='black')
# ax3.set_ylabel('SOAR Residuals', color='black')
# ax4.set_ylabel('Lanschutzer Data (--)', color='black')
# ax5.set_ylabel('Lanschutzer Data (--)', color='black')
# ax6.set_ylabel('Lanschutzer Data (--)', color='black')

ax1.legend(), ax2.legend(), ax3.legend()
ymin = -10
ymax = 10
xmin = 1980
xmax = 2020
ax1.axis(ymin=ymin, ymax=ymax), ax2.axis(ymin=ymin, ymax=ymax), ax3.axis(ymin=ymin, ymax=ymax)
ax1.axis(xmin=xmin, xmax=xmax), ax2.axis(xmin=xmin, xmax=xmax), ax3.axis(xmin=xmin, xmax=xmax)
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot8.png',
            dpi=300, bbox_inches="tight")
plt.close()


"""
I want to plot my data vs Landschutzer

As its written now I'm plotting the WHOLE dataset (my data) and just a chunk of Landies (see indexing below) 
"""

nc_f = 'H:/Science/Datasets/spco2_1982-2015_MPI_SOM-FFN_v2016.nc'
nc_fid = Dataset(nc_f, 'r')  # Dataset is the class behavior to open the file
# and create an instance of the ncCDF4 class

#tells you the info in the file
nc_attrs, nc_dims, nc_vars = ncdump(nc_fid) # Extract data from NetCDF file

# have a look at the variable of interest
fgc02_smooth = nc_fid['fgco2_smoothed']
lats = nc_fid.variables['lat'][:]  # extract/copy the data
lons = nc_fid.variables['lon'][:]
time = nc_fid.variables['time_bnds'][:]
# print(fgc02_smooth)

# X, lat, lon
test = fgc02_smooth[:,30,1]
# only grab the second column of the time_bands (the end of each time - chunk)
time = time[:,1]

# plt.scatter(time, test)
# plt.scatter(df_2['Landschutzer_time'], df_2['r2_diff_trend'])
# plt.show()

fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(3, 6)
gs.update(wspace=.35, hspace=.6)
xtr_subsplot = fig.add_subplot(gs[0:3, 0:3])
plt.title('Landschutzer Data (only 1 latitude, only 1 longitude)')
plt.scatter(time, test)

xtr_subsplot = fig.add_subplot(gs[0:3, 3:6])
plt.title('Tree Ring Data (All Sites, All Times)')
plt.scatter(df_2['Landschutzer_time'], df_2['r2_diff_trend'])
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot_x1.png',
            dpi=300, bbox_inches="tight")










