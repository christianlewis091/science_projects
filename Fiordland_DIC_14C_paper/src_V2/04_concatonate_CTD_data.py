"""
Concatonate the CTD data and make sure columns match

"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nzgeom.coastlines
from cmcrameri import cm
import gsw
import matplotlib.gridspec as gridspec

"""
i have data from three cruises all with different column headers in the ctd files: 
S309 ctd oxygen data is in: 'sbox0Mm/Kg', 'sbox1Mm/kg', 'sbeox0PS', 'sboeox1PS' 
SFCS2405 is in 'Sbeox0Mg/L', 
SFCS2505 is in 'sbox0Mm/Kg', 'sbeox0ML/L',

We want them all to be in mmol/kg, which we have for S309 and SFCS2505, but not SFCS2405, but we can do that by converting from g-> mol
"""
"""
SFCS2405
"""
# READ IN SFCS2405 DATA,
sfcs2405_ctd = pd.read_csv(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2405_CTD_DATA_FINAL.csv')
sfcs2405_ctd = sfcs2405_ctd.rename(columns={'Sal00':'sal00', 'T090C':'t090C','DepSM':'depSM','Lat':'latitude','Lon':'longitude'})
# Convert oxygen to mm/kg
sfcs2405_ctd['sbox0Mm/Kg'] = sfcs2405_ctd['Sbeox0Mg/L']*(1/32)*1000 # TODO why do i need this factor of 1000 in order to get values to match?????
sfcs2405_ctd = sfcs2405_ctd[['FileName', 'latitude','longitude', 'depSM', 'sal00','t090C','sbox0Mm/Kg']]
sfcs2405_ctd['EXPOCODE'] = 'SFCS2405'

# Only keep my stations
cruise1 = ['DBT001_01CTD','DBT003_01CTD', 'DBT006_01CTD', 'DBT008_01CTD',
           'DBT010_02CTD', 'DBT011_02CTD', 'DBT012_01CTD', 'DUS020_01CTD',
           'DUS023_01CTD']
sfcs2405_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'].isin(cruise1)]


"""
S309 CTD 
"""
# READ IN SONNE DATA AND GRAB IMPORTANT VARS
sonne_ctd = pd.read_excel(f"C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\s309_step3\Concatonated_CTD_SONNE.xlsx")
sonne_ctd = sonne_ctd[['FileName', 'latitude','longitude','depSM','sal00','t090C', 'sbox0Mm/Kg']]

# Only keep my stations
cruise2 = ['SO309-46-17_by_depth_1_m', 'SO309-53-1_by_depth_1_m', 'SO309-59-13_by_depth_1_m']
sonne_ctd = sonne_ctd.loc[sonne_ctd['FileName'].isin(cruise2)]
sonne_ctd['EXPOCODE'] = 'S309'
"""
SFCS2505
"""
# 2505 has depSM, sal00, t090C
sfcs2505_ctd = pd.read_csv(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2505_CTD_DATA_FINAL.csv')
sfcs2505_ctd = sfcs2505_ctd.rename(columns={'dropLatitude':'latitude','dropLongitude':'longitude'})
sfcs2505_ctd = sfcs2505_ctd[['FileName', 'latitude','longitude','depSM','sal00','t090C', 'sbox0Mm/Kg']]
sfcs2505_ctd['EXPOCODE'] = 'SFCS2505'
# Only keep my stations
cruise3 = ['sfcs2505_dbt019_01ctd','sfcs2505_dbt020_01ctd', 'sfcs2505_dbt021_01ctd',
           'sfcs2505_dus028_01ctd', 'sfcs2505_dus030_01ctd', 'sfcs2505_dus036_01ctd']

sfcs2505_ctd  = sfcs2505_ctd .loc[sfcs2505_ctd ['FileName'].isin(cruise3)]

ctd_cat = pd.concat([sonne_ctd, sfcs2405_ctd, sfcs2505_ctd])
ctd_cat.to_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output_V2/04_concatonate_CTD_data/ctd_cat.xlsx')
