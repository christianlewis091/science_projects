"""
This short script will take the DIC 14C radiocarbon data and merge it
with the lat lon and other metadata from Helen for Sonne Cruise S309 in Fiordland
"""
import pandas as pd

# METADATA from HELEN
met = pd.read_excel(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw/14C_samples_for_Christian_Lewis_GNS.xlsx', comment='#')
# DIC 14C data from XCAMS
df = pd.read_excel(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw/Sonne_DIC_results.xlsx', sheet_name='sheet2')

df = met.merge(df, on='Sample ID')
df.to_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/S309_DIC_14C_FINAL.xlsx')




