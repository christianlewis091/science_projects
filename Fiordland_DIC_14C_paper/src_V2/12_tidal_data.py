"""
https://tides.niwa.co.nz/?startDate=2025-05-01&numberOfDays=30&interval=10&latitude=-44.867&longitude=167.367

"""

import pandas as pd
import numpy as np
from datetime import datetime, timezone
import matplotlib.pyplot as plt

t2024 = pd.read_csv(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\raw\george_sound_tides_May2024.csv", comment='#')
t2025 = pd.read_csv(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\raw\george_sound_tides_May2025.csv", comment='#')
df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\05_concatonate_DIC_data/DIC_JOINED_FINAL_V2_edited.xlsx', comment='#')

df2024 = df.loc[((df['Date (UTC)'] >= '2024-05-01') & (df['Date (UTC)'] <  '2024-06-01'))]
df2025 = df.loc[((df['Date (UTC)'] >= '2025-05-01') & (df['Date (UTC)'] <  '2025-06-01'))]

t2024['TIME'] = pd.to_datetime(t2024['TIME'], utc=True)
t2025['TIME'] = pd.to_datetime(t2025['TIME'], utc=True)

fig, axs = plt.subplots(1, 2, figsize=(12, 8))  # 3 rows, 1 column\

axs[0].plot(t2024['TIME'], t2024['VALUE'])

for d in df2024['Date (UTC)']:
    axs[0].axvline(d, color='red', alpha=0.1, linewidth=1)

axs[1].plot(t2025['TIME'], t2025['VALUE'])

for d in df2025['Date (UTC)']:
    axs[1].axvline(d, color='red', alpha=0.1, linewidth=1)

axs[0].tick_params(axis='x', rotation=45)
axs[1].tick_params(axis='x', rotation=45)
axs[0].set_ylabel('Rainfall [mm]')
plt.savefig(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\12_tide_data/tidefig.png",
            dpi=300, bbox_inches="tight")
