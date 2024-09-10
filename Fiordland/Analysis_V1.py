import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import seawater
import numpy as np
import gsw
from scipy import stats
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap
import warnings
warnings.simplefilter("ignore")

"""
September 10, 2024
I'm editing/re-structuring this to make it more complete and clean for my talk and future writing of the paper or proposal based on this data;
some nice figures still exist in "Basic_Figures.py" and while these may work for my Hobart talk, I may change them eventually

August 21, 2024
This analysis is based on trying to understand the mixing of river and ocean waters in the Fiords. See my Results powerpoint in the directory below;
H:\Science\Current_Projects/03_CCE_24_25/01_May_2024_Cruise\RESULTS

"""

"""
Read in my data, and merge it with the AMS data straight from RLIMS to avoid any manual "copying" errors. 
"""
# df = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/02_Results_and_Data/DATA_PROCESSING_RAW.xlsx', sheet_name='Cruise_Data_Sheet_ALL', comment='#')
# df = df[['My Station Name', 'Cruise Station Name','Latitude_N_decimal','Longitude_E_decimal','Bottom Depth (m)','Depth','Qflag','Sample','TP']]
# df = df.loc[df['Qflag'] != '.X.']
# dic = df.loc[((df['Sample'] == 'DIC') | (df['Sample'] == 'DIC Duplicate'))]
#
# tw3530 = pd.read_excel('H:/Science/Datasets/Fiordland/TW3530_export.xlsx')
# tw3530 = tw3530.loc[tw3530['Samples::Sample Description'] == 'Fiordland DIC samples from SFCS2405'] # remove oxalics, kapunis, etc
#
# df = dic.merge(tw3530, on='TP')
#
# df.to_excel('H:/Science/Current_Projects/03_CCE_24_25/02_Results_and_Data/Finalized_Results/DI14C_FINAL.xlsx')

"""
I've re-written the more clean final results above, and now I'm re-reading it into python now. 
"""
df = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/02_Results_and_Data/Finalized_Results/DI14C_FINAL.xlsx', comment='#')
df = df.rename(columns={'Latitude_N_decimal': 'lat', 'Longitude_E_decimal': 'lon','Water Carbonate CO2 Evolution::TDIC':'tdic_processing'})
ctd = pd.read_excel('H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP4\mystations.xlsx')

"""
I'm going to spend a few lines briefly adding some columns to the data, based on common oceanograpic 
metrics used for plotting. 

Potential density and GSW's. 
This will be done according to :
McDougall T. J. and P. M. Barker, 2011: Getting started with TEOS-10 and the Gibbs Seawater (GSW)
Oceanographic Toolbox, 28pp., SCOR/IAPSO WG127, ISBN 978-0-646-55621-5.
Followed steps on bottom of page 2.

Oxygen saturation equation grabbed fom RPADOSaturationEquation.xls State of Oregon Department of Environmental Quality excel sheet
H:\Science\Current_Projects/03_CCE_24_25/02_Results_and_Data\BRAINSTORM_RESULTS
** equation developed by Benson and Krause (1984)
!!! Axed the above three lines in favor of below: !!!
https://pythonhosted.org/seawater/extras.html seawater.extras.satO2(s, t); however, the two methods (python code and excel sheet) agree once units are converted

"""
df['fake_ref'] = 0 # create a column with zeroes to allow functions to continue in pandas (0 = reference pressure)
df['SA'] = gsw.conversions.SA_from_SP(df['Sal00'], df['T090C'], df['lat'], df['lon'])
df['CT'] = gsw.conversions.CT_from_t(df['Sal00'], df['T090C'], df['DepSM'])
df['Pot_density'] = gsw.pot_rho_t_exact(df['SA'], df['T090C'], df['DepSM'], df['fake_ref'])
df['Pot_density_anomaly'] = gsw.sigma0(df['SA'], df['CT'])
df['satO2_ml_l'] = seawater.extras.satO2(df['Sal00'], df['T090C']) # returns in mL/L! # see https://www.ices.dk/data/tools/Pages/Unit-conversions.aspx
df['satO2_Mg/L'] = df['satO2_ml_l']/0.7
df['AOU'] = df['satO2_Mg/L'] - df['Sbeox0Mg/L']

# What percentage of water came from terrestrial remineralization, versus original "marine" water
def o2_mass_balance(m, d1, d2, tDIC):
    # m = 24  # measured value
    # d1 = -30 # terrestrial end-member
    # d2 = 30  # marine end-member
    # tDIC = 2.2 # mmol/kg

    f1 = (m-d2)/(d1-d2)
    f2 = 1-f1

    x = (tDIC*f1)
    x = round(x,2)

    # CH2O + O2 -> CO2 + H20
    consumed = x*32  # 02 = 32 g/mol

    # print(f"With measured Delta14C of {m}, marine and terrestrial DIC end-members of {d2} and {d1} respectively, terrestrial fraction is {f1}")
    # print(f"With [DIC] of {tDIC} total, {f1} terrestrial fraction means {x} came from remineralization")
    # print()
    # print(f"In a simplified system, one can assume one mol of CO2 made from each mol of O2")
    # print(f"{consumed} mg/L O2 consumed")
    return consumed

df['O2_consumed'] = o2_mass_balance(df['DELTA14C'], 0, 30, df['tdic_processing'])

# df.to_excel(r"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Analysis_V1/test.xlsx")

"""
PLAY AROUND WITH MASS BALANCE BY HAND BELOW IF YOU WANT
"""
m = 24  # measured value
d1 = -30 # terrestrial end-member
d2 = 30  # marine end-member
tDIC = 2.2 # mmol/kg

f1 = (m-d2)/(d1-d2)
f2 = 1-f1

x = (tDIC*f1)
x = round(x,2)

# CH2O + O2 -> CO2 + H20
consumed = x*32  # 02 = 32 g/mol

print(f"With measured Delta14C of {m}, marine and terrestrial DIC end-members of {d2} and {d1} respectively, terrestrial fraction is {f1}")
print(f"With [DIC] of {tDIC} total, {f1} terrestrial fraction means {x} came from remineralization")
print()
print(f"In a simplified system, one can assume one mol of CO2 made from each mol of O2")
print(f"{consumed} mg/L O2 consumed")

"""
PLAY AROUND WITH MASS BALANCE BY HAND ABOVE IF YOU WANT
"""

"""
Make a new plot for my Hobart talk...
"""

fig = plt.figure(figsize=(7,5))
mako = sns.color_palette("mako", 6)
colors_dbt = ['SeaGreen','Teal','deepskyblue','Blue']
colors_dus = ['SeaGreen','Teal','Sienna','deepskyblue','Blue']
marks = ['o','D','^','s','X']

df['Sound'] = 'Dusky' # set initial status to Dusky
dbt_station = [1,2,3,4]
df.loc[(df['My Station Name'].isin(dbt_station)), 'Sound'] = 'Doubtful'

# AOU plot
dbt_surfs = df.loc[(df['Depth'] == 1) & (df['Sound'] == 'Doubtful')]
dbt_else = df.loc[(df['Depth'] > 1) & (df['Sound'] == 'Doubtful')]
dus_surfs = df.loc[(df['Depth'] == 1) & (df['Sound'] == 'Dusky')]
dus_else = df.loc[(df['Depth'] > 1) & (df['Sound'] == 'Dusky')]

plt.scatter(dbt_surfs['DELTA14C'], dbt_surfs['AOU'], color=mako[2], marker='D', label='Doubtful Sound, Surface')
plt.scatter(dbt_else['DELTA14C'], dbt_else['AOU'], color=mako[4], marker='D', label='Doubtful Sound, Subsurface')
# plt.scatter(dus_surfs['DELTA14C'], dus_surfs['AOU'], color=mako[2], marker='o', label='Dusky Sound, Surface')
# plt.scatter(dus_else['DELTA14C'], dus_else['AOU'], color=mako[4], marker='o', label='Dusty Sound, Subsurface')
plt.xlim(21, 33)
plt.ylim(0,8)
plt.legend()
plt.xlabel('\u0394$^1$$^4$C (\u2030)')
plt.ylabel('AOU (O2sat - Measured), Mg/L')
plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Analysis_V1/AOU_DBT.png", dpi=300, bbox_inches="tight")




# plt.scatter(df['DELTA14C'], df['AOU'])



















# df = pd.read_excel('H:/Science/Datasets/Fiordland/Fiordland_DIC_14C_2024.xlsx', sheet_name='Duplicates_Removed', comment='#')
# df = df.rename(columns={'Latitude_N_decimal': 'lat', 'Longitude_E_decimal': 'lon','Water Carbonate CO2 Evolution::TDIC':'tdic_processing'})
# # atmospheric background
# ref1 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference1/reference1.xlsx')
#
# # I need to analyze these data, at least initally, as seperate "things" as 1) river water and 2) marine water
# df['River_Ocean'] = 'Ocean' # set inital status to ocean
# df.loc[(df['Depth'] == 1), 'River_Ocean'] = 'River'
#
# # add Sound labels
# df['Sound'] = 'Dusky' # set initial status to Dusky
# dbt_station = [1,2,3,4]
# df.loc[(df['My Station Name'].isin(dbt_station)), 'Sound'] = 'Doubtful'
#
# # Set DIC end-members:
# # this is going to need much more digging and reading and justifying:
# # https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2016GB005460
# # https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1029/2019GB006170
# # both values are time-dependent because of fossil fuel emissions...
# # also, is the c13 of the atmopshere at any given time really applicable to an anoxic bottom of Sportman cove? It's going to be through remineralization...
# c13_atmosphere = -8.5
# c13_remind = -2.1 # https://www.sciencedirect.com/science/article/pii/S0079661117300526
# c13_ocean = 1.2
# c14_ocean = 30
# # change C13 atmosphere to remin'd for bottom waters?
#
# what's the C14 of surface tasman sea waters according to GLODAP1
# see water mass dataset:
glodap = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP2_assign_masses/STEP2_WATER_MASSES_ASSIGNED.xlsx')
glodap = glodap.loc[((glodap['LATITUDE'] > -60) & (glodap['LATITUDE'] < -30)) & ((glodap['LONGITUDE'] > 160) & (glodap['LONGITUDE'] < 180)) & (glodap['CTDPRS'] < 100)]
print(len(glodap))
print(np.average(glodap['DELC14']))
print(np.std(glodap['DELC14']))
plt.close()


m = Basemap(projection='hammer',lon_0=180)
x, y = m(glodap['LONGITUDE'],glodap['LATITUDE'])
m.drawmapboundary(fill_color='#99ffff')
m.fillcontinents(color='#cc9966',lake_color='#99ffff')
m.scatter(x,y,marker='o',color='k')
plt.title(f"Mean Delta14C = {92}+/-{20}")
plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Analysis_V1/glodap.png", dpi=300, bbox_inches="tight")



# # calculate riverine and ocean percentages for my data
# df['X_r'] = ((df['delta13C_IRMS']-c13_ocean)) / (c13_ocean + c13_atmosphere)
# df['X_o'] = 1-df['X_r']
#
# # are the values sensible?
# print(df['X_r'])
#
# df['DELTA14C_R'] = ((df['DELTA14C']) - (df['X_o']*c14_ocean)) / df['X_r']
# print(df['DELTA14C_R'])





















# """
# Re write the figures...
# """
#
# # set initial figure settings
# mako = sns.color_palette("mako", 6)
# colors_dbt = ['SeaGreen','Teal','deepskyblue','Blue']
# colors_dus = ['SeaGreen','Sienna','Teal','deepskyblue','Blue']
# marks = ['o','D','^','s','X']
#
# dus_oc = df.loc[(df['Sound'] == 'Dusky') & (df['River_Ocean'] == 'Ocean')]
# dbt_oc = df.loc[(df['Sound'] == 'Doubtful') & (df['River_Ocean'] == 'Ocean')]
#
# dbt_station = [1, 2, 3, 4]  # arranging in longirude order, not sampling order, more imp for Dusky
# dus_station = [7, 5, 6, 9, 8]
# size1 = 70
#
#
# fig = plt.figure(figsize=(10, 10))
#
# # Create a GridSpec with 3 rows and 2 columns
# gs = gridspec.GridSpec(2, 2)
# gs.update(wspace=.2, hspace=0.05)
#
# # Add subplots to the GridSpec
# ax3 = fig.add_subplot(gs[0, 0])
# ax4 = fig.add_subplot(gs[0, 1])
# ax1 = fig.add_subplot(gs[1, 0])
# ax2 = fig.add_subplot(gs[1, 1])
#
#
# for i in range(0, len(dbt_station)):
#     site = dbt_oc.loc[dbt_oc['My Station Name'] == dbt_station[i]]
#     ax1.errorbar(site['DELTA14C_R'], site['Depth'], xerr=site['DELTA14C_Error'], color=colors_dbt[i], marker=marks[i], label=f'{dbt_station[i]}', capsize=5)
#
#     # Plotting map on ax3
#     # dbt
#     maxlat = -45.1
#     minlat = -45.5
#     nz_max_lon = 167.25
#     nz_min_lon = 166.75
#
#     map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h', ax=ax3)
#     map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.1)
#     map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.1)
#     map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
#     map.drawmapboundary(fill_color="#DDEEFF")
#     map.drawcoastlines()
#
#     lat = site['lat']
#     lon = site['lon']
#     x, y = map(lon, lat)
#     ax3.scatter(x, y, label=f'{dbt_station[i]}', color=colors_dbt[i], s=size1, zorder=2, marker=marks[i])
#
# for i in range(0, len(dus_station)):
#     site = dus_oc.loc[dus_oc['My Station Name'] == dus_station[i]]
#     ax2.errorbar(site['DELTA14C_R'], site[['Depth']],  xerr=site['DELTA14C_Error'], color=colors_dus[i], marker=marks[i], label=f'{dus_station[i]}', capsize=5)
#
#     # Plotting map on ax4
#     # dbt
#     maxlat = -45.5
#     minlat = -45.9
#     nz_max_lon = (166.3+.75)
#     nz_min_lon = 166.3
#     map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution='h', ax=ax4)
#     map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.1)
#     map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.1)
#     map.fillcontinents(color="darkseagreen", lake_color='#DDEEFF')
#     map.drawmapboundary(fill_color="#DDEEFF")
#     map.drawcoastlines()
#
#     lat = site['lat']
#     lon = site['lon']
#     x, y = map(lon, lat)
#     ax4.scatter(x, y, label=f'{dus_station[i]}', color=colors_dus[i], s=size1, zorder=2, marker=marks[i])
#
#
# ax1.set_ylabel('Depth')
# ax1.set_ylim(350, 0)
# # ax1.set_xlim(22, 36)
# ax1.set_xlabel('\u0394$^1$$^4$C (\u2030) ERRORS NOT PROPOGATED YET')
# ax1.legend()
#
# ax2.set_ylim(350, 0)
# # ax2.set_xlim(22, 36)
# ax2.set_xlabel('\u0394$^1$$^4$C (\u2030)')
# ax2.legend()
# plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/analysis1/DELTA14C_R_model.png", dpi=300, bbox_inches="tight")
# plt.close()
