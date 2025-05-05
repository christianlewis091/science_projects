"""
This may become deprecated as I try to figure out ArcGIS for mapping
"""

"""
HIGH RES COASTLINE!
https://ctroupin.github.io/posts/2019-09-02-fine-coast/
"""

#
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import pandas as pd
#
# # grab data
# df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/data/raw/Sampling_Log.xlsx')
# sonne = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw/14C_samples_for_Christian_Lewis_GNS.xlsx', comment = '#')
# yam = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw/yamashita_2015.xlsx', comment = '#')
#
# # extract lat lons for Sonne and SFCS2405 cruises
# lat = df['Latitude_N_decimal'].values
# lon = df['Longitude_E_decimal'].values
# lat_s = sonne['Lat_corrected'].values
# lon_s = sonne['Lon'].values
# lat_y = yam['Latitude'].values
# lon_y = yam['Longitude'].values
#
# ax = plt.axes(projection=ccrs.PlateCarree())
# ax.set_extent((166.14, 167.89, -46.35, -44.31))
# ax.coastlines(resolution='10m',)
#
#
# sc = plt.scatter(lon, lat, transform=ccrs.PlateCarree(), label='SFCS2405')  # Data is in lat/lon format)
# sc2 = plt.scatter(lon_s, lat_s, transform=ccrs.PlateCarree(), label='S309', color='red')  # Data is in lat/lon format)
# sc3 = plt.scatter(lon_y, lat_y, transform=ccrs.PlateCarree(), label='Yamashita et al., (2015)', color='black')  # Data is in lat/lon format)
# plt.legend()
#
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/SFCS2405_locations_plus_309_plus_yamashita.png',
#             dpi=300, bbox_inches="tight")
# #
#
# """
# OLDER VERSION
# """
# resolutions = {"c": "crude",
#                "l": "low",
#                "i": "intermediate",
#                "h": "high",
#                "f": "full"}
#
# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cf
# import cartopy.io.shapereader as shpreader
# import matplotlib.colors as mcolors
# from cmcrameri import cm
# import pandas as pd
# import matplotlib.patches as mpatches
#
# # --- Zissou1 palette ---
# zissou1 = ['#3B9AB2', '#78B7C5', '#EBCC2A', '#E1AF00', '#F21A00']
# color_sfcs = cm.lajolla(0.7)  # Lighter tone of Roma palette
# color_sonne = cm.lajolla(0.3)  # Darker tone of Roma palette
#
# # --- Load data ---
# sfcs = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/data/raw/Sampling_Log.xlsx')
# sonne = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/data/raw/14C_samples_for_Christian_Lewis_GNS.xlsx', comment='#')
# sfcs = sfcs[(sfcs['Sample'] == 'DIC') | (sfcs['Sample'] == 'DIC Duplicate')]
#
#
# # --- Plot ---
# fig = plt.figure(figsize=(8, 8))
# ax1 = fig.add_subplot(projection=ccrs.PlateCarree())
#
# # Map extent for Fiordland
# minlat, maxlat = -46, -45
# nz_min_lon, nz_max_lon = 166.25, 167.5
# ax1.set_extent([nz_min_lon, nz_max_lon, minlat, maxlat], crs=ccrs.PlateCarree())
#
#
# # Add map features
# ax1.add_feature(cf.LAND, edgecolor='gray', zorder=1)
# ax1.add_feature(cf.OCEAN, zorder=0)
# ax1.coastlines(resolution='10m', linewidth=0.5, zorder=2)
# gl = ax1.gridlines(draw_labels=True, linewidth=0.3, color='gray')
# gl.top_labels = False
# gl.right_labels = False
#
# # Plot sample data
# ax1.scatter(sfcs['Longitude_E_decimal'], sfcs['Latitude_N_decimal'], color=color_sfcs, edgecolors='black', marker='o', label='SFCS2405, May 2024', zorder=3)
# ax1.scatter(sonne['Lon'], sonne['Lat_corrected'], edgecolors='black', color=color_sonne, marker='D', label='S309, February 2025', zorder=3)
#
# ax1.text(0.5, 0.5, 'final colors tbd, check stations when 14C is done', transform=ax1.transAxes,
#          fontsize=40, color='gray', alpha=0.5,
#          ha='center', va='center', rotation=30)
# ax1.legend()
# plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/FIG1_Main.png", dpi=300, bbox_inches="tight")
# plt.close()
#
# """Generate second map which will be the inset"""
# fig = plt.figure(figsize=(8, 8))
# ax1 = fig.add_subplot(projection=ccrs.PlateCarree())
# maxlat2 = -30
# minlat2 = -50
# nz_max_lon2 = 165
# nz_min_lon2 = 179
# ax1.set_extent([nz_min_lon2, nz_max_lon2, minlat2, maxlat2], crs=ccrs.PlateCarree())  # Set map extent
# ax1.add_feature(cf.OCEAN)
# ax1.add_feature(cf.LAND, edgecolor='gray')
#
# # Define rectangle properties
# lower_left_lon = nz_min_lon  # min longitude
# lower_left_lat = minlat   # min latitude
# width = nz_max_lon-nz_min_lon            # degrees of longitude
# height = maxlat-minlat           # degrees of latitude
#
# # Create rectangle
# rect = mpatches.Rectangle(
#     (lower_left_lon, lower_left_lat),  # (x, y)
#     width,
#     height,
#     linewidth=2,
#     edgecolor='red',
#     facecolor='none',  # transparent fill
#     transform=ccrs.PlateCarree()  # coordinate system of the rectangle
# )
#
# # Add rectangle to the map
# ax1.add_patch(rect)
#
# # Show the map
# plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/FIG1_inset.png", dpi=300, bbox_inches="tight")
# plt.close()
#
