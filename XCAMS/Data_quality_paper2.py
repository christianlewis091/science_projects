import pandas as pd
import numpy as np
import warnings
import xlsxwriter
from datetime import date
warnings.simplefilter(action='ignore')
import plotly.express as px
import matplotlib.pyplot as plt
today = date.today()
from drawing import *

"""
Below are the descriptors that have been added to all data in the script "Data_quality_paper1.py"
['PHASE1_1-Char' 'PHASE1_Common_Repeats' 'PHASE1_Contains_TEST'
 'PHASE1_EA_XYZ' 'PHASE1_EmptyJobNotes' 'PHASE1_Only_Digits'
 'PHASE1_X_of_Y' 'PHASE2_13C_soft_filter' 'PHASE2_OK' 'PHASE2_Remove'
 'PHASE2_needs_discussion' 'PHASE2_softfilter' 'Phase4_3_sigma_out']

"""

df = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_4.csv')

b4 = len(df)
# IMMEDIATELY REMOVE ALL HARD AND SOFT FLAGS
df = df.loc[df['flag'] != 'X..']
df = df.loc[df['flag'] != '.X.']
after = len(df)
print(f"After removing both hard and soft flags, data went from original lenght of {b4} to {after}")
print()

x_0 = len(df)
maxTP = max(df['TW'])  # whats the max TW numbers so I can decide where to begin snipping on the next line?
minTP = min(df['TW'])
selectTP = minTP
df = df.loc[df['TW'] > selectTP]
x_05 = len(df)

# decide on what descriptiors I added last script to filter on
chosen_filters = ['PHASE1_Contains_TEST','Phase4_3_sigma_out','PHASE2_softfilter']
for item in chosen_filters:
    df = df.loc[df['CBL_Filtering_Category'] != item]
x_1 = len(df)

"""
Question 1: Am I able to re-create Albert's data without the removal of ANY points? 
Lets begin with his "Table 1" 
I'm going to recalculate RTS_bl and sigma_RTS_bl the same as his table 1

The logic is as follows: 
acid-alkali-acid → sealed-tube combustion → graphitisation = 40142/2 (& where 'EARun' == "Missing")
cellulose extraction → sealed-tube combustion → graphitisation = 40142/1 (& where 'EARun' == "Missing")
acid-alkali-acid → elemental-analyser combustion → graphitisation = 40142/2 (& where 'EARun' != "Missing")
cellulose extraction → elemental-analyser combustion → graphitisation = 40142/1 (& where 'EARun' != "Missing")
CO2 evolution from solid carbonate → graphitisation = 14047/1
CO2 evolution from dissolved carbonate → graphitisation = 14047/11
CO2 extraction from ambient air → graphitisation = 40430/3
graphitisation only - ? 
"""
#
# subset of data that are organic and SEALED TUBE
aaa_st_graph = df.loc[(df['New_R'] == '40142_2') & (df['EArun'] == 'Missing[]')]
cell_st_graph = df.loc[(df['New_R'] == '40142_1') & (df['EArun'] == 'Missing[]')]

# subset of data that are organic and EA
aaa_ea_graph = df.loc[(df['New_R'] == '40142_2') & (df['EArun'] != 'Missing[]')]
cell_ea_graph = df.loc[(df['New_R'] == '40142_1') & (df['EArun'] != 'Missing[]')]

# remaining subsets explained above
co2_dic = df.loc[(df['New_R'] == '14047_11')]
co2_carb = df.loc[(df['New_R'] == '14047_1')]
air = df.loc[(df['New_R'] == '40430_3')]

# now I can loop through the categories and calculate the statistucs
cats = [aaa_st_graph, cell_st_graph, aaa_ea_graph, cell_ea_graph, co2_carb, co2_dic, air]
process_abbreviations = ['AAA_ST_GR','CE_ST_GR','AAA_EA_GR','CE_EA_GR','EvolSolid-GR','EvolDIC', 'ExtrAir']
bl_rts = []
bl_rts_1sig = []
n = []
waiting_per = []
name = []
for cat in cats:
    x = cat['RTS']
    bl_rts.append(np.mean(x))
    bl_rts_1sig.append(np.std(x))
    n.append(len(x))
    waiting_per.append(180)

res = pd.DataFrame({"Name": process_abbreviations, "RTS_bl": bl_rts, "RTS_bl_1sigma": bl_rts_1sig, "Waiting Period": waiting_per, "n": n})

print(f"The dataset extended from TP# {minTP} to {maxTP}, but has snipped to only include after {selectTP}")
print(f"After filtering for TP#, data reduced from {x_0} to {x_05}.")
print()
print(f"After filtering on descriptors, data reduced from {x_05} to {x_1}.")
print(f"Currently the descriptor arguements that have been used to filter out data are: {chosen_filters}, and remember all data with X.. and .X. are removed as well")
print(res)
print("Dont forget to edit *waiting period* later in excel for airs to 360")
print()
print("But, what time period is albert using in his data? I end up with loads more than him. Its no wonder his blanks are lower with 10x less data.")
print("I can tell by playing around with the TP filtering that he probably only used the most recent ~60ish wheels in the simplified_rlims dataset.")
print("Setting variable of maxTP to *maxTP - 60* yields data very close to what albert has in his paper.")

draw_staggered_fish()

"""
Now I'm trying to recreate the plot in Albert's xslx called Fig1
C2 Travertine = 14047/2
LAC1 coral = 41347/2
LAA1 coral = 41347/3

We're going to find the data of each relative to their own MEAN
"""
print("It seems like there is a discrepancy in the time-span in which the data is being filtered upon. For instance, above, ")
print("it seems like a very short timespan since the data is sparse. However, if I use that same small timespan to filter on below, ")
print("I won't have nearly enough data to recreate Albert's plot for travertime for instance. I think for the paper, the time-frame")
print("needs to be consistent")
# create some arrays to store data
n = []
mean = []
stdev = []
wmean = []
sterr = []
chisq_red = []
concensus = []

rs = ['14047_2', '41347_2', '41347_3']
names = ['Travertine','LAC1','LAA']
markers = ['o', 'x', 's']
colors = ['black','dodgerblue','cyan']

fig = plt.figure(figsize=(8, 8)) # I'll make the plot while I loop...
size1 = 5
for i in range(0, len(rs)):
    subset = df.loc[df['New_R'] == rs[i]].reset_index(drop=True)
    # having issues with reading in this data for some reason, needs a format change
    subset["FracMOD"] = subset.FracMOD.astype(float)
    subset['FerrNOwtwNOsys'] = subset.FerrNOwtwNOsys.astype(float)
    n.append(len(subset))
    wmean.append(np.mean(subset["FracMOD"]))
    stdev.append(np.nanstd(subset['FracMOD']))
    sterr.append(np.nansum(1/(subset['FerrNOwtwNOsys']))**(-.5))

    fracmod_norm = subset["FracMOD"] / (np.mean(subset["FracMOD"]))  # normalize the data by the mean
    plt.errorbar(subset['TP'], fracmod_norm, yerr=subset['FerrNOwtwNOsys'], label=f"{names[i]}", markersize = size1, elinewidth=1, capsize=2, alpha=1, ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

plt.axhline(1, color='black', linewidth = 0.5)
plt.legend()
plt.show()









fig1_results = pd.DataFrame({"Name": names, "R": rs, "Mean": wmean, "1-sigma STD": stdev, "STD ERR": sterr, "n": n})
print(fig1_results)


