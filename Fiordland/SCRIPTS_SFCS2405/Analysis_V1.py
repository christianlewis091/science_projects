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

# This is a test to see if my new commit works, on my new GNS PC. If this works, I think I'll be pretty much set up to continue working.
print('This is a test')

"""
September 10, 2024
I'm editing/re-structuring this to make it more complete and clean for my talk and future writing of the paper or proposal based on this data;
some nice figures still exist in "Basic_Figures.py" and while these may work for my Hobart talk, I may change them eventually

August 21, 2024
This analysis is based on trying to understand the mixing of river and ocean waters in the Fiords, from cruise SFCS2405. See my Results powerpoint in the directory below;
H:\Science\Current_Projects/03_CCE_24_25/01_May_2024_Cruise\RESULTS. 
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

df['Sound'] = 'Dusky' # set initial status to Dusky
dbt_station = [1,2,3,4]
df.loc[(df['My Station Name'].isin(dbt_station)), 'Sound'] = 'Doubtful'

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

def calc_straight_line_dist(row, reflat, reflon):
    lat, lon = row['lat'], row['lon']
    dist = np.arccos(np.sin(np.radians(reflat)) * np.sin(np.radians(lat)) +
                     np.cos(np.radians(reflat)) * np.cos(np.radians(lat)) *
                     np.cos(np.radians(lon - reflon))) * 6371
    return dist

# Calculate distances for Doubtful and Dusky sounds
df.loc[df['Sound'] == 'Doubtful', 'Straight_Line_Dist'] = df.apply(calc_straight_line_dist, axis=1, reflat=-45.46149, reflon=167.15852)
df.loc[df['Sound'] == 'Dusky', 'Straight_Line_Dist'] = df.apply(calc_straight_line_dist, axis=1, reflat=-45.7285833, reflon=166.940366)


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
PLOTSPLOTPLOTSPLOTSPLOTS
PLOTSPLOTPLOTSPLOTSPLOTS
PLOTSPLOTPLOTSPLOTSPLOTS
PLOTSPLOTPLOTSPLOTSPLOTS
PLOTSPLOTPLOTSPLOTSPLOTS
PLOTSPLOTPLOTSPLOTSPLOTS
PLOTSPLOTPLOTSPLOTSPLOTS
PLOTSPLOTPLOTSPLOTSPLOTS
"""

# """
# Surface_DIC_vs_Longitude
# """

dbt_surfs = df.loc[(df['Depth'] == 1) & (df['Sound'] == 'Doubtful')]
dbt_else = df.loc[(df['Depth'] > 1) & (df['Sound'] == 'Doubtful')]
dus_surfs = df.loc[(df['Depth'] == 1) & (df['Sound'] == 'Dusky')]
dus_else = df.loc[(df['Depth'] > 1) & (df['Sound'] == 'Dusky')]

# Regression of surface data
dus_surfs_x = dus_surfs['Straight_Line_Dist']
dus_surfs_x = np.array(dus_surfs_x)
dus_surfs_y = dus_surfs['DELTA14C']
dus_surfs_y = np.array(dus_surfs_y)
#
dbt_surfs_x = dbt_surfs['Straight_Line_Dist']
dbt_surfs_x = np.array(dbt_surfs_x)
dbt_surfs_y = dbt_surfs['DELTA14C']
dbt_surfs_y = np.array(dbt_surfs_y)

# regress the data
slope, intercept, rvalue, pvalue, stderr = stats.linregress(dus_surfs_x, dus_surfs_y)
print("Dusky Surface: y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2))

sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(dbt_surfs_x, dbt_surfs_y)
print("Doubtful Surface: y=%.3fx+%.3f\R$^2$=%.3f"%(sslope, sintercept,srvalue**2))

fig = plt.figure()
plt.errorbar(dus_surfs['Straight_Line_Dist'], dus_surfs['DELTA14C'], yerr=dus_surfs['DELTA14C_Error'], label='Dusky', marker='o', linestyle='', color='black', capsize=5)
plt.errorbar(dbt_surfs['Straight_Line_Dist'], dbt_surfs['DELTA14C'], yerr=dbt_surfs['DELTA14C_Error'], label='Doubtful', marker='D', linestyle='', color='seagreen', capsize=5)
plt.plot(dus_surfs_x, slope*dus_surfs_x+intercept, color='black', alpha= 0.5) # ONLY PLOT TRENDLINES FOR lon
plt.plot(dbt_surfs_x, sslope*dbt_surfs_x+sintercept, color='seagreen', alpha= 0.5)
plt.xlabel('Distance from Fiord Head')
plt.title('Surface Data (1m)')
plt.legend()
plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Analysis_V1/Surface_DIC_vs_straight_dist.png", dpi=300, bbox_inches="tight")
plt.close()

"""
DIC vs Salinity
"""

# Regression of surface data
dus_surfs_x = dus_surfs['Sal00']
dus_surfs_x = np.array(dus_surfs_x)
dus_surfs_y = dus_surfs['DELTA14C']
dus_surfs_y = np.array(dus_surfs_y)
#
dbt_surfs_x = dbt_surfs['Sal00']
dbt_surfs_x = np.array(dbt_surfs_x)
dbt_surfs_y = dbt_surfs['DELTA14C']
dbt_surfs_y = np.array(dbt_surfs_y)

# regress the data
slope, intercept, rvalue, pvalue, stderr = stats.linregress(dus_surfs_x, dus_surfs_y)
print("Dusky Surface: y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2))

sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(dbt_surfs_x, dbt_surfs_y)
print("Doubtful Surface: y=%.3fx+%.3f\R$^2$=%.3f"%(sslope, sintercept,srvalue**2))

fig = plt.figure()
plt.errorbar(dus_surfs['Sal00'], dus_surfs['DELTA14C'], yerr=dus_surfs['DELTA14C_Error'], label='Dusky', marker='o', linestyle='', color='black', capsize=5)
plt.errorbar(dbt_surfs['Sal00'], dbt_surfs['DELTA14C'], yerr=dbt_surfs['DELTA14C_Error'], label='Doubtful', marker='D', linestyle='', color='seagreen', capsize=5)
plt.plot(dus_surfs_x, slope*dus_surfs_x+intercept, color='black', alpha= 0.5) # ONLY PLOT TRENDLINES FOR lon
plt.plot(dbt_surfs_x, sslope*dbt_surfs_x+sintercept, color='seagreen', alpha= 0.5)
plt.xlabel('Sal00')
plt.title('Surface Data (1m)')
plt.legend()
plt.ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Analysis_V1/Surface_DIC_vs_Sal00.png", dpi=300, bbox_inches="tight")
plt.close()


"""
AOU PLOT
"""

fig = plt.figure(figsize=(7,5))
mako = sns.color_palette("mako", 6)
colors_dbt = ['SeaGreen','Teal','deepskyblue','Blue']
colors_dus = ['SeaGreen','Teal','Sienna','deepskyblue','Blue']
marks = ['o','D','^','s','X']

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


