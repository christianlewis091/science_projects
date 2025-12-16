import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# edited some column names to match up better
df1= pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2405_DIC_14C_FINAL.xlsx', comment='#')
df2= pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/S309_DIC_14C_FINAL.xlsx', comment='#', sheet_name='Cleaner')
df3= pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2505_DIC_14C_FINAL.xlsx', comment='#')
df1['EXPOCODE'] = 'SFCS2405'
df2['EXPOCODE'] = 'S309'
df3['EXPOCODE'] = 'SFCS2405'

df1 = df1[['Cruise Station Name',
           'Latitude_N_decimal', 'Longitude_E_decimal', 'Bottom Depth (m)',
           'Depth', 'Sample', 'ID', 'R_number', 'Job', 'wtgraph', 'TW',
           'TP',
           'Collection Decimal Date', 'Date Run', 'F_corrected_normed',
           'F_corrected_normed_error', 'Samples::Sample Description', 'DELTA14C',
           'DELTA14C_Error', 'delta13C_IRMS', 'delta13C_IRMS_Error','EXPOCODE']]

df1 = df1.rename(columns={"Latitude_N_decimal": "Lat N",
                          "Longitude_E_decimal": "Lon E",
                          'Bottom Depth (m)':"Bottom Depth",
                          'Depth':"Depth",
                          'Cruise Station Name':'Station',
                          })

df2 = df2[['Station', 'Site', 'Date (UTC)', 'Time (UTC)',
           'Lat N', 'Lon E', 'Niskin', 'Depth', 'Notes ', 'Sound',
           'Samples::Sample Description', 'TW', 'Date Run',
           'Description', 'Fraction dated', 'R_number', 'NZA', 'CRA', 'CRA error',
           'delta13C_IRMS', 'delta13C_IRMS_Error', 'd13C source',
           'F_corrected_normed', 'F_corrected_normed_error', 'Lab comments',
           'Pretreatment description', 'DELTA14C', 'DELTA14C_Error',
           'Collection date','EXPOCODE']]

df2 = df2.rename(columns={"NZA":"TP"})

df3 = df3[['delta13C_IRMS', 'delta13C_IRMS_Error', 'DELTA14C',
           'DELTA14C_Error', 'F_corrected_normed', 'F_corrected_normed_error',
           'ID', 'TP', 'TW', 'wtgraph', 'Samples::Sample ID', 'expedAcronym',
           'siteCode', 'siteNumber', 'dropNumber', 'dropLongitude',
           'dropLatitude', 'dropWaterDepth',
           'bottleDepth','Job::R','EXPOCODE']]
#
df3 = df3.rename(columns={"bottleDepth":"Depth",
                          "dropWaterDepth":"Bottom Depth",
                          'Samples::Sample ID':'Samples::Sample Description',
                          'Job::R':'R_number',
                          'dropLatitude':'Lat N',
                          'dropLongitude':'Lon E'})
df3['Station'] = df3['Samples::Sample Description']

df = pd.concat([df1, df2, df3], ignore_index=True)

df = df[['EXPOCODE', 'Station', 'Lat N', 'Lon E', 'Bottom Depth', 'Depth',
          'R_number','TW', 'TP',
          'F_corrected_normed', 'F_corrected_normed_error',
           'DELTA14C', 'DELTA14C_Error',
          'delta13C_IRMS', 'delta13C_IRMS_Error',
          'Date (UTC)', 'Time (UTC)']]

print(df.columns)

df.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\05_concatonate_DIC_data/DIC_JOINED_FINAL_V2.xlsx')
