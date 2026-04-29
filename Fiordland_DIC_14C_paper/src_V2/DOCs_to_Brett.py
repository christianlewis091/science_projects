import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_excel(r"H:\Science\Current_Projects\03_CCE_24_25\MY_SAMPLES_DATABASE.xlsx", comment='#')

a = df.loc[((df['Cruise'] == 'SFCS2511') & (df['Sample Type'] == 'DOC'))]

print(np.unique(a['Station']))

dusstn = ['DUS056-01CTD','DUS058-01CTD', 'DUS060-02CTD', 'DUS065-01CTD']
dbtstn = ['DBT043-02CTD', 'DBT051-01CTD', 'DBT053-01CTD', 'DBT053-02CTD']

b_dus = df.loc[((df['Comment'] == 'Going to Brett in March 2026 Trip') & (df['Station'].isin(dusstn)))]
b_dbt = df.loc[((df['Comment'] == 'Going to Brett in March 2026 Trip') & (df['Station'].isin(dbtstn)))]

dus = a.loc[a['Station'].isin(dusstn)]
dbt = a.loc[a['Station'].isin(dbtstn)]

siz = 50

fig, axes = plt.subplots(1, 2, figsize=(10, 6), sharey=True)

# --- Dusky Sound ---
axes[0].scatter(dus['Lon'], dus['Depth'], marker='o', alpha=0.5, s=siz)
axes[0].scatter(b_dus['Lon'], b_dus['Depth'], marker='x', alpha=0.5, s=siz, color='red')
axes[0].set_title('Dusky Sound')
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Depth (m)')
axes[0].set_ylim(400, 0)

# --- Doubtful Sound ---
axes[1].scatter(dbt['Lon'], dbt['Depth'], marker='o', alpha=0.5, s=siz)
axes[1].scatter(b_dbt['Lon'], b_dbt['Depth'], marker='x', alpha=0.5, s=siz, color='red')
axes[1].set_title('Doubtful Sound')
axes[1].set_xlabel('Longitude')
axes[1].set_ylim(400, 0)

# Show the map
plt.savefig(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\09_Main_Map_Figure/DOCs_4_BRETT.png", dpi=300, bbox_inches="tight")
plt.close()
