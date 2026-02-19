"""
Feb 18, 2026
Why does this file exist? It builds off of Data_Quality_Paper_2_2026_v1.
JCT wants me to calculate statistics for individual items (BHDamb, BHDspike), but ALSO
would like a sigbw for the WHOLE GROUP. I found this difficult to do all in one file,
although a better scientist of coder may have been able to with elegant pythoning. It will
be written out ugly but explicitly here below.
"""

"""
IMPORT STATEMENT
"""
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import os
from scipy import stats
import mplcursors

# """
# LINES 24-100 are a copy from Data_Quality_Paper_2_2026_v1!!!!!
#
# """
# def calc_delta_14C(FM, FM_err, colldate):
#     # delta_14C = ((FM*np.exp((1950-colldate)/8267))-1)*1000 # my written version
#     delta_14C =  1000*(FM*np.exp((1950-colldate)/8267)-1)
#     delta_14C_err = 1000*(FM_err*np.exp((1950-colldate)/8267))
#     return delta_14C, delta_14C_err
#
# # def calc_FM_from_d14C():
#
def rts_to_permille_for_errors(rts, colldate):
    rts_to_FM  = (np.sqrt(rts**2)/0.95)*0.98780499
    FM_to_permille = 1000*(rts_to_FM*np.exp((1950-1950)/8267))
    return FM_to_permille

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/12_manual_plotly_drop.xlsx', sheet_name= 'Whole Dataframe')
print(f"Dataframe length at t0 for this script: {len(df)}")
df = df.loc[df['Keep_Remove'] == 'Keep']
df.to_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/check1.xlsx') # wanted to check that TP 67815 was removed...
print(f"Dataframe length at t1, after selecting only !Keeps!: {len(df)}")


"""
Please find the scanned derivation of key formulas below in "I:\C14Data\Data Quality Paper\CBL_V4\Supporting Information and CoAuthor NOtes" by CBL
"""
#  Strongest check: try converting to numeric and see if anything fails
pd.to_numeric(df['RTS_corrected_error'], errors='raise')
pd.to_numeric(df['RTS_corrected'], errors='raise')
pd.to_numeric(df['DELTA 14C'], errors='raise')

"""
Below is some code copied from Data Quality 4.py but edited with more comments for clarity
"""
"""
I output all oxalics, alongside their preparation (sealed tube or flask). We were asked to only use data from
secondaries that use the flask OX, beacuse they're better. This code below adds the prep label onto the dataframe that
we're working with
"""
# September 12, merge with STD prep type: We only want air secondaries run with Flask OX
spt = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/flask_ox_label.xlsx')
spt = spt.drop_duplicates(subset='TP', keep='first') # get rid of duplicates on the prep type output from RLIMS
df = df.merge(spt, on='TP')
df.to_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/ox_prep_labels_added.xlsx')
print(f"Dataframe length at t2, after adding prep types: {len(df)}")


"""
Text from Data Quality Paper 2 2025:
I need to parse between the different types of FIRI pretreatments from albert's TABLES.xlsx and see if I can find the same difference
after getting rid of flagged data.
FIRI-D is cellulose pretreated.
FIRI-E is AAA
FIRI-I is AAA
TIRL-L only has 2 measurements in RLIMS so lets forget about this.
I'm going to EDIT the R numbers for those names which may have EA and ST to look at these differences. This will be shown below. "EA Combustion::Run Numner"
After spending a bunch of July 4, 2024 on this: I just have to manually go through and check the pre-treatments for all FIRIs that were in Alberts sheet

New notes:
Contrasting to above, we'll be changing things from here, see more notes as we go below.
The first change to the block below which will happen on excel, is that FIRI-F's will be manually added to the FIRI_edited excel sheet


"""
firilist = ['24889/4','24889/5','24889/9','26281/1','24889/7'] # here is the list of R numbers I want to check
firis = df.loc[(df['Job::R'].isin(firilist))]        # make a subset dataframe where these FIRIs are found
firis.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/firis.xlsx')  # write it to excel
firis = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/firis_edited.xlsx', comment='#') # I edited it by checking RLIMS. Read it back in
firis = firis[['TP','EA_ST','AAA_CELL']]  # drop columns to prep for merge
firis = firis.drop_duplicates(subset='TP', keep='first') # get rid of duplicates on the prep type output from RLIMS
df = df.merge(firis, on='TP', how='left')  # merge
df.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2026_output/mergecheck.xlsx') # output to recheck
print(f"Dataframe length at t3, after checking FIRI prep types and mergeing: {len(df)}")

"""
Now is where things will shift from the previous file.
We're going to do the bigger groupings of data to get sig_bw and chi2!
"""
# first I only want a sub-dataset of these R numbers we care about so its easier to view.
seconds = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_quality_paper_2_2025_FIRIsTogether\seconds.xlsx", comment='#')
rs = np.unique(seconds['R_number'])
df = df.loc[(df['Job::R'].isin(rs))]

df.to_excel(f"C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_3_2026_v1_output/subdataset_check.xlsx")

"""
Reading from here to save time! 
"""

df = pd.read_excel(f"C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_3_2026_v1_output/subdataset_check.xlsx")

"""
# I have to assign the weighted mean values calculated from the previous sheet to the groups here.
# This is required for chi2 and sig_bw
# see "C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Paper_2_2026_output\statistics_feb18_2026.xlsx" for the
calculated FM and FMerr which are the wmeans for the groups which will be added here below
"""

# add values calculated from last sheet, see directory above
df['fm_wmean'] = -999
df['fm_wmean_err'] = -999
df['Collection_Date'] = -999

df.loc[(df['Job::R'] == '40430/1'), 'fm_wmean'] = 1.03934531595233
df.loc[(df['Job::R'] == '40430/1'), 'fm_wmean_err'] = 0.00156026418798876
df.loc[(df['Job::R'] == '40430/1'), 'Collection_Date'] = 2013.759

df.loc[(df['Job::R'] == '40430/2'), 'fm_wmean'] = 0.935308071489587
df.loc[(df['Job::R'] == '40430/2'), 'fm_wmean_err'] = 0.00156244666842016
df.loc[(df['Job::R'] == '40430/1'), 'Collection_Date'] = 2013.759

air_r = ['40430/1','40430/2']
air_materials = df.loc[(df['Job::R'].isin(air_r)) & (df['preptype'] == 'FLASK')].copy()

"""
"""

df.loc[(df['Job::R'] == '41347/2'), 'fm_wmean'] = 0.668043918222837
df.loc[(df['Job::R'] == '41347/2'), 'fm_wmean_err'] = 0.0017483014606519
df.loc[(df['Job::R'] == '41347/2'), 'Collection_Date'] = 1991

df.loc[(df['Job::R'] == '41347/3'), 'fm_wmean'] = 0.558764422914354
df.loc[(df['Job::R'] == '41347/3'), 'fm_wmean_err'] = 0.00220641295895095
df.loc[(df['Job::R'] == '41347/3'), 'Collection_Date'] = 1991

df.loc[(df['Job::R'] == '26281/1'), 'fm_wmean'] = 0.203183828615025
df.loc[(df['Job::R'] == '26281/1'), 'fm_wmean_err'] = 0.00195897326437895
df.loc[(df['Job::R'] == '26281/1'), 'Collection_Date'] = 1991


inor_r = ['41347/2','41347/3','26281/1']
# LAC, LAA, and FIRI-L (whalebone)
inorganic_materials = df.loc[(df['Job::R'].isin(inor_r))].copy()

"""
"""
df.loc[(df['Job::R'] == '41347/12'), 'fm_wmean'] = 0.667417646314886
df.loc[(df['Job::R'] == '41347/12'), 'fm_wmean_err'] = 0.00200699452364937
df.loc[(df['Job::R'] == '41347/12'), 'Collection_Date'] = 1991

df.loc[(df['Job::R'] == '41347/13'), 'fm_wmean'] = 0.558842205119581
df.loc[(df['Job::R'] == '41347/13'), 'fm_wmean_err'] = 0.00267598505256026
df.loc[(df['Job::R'] == '41347/13'), 'Collection_Date'] = 1991

water_r = ['41347/12','41347/13']
#LAC, LAA waters
water_materials = df.loc[(df['Job::R'].isin(water_r))].copy()

"""
"""

df.loc[(df['Job::R'] == '24889/4'), 'fm_wmean'] = 0.568873252914933
df.loc[(df['Job::R'] == '24889/4'), 'fm_wmean_err'] = 0.00202390505881971
df.loc[(df['Job::R'] == '24889/4'), 'Collection_Date'] = 1991

df.loc[(df['Job::R'] == '24889/5'), 'fm_wmean'] = 0.229893607055364
df.loc[(df['Job::R'] == '24889/5'), 'fm_wmean_err'] = 0.00146866200228686
df.loc[(df['Job::R'] == '24889/5'), 'Collection_Date'] = 1991

df.loc[(df['Job::R'] == '24889/7'), 'fm_wmean'] = 1.10494260115128
df.loc[(df['Job::R'] == '24889/7'), 'fm_wmean_err'] = 1.10494260115128
df.loc[(df['Job::R'] == '24889/7'), 'Collection_Date'] = 1991

df.loc[(df['Job::R'] == '24889/9'), 'fm_wmean'] = 0.571824033726284
df.loc[(df['Job::R'] == '24889/9'), 'fm_wmean_err'] = 0.00219575194978921
df.loc[(df['Job::R'] == '24889/9'), 'Collection_Date'] = 1991


organic_r = ['24889/4','24889/5','24889/7','24889/9']

# FIRI-D, FIRI-E, FIRI-G, FIRI-I
organic_materials = df.loc[(df['Job::R'].isin(organic_r))].copy()


"""
Now we can run a similar set of lines as the previous script, but for the groups of data, and removing some 
calc's that won't work.
"""
datasets = [air_materials, inorganic_materials, water_materials, organic_materials]
names = ['air_materials', 'inorganic_materials', 'water_materials', 'organic_materials']

length = []
desc_arr = []
chi2_red_arr = []
sig_bw_pm_arr = []

for i in range(0, len(datasets)):


    # holdover from previous version
    df2 = datasets[i]

    """
    Append length
    """
    length.append(len(df2))


    """
    Append the group "name"
    """

    desc_arr.append(names[i])

    """
    CALCULATE RESIDUAL
    !!! In previous sheet, the residual is calculated using RTS. This is beacuse it was done before the FM calculation,
    which required sigbw. So we couldn't use FM until we had the wmean, which is required for the residual and the sig_bw (and the chi2)
    But it shouldn't matter since they are scaled similarly
    """

    df2['residual'] = ( df2['F_corrected_normed'] - df2['fm_wmean']) / df2['F_corrected_normed_error']


    """
    Step 1, calculate chi2 reduced
    """
    # calc chi2
    chi2_red_num = np.sum((df2['F_corrected_normed']-df2['fm_wmean'])**2/df2['F_corrected_normed_error']**2)
    chi2_red_denom = len(df2)-1 # subtract number of groups in degrees of freedom calc.
    chi2_red = chi2_red_num/chi2_red_denom
    chi2_red_arr.append(chi2_red)

    """
    calculate sigma_bw striaght up (This is the turnbull 2015 method) (if this doesn't work, its beacuse the sqrt function went negative because chi2 was less than 1)
    See Eqn at bottom of page 1 of scan file:///I:/C14Data/Data%20Quality%20Paper/CBL_V3/Data_Quality_Eqns_CBL_JCT.pdf
    """
    if chi2_red < 1:
        sigbw = 0
        print('I found a zero!')

    else:
        term2 = np.sqrt(chi2_red - 1)
        term1 = np.nanmean(df2['RTS_corrected_error'])
        sigbw = term1*term2

    colldate1 = df2['Collection_Date'].iloc[0]
    sig_bw_pm_arr.append(rts_to_permille_for_errors(sigbw, colldate1))

    """
    Draw a nice plot with residuals and FM's (we're not using D14C because the collection dates for FIRI are too difficult to pin down)...
    """

    # Residuals on the bottom
    rs_here = np.unique(df2['Job::R'])
    markers = ['o','D','X','s']
    colors = ['blue','green','red','black']

    for j in range(0,len(rs_here)):
        this_r = df2.loc[(df2['Job::R'] == rs_here[j])]

        plt.scatter(this_r['TP'], this_r['residual'], color=colors[j], linestyle='', marker=markers[j], label=f'{rs_here[j]}')
        plt.axhline(y=0, color='black')
    plt.legend()


    plt.tight_layout()

    """
    IF YOU WANT TO HOVER OVER TO CHECK, USE BOX BELOW
    """
    # Connect the mplcursors library to the plot
    # mplcursors.cursor(hover=True)
    # plt.show()
    """
    """

    plt.savefig(f"C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_3_2026_v1_output/mpl_output/{i}.png",
                dpi=300, bbox_inches="tight")
    plt.close()

output1 = pd.DataFrame({
                        'Description': desc_arr,
                        'Data Length (n)': length,
                        'Chi2 Reduced': chi2_red_arr,
                        'sigma_bw_in_pm': sig_bw_pm_arr,
                        })

output1.to_excel("C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_3_2026_v1_output/statistics_grouped.xlsx")








