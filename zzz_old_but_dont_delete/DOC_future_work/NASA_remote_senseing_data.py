from netCDF4 import Dataset as NetCDFFile
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Function to summarize netcdf files for me
# def summarize_nc_file(file_path):
#     # Open the NetCDF file
#     with nc.Dataset(file_path, 'r') as ds:
#         # Print basic information
#         print("NetCDF File Summary:")
#         print(f"File Path: {file_path}")
#         print(f"Number of Dimensions: {len(ds.dimensions)}")
#         print(f"Number of Variables: {len(ds.variables)}")
#         print(f"Global Attributes: {ds.__dict__}")
#
#         # Print information about dimensions
#         print("\nDimensions:")
#         for dim_name, dim in ds.dimensions.items():
#             print(f"{dim_name}: {len(dim)}")
#
#         # Print information about variables
#         print("\nVariables:")
#         for var_name, var in ds.variables.items():
#             print(f"{var_name}: {var.shape} - {var.dtype}")
#             print(f"  Attributes: {var.__dict__}")


file_path = r'H:\Science\Datasets\NASA\mon201512.R2017.nc4'

nc = NetCDFFile(file_path)
lats = nc.variables['lat'][:]
lons = nc.variables['lon'][:]
tot = nc.variables['tot'][:]
tot_units = nc.variables['tot'].units
nc.close()

maxlat = -30
minlat = -60
nz_max_lon = 185
nz_min_lon = 155
m = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon)

# Because our lon and lat variables are 1D,
# use meshgrid to create 2D arrays
# Not necessary if coordinates are already in 2D arrays.
lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

# Plot
x = np.transpose(np.squeeze(tot))
cs = m.pcolormesh(xi, yi, x, cmap='viridis', shading='auto')
# cs = m.pcolor(xi,yi,np.squeeze(tot))

# Add Grid Lines
m.drawparallels(np.arange(-39., 81., 10.), labels=[1,0,0,0], fontsize=10)
m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()

# Add Colorbar
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(tot_units)

# Add Title
plt.title('Test')

plt.show()