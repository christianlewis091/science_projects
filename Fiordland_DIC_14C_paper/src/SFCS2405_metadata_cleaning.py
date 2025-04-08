"""
April 8, 2025
This short script will merge the sampling log (lat, lon, notes) with the 14C data (output from RLIMS)
"""
import pandas as pd

df = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw/Sampling_Log.xlsx')

# just keep the important columns
df = df[['My Station Name', 'Cruise Station Name','Latitude_N_decimal','Longitude_E_decimal','Bottom Depth (m)','Depth','Sample','ID']]
# retain just the DIC samples for now (not thinking about SPE-DOC or DOC)
dic = df.loc[((df['Sample'] == 'DIC') | (df['Sample'] == 'DIC Duplicate'))]

tw3530 = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw//TW3530_export.xlsx')
tw3530 = tw3530.loc[tw3530['Samples::Sample Description'] == 'Fiordland DIC samples from SFCS2405'] # remove oxalics, kapunis, etc
print(tw3530.columns)
print(dic.columns)

df = dic.merge(tw3530, on='ID')

df.to_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate/SFCS2405_DIC.xlsx')