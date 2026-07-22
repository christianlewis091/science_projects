import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import pandas as pd
import matplotlib.patches as mpatches

# SEE SOAR GLODAP FILES
df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_submission/Data_Files/STEP1_GLODAP_C14.csv')

# get rid of ghost points
df = df.loc[df['G2c14'] > -990]

# grab data in M Bowen's rectangle from her presentatino
df = df.loc[df['G2latitude'] < -61]
df = df.loc[((df['G2longitude'] >160) & (df['G2longitude'] < 200)) | ((df['G2longitude'] > -180 ) & (df['G2longitude'] < -140))] # gets left side
df.to_excel(rf"H:\Science\Current_Projects\07_Collaborations\M_Bowen\glodap_ross_sea.xlsx")


fig = plt.figure(figsize=(10, 8))

ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))

ax.set_extent(
    [-180, 180, -90, -55],   # lon_min, lon_max, lat_min, lat_max
    crs=ccrs.PlateCarree()
)

ax.add_feature(cf.OCEAN)
ax.add_feature(cf.LAND, edgecolor='black')
ax.gridlines()

# Melissa's Plot is from: 160–170°E, 70–76°S
# add the nitrate and 14C data
cmap_reversed = plt.cm.get_cmap('coolwarm_r')
latitudes_data = df['G2latitude'].values
longitudes_data = df['G2longitude'].values
c14 = df['G2c14'].values
sc = ax.scatter(
    longitudes_data,
    latitudes_data,
    c=c14,
    cmap=cmap_reversed, vmin=-150, vmax=150,
    transform=ccrs.PlateCarree())  # Data is in lat/lon format)

cb = plt.colorbar(sc, ax=ax, orientation='vertical', pad=0.05, label='DIC \u0394$^1$$^4$C (\u2030)')

plt.show()


