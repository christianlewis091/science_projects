import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import cartopy.feature as cf
import pandas as pd

# Load the data
df = pd.read_excel(
    'C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/data/processed/TAN2502_DIC_14C_FINAL.xlsx',
    sheet_name='simplified', comment='#'
)
# add the SFCS2405 Data to see if DIC 14C is linear with latitudes
dic = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2405_DIC_14C_FINAL.xlsx', sheet_name='Sheet1')

# Normalize longitudes
df['Lon_deg'] = ((df['Lon_deg'] + 180) % 360) - 180

# Set up figure and gridspec
fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 2)  # Wider map

# Map on the left
ax0 = fig.add_subplot(gs[0], projection=ccrs.PlateCarree(central_longitude=180))
ax0.set_extent((161, 191, -80, -40))
ax0.add_feature(cf.GSHHSFeature(scale='l'), facecolor='lightgray')
sc = ax0.scatter(df['Lon_deg'], df['Lat_deg'], transform=ccrs.PlateCarree(), s=30, c='blue')
sc2 = ax0.scatter(dic['Longitude_E_decimal'], dic['Latitude_N_decimal'], transform=ccrs.PlateCarree(), s=30, c='red')

# Data plot on the right
ax1 = fig.add_subplot(gs[1])
ax1.errorbar(df['Lat_deg'], df['∆14C'], yerr=df['∆14C error'], color='blue', linestyle='None', marker='o')
ax1.set_xlabel("Latitude (°)")
ax1.set_ylabel("Δ14C")
ax1.errorbar(dic['Latitude_N_decimal'], dic['DELTA14C'], yerr = dic['DELTA14C_Error'], color='red', linestyle='None', marker='o')



plt.tight_layout()
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/TAN2502_DIC14C.png', dpi=300, bbox_inches="tight")
plt.show()

