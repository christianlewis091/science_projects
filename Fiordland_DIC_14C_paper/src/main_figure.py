
"""
Main figures
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nzgeom.coastlines
from cmcrameri import cm
import gsw
import matplotlib.gridspec as gridspec

df = pd.read_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/DIC_JOINED_FINAL_EDITED.xlsx', sheet_name='for_paper')

sonne_ctd = pd.read_excel(f'H:\Science\Datasets\Fiordland\RVSONNE\STEP3/Concatonated_CTD_SONNE.xlsx')
sfcs2405_ctd = pd.read_excel('H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4/mystations.xlsx')
sfcs2505_ctd = pd.read_csv(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2505_CTD_DATA_FINAL.csv')

"""
i have data from three cruises all with different column headers in the ctd files: 
S309 ctd oxygen data is in: 'sbox0Mm/Kg', 'sbox1Mm/kg', 'sbeox0PS', 'sboeox1PS' 
SFCS2405 is in 'Sbeox0Mg/L', 
SFCS2505 is in 'sbox0Mm/Kg', 'sbeox0ML/L',

We want them all to be in mmol/kg, which we have for S309 and SFCS2505, but not SFCS2405, but we can do that by converting from g-> mol
"""
sfcs2405_ctd['sbox0Mm/Kg'] = sfcs2405_ctd['Sbeox0Mg/L']*(1/32)*1000 # TODO why do i need this factor of 1000 in order to get values to match?????
sfcs2405_ctd['pt'] = gsw.conversions.pt_from_t(sfcs2405_ctd['Sal00'],sfcs2405_ctd['T090C'], sfcs2405_ctd['DepSM'],0)
sonne_ctd['pt'] = gsw.conversions.pt_from_t(sonne_ctd['sal00'],sonne_ctd['t090C'], sonne_ctd['depSM'],0)
sfcs2505_ctd['pt'] = gsw.conversions.pt_from_t(sfcs2405_ctd['Sal00'],sfcs2405_ctd['T090C'], sfcs2405_ctd['DepSM'],0)

dus = df.loc[df['Site'] == 'Dusky']
dbt = df.loc[df['Site'] == 'Doubtful']
# print(dus)

# ability to change transparecny
a1 = 1
a2 = 1
a3 = 1

cmap = cm.vik  # <-- or whichever scheme you want
colors = cmap(np.linspace(0.1, 0.4, 3))

c1 = '#0072B2'
c2 = '#D55E00'
c3 = '#009E73'

m1 = 'o'
m2 = 'D'
m3 = 'x'

plt.close()
fig, axs = plt.subplots(5, 4, figsize=(20, 20))  # 3 rows, 1 column

map1 =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.6, -45.5, 167.2, -45.2))
map2 =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.8, 167.0, -45.7))
map1.plot(ax=axs[0,0], color="lightgray")
map2.plot(ax=axs[0,2], color="lightgray")

"""
PLOT THE MAPS
"""

siz = 50

sfcs2405 = dbt.loc[(dbt['Expedition'] == 'SFCS2405')]
s309 = dbt.loc[(dbt['Expedition'] == 'S309')]
sfcs2505 = dbt.loc[(dbt['Expedition'] == 'SFCS2505')]

axs[0, 0].scatter(sfcs2405['Lon E'], sfcs2405['Lat N'], color=c1, marker=m1, label='SFCS2405, May 2024', alpha=0.5, s=siz)
axs[0, 0].scatter(s309['Lon E'], s309['Lat N'], color=c2, marker=m2, label='S309, January 2025', alpha=0.5, s=siz)
axs[0, 0].scatter(sfcs2505['Lon E'],sfcs2505['Lat N'], color=c3, marker=m3, label='SFCS2505, May 2025', alpha=0.5, s=siz)

sfcs2405 = dus.loc[(dus['Expedition'] == 'SFCS2405')]
s309 = dus.loc[(dus['Expedition'] == 'S309')]
sfcs2505 = dus.loc[(dus['Expedition'] == 'SFCS2505')]

axs[0, 2].scatter(sfcs2405['Lon E'], sfcs2405['Lat N'], color=c1, marker=m1, label='SFCS2405, May 2024', alpha=0.5, s=siz)
axs[0, 2].scatter(s309['Lon E'], s309['Lat N'], color=c2, marker=m2, label='S309, January 2025', alpha=0.5, s=siz)
axs[0, 2].scatter(sfcs2505['Lon E'],sfcs2505['Lat N'], color=c3, marker=m3, label='SFCS2505, May 2025', alpha=0.5, s=siz)


plt.legend()

"""
GROUP 1, DEEP COVE
"""
dbt001 = df.loc[df['Station'] == 'DBT001']
dbt021 = df.loc[df['Station'] == 'DBT021']

dbt001_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT001_01CTD']
dbt021_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dbt021_01ctd']

axs[1,0].errorbar(dbt001['∆14C'], dbt001['Depth'], xerr=dbt001['∆14C error'], marker=m1, color=c1, label='DBT001', alpha=a1)
axs[1,0].errorbar(dbt021['∆14C'], dbt021['Depth'], xerr=dbt021['∆14C error'], marker=m3, color=c3, label='DBT021', alpha=a1)

axs[1,1].scatter(dbt001_ctd['T090C'], dbt001_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[1,1].scatter(dbt021_ctd['t090C'], dbt021_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.


"""
GROUP 2, DEEP COVE
"""
dbt003 = df.loc[df['Station'] == 'DBT003']
dbt003_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT003_01CTD']

axs[2,0].errorbar(dbt003['∆14C'], dbt003['Depth'], xerr=dbt003['∆14C error'], marker=m1, color=c1, label='DBT003', alpha=a1)
axs[2,1].scatter(dbt003_ctd['T090C'], dbt003_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.

"""
GROUP 3, Malaspina Reach
"""
dbt006 = df.loc[df['Station'] == 'DBT006']
SO30946 = df.loc[df['Station'] == 'SO309-46']
dbt020 = df.loc[df['Station'] == 'DBT020']

dbt006_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT006_01CTD']
so30946_ctd = sonne_ctd.loc[sonne_ctd['FileName'] == 'SO309-46-17_by_depth_1_m']
dbt020_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dbt020_01ctd']

axs[3,0].errorbar(dbt006['∆14C'], dbt006['Depth'], xerr=dbt006['∆14C error'], marker=m1, color=c1, label='DBT006', alpha=a2)
axs[3,0].errorbar(SO30946['∆14C'], SO30946['Depth'], xerr=SO30946['∆14C error'], marker=m2, color=c2, label='SO30946', alpha=a2)
axs[3,0].errorbar(dbt020['∆14C'], dbt020['Depth'], xerr=dbt020['∆14C error'], marker=m3, color=c3, label='DBT020', alpha=a2)

axs[3,1].scatter(dbt006_ctd['T090C'], dbt006_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[3,1].scatter(so30946_ctd['t090C'], so30946_ctd['depSM'], color=c2)  # or 'plasma', 'coolwarm', etc.
axs[3,1].scatter(dbt020_ctd['t090C'], dbt020_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.

"""
GROUP 4, Doubtful Sound Mouth
"""
dbt008 = df.loc[df['Station'] == 'DBT008']
SO30953 = df.loc[df['Station'] == 'SO309-53']
dbt019 = df.loc[df['Station'] == 'DBT019']

dbt008_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT008_01CTD']
SO30953_ctd = sonne_ctd.loc[sonne_ctd['FileName'] == 'SO309-53-1_by_depth_1_m']
dbt019_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dbt019_01ctd']

axs[4,0].errorbar(dbt008['∆14C'], dbt008['Depth'], xerr=dbt008['∆14C error'], marker=m1, color=c1, label='DBT008', alpha=a3)
axs[4,0].errorbar(SO30953['∆14C'], SO30953['Depth'], xerr=SO30953['∆14C error'], marker=m2, color=c2, label='SO30953', alpha=a3)
axs[4,0].errorbar(dbt019['∆14C'], dbt019['Depth'], xerr=dbt019['∆14C error'], marker=m3, color=c3, label='dbt019', alpha=a3)

axs[4,1].scatter(dbt008_ctd['T090C'], dbt008_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[4,1].scatter(SO30953_ctd['t090C'], SO30953_ctd['depSM'], color=c2)  # or 'plasma', 'coolwarm', etc.
axs[4,1].scatter(dbt019_ctd['t090C'], dbt019_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.


"""
GROUP 5, Dusky Head
"""

dus012= df.loc[df['Station'] == 'DUS012']
dus028= df.loc[df['Station'] == 'DUS028']

dus012_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT012_01CTD'] # ctd filename was mislabelled (this was the debate I had with greer on MS Teams)
dus028_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dus028_01ctd']

axs[1,2].errorbar(dus012['∆14C'], dus012['Depth'], xerr=dus012['∆14C error'], marker=m1, color=c1, label='DUS012', alpha=a3)
axs[1,2].errorbar(dus028['∆14C'], dus028['Depth'], xerr=dus028['∆14C error'], marker=m3, color=c3, label='DUS028', alpha=a3)

axs[1,3].scatter(dus012_ctd['T090C'], dus012_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[1,3].scatter(dus028_ctd['t090C'], dus028_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.


"""
GROUP 7 Sportman's Cove
"""
# HERE ARE DBT FROM SFCS2405 (GROUP7)
dus010= df.loc[df['Station'] == 'DUS010']
dus030= df.loc[df['Station'] == 'DUS030']
axs[2,2].errorbar(dus010['∆14C'], dus010['Depth'], xerr=dus010['∆14C error'], marker=m1, color=c1, label='DUS010', alpha=a3)
axs[2,2].errorbar(dus030['∆14C'], dus030['Depth'], xerr=dus030['∆14C error'], marker=m3, color=c3, label='DUS030', alpha=a3)

dus010_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT010_02CTD'] # ctd filename was mislabelled (this was the debate I had with greer on MS Teams)
dus030_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dus030_01ctd']
axs[2,3].scatter(dus010_ctd['T090C'], dus010_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[2,3].scatter(dus030_ctd['t090C'], dus030_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.


"""
GROUP 8 North of Long Island
"""
dus023= df.loc[df['Station'] == 'DUS023']
print(dus023)
SO30959= df.loc[df['Station'] == 'SO309-59']
axs[3,2].errorbar(SO30959['∆14C'], SO30959['Depth'], xerr=SO30959['∆14C error'], marker=m2, color=c2, label='SO30959', alpha=a3)
axs[3,2].errorbar(dus023['∆14C'], dus023['Depth'], xerr=dus023['∆14C error'], marker=m1, color=c1, label='DUS023', alpha=a3)

dus023_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DUS023_01CTD'] # ctd filename was mislabelled (this was the debate I had with greer on MS Teams)

SO30959_ctd = sonne_ctd.loc[sonne_ctd['FileName'] == 'SO309-59-13_by_depth_1_m']

axs[3,3].scatter(dus023_ctd['T090C'], dus023_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[3,3].scatter(SO30959_ctd['t090C'], SO30959_ctd['depSM'], color=c2)  # or 'plasma', 'coolwarm', etc.


"""
GROUP 9 Dusky Head
"""
dus020= df.loc[df['Station'] == 'DUS020']
dus036= df.loc[df['Station'] == 'DUS036']
axs[4,2].errorbar(dus020['∆14C'], dus020['Depth'], xerr=dus020['∆14C error'], marker=m1, color=c1, label='DUS010', alpha=a3)
axs[4,2].errorbar(dus036['∆14C'], dus036['Depth'], xerr=dus036['∆14C error'], marker=m3, color=c3, label='DUS030', alpha=a3)

dus020_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DUS020_01CTD'] # ctd filename was mislabelled (this was the debate I had with greer on MS Teams)
dus036_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dus036_01ctd']
axs[4,3].scatter(dus020_ctd['T090C'], dus020_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[4,3].scatter(dus036_ctd['t090C'], dus036_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.


axs[1,0].set_ylim(500,-10)
axs[2,0].set_ylim(500,-10)
axs[3,0].set_ylim(500,-10)
axs[1,2].set_ylim(500,-10)
axs[2,2].set_ylim(500,-10)
axs[3,2].set_ylim(500,-10)
axs[4,2].set_ylim(500,-10)
axs[4,0].set_ylim(500,-10)

axs[1,1].set_ylim(500,-10)
axs[2,1].set_ylim(500,-10)
axs[3,1].set_ylim(500,-10)
axs[1,3].set_ylim(500,-10)
axs[2,3].set_ylim(500,-10)
axs[3,3].set_ylim(500,-10)
axs[4,3].set_ylim(500,-10)
axs[4,1].set_ylim(500,-10)


# axs[2].set_ylabel('Depth (m)')axs[0].set_ylabel('\u0394$^1$$^4$C (\u2030)')
# axs[3].set_xlabel('14C')
axs[4,0].set_xlabel('\u0394$^1$$^4$C (\u2030)')
axs[4,2].set_xlabel('\u0394$^1$$^4$C (\u2030)')
axs[1,0].set_ylabel('Depth (m)')
axs[2,0].set_ylabel('Depth (m)')
axs[3,0].set_ylabel('Depth (m)')
axs[4,0].set_ylabel('Depth (m)')


axs[1,0].set_xlim(15,34)
axs[2,0].set_xlim(15,34)
axs[3,0].set_xlim(15,34)
axs[4,0].set_xlim(15,34)

axs[1,1].set_xlim(10,20)
axs[2,1].set_xlim(10,20)
axs[3,1].set_xlim(10,20)
axs[4,1].set_xlim(10,20)

axs[1,2].set_xlim(15,34)
axs[2,2].set_xlim(15,34)
axs[3,2].set_xlim(15,34)
axs[4,2].set_xlim(15,34)

axs[1,3].set_xlim(10,20)
axs[2,3].set_xlim(10,20)
axs[3,3].set_xlim(10,20)
axs[4,3].set_xlim(10,20)


axs[0,0].legend()

plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/ongoing1.png", dpi=300, bbox_inches="tight")
plt.close()







"""
SALNITY
"""




plt.close()
fig, axs = plt.subplots(5, 4, figsize=(20, 20))  # 3 rows, 1 column

map1 =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.6, -45.5, 167.2, -45.2))
map2 =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.8, 167.0, -45.7))
map1.plot(ax=axs[0,0], color="lightgray")
map2.plot(ax=axs[0,2], color="lightgray")

"""
PLOT THE MAPS
"""

siz = 50

sfcs2405 = dbt.loc[(dbt['Expedition'] == 'SFCS2405')]
s309 = dbt.loc[(dbt['Expedition'] == 'S309')]
sfcs2505 = dbt.loc[(dbt['Expedition'] == 'SFCS2505')]

axs[0, 0].scatter(sfcs2405['Lon E'], sfcs2405['Lat N'], color=c1, marker=m1, label='SFCS2405, May 2024', alpha=0.5, s=siz)
axs[0, 0].scatter(s309['Lon E'], s309['Lat N'], color=c2, marker=m2, label='S309, January 2025', alpha=0.5, s=siz)
axs[0, 0].scatter(sfcs2505['Lon E'],sfcs2505['Lat N'], color=c3, marker=m3, label='SFCS2505, May 2025', alpha=0.5, s=siz)

sfcs2405 = dus.loc[(dus['Expedition'] == 'SFCS2405')]
s309 = dus.loc[(dus['Expedition'] == 'S309')]
sfcs2505 = dus.loc[(dus['Expedition'] == 'SFCS2505')]

axs[0, 2].scatter(sfcs2405['Lon E'], sfcs2405['Lat N'], color=c1, marker=m1, label='SFCS2405, May 2024', alpha=0.5, s=siz)
axs[0, 2].scatter(s309['Lon E'], s309['Lat N'], color=c2, marker=m2, label='S309, January 2025', alpha=0.5, s=siz)
axs[0, 2].scatter(sfcs2505['Lon E'],sfcs2505['Lat N'], color=c3, marker=m3, label='SFCS2505, May 2025', alpha=0.5, s=siz)


plt.legend()

"""
GROUP 1, DEEP COVE
"""
dbt001 = df.loc[df['Station'] == 'DBT001']
dbt021 = df.loc[df['Station'] == 'DBT021']

dbt001_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT001_01CTD']
dbt021_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dbt021_01ctd']

axs[1,0].errorbar(dbt001['∆14C'], dbt001['Depth'], xerr=dbt001['∆14C error'], marker=m1, color=c1, label='DBT001', alpha=a1)
axs[1,0].errorbar(dbt021['∆14C'], dbt021['Depth'], xerr=dbt021['∆14C error'], marker=m3, color=c3, label='DBT021', alpha=a1)

axs[1,1].scatter(dbt001_ctd['Sal00'], dbt001_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[1,1].scatter(dbt021_ctd['sal00'], dbt021_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.


"""
GROUP 2, DEEP COVE
"""
dbt003 = df.loc[df['Station'] == 'DBT003']
dbt003_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT003_01CTD']

axs[2,0].errorbar(dbt003['∆14C'], dbt003['Depth'], xerr=dbt003['∆14C error'], marker=m1, color=c1, label='DBT003', alpha=a1)
axs[2,1].scatter(dbt003_ctd['Sal00'], dbt003_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.

"""
GROUP 3, Malaspina Reach
"""
dbt006 = df.loc[df['Station'] == 'DBT006']
SO30946 = df.loc[df['Station'] == 'SO309-46']
dbt020 = df.loc[df['Station'] == 'DBT020']

dbt006_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT006_01CTD']
so30946_ctd = sonne_ctd.loc[sonne_ctd['FileName'] == 'SO309-46-17_by_depth_1_m']
dbt020_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dbt020_01ctd']

axs[3,0].errorbar(dbt006['∆14C'], dbt006['Depth'], xerr=dbt006['∆14C error'], marker=m1, color=c1, label='DBT006', alpha=a2)
axs[3,0].errorbar(SO30946['∆14C'], SO30946['Depth'], xerr=SO30946['∆14C error'], marker=m2, color=c2, label='SO30946', alpha=a2)
axs[3,0].errorbar(dbt020['∆14C'], dbt020['Depth'], xerr=dbt020['∆14C error'], marker=m3, color=c3, label='DBT020', alpha=a2)

axs[3,1].scatter(dbt006_ctd['Sal00'], dbt006_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[3,1].scatter(so30946_ctd['sal00'], so30946_ctd['depSM'], color=c2)  # or 'plasma', 'coolwarm', etc.
axs[3,1].scatter(dbt020_ctd['sal00'], dbt020_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.

"""
GROUP 4, Doubtful Sound Mouth
"""
dbt008 = df.loc[df['Station'] == 'DBT008']
SO30953 = df.loc[df['Station'] == 'SO309-53']
dbt019 = df.loc[df['Station'] == 'DBT019']

dbt008_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT008_01CTD']
SO30953_ctd = sonne_ctd.loc[sonne_ctd['FileName'] == 'SO309-53-1_by_depth_1_m']
dbt019_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dbt019_01ctd']

axs[4,0].errorbar(dbt008['∆14C'], dbt008['Depth'], xerr=dbt008['∆14C error'], marker=m1, color=c1, label='DBT008', alpha=a3)
axs[4,0].errorbar(SO30953['∆14C'], SO30953['Depth'], xerr=SO30953['∆14C error'], marker=m2, color=c2, label='SO30953', alpha=a3)
axs[4,0].errorbar(dbt019['∆14C'], dbt019['Depth'], xerr=dbt019['∆14C error'], marker=m3, color=c3, label='dbt019', alpha=a3)

axs[4,1].scatter(dbt008_ctd['Sal00'], dbt008_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[4,1].scatter(SO30953_ctd['sal00'], SO30953_ctd['depSM'], color=c2)  # or 'plasma', 'coolwarm', etc.
axs[4,1].scatter(dbt019_ctd['sal00'], dbt019_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.


"""
GROUP 5, Dusky Head
"""

dus012= df.loc[df['Station'] == 'DUS012']
dus028= df.loc[df['Station'] == 'DUS028']

dus012_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT012_01CTD'] # ctd filename was mislabelled (this was the debate I had with greer on MS Teams)
dus028_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dus028_01ctd']

axs[1,2].errorbar(dus012['∆14C'], dus012['Depth'], xerr=dus012['∆14C error'], marker=m1, color=c1, label='DUS012', alpha=a3)
axs[1,2].errorbar(dus028['∆14C'], dus028['Depth'], xerr=dus028['∆14C error'], marker=m3, color=c3, label='DUS028', alpha=a3)

axs[1,3].scatter(dus012_ctd['Sal00'], dus012_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[1,3].scatter(dus028_ctd['sal00'], dus028_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.


"""
GROUP 7 Sportman's Cove
"""
# HERE ARE DBT FROM SFCS2405 (GROUP7)
dus010= df.loc[df['Station'] == 'DUS010']
dus030= df.loc[df['Station'] == 'DUS030']
axs[2,2].errorbar(dus010['∆14C'], dus010['Depth'], xerr=dus010['∆14C error'], marker=m1, color=c1, label='DUS010', alpha=a3)
axs[2,2].errorbar(dus030['∆14C'], dus030['Depth'], xerr=dus030['∆14C error'], marker=m3, color=c3, label='DUS030', alpha=a3)

dus010_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DBT010_02CTD'] # ctd filename was mislabelled (this was the debate I had with greer on MS Teams)
dus030_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dus030_01ctd']
axs[2,3].scatter(dus010_ctd['Sal00'], dus010_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[2,3].scatter(dus030_ctd['sal00'], dus030_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.


"""
GROUP 8 North of Long Island
"""
dus023= df.loc[df['Station'] == 'DUS023']
print(dus023)
SO30959= df.loc[df['Station'] == 'SO309-59']
axs[3,2].errorbar(SO30959['∆14C'], SO30959['Depth'], xerr=SO30959['∆14C error'], marker=m2, color=c2, label='SO30959', alpha=a3)
axs[3,2].errorbar(dus023['∆14C'], dus023['Depth'], xerr=dus023['∆14C error'], marker=m1, color=c1, label='DUS023', alpha=a3)

dus023_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DUS023_01CTD'] # ctd filename was mislabelled (this was the debate I had with greer on MS Teams)

SO30959_ctd = sonne_ctd.loc[sonne_ctd['FileName'] == 'SO309-59-13_by_depth_1_m']

axs[3,3].scatter(dus023_ctd['Sal00'], dus023_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[3,3].scatter(SO30959_ctd['sal00'], SO30959_ctd['depSM'], color=c2)  # or 'plasma', 'coolwarm', etc.


"""
GROUP 9 Dusky Head
"""
dus020= df.loc[df['Station'] == 'DUS020']
dus036= df.loc[df['Station'] == 'DUS036']
axs[4,2].errorbar(dus020['∆14C'], dus020['Depth'], xerr=dus020['∆14C error'], marker=m1, color=c1, label='DUS010', alpha=a3)
axs[4,2].errorbar(dus036['∆14C'], dus036['Depth'], xerr=dus036['∆14C error'], marker=m3, color=c3, label='DUS030', alpha=a3)

dus020_ctd = sfcs2405_ctd.loc[sfcs2405_ctd['FileName'] == 'DUS020_01CTD'] # ctd filename was mislabelled (this was the debate I had with greer on MS Teams)
dus036_ctd = sfcs2505_ctd.loc[sfcs2505_ctd['FileName'] == 'sfcs2505_dus036_01ctd']
axs[4,3].scatter(dus020_ctd['Sal00'], dus020_ctd['DepSM'], color=c1)  # or 'plasma', 'coolwarm', etc.
axs[4,3].scatter(dus036_ctd['sal00'], dus036_ctd['depSM'], color=c3)  # or 'plasma', 'coolwarm', etc.


axs[1,0].set_ylim(500,-10)
axs[2,0].set_ylim(500,-10)
axs[3,0].set_ylim(500,-10)
axs[1,2].set_ylim(500,-10)
axs[2,2].set_ylim(500,-10)
axs[3,2].set_ylim(500,-10)
axs[4,2].set_ylim(500,-10)
axs[4,0].set_ylim(500,-10)

axs[1,1].set_ylim(500,-10)
axs[2,1].set_ylim(500,-10)
axs[3,1].set_ylim(500,-10)
axs[1,3].set_ylim(500,-10)
axs[2,3].set_ylim(500,-10)
axs[3,3].set_ylim(500,-10)
axs[4,3].set_ylim(500,-10)
axs[4,1].set_ylim(500,-10)


# axs[2].set_ylabel('Depth (m)')axs[0].set_ylabel('\u0394$^1$$^4$C (\u2030)')
# axs[3].set_xlabel('14C')
axs[4,0].set_xlabel('\u0394$^1$$^4$C (\u2030)')
axs[4,2].set_xlabel('\u0394$^1$$^4$C (\u2030)')
axs[1,0].set_ylabel('Depth (m)')
axs[2,0].set_ylabel('Depth (m)')
axs[3,0].set_ylabel('Depth (m)')
axs[4,0].set_ylabel('Depth (m)')


axs[1,0].set_xlim(15,34)
axs[2,0].set_xlim(15,34)
axs[3,0].set_xlim(15,34)
axs[4,0].set_xlim(15,34)

axs[1,1].set_xlim(32,38)
axs[2,1].set_xlim(32,38)
axs[3,1].set_xlim(32,38)
axs[4,1].set_xlim(32,38)

axs[1,2].set_xlim(15,34)
axs[2,2].set_xlim(15,34)
axs[3,2].set_xlim(15,34)
axs[4,2].set_xlim(15,34)

axs[1,3].set_xlim(32,38)
axs[2,3].set_xlim(32,38)
axs[3,3].set_xlim(32,38)
axs[4,3].set_xlim(32,38)

axs[0,0].legend()

plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/ongoing1_SAL.png", dpi=300, bbox_inches="tight")
plt.close()


"""

"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nzgeom.coastlines
from cmcrameri import cm
import gsw
import matplotlib.gridspec as gridspec
import matplotlib.cm as mpl_cm
cmap = mpl_cm.viridis
from scipy import stats

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/ctds/ctdmeans_edited.xlsx',
                   sheet_name='edited', comment='#')
plt.close()

# Choose a perceptually uniform colormap
cmap = mpl_cm.viridis

# Helper function to plot scatter + errorbars with Lon-E color mapping
def scatter_with_errorbars(ax, x, y, yerr, lon, marker):
    sc = ax.scatter(x, y, c=lon, cmap=cmap, marker=marker, edgecolor='k')
    ax.errorbar(x, y, yerr=yerr, fmt='none', ecolor='k', alpha=0.5)
    return sc

# Subset your datasets
s2405_dbt = df.loc[(df['Expedition'] == 'SFCS2405') & (df['Site'] == 'Doubtful')]
s2505_dbt = df.loc[(df['Expedition'] == 'SFCS2505') & (df['Site'] == 'Doubtful')]

s2405_dus = df.loc[(df['Expedition'] == 'SFCS2405') & (df['Site'] == 'Dusky')]
s2505_dus = df.loc[(df['Expedition'] == 'SFCS2505') & (df['Site'] == 'Dusky')]

fig, axs = plt.subplots(2, 3, figsize=(12, 8))

# --- Row 1: Doubtful Sound ---
sc1 = scatter_with_errorbars(axs[0,0], s2405_dbt['Mean Temp'], s2405_dbt['∆14C'], s2405_dbt['∆14C error'], s2405_dbt['Lon E'], 'o')
scatter_with_errorbars(axs[0,0], s2505_dbt['Mean Temp'], s2505_dbt['∆14C'], s2505_dbt['∆14C error'], s2505_dbt['Lon E'], 'D')

scatter_with_errorbars(axs[0,1], s2405_dbt['Mean Sal'], s2405_dbt['∆14C'], s2405_dbt['∆14C error'], s2405_dbt['Lon E'], 'o')
scatter_with_errorbars(axs[0,1], s2505_dbt['Mean Sal'], s2505_dbt['∆14C'], s2505_dbt['∆14C error'], s2505_dbt['Lon E'], 'D')

scatter_with_errorbars(axs[0,2], s2405_dbt['Mean Oxygen Edited'], s2405_dbt['∆14C'], s2405_dbt['∆14C error'], s2405_dbt['Lon E'], 'o')
scatter_with_errorbars(axs[0,2], s2505_dbt['Mean Oxygen Edited'], s2505_dbt['∆14C'], s2505_dbt['∆14C error'], s2505_dbt['Lon E'], 'D')

# --- Row 2: Dusky Sound ---
scatter_with_errorbars(axs[1,0], s2405_dus['Mean Temp'], s2405_dus['∆14C'], s2405_dus['∆14C error'], s2405_dus['Lon E'], 'o')
scatter_with_errorbars(axs[1,0], s2505_dus['Mean Temp'], s2505_dus['∆14C'], s2505_dus['∆14C error'], s2505_dus['Lon E'], 'D')

scatter_with_errorbars(axs[1,1], s2405_dus['Mean Sal'], s2405_dus['∆14C'], s2405_dus['∆14C error'], s2405_dus['Lon E'], 'o')
scatter_with_errorbars(axs[1,1], s2505_dus['Mean Sal'], s2505_dus['∆14C'], s2505_dus['∆14C error'], s2505_dus['Lon E'], 'D')

scatter_with_errorbars(axs[1,2], s2405_dus['Mean Oxygen Edited'], s2405_dus['∆14C'], s2405_dus['∆14C error'], s2405_dus['Lon E'], 'o')
scatter_with_errorbars(axs[1,2], s2505_dus['Mean Oxygen Edited'], s2505_dus['∆14C'], s2505_dus['∆14C error'], s2505_dus['Lon E'], 'D')

# ---- Labels / Titles ----
axs[0,0].set_ylabel('Δ$^{14}$C (‰)')
axs[1,0].set_ylabel('Δ$^{14}$C (‰)')

axs[0,1].set_title('Patea / Doubtful Sound')
axs[1,1].set_title('Tamatea / Dusky Sound')

axs[1,0].set_xlabel('Temperature (°C)')
axs[1,1].set_xlabel('Salinity (psu)')
axs[1,2].set_xlabel('Dissolved Oxygen (mmol/kg)')

# after plotting the scatter/errorbars for 2405 and 2505
axs[0,0].scatter([], [], marker='o', color='k', label='SFCS2405')
axs[0,0].scatter([], [], marker='D', color='k', label='SFCS2505')
axs[0,0].legend()

axs[0,0].set_xlim(10,16)
axs[1,0].set_xlim(10,16)

axs[0,1].set_xlim(5,35)
axs[1,1].set_xlim(5,35)

axs[0,2].set_xlim(200,300)
axs[1,2].set_xlim(200,300)

axs[0,0].set_ylim(16,32)
axs[1,0].set_ylim(16,32)

axs[0,1].set_ylim(16,32)
axs[1,1].set_ylim(16,32)

axs[0,2].set_ylim(16,32)
axs[1,2].set_ylim(16,32)


# ---- Shared Colorbar ----
cbar = fig.colorbar(sc1, ax=axs, label='Longitude (°E)', shrink=0.8)

plt.savefig("C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/Surface_vs_Oxygen_lon_colored.png",
            dpi=300, bbox_inches="tight")
# plt.show()

print(f"Mean Temp: DBT: 2405 {np.nanmean(s2405_dbt['Mean Temp'])} +- {np.nanstd(s2405_dbt['Mean Temp'])}")
print(f"Mean Temp: DBT: 2505 {np.nanmean(s2505_dbt['Mean Temp'])} +- {np.nanstd(s2505_dbt['Mean Temp'])}")

print(f"Mean Temp: DUS: 2405 {np.nanmean(s2405_dus['Mean Temp'])} +- {np.nanstd(s2405_dus['Mean Temp'])}")
print(f"Mean Temp: DUS: 2505 {np.nanmean(s2505_dus['Mean Temp'])} +- {np.nanstd(s2505_dus['Mean Temp'])}")

plt.close()

fig = plt.subplots(figsize=(12, 8))
s2405_dus = s2405_dus.sort_values(by='Lon E')
plt.errorbar(s2405_dbt['Lon E'], s2405_dbt['∆14C'], yerr=s2405_dbt['∆14C error'], marker='o', label='SFCS2405, DBT', color='#0072B2', capsize=5)
plt.errorbar(s2505_dbt['Lon E'], s2505_dbt['∆14C'], yerr=s2505_dbt['∆14C error'], marker='D', label='SFCS2505, DBT', color='#0072B2', capsize=5)
plt.errorbar(s2405_dus['Lon E'], s2405_dus['∆14C'], yerr=s2405_dus['∆14C error'], marker='o', label='SFCS2405, DUS', color='#D55E00', capsize=5)
plt.errorbar(s2505_dus['Lon E'], s2505_dus['∆14C'], yerr=s2505_dus['∆14C error'], marker='D', label='SFCS2505, DUS', color='#D55E00', capsize=5)
plt.legend()
plt.ylabel('Δ$^{14}$C (‰)')
plt.xlabel('Longitude (E)')
plt.savefig("C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/LSL_14Cd.png",
            dpi=300, bbox_inches="tight")

print('')
print('Is there a difference between DUSKY SFCS2024 and DUSKY SFCS2025?')
c = stats.ttest_ind(s2405_dus['∆14C'], s2505_dus['∆14C'])
print(c)

print('')
print('Is there a difference between DUSKY SFCS2024 and DUSKY SFCS2025?')
c = stats.ttest_ind(s2405_dbt['∆14C'], s2505_dbt['∆14C'])
print(c)

plt.close()
fig = plt.subplots(figsize=(12, 8))
s2405_dus = s2405_dus.sort_values(by='Lon E')
plt.errorbar(s2405_dbt['Distance from Fjord Head'], s2405_dbt['∆14C'], yerr=s2405_dbt['∆14C error'], marker='o', label='SFCS2405, DBT', color='#0072B2', capsize=5)
plt.errorbar(s2505_dbt['Distance from Fjord Head'], s2505_dbt['∆14C'], yerr=s2505_dbt['∆14C error'], marker='D', label='SFCS2505, DBT', color='#0072B2', capsize=5)
plt.errorbar(s2405_dus['Distance from Fjord Head'], s2405_dus['∆14C'], yerr=s2405_dus['∆14C error'], marker='o', label='SFCS2405, DUS', color='#D55E00', capsize=5)
plt.errorbar(s2505_dus['Distance from Fjord Head'], s2505_dus['∆14C'], yerr=s2505_dus['∆14C error'], marker='D', label='SFCS2505, DUS', color='#D55E00', capsize=5)
plt.legend()
plt.ylabel('Δ$^{14}$C (‰)')
plt.xlabel('Longitude (E)')
plt.xlim(33,-2)
plt.savefig("C:/Users/clewis/IdeaProjects/GNS/Fiordland_DIC_14C_paper/output/figures/LSL_14Cd_distfromhead.png",
            dpi=300, bbox_inches="tight")


