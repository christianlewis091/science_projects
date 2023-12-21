import pandas as pd
import numpy as np
import warnings
import xlsxwriter
from datetime import date
warnings.simplefilter(action='ignore')
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
today = date.today()
from drawing import *
import seaborn as sns


"""
Initially, I begin this file to try to recreate the results in ALbert's Fig1 and Table1. However, 
after talking to JT, it seems we're going to more or less re-vamp the paper. We're going to run the data from the 
past ten years and look at our long-term data quality. For this reason, we will not "aim" to recreate ALbert's data 
and we will expect it to be different. 

The goal of this script is to take output from Data_quality_paper1.py, which adds descriptors to the output from RLIMS, 
which we can filter on, and THIS file does the analytics (stats, making figures, etc). 

I want the output to be as follows: 
1. A dataframe / table of results regarding system blanks (ideally over time)
2. Residual plots of secondary starndards over time, ideally with some figures that are "publishable", looking at 
our most common secondaries overlaid in a plot using residuals. 
"""

"""
Below are the descriptors that have been added to all data in the script "Data_quality_paper1.py"
['PHASE1_1-Char' 'PHASE1_Common_Repeats' 'PHASE1_Contains_TEST'
 'PHASE1_EA_XYZ' 'PHASE1_EmptyJobNotes' 'PHASE1_Only_Digits'
 'PHASE1_X_of_Y' 'PHASE2_13C_soft_filter' 'PHASE2_OK' 'PHASE2_Remove'
 'PHASE2_needs_discussion' 'PHASE2_softfilter' 'Phase4_3_sigma_out']

THIS SECTION BELOW REMOVES DATA BASED ON FLAGGING, AND DESCRIPTORS
"""

df = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_4.csv')
b4 = len(df) # record the inital length of the data for de-bugging checks

df = df.loc[df['flag'] != 'X..'] # IMMEDIATELY REMOVE ALL HARD AND SOFT FLAGS
df = df.loc[df['flag'] != '.X.'] # IMMEDIATELY REMOVE ALL HARD AND SOFT FLAGS
after = len(df) # record the length again to see how much data has been removed so far

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
Question 1: How do our blanks look over time? Lets assess according to different pre-treatment techniques

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
aaa_st_graph = df.loc[(df['New_R'] == '40142_2') & (df['EArun'] == 'Missing[]')].sort_values(by=['TP']).reset_index(drop=True)
cell_st_graph = df.loc[(df['New_R'] == '40142_1') & (df['EArun'] == 'Missing[]')].sort_values(by=['TP']).reset_index(drop=True)

# subset of data that are organic and EA
aaa_ea_graph = df.loc[(df['New_R'] == '40142_2') & (df['EArun'] != 'Missing[]')].sort_values(by=['TP']).reset_index(drop=True)
cell_ea_graph = df.loc[(df['New_R'] == '40142_1') & (df['EArun'] != 'Missing[]')].sort_values(by=['TP']).reset_index(drop=True)

# remaining subsets explained above
co2_dic = df.loc[(df['New_R'] == '14047_11')].sort_values(by=['TP']).reset_index(drop=True)
co2_carb = df.loc[(df['New_R'] == '14047_1')].sort_values(by=['TP']).reset_index(drop=True)
air = df.loc[(df['New_R'] == '40430_3')].sort_values(by=['TP']).reset_index(drop=True)

# now I can loop through the categories and calculate the statistucs
cats = [aaa_st_graph, cell_st_graph, aaa_ea_graph, cell_ea_graph, co2_carb, co2_dic, air]
process_abbreviations = ['AAA_ST_GR','CE_ST_GR','AAA_EA_GR','CE_EA_GR','EvolSolid-GR','EvolDIC', 'ExtrAir']

# initialize arrays where the resultingd data can be stored
bl_rts = []
bl_rts_1sig = []
n = []
waiting_per = []
name = []
rolling_mean = []

# prepare the figure that will be populated below
fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=0.1, hspace=0.35)

# setting different toptions for colors
colors = sns.color_palette("mako", len(cats))
colors2 = sns.color_palette("rocket", len(cats))
colors = ['forestgreen','turquoise','darkgreen','teal','slateblue','darkorchid','cornflowerblue']
markers = ['o','s','D','*','^','<','>']

# set plot params
ymax_plot = 0.05

xtr_subsplot = fig.add_subplot(gs[0:1, 0:2]) # the first subplot will be the running average
plt.title('Moving Average')
for i in range(0, len(cats)): # loop through the categories
    # save the data for a table later
    cat = cats[i]
    x = cat['RTS']
    bl_rts.append(np.mean(x))
    bl_rts_1sig.append(np.std(x))
    n.append(len(x))
    waiting_per.append(180)

    # put the data into the first figure
    cat['MA'] = cat['RTS'].rolling(window=(int(len(cat)/3))).mean() # set the average length according to the length of data
    plt.scatter(cat['TP'], cat['RTS'], color=colors[i], alpha=0.25, marker=markers[i])
    plt.plot(cat['TP'], cat['MA'], color=colors[i], label=process_abbreviations[i])

plt.ylim(0.00, ymax_plot)
plt.ylabel('Ratio to Standard')
plt.xlabel('TP (chronological lab identifier)')
plt.legend()


# save the arrays into a dataframe
res = pd.DataFrame({"Name": process_abbreviations, "RTS_bl": bl_rts, "RTS_bl_1sigma": bl_rts_1sig, "Waiting Period": waiting_per, "n": n})


xtr_subsplot = fig.add_subplot(gs[0:1, 2:3]) # second subplot will be the scatter
plt.title('Full-Time Mean')
# in order for the colors to match the first plot, I'll need to do another loop
for i in range(0, len(res)):
    row = res.iloc[i]
    plt.errorbar(row['Name'], row['RTS_bl'], yerr=row['RTS_bl_1sigma'], marker=markers[i], color=colors[i])
#     plt.errorbar(row['Name'], row['RTS_bl'], yerr='RTS_bl_1sigma', marker=markers[i], color=colors[i])
plt.ylim(0.00, ymax_plot)
plt.yticks([], [])
plt.xticks(rotation=45)
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_2_output/Fig1.png',
            dpi=300, bbox_inches="tight")


print(f"The dataset extended from TP# {minTP} to {maxTP}, but has snipped to only include after {selectTP}")
print(f"After filtering for TP#, data reduced from {x_0} to {x_05}.")
print()
print(f"After filtering on descriptors, data reduced from {x_05} to {x_1}.")
print(f"Currently the descriptor arguements that have been used to filter out data are: {chosen_filters}, and remember all data with X.. and .X. are removed as well")
print(res)
print("Dont forget to edit *waiting period* later in excel for airs to 360")
print()
print("Later!!!! will have to re-reun after figuring out RLIMS export properly")
print("Later!!!! Add flagging parameter that any blanks worse than X are flagged")


df.to_csv('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_2_output/DF.csv')
draw_staggered_fish()





















































































