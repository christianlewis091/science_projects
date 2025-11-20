import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs

sun = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/S309_DIC_14C_FINAL.xlsx')
sfcs = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2405_DIC_14C_FINAL.xlsx')
sfcs25 = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw/sfcs2505_gpkg_waterSamples_202508111535.xlsx', comment='#')

# make clone df's to simplify things
sun2 = sun[['Lat_corrected','Lon','Station','Water depth (m)','∆14C','∆14C error','d13C','d13C error']]
sun2 = sun2.rename(columns={"Lat_corrected": "Lat", "Water depth (m)": "Depth","∆14C":"DELTA14C","∆14C error": "DELTA14C_Error"})
sun2['Cruise'] = 'Sonne'

sfcs2 = sfcs[['Longitude_E_decimal','Latitude_N_decimal','Cruise Station Name','DELTA14C','Depth', 'DELTA14C_Error','delta13C_IRMS','delta13C_IRMS_Error']]
sfcs2 = sfcs2.rename(columns={"Latitude_N_decimal": "Lat", "Longitude_E_decimal": "Lon", "Cruise Station Name": "Station"})
sfcs2['Cruise'] = 'SFCS'

# SFCS2505 hasn't been measured yet. I just want to see where the samples are relative to SFCS2405 and S309
sfcs25 = sfcs25.dropna(subset = 'waterAnalysisCode')
sfcs25 = sfcs25.loc[
    (sfcs25['waterAnalysisCode'] == 'DIC_C14') |
    (sfcs25['waterAnalysisCode'] == 'DOC')
    ]
sfcs25.to_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate/SFCS2505_filtered_for_CBL_samples.xlsx')


# Combine
plot_df = pd.concat([sun2, sfcs2])

# Ensure lat and lon columns are correct
# Adjust these if your actual column names are different
fig = px.scatter_geo(
    plot_df,
    lat='Lat',
    lon='Lon',
    text='Station',  # This shows on hover
    color='Cruise',
    projection='natural earth',
    scope='world',  # Will zoom in later
)

fig.update_geos(
    resolution=50,
    showcountries=True,
    showcoastlines=True,
    lonaxis_range=[166.14, 167.89],
    lataxis_range=[-46.35, -44.31],
)

# fig.update_layout(height=800, width=800, title="Station Map with Hover Labels")
# fig.show()

"""
So the map reveals that we should be comparing the following stations: 
DBT Mouth
sfcs2405-DBT008-01
SO309-53-1

DBT inside
SFCS2405-DBT006-01
SO309-46-17

Dusky Mouth
DUS023_01
SO309-59-18
"""

fig = plt.figure(figsize=(20, 5))  # Adjust size as needed
gs = gridspec.GridSpec(1, 4, width_ratios=[1, 1, 1,1], wspace=0.3)  # 1 row, 3 columns

ax1 = fig.add_subplot(gs[1])
ax2 = fig.add_subplot(gs[2])
ax3 = fig.add_subplot(gs[3])
ax4 = fig.add_subplot(gs[0], projection=ccrs.PlateCarree())
ax4.set_extent((166.4, 167.3, -46.0, -45.14))
ax4.coastlines(resolution='10m')

a = sfcs2.loc[sfcs2['Station'] == 'SFCS2405-DBT008-01']
b = sun2.loc[sun2['Station'] == 'SO309-53-1']
c = sfcs2.loc[sfcs2['Station'] == 'SFCS2405-DBT006-01']
d = sun2.loc[sun2['Station'] == 'SO309-46-17']
e = sfcs2.loc[sfcs2['Station'] == 'DUS023_01']
f = sun2.loc[sun2['Station'] == 'SO309-59-18']

ax1.errorbar(a['DELTA14C'], a['Depth'], xerr=a['DELTA14C_Error'], color='black', label='SFCS2405', marker='D')
ax1.errorbar(b['DELTA14C'], b['Depth'], xerr=b['DELTA14C_Error'], color='gray', label='S309', marker='o')
ax2.errorbar(c['DELTA14C'], c['Depth'], xerr=c['DELTA14C_Error'], color='black', marker='D')
ax2.errorbar(d['DELTA14C'], d['Depth'], xerr=d['DELTA14C_Error'], color='gray', marker='o')
ax3.errorbar(e['DELTA14C'], e['Depth'], xerr=e['DELTA14C_Error'], color='black', marker='D')
ax3.errorbar(f['DELTA14C'], f['Depth'], xerr=f['DELTA14C_Error'], color='gray', marker='o')

ax4.scatter(sfcs2['Lon'], sfcs2['Lat'], color='black', marker='D', alpha=0.5)
ax4.scatter(sun2['Lon'], sun2['Lat'], color='red', marker='o', alpha=0.5)
ax4.scatter(sfcs25['dropLongitude'], sfcs25['dropLatitude'], color='blue', marker='s', alpha=0.5)

# Example plot content
ax1.set_title("DBT Mouth")
ax2.set_title("DBT Interior")
ax3.set_title("DUS Mouth")

ax1.set_ylim(350,0)
ax2.set_ylim(350,0)
ax3.set_ylim(350,0)

ax1.set_xlim(20,35)
ax2.set_xlim(20,35)
ax3.set_xlim(20,35)

ax1.legend()
plt.tight_layout()
plt.show()
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/S309_SFCS2405_DIC_comparison.png', dpi=300, bbox_inches="tight")
plt.close()


"""
Is there any discrepancies with the 13C data overall??
"""
# read in dave's data
dave = pd.read_csv('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw/2405_d13C_ForCL.csv')
plt.errorbar(sun2['d13C'], sun2['Depth'], xerr=sun2['d13C error'], marker='o', linestyle='', label='S309', color='gray')
plt.errorbar(sfcs2['delta13C_IRMS'], sfcs2['Depth'], xerr=sfcs2['delta13C_IRMS_Error'], marker='D', color='black', label='SFCS2405', linestyle='')
plt.scatter(dave['Mean_d13C'], dave['Depth'], color='rosybrown', label='SFCS2405_stanford_comparison', marker='X')
plt.ylim(300,0)
plt.legend()
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/S309_SFCS2405_Mucc_13C_comparison.png', dpi=300, bbox_inches="tight")
plt.close()







