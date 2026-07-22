import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import seawater
import numpy as np
import gsw
from scipy import stats
import matplotlib.gridspec as gridspec
# from mpl_toolkits.basemap import Basemap

import warnings
warnings.simplefilter("ignore")

# This is a test to see if my new commit works, on my new GNS PC. If this works, I think I'll be pretty much set up to continue working.
print('This is a test')

"""
April 8, 2025. 
I'm planning to write a paper focusing on the first DIC 14C measurements in Fiordland national park. 
It looks like we may have caught some seasonality in the CTD data, but first, I want to finish analyzing the DIC 14C data
from the Sonne and SFCS2405. 
I've learned some coding lessons through the tree-ring work that I'm going to try to implement into the workflow for this paper.

September 10, 2024
I'm editing/re-structuring this to make it more complete and clean for my talk and future writing of the paper or proposal based on this data;
some nice figures still exist in "Basic_Figures.py" and while these may work for my Hobart talk, I may change them eventually

August 21, 2024
This analysis is based on trying to understand the mixing of river and ocean waters in the Fiords, from cruise SFCS2405. See my Results powerpoint in the directory below;
H:\Science\Current_Projects/03_CCE_24_25/01_May_2024_Cruise\RESULTS. 
"""

"""
STEP1. 
Read in my data, and merge it with the AMS data straight from RLIMS to avoid any manual "copying" errors. 
"""

# READ IN SFCS2405 sampling data
df = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/02_Results_and_Data/DATA_PROCESSING_RAW.xlsx', sheet_name='Cruise_Data_Sheet_ALL', comment='#')
df = df[['My Station Name', 'Cruise Station Name','Latitude_N_decimal','Longitude_E_decimal','Bottom Depth (m)','Depth','Qflag','Sample','TP']]
dic = df.loc[((df['Sample'] == 'DIC') | (df['Sample'] == 'DIC Duplicate'))]

# read in data output from RLIMS 14C measurement of SFCS2405 data
tw3530 = pd.read_excel('H:/Science/Datasets/Fiordland/TW3530_export.xlsx')
tw3530 = tw3530.loc[tw3530['Samples::Sample Description'] == 'Fiordland DIC samples from SFCS2405'] # remove oxalics, kapunis, etc
df = dic.merge(tw3530, on='TP')

# Read in Sonne sampling data
sonne = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/S309_RV_Sonne_DIC/14C_samples_for_Christian_Lewis_GNS.xlsx', comment='#')



df.to_excel('H:/Science/Current_Projects/03_CCE_24_25/02_Results_and_Data/Finalized_Results/DI14C_FINAL.xlsx')