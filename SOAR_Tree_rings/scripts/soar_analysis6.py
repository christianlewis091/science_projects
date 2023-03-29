"""
The creation of this file was brought on by the meeting I had with Sara Fletcher and Erik Behrens at NIWA on
Feb 24, 2023.

The following ideas were brought up:
1. I can compare my records / 5-year latitdinally banded averages to Landschutzer's data, which is publicly available.
https://www.ncei.noaa.gov/access/ocean-carbon-acidification-data-system/oceans/SPCO2_1982_2015_ETH_SOM_FFN.html

2. We should de-trend the trends from the main plot (Plot 7).
3. Can look at average D14C through time, relative to atmosphere (Wannikov Style); this will look similar to Heather Graven's 2012 paper
4. Calculate the component of our trend that can be explained through temperature alone (temperature can explain a lot, cold water will absorb more gas and change the solubility). Start with the Sarmiento and Gruber Textbook.
5. We should be able to seperate the trends we see into two categories, components affected by 1) temperature and 2) upwelling.
6. Look at Erik's NEMO Model, binning two boxes for the Pacific, and two boxes for the Indian Ocean (don't locate by latitude!), and see in the model if mixed layer depth in summer vs winter; summer may be the growing season, but winter will have deeper mixed layer and more outgassing.
7. If you compare the climatological runs (which have no temperture effect) with the real variability, we can isolate the component that is due to temperature.
8. We can use an age tracer in the model to...
9. Setup a monthly meeting with these guys.

"""
# grab the import info from the netcdf example file
from soar_analysis4 import *
from netcdf_example import *
import array as arr
import numpy as np
from numpy import ma
import pandas as pd
import matplotlib.pyplot as plt
# netCDF4 needs to be installed in your environment for this to work
import xarray as xr
import rioxarray as rxr
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
import seaborn as sns
import geopandas as gpd
import earthpy as et


#import the netcdf landschutzer data
nc_f = 'H:/Science/Datasets/spco2_1982-2015_MPI_SOM-FFN_v2016.nc'

# Dataset is the class behavior to open the file
nc_fid = Dataset(nc_f, 'r')

# function pulled from import statement; tells you the info in the file
nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)

# have a look at the variable of interest
fgc02_smooth = nc_fid['fgco2_smoothed']
# print(fgc02_smooth)

# extract data
# compressed removes mask
# list conversion allows future indexing
lats = nc_fid.variables['lat'][:].compressed().tolist()  # extract/copy the data
lons = nc_fid.variables['lon'][:].compressed().tolist()
time = nc_fid.variables['time_bnds'][:]
time = time[:,1]
# the latitude bands I'm interested in are as follows, going on from analysis 4 (see lines 54 - 70).
# because the indeces are in 0.5 degrees, I'll expand the boundaries as follows:
b1_max = -37.5  # index =
b1_min = -45.5
b1_index_max = lats.index(b1_max)
b1_index_min = lats.index(b1_min)
# print(b1_index_min)
# print(b1_index_max)
#
b2_max = -44.5
b2_min = -50.5
b2_index_max = lats.index(b2_max)
b2_index_min = lats.index(b2_min)
#
#
b3_max = -49.5
b3_min = -55.5
b3_index_max = lats.index(b3_max)
b3_index_min = lats.index(b3_min)
#
b4_max = -59.5
b4_min = -80.5
b4_index_max = lats.index(b4_max)
b4_index_min = lats.index(b4_min)

lon_max = -20.5
lon_min = -40.5
lon_index_max = lats.index(lon_max)
lon_index_min = lats.index(lon_min)

#
# # Now I want to index the netCDF data within these bands, and average them, and find their STD, and make a plot similar
# # to plot 7.
# # first I need to identify the indeces where these latitudes are...should I put the lats and lons into a dataframe? No.
# # Index them, and average across the lats and lon's, then you plot the result over TIME.
# # ls is for landschutzer
# # I'm following indexing pattern here https://stackoverflow.com/questions/49762136/how-to-index-a-netcdf-file-very-quickly
# # dis[:,lat_index,lon_index]
#

def indexing_data(min_lat, max_lat, min_lon, max_lon):
    # CREATE BAND1; using latitudes defined above
    data = fgc02_smooth[:, min_lat:max_lat, min_lon:max_lon]

    # see how the shape has changed
    # print(f"The shape of band1_ls after indexing is {np.shape(band1_ls)}")

    # and its still 3D
    # print(f"DIMENSIONS of band1_ls after indexing is {band1_ls.ndim}")
    # now let's average across the latitudes first

    # Average across LATITUDES
    data = np.ma.average(data, axis=1, keepdims=True)
    # print(f"After averaging across LATITUDES, the shape is {np.shape(band1_ls)}")

    # Average across LONGITUDES
    data = np.ma.average(data, axis=2, keepdims=True)
    # print(f"After averaging across LONGITUDES, the shape is {np.shape(band1_ls)}")
    data = data.tolist()

    return data


band1_ls = indexing_data(b1_index_min,b1_index_max, lon_index_min,lon_index_max)
band2_ls = indexing_data(b2_index_min,b2_index_max, lon_index_min,lon_index_max)
band3_ls = indexing_data(b3_index_min,b3_index_max, lon_index_min,lon_index_max)
band4_ls = indexing_data(b4_index_min,b4_index_max, lon_index_min,lon_index_max)
df = pd.DataFrame({"Landschutzer_time": time.tolist(),
                   "Band1":int(band1_ls),
                   "Band2":int(band2_ls),
                   "Band3":int(band3_ls),
                   "Band4":int(band4_ls)})


df['Decimal_date'] = (df['Landschutzer_time']/conversion)+2000
# df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/test.xlsx')
band1_ls = df['Band1'].rolling(dt).mean()
band2_ls = df['Band2'].rolling(dt).mean()
band3_ls = df['Band3'].rolling(dt).mean()
band4_ls = df['Band4'].rolling(dt).mean()

"""
Plot the data
"""
fig = plt.figure(figsize=(9, 9))
gs = gridspec.GridSpec(6, 4)
gs.update(wspace=.75, hspace=1)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.title(f"Chile Tree Ring Data, {b1_max} to {b1_min}", fontsize=11)
plt.plot(means_ch1['Decimal_date'], means_ch1['r2_diff_trend'], label='Tree Rings', color = a1)
plt.fill_between(means_ch1['Decimal_date'], (means_ch1['r2_diff_trend']+stds_ch1['r2_diff_trend']), (means_ch1['r2_diff_trend']-stds_ch1['r2_diff_trend']), alpha = 0.3, color = a1)

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.title(f"Chile Tree Ring Data, {b2_max} to {b2_min}", fontsize=11)
plt.plot(means_ch2['Decimal_date'], means_ch2['r2_diff_trend'], label='Tree Rings', color = a3)
plt.fill_between(means_ch2['Decimal_date'], (means_ch2['r2_diff_trend']+stds_ch2['r2_diff_trend']), (means_ch2['r2_diff_trend']-stds_ch2['r2_diff_trend']), alpha = 0.3, color = a3)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - Reference]', color='black', fontsize=11)

xtr_subsplot = fig.add_subplot(gs[4:6, 0:2])
plt.title(f"Chile Tree Ring Data, {b3_max} to {b3_min}", fontsize=11)
plt.plot(means_ch3['Decimal_date'], means_ch3['r2_diff_trend'], label='Tree Rings', color = a5)
plt.fill_between(means_ch3['Decimal_date'], (means_ch3['r2_diff_trend']+stds_ch3['r2_diff_trend']), (means_ch3['r2_diff_trend']-stds_ch3['r2_diff_trend']), alpha = 0.3, color = a5)

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.title(f"Landschutzer Model, {b1_max} to {b1_min}, 40W - 20W", fontsize=11)
plt.scatter(df['Decimal_date'], band1_ls)


xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
plt.scatter(df['Decimal_date'], band2_ls)
plt.title(f"Landschutzer Model, {b2_max} to {b2_min}, 40W - 20W", fontsize=11)
plt.ylabel('CO2 flux density smoothed: mol m^{-2} yr^{-1}', color='black', fontsize=11)

xtr_subsplot = fig.add_subplot(gs[4:6, 2:4])
plt.title(f"Landschutzer Model, {b3_max} to {b3_min}, 40W - 20W", fontsize=11)
plt.scatter(df['Decimal_date'], band3_ls)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/analysis6_1.png',
            dpi=300, bbox_inches="tight")

"""
Plot the data
"""
fig = plt.figure(figsize=(9, 9))
gs = gridspec.GridSpec(6, 4)
gs.update(wspace=.75, hspace=1)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.title(f"NZ Tree Ring Data, {b1_max} to {b1_min}", fontsize=11)
plt.plot(means_nz1['Landschutzer_time'], means_nz1['r2_diff_trend'], label='Tree Rings', color = a1)
plt.fill_between(means_nz1['Landschutzer_time'], (means_nz1['r2_diff_trend']+stds_nz1['r2_diff_trend']), (means_nz1['r2_diff_trend']-stds_nz1['r2_diff_trend']), alpha = 0.3, color = a1)

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.title(f"NZ Tree Ring Data, {b2_max} to {b2_min}", fontsize=11)
plt.plot(means_nz2['Landschutzer_time'], means_nz2['r2_diff_trend'], label='Tree Rings', color = a3)
plt.fill_between(means_nz2['Landschutzer_time'], (means_nz2['r2_diff_trend']+stds_nz2['r2_diff_trend']), (means_nz2['r2_diff_trend']-stds_nz2['r2_diff_trend']), alpha = 0.3, color = a3)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - Reference]', color='black', fontsize=11)

xtr_subsplot = fig.add_subplot(gs[4:6, 0:2])
plt.title(f"NZ Tree Ring Data, {b3_max} to {b3_min}", fontsize=11)
plt.plot(means_nz3['Landschutzer_time'], means_nz3['r2_diff_trend'], label='Tree Rings', color = a5)
plt.fill_between(means_nz3['Landschutzer_time'], (means_nz3['r2_diff_trend']+stds_nz3['r2_diff_trend']), (means_nz3['r2_diff_trend']-stds_nz3['r2_diff_trend']), alpha = 0.3, color = a5)

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.title(f"Landschutzer Model, {b1_max} to {b1_min}, 40W - 20W", fontsize=11)
plt.scatter(time, band1_ls)


xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
plt.scatter(time, band2_ls)
plt.title(f"Landschutzer Model, {b2_max} to {b2_min}, 40W - 20W", fontsize=11)
plt.ylabel('CO2 flux density smoothed: mol m^{-2} yr^{-1}', color='black', fontsize=11)

xtr_subsplot = fig.add_subplot(gs[4:6, 2:4])
plt.title(f"Landschutzer Model, {b3_max} to {b3_min}, 40W - 20W", fontsize=11)
plt.scatter(time, band3_ls)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/analysis6_2.png',
            dpi=300, bbox_inches="tight")

