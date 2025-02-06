"""
February 2, 2025
I want to make a nice map that shows the overlap between my Polaris II trip (SFCS2405) and the samples Helen took
on the RV Sonne S309.

But I'm going to try to us Tim's NZ coastline python package. Can't use TIM's because i'm using python 3.9

"""

"""
HIGH RES COASTLINE!
https://ctroupin.github.io/posts/2019-09-02-fine-coast/
"""
resolutions = {"c": "crude",
               "l": "low",
               "i": "intermediate",
               "h": "high",
               "f": "full"}

from cmcrameri import cm
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import pandas as pd
import numpy as np
import cartopy.feature as cf

cmcrameri_colormaps = ["batlow",
                       "batlowW",
                       "batlowK",
                       "glasgow",
                       "lipari",
                       "navia",
                       "hawaii",
                       "buda",
                       "imola",
                       "oslo",
                       "grayC",
                       "nuuk",
                       "devon",
                       "lajolla",
                       "bamako",
                       "davos",
                       "bilbao",
                       "lapaz",
                       "acton",
                       "turku",
                       "tokyo"]

cmap=cm.batlow
color_sfcs = cm.batlow(0.2)  # Lighter shade from batlow
color_s309 = cm.batlow(0.8)  # Darker shade from batlow

df = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/01_Fiordland/01_May_2024_Cruise/2024_Polaris_II/Sampling_Log.xlsx', skiprows=1)
sonne = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/S309_RV_Sonne_DIC/14C_samples_for_Christian_Lewis_GNS.xlsx')

lat = df['Latitude_N_decimal'].values
lon = df['Longitude_E_decimal'].values

lat_s = sonne['Lat'].values
lat_s = lat_s*-1
lon_s = sonne['Lon'].values


ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent((166.3, 167.25, -46.0, -45))
coast = cf.GSHHSFeature(scale="full")
ax.add_feature(coast)

ax.add_feature(cf.OCEAN, color='lightblue')  # Ocean background
ax.add_feature(cf.LAND, color='whitesmoke')  # Land background

sc = ax.scatter(lon, lat, color=color_sfcs, transform=ccrs.PlateCarree(), label='SFCS2405', marker='o')
sc2 = ax.scatter(lon_s, lat_s, color=color_s309, transform=ccrs.PlateCarree(), label='S309', marker='D')

plt.legend()
plt.savefig('H:/Science/Current_Projects/03_CCE_24_25/S309_RV_Sonne_DIC/SFCS2405_vs_S309SonneLocations.png',
            dpi=300, bbox_inches="tight")
