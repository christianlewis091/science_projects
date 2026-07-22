import pandas as pd
import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

rain = pd.read_csv(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\raw\40987__Rain__daily.csv") # rain is from Milfod Sound! Not great...
t2024 = pd.read_csv(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\raw\george_sound_tides_May2024.csv", comment='#') # Tides are from George Sound....also not ideal
tso9 = pd.read_csv(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\raw\george_sound_tides_Jan2025.csv", comment='#') 
print(tso9.columns)

t2025 = pd.read_csv(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\raw\george_sound_tides_May2025.csv", comment='#')
df = pd.read_excel("C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/13_AOU_plot/JOINED_DATA_wAOU.xlsx")
# fix the datetimes for S309, helped by ChatGPT
df['UTC_ctd'] = pd.to_datetime(df['UTC_ctd'], format='mixed', dayfirst=True, utc=True)
# fix the datetimes for the tides
t2024['TIME'] = pd.to_datetime(t2024['TIME'], utc=True)
t2025['TIME'] = pd.to_datetime(t2025['TIME'], utc=True)
tso9['TIME'] = pd.to_datetime(tso9['TIME'], utc=True)

rain['Date (UTC)'] = pd.to_datetime(rain['Observation time UTC'], utc=True)
df['Date (UTC)'] = pd.to_datetime(df['UTC_ctd'], utc=True)


sfcs24 = df.loc[df['EXPOCODE']=='SFCS2405']
s309 = df.loc[df['EXPOCODE']=='S309']
sfcs25 = df.loc[df['EXPOCODE']=='SFCS2505']

fig, axs = plt.subplots(2, 3, figsize=(9,5.5))

c1 = "#0072B2"
c2 = "#D55E00"
c3 = "#009E73"

# First set the code to mark the UTC's for sampling times on each of the 6 graphs

for d in sfcs24['Date (UTC)']:
    axs[0,0].axvline(d, color=c1, alpha=0.1, linewidth=1)

for d in s309['Date (UTC)']:
    axs[0,1].axvline(d, color=c2, alpha=0.1, linewidth=1)

for d in sfcs25['Date (UTC)']:
    axs[0,2].axvline(d, color=c3, alpha=0.1, linewidth=1)

for d in sfcs24['Date (UTC)']:
    axs[1,0].axvline(d, color=c1, alpha=0.1, linewidth=1)

for d in s309['Date (UTC)']:
    axs[1,1].axvline(d, color=c2, alpha=0.1, linewidth=1)

for d in sfcs25['Date (UTC)']:
    axs[1,2].axvline(d, color=c3, alpha=0.1, linewidth=1)

# add the rainfall data to the top 3.
rain2024 = rain.loc[((rain['Date (UTC)'] >= '2024-05-01') & (rain['Date (UTC)'] <  '2024-06-01'))]
axs[0,0].plot(rain2024['Date (UTC)'], rain2024['Rainfall [mm]'])

rain2025 = rain.loc[((rain['Date (UTC)'] >= '2025-01-15') & (rain['Date (UTC)'] <  '2025-02-15'))]
axs[0,1].plot(rain2025['Date (UTC)'], rain2025['Rainfall [mm]'])

rain2025_2 = rain.loc[((rain['Date (UTC)'] >= '2025-05-01') & (rain['Date (UTC)'] <  '2025-06-01'))]
axs[0,2].plot(rain2025_2['Date (UTC)'], rain2025_2['Rainfall [mm]'])
# set top 3 maximum's to match max rain
axs[0,0].set_ylim(0,200)
axs[0,1].set_ylim(0,200)
axs[0,2].set_ylim(0,200)

# plot tides
axs[1,0].plot(t2024['TIME'], t2024['VALUE'])
axs[1,1].plot(tso9['TIME'], tso9['VALUE'])
axs[1,2].plot(t2025['TIME'], t2025['VALUE'])

# set X-limits for rain
axs[0,0].set_xlim(pd.Timestamp('2024-05-01', tz='UTC'), pd.Timestamp('2024-06-01', tz='UTC'))
axs[0,1].set_xlim(pd.Timestamp('2025-01-15', tz='UTC'), pd.Timestamp('2025-02-15', tz='UTC'))
axs[0,2].set_xlim(pd.Timestamp('2025-05-01', tz='UTC'), pd.Timestamp('2025-06-01', tz='UTC'))

# set X-limits for tides
axs[1,0].set_xlim(pd.Timestamp('2024-05-25', tz='UTC'), pd.Timestamp('2024-05-31', tz='UTC'))
axs[1,1].set_xlim(pd.Timestamp('2025-01-26', tz='UTC'), pd.Timestamp('2025-01-31', tz='UTC'))
axs[1,2].set_xlim(pd.Timestamp('2025-05-22', tz='UTC'), pd.Timestamp('2025-05-27', tz='UTC'))

axs[0,0].set_title('SFCS2405')
axs[0,1].set_title('S309')
axs[0,2].set_title('SCFS2505')

date_fmt = mdates.DateFormatter('%b %d')

for ax in axs.flat:
    ax.xaxis.set_major_formatter(date_fmt)
for ax in axs.flat:
    ax.tick_params(axis='x', rotation=60)
# for ax in axs[0,:]:
#     ax.tick_params(axis='x', labelbottom=False)

# plt.show()
plt.savefig(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\11_rainfall_data/rainfig.png",
            dpi=300, bbox_inches="tight")


"""
SOME SUMMARY COMMENTS
"""

rain2025_2 = rain.loc[((rain['Date (UTC)'] >= '2025-05-01') & (rain['Date (UTC)'] <  '2025-05-23'))]
rain2025_2_2 = rain.loc[((rain['Date (UTC)'] >= '2025-05-23') & (rain['Date (UTC)'] <  '2025-05-27'))]

total_2025_2 = np.sum(rain2025_2['Rainfall [mm]'])
total_2025_2_2 = np.sum(rain2025_2_2['Rainfall [mm]'])

rain2024 = rain.loc[((rain['Date (UTC)'] >= '2024-05-01') & (rain['Date (UTC)'] <  '2024-06-01'))]
axs[0,0].plot(rain2024['Date (UTC)'], rain2024['Rainfall [mm]'])

print(f"Between May 1, 2025 and the beginning of sampling (May 23, 2025) there was {total_2025_2}mm of rainfall.")
print(f"And after sampling begun, during the last three stations, there was another pulse of {total_2025_2_2}mm.")

rain2024 = rain.loc[((rain['Date (UTC)'] >= '2024-05-01') & (rain['Date (UTC)'] <  '2024-05-27'))]
total_2024 = np.sum(rain2024['Rainfall [mm]'])
rain2024_2 = rain.loc[((rain['Date (UTC)'] >= '2024-05-27') & (rain['Date (UTC)'] <  '2024-05-31'))]
total_2024_2 = np.sum(rain2024_2['Rainfall [mm]'])

print(f"The month beore SFCS2405 sampling, there was {total_2024}mm, and during had {total_2024_2}")