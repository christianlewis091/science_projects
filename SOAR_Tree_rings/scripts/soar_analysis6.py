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
from netcdf_example import *

# # fn = '/path/to/file.nc4'
# fn = 'H:/Science/Datasets/spco2_clim_1985-2015_MPI_SOM-FFN_v2016.nc'
# ds = nc.Dataset(fn)
#
# for var in ds.variables.values():
#     print(var)

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
test = fgc02_smooth[:,30,1]
print(len(test))
print(len(time))
# # lets say I want data from -60, that index is 30
#
time = time[:,1]
# print(test)
# print(lats)
# print(lats)
# print(test)
# print(time[:,1])
plt.scatter(time, test)
plt.show()