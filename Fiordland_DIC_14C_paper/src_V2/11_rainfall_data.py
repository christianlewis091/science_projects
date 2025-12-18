import pandas as pd
import numpy as np
from datetime import datetime, timezone
import matplotlib.pyplot as plt

rain = pd.read_csv(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\raw\40987__Rain__daily.csv")
df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\05_concatonate_DIC_data/DIC_JOINED_FINAL_V2_edited.xlsx', comment='#')

rain['Date (UTC)'] = pd.to_datetime(rain['Observation time UTC'], utc=True)
df['Date (UTC)'] = pd.to_datetime(df['Date (UTC)'], utc=True)

# grab only april and may
rain2024 = rain.loc[((rain['Date (UTC)'] >= '2024-05-01') & (rain['Date (UTC)'] <  '2024-06-01'))]
df2024 = df.loc[((df['Date (UTC)'] >= '2024-05-01') & (df['Date (UTC)'] <  '2024-06-01'))]
# grab only april and may
rain2025 = rain.loc[((rain['Date (UTC)'] >= '2025-05-01') & (rain['Date (UTC)'] <  '2025-06-01'))]
df2025 = df.loc[((df['Date (UTC)'] >= '2025-05-01') & (df['Date (UTC)'] <  '2025-06-01'))]

fig, axs = plt.subplots(1, 2, figsize=(12, 8))  # 3 rows, 1 column
axs[0].plot(rain2024['Date (UTC)'], rain2024['Rainfall [mm]'])
for d in df2024['Date (UTC)']:
    axs[0].axvline(d, color='red', alpha=0.1, linewidth=1)

axs[1].plot(rain2025['Date (UTC)'], rain2025['Rainfall [mm]'])
for d in df2025['Date (UTC)']:
    axs[1].axvline(d, color='red', alpha=0.1, linewidth=1)

axs[0].set_ylim(0,275)
axs[1].set_ylim(0,275)
axs[0].tick_params(axis='x', rotation=45)
axs[1].tick_params(axis='x', rotation=45)
axs[0].set_ylabel('Rainfall [mm]')
plt.savefig(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\11_rainfall_data/rainfig.png",
            dpi=300, bbox_inches="tight")
