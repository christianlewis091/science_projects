import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np
from matplotlib.patches import Polygon
# from Basemap import basemap-data-hires
import seaborn as sns
import pandas as pd
import re
size1 = 90
size2 = 1.5*size1
colors2 = sns.color_palette("mako", 30)
colors2 = list(reversed(colors2))
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D']

df = pd.read_excel('C:/2024_Polaris_II/Sampling_Log.xlsx')
stns = np.unique(df['My Station Name'])

# we'll loop through the filenames and create a marker for each one
stn_names = np.unique(df['My Station Name'])

plt.figure(figsize=(10, 8))
maxlat = -45.0
minlat = -46
nz_max_lon = 167.25
nz_min_lon = 166.25
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h')
map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
map.drawmapboundary(fill_color="#DDEEFF")
map.drawcoastlines()

plt.text(167.1, -45.5, 'Doubtful S.', fontsize=12)
plt.text(167, -45.75, 'Dusky S.', fontsize=12)

lat = df['Latitude_N_decimal']
lon = df['Longitude_E_decimal']
x, y = map(lon, lat)
map.scatter(x, y, edgecolor='black', zorder=2, s=50, color='blue')

maxlat2 = -30
minlat2 = -50
nz_max_lon2 = 180
nz_min_lon2 = 160

# # Create the inset map
# ax = plt.gca()
# axin = ax.inset_axes([0.06, 0.65, 0.4, 0.4])  # [left, bottom, width, height]
# inset_map = Basemap(llcrnrlat=minlat2, urcrnrlat=maxlat2, llcrnrlon=nz_min_lon2, urcrnrlon=nz_max_lon2, resolution='h', ax=axin)
# inset_map.drawcoastlines()
# inset_map.drawcountries()
# inset_map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
# inset_map.drawmapboundary(fill_color="#DDEEFF")
# inset_map.drawcoastlines()
#
# inset_map.drawparallels(range(-90, 91, 5), labels=[1, 0, 0, 0], linewidth=0.1)
# inset_map.drawmeridians(range(-180, 181, 5), labels=[0, 0, 0, 1], linewidth=0.1)
#
# # Define polygon coordinates in the inset map's projection
# x1, y1 = inset_map(nz_min_lon, minlat)
# x2, y2 = inset_map(nz_min_lon, maxlat)
# x3, y3 = inset_map(nz_max_lon, minlat)
# x4, y4 = inset_map(nz_max_lon, maxlat)
#
# # Plot the polygon on the inset map
# poly = Polygon([(x2, y2), (x1, y1), (x3, y3), (x4, y4)], facecolor='blue', edgecolor='black', linewidth=1)
# axin.add_patch(poly)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/May_2024_Field_Actual/Fiordland_Sampling_noinset.png',
            dpi=300, bbox_inches="tight")


"""
Making a plot for cathy
"""

size1 = 90
size2 = 1.5*size1
colors2 = sns.color_palette("mako", 30)
colors2 = list(reversed(colors2))
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D']

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland/ANZIC.xlsx')
ex = df.loc[df['status'] == 'existing data']
prop = df.loc[df['status'] == 'proposed']

plt.figure(figsize=(10, 8))
maxlat = -45.0
minlat = -46
nz_max_lon = 167.25
nz_min_lon = 166.25
map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h')
map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
map.drawmapboundary(fill_color="#DDEEFF")
map.drawcoastlines()
plt.text(167.1, -45.5, 'Doubtful S.', fontsize=12)
plt.text(167, -45.75, 'Dusky S.', fontsize=12)

lat_ex = ex['Latitude']
lon_ex = ex['Longitude']
x_ex, y_ex = map(lon_ex, lat_ex)
map.scatter(x_ex, y_ex, edgecolor='black', zorder=2, s=50, color='blue', marker='o', label='Existing')

lat_prop = prop['Latitude']
lon_prop = prop['Longitude']
x_prop, y_prop = map(lon_prop, lat_prop)
map.scatter(x_prop, y_prop, edgecolor='black', zorder=2, s=50, color='red', marker='D', label='Proposed')

maxlat2 = -30
minlat2 = -50
nz_max_lon2 = 180
nz_min_lon2 = 160

# # Create the inset map
ax = plt.gca()
axin = ax.inset_axes([0.06, 0.65, 0.3, 0.3])  # [left, bottom, width, height]
inset_map = Basemap(llcrnrlat=minlat2, urcrnrlat=maxlat2, llcrnrlon=nz_min_lon2, urcrnrlon=nz_max_lon2, resolution='h', ax=axin)
inset_map.drawcoastlines()
inset_map.drawcountries()
inset_map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
inset_map.drawmapboundary(fill_color="#DDEEFF")
inset_map.drawcoastlines()

inset_map.drawparallels(range(-90, 91, 5), labels=[1, 0, 0, 0], linewidth=0.1)
inset_map.drawmeridians(range(-180, 181, 5), labels=[0, 0, 0, 1], linewidth=0.1)

# Define polygon coordinates in the inset map's projection
x1, y1 = inset_map(nz_min_lon, minlat)
x2, y2 = inset_map(nz_min_lon, maxlat)
x3, y3 = inset_map(nz_max_lon, minlat)
x4, y4 = inset_map(nz_max_lon, maxlat)

# Plot the polygon on the inset map
poly = Polygon([(x2, y2), (x1, y1), (x3, y3), (x4, y4)], facecolor='red', edgecolor='black', linewidth=1)
axin.add_patch(poly)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/May_2024_Field_Actual/Fiordland_Sampling_CAT.png',
            dpi=300, bbox_inches="tight")












































# plt.figure(figsize=(10, 8))
# maxlat = -45.0
# minlat = -46
# nz_max_lon = 167.25
# nz_min_lon = 166.25
# map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h')
# map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.1)
# map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.1)
# map.fillcontinents(color="mediumaquamarine", lake_color='#DDEEFF')
# map.drawmapboundary(fill_color="#DDEEFF")
# map.drawcoastlines()
#
#
# plt.text(167.1, -45.5, 'Doubtful S.', fontsize=12)
# plt.text(167, -45.75, 'Dusky S.', fontsize=12)
# #
# for i in range(0, len(stns)):
#     subdf = df.loc[df['My Station Name'] == stns[i]].reset_index(drop=True)
#
#     lat = subdf['Latitude_N_decimal']
#     lon = subdf['Longitude_E_decimal']
#     lat = lat[0]
#     lon = lon[0]
#     x, y = map(lon, lat)
#     map.scatter(x, y, color='blue', edgecolor='black', label='DIC only', s=size2, marker='^')
#
#
# # not all stations have DOC though, so I"m going to plot DOC overtop
# docs_df = df.loc[df['Sample'] == 'DOC']
# stns = np.unique(docs_df['My Station Name'])
# for i in range(0, len(stns)):
#     subdf = docs_df.loc[docs_df['My Station Name'] == stns[i]].reset_index(drop=True)
#     lat = subdf['Latitude_N_decimal']
#     lon = subdf['Longitude_E_decimal']
#     lat = lat[0]
#     lon = lon[0]
#
#     x, y = map(lon, lat)
#
#     map.scatter(x, y, color='yellow', edgecolor='black', label='DOC and DIC', s=size1, marker='o')
#
# print(df_cat.columns)
# stns = np.unique(df_cat['siteNumber'])
# for i in range(0, len(stns)):
#     subdf = df_cat.loc[df_cat['siteNumber'] == stns[i]].reset_index(drop=True)
#     lat = subdf['dropLatitude']
#     lon = subdf['dropLongitude']
#     lat = lat[0]
#     lon = lon[0]
#
#     x, y = map(lon, lat)
#
#     map.scatter(x, y, color='red', edgecolor='black', label='DOC and DIC', s=size1, marker='D')
#
#
# plt.savefig('C:/2024_Polaris_II/Map_actual_May29_2024_plus_cathys.png',
#             dpi=300, bbox_inches="tight")
#




