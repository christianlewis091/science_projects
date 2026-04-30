import pandas as pd

dic = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\05_concatonate_DIC_data/DIC_JOINED_FINAL_V2.xlsx')
ctd = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output_V2/04_concatonate_CTD_data/ctd_cat.xlsx')

# I have to associate the CTD filenames with the Stations listed on DIC_joined_FINAL_V2
dic['FileName'] = 'EMPTY SO FAR'
dic.loc[(dic['Station'] == 'DUS020_01'), 'FileName'] = 'DUS020_01CTD'
dic.loc[(dic['Station'] == 'DUS023_01'), 'FileName'] = 'DUS023_01CTD'
dic.loc[(dic['Station'] == 'SFCS2405-DUS010-01'), 'FileName'] = 'DBT010_02CTD' # this is where the discrepancy in the original CTD data crops up. Three stations in Dusky were named DBT.
dic.loc[(dic['Station'] == 'SFCS2405-DUS011-01'), 'FileName'] = 'DBT011_02CTD' # this is where the discrepancy in the original CTD data crops up. Three stations in Dusky were named DBT.
dic.loc[(dic['Station'] == 'SFCS2405-DUS012-01'), 'FileName'] = 'DBT012_01CTD' # this is where the discrepancy in the original CTD data crops up. Three stations in Dusky were named DBT.

dic.loc[(dic['Station'] == 'SFCS2405-DBT001-01'), 'FileName'] = 'DBT001_01CTD' # this is where the discrepancy in the original CTD data crops up. Three stations in Dusky were named DBT.
dic.loc[(dic['Station'] == 'SFCS2405-DBT003-01'), 'FileName'] = 'DBT003_01CTD' # this is where the discrepancy in the original CTD data crops up. Three stations in Dusky were named DBT.
dic.loc[(dic['Station'] == 'SFCS2405-DBT006-01'), 'FileName'] = 'DBT006_01CTD' # this is where the discrepancy in the original CTD data crops up. Three stations in Dusky were named DBT.
dic.loc[(dic['Station'] == 'SFCS2405-DBT008-01'), 'FileName'] = 'DBT008_01CTD' # this is where the discrepancy in the original CTD data crops up. Three stations in Dusky were named DBT.

dic.loc[(dic['Station'] == 'SO309-59-18'), 'FileName'] = 'SO309-59-13_by_depth_1_m' # Naming discrepancy between Helen's excel file and the CTD data, but the lat lons match.
dic.loc[(dic['Station'] == 'SO309-46-17'), 'FileName'] = 'SO309-46-17_by_depth_1_m'
dic.loc[(dic['Station'] == 'SO309-53-1'), 'FileName'] = 'SO309-53-1_by_depth_1_m'

x36 = ['SFCS2505-DUS036-01CTD-6', 'SFCS2505-DUS036-01CTD-4', 'SFCS2505-DUS036-01CTD-1']
dic.loc[(dic['Station'].isin(x36)), 'FileName'] = 'sfcs2505_dus036_01ctd'

x30 = ['SFCS2505-DUS030-01CTD-12', 'SFCS2505-DUS030-01CTD-11', 'SFCS2505-DUS030-01CTD-7']
dic.loc[(dic['Station'].isin(x30)), 'FileName'] = 'sfcs2505_dus030_01ctd'

x28 = ['SFCS2505-DUS028-01CTD-12', 'SFCS2505-DUS028-01CTD-11', 'SFCS2505-DUS028-01CTD-7']
dic.loc[(dic['Station'].isin(x28)), 'FileName'] = 'sfcs2505_dus028_01ctd'

x21 = ['SFCS2505-DBT021-01CTD-11', 'SFCS2505-DBT021-01CTD-7', 'SFCS2505-DBT021-02CTD-12']
dic.loc[(dic['Station'].isin(x21)), 'FileName'] = 'sfcs2505_dbt021_01ctd'

x20 = ['SFCS2505-DBT020-01CTD-11', 'SFCS2505-DBT020-01CTD-12', 'SFCS2505-DBT020-01CTD-7']
dic.loc[(dic['Station'].isin(x20)), 'FileName'] = 'sfcs2505_dbt020_01ctd'

x19 = ['SFCS2505-DBT019-01CTD-12', 'SFCS2505-DBT019-01CTD-11', 'SFCS2505-DBT019-01CTD-7']
dic.loc[(dic['Station'].isin(x19)), 'FileName'] = 'sfcs2505_dbt019_01ctd'

ctd = ctd.rename(columns={"depSM":"Depth"})

















results = []

for i in range(len(dic)):
    row = dic.iloc[i]
    fname = row['FileName']
    depth = row['Depth']

    # subset CTD by filename
    subset = ctd[ctd['FileName'] == fname]

    if subset.empty:
        # append empty row with same columns as CTD
        results.append(pd.Series([None]*len(ctd.columns), index=ctd.columns))
        continue

    # find closest depth
    idx = (subset['Depth'] - depth).abs().idxmin()
    closest = subset.loc[idx]

    # store full CTD row
    results.append(closest)

# convert to dataframe
ctd_matched = pd.DataFrame(results).reset_index(drop=True)

# avoid overwriting columns
ctd_matched = ctd_matched.add_suffix('_ctd')

# combine with dic
final = pd.concat([dic.reset_index(drop=True), ctd_matched], axis=1)

"""
IMPORTANT INVESTIGATIONAL POINT:
There is a significant discrepancy between the bottle depth recorded on this bottle (“SFCS2505-DUS036-01CTD-1; bottle depth (m): 323.7.”), 
and the max/bottom depth at the site. 

The bottom depth for this site can be found here "H:\Science\Current_Projects/03_CCE_24_25/01_Fiordland/02_May_2025_Cruise\sfcs2505_gpkg_waterSamples_202508111535.xlsx",
which is a file Bob sent to me on Mon 11/08/2025 15:45, with that attached. DUS36 max depth is 234. 

The CTD data also have the same bottom depth: "C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data/raw\SFCS2505_CTD_raw\sfcs2505_dus036_01ctd.cnv"

I'll email Bob about it, but for now, I'll EDIT the BOTTLE DEPTH TO THE BOTTOM DEPTH...
"""
final.loc[(final['Depth'] == 323.7), 'Depth'] = 233

# lets tidy up the file a little bit:
# check that the values from the CTD raw files and the excel sheets I was given match
final['delta_depth'] = final['Depth'] - final['Depth_ctd']
final['delta_lat'] = final['Lat N'] - final['latitude_ctd']
final['delta_lon'] = final['Lon E'] - final['longitude_ctd']

final = final[['EXPOCODE','EXPOCODE_ctd',
         'Station', 'FileName_ctd',
         'Lat N', 'Lon E', 'latitude_ctd', 'longitude_ctd',
         'Bottom Depth',
         'Depth', 'Depth_ctd',
         'delta_depth', 'delta_lat', 'delta_lon',
         'sal00_ctd', 't090C_ctd', 'sbox0Mm/Kg_ctd',
         'Date (UTC)', 'Time (UTC)', 'UTC_ctd',
         'R_number', 'TW', 'TP',
         'F_corrected_normed',
         'F_corrected_normed_error', 'DELTA14C', 'DELTA14C_Error', 'delta13C_IRMS', 'delta13C_IRMS_Error',
         ]]

final.to_excel("C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/05part2_joinCTD_and_DIC14C/JOINED_DATA.xlsx")
