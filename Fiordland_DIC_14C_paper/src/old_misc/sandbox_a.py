import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs

sun = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/S309_DIC_14C_FINAL.xlsx')
sfcs = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2405_DIC_14C_FINAL.xlsx')
sfcs25 = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate/SFCS2505_filtered_for_CBL_samples.xlsx', comment='#', sheet_name='Sheet2')

# make clone df's to simplify things
sun2 = sun[['Lat_corrected','Lon','Station','Water depth (m)','∆14C','∆14C error','d13C','d13C error']]
sun2 = sun2.rename(columns={"Lat_corrected": "Lat", "Water depth (m)": "Depth","∆14C":"DELTA14C","∆14C error": "DELTA14C_Error"})
sun2['Cruise'] = 'Sonne'

sfcs2 = sfcs[['Longitude_E_decimal','Latitude_N_decimal','Cruise Station Name','DELTA14C','Depth', 'DELTA14C_Error','delta13C_IRMS','delta13C_IRMS_Error']]
sfcs2 = sfcs2.rename(columns={"Latitude_N_decimal": "Lat", "Longitude_E_decimal": "Lon", "Cruise Station Name": "Station", 'delta13C_IRMS':'d13C', 'delta13C_IRMS_Error':'d13C error'})
sfcs2['Cruise'] = 'SFCS2405'

# SFCS2505 hasn't been measured yet. I just want to see where the samples are relative to SFCS2405 and S309
sfcs25 = sfcs25.dropna(subset = 'waterAnalysisCode')
# sfcs25 = sfcs25.loc[(sfcs25['waterAnalysisCode'] == 'DIC_C14') | (sfcs25['waterAnalysisCode'] == 'DOC')]
sfcs25 = sfcs25[["dropLatitude", "dropLongitude", "bottleDepth", "expedAcronym"]]
sfcs25 = sfcs25.rename(columns={"dropLatitude": "Lat", "bottleDepth": "Depth","dropLongitude":"Lon","expedAcronym":'Cruise'})

# Combine
plot_df = pd.concat([sun2, sfcs2])
plot_df = pd.concat([plot_df, sfcs25])
# plot_df.to_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate/sandbox_a.xlsx')

# Make depth positive downwards
plot_df["Depth_positive"] = -plot_df["Depth"]

# Plot
fig = px.scatter_3d(
    plot_df,
    x="Lon",
    y="Lat",
    z="Depth_positive",
    color="Cruise",
    symbol="Cruise",  # helps distinguish overlapping points
    hover_data=["Station", "Depth", "DELTA14C"],
    title="Sample Locations by Cruise",
)

fig.update_layout(scene=dict(zaxis_title="Depth (m, down)"))
fig.show()