"""
A new version of this file was created for 2026 (Data_Quality_Paper_2_2026) because of a large batch of changes
requested by Jocelyn. Specifically, the way we calculate and output data in Data_Quality_Paper_2_2025 will beome a problem
Specifically, I had been seperating R numbers based on pretreatments in Data_Quality_Paper 2, but then realized its alos required
to have statistics for the whole batch of data.
Now, adding different comparisons on top of that, we really need to generate individual datasets for each group.
This will allow us to do things faster and simpler, which seems to always be the case in hindsight.

In this script, we'll use df.loc to create individual datasets for each secondary standard, and their sub-categorizations
(i.e., FIRI-D (all), then FIRI-D AAA_EA, etc.


"""
import cursor

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

def calc_delta_14C(FM, FM_err, colldate):
    # delta_14C = ((FM*np.exp((1950-colldate)/8267))-1)*1000 # my written version
    delta_14C =  1000*(FM*np.exp((1950-colldate)/8267)-1)
    delta_14C_err = 1000*(FM_err*np.exp((1950-colldate)/8267))
    return delta_14C, delta_14C_err

# def calc_FM_from_d14C():

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
We'll create individual datasets based on each secondary and pretreatment split of each secondary that we're interested in
AND
We can do it in the order of the table that we'll create, to keep things streamlined later on. 
"""
"""
See r"C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_paper_2_2025_output\seconds.xlsx" for expected age calculations!!!
"""

kapuni = df.loc[(df['Job::R'] == '40699/1')].copy()
kapuni['Collection_Date'] = 1950
kapuni['Concensus_fm'] = .002


airdeadCO2 = df.loc[(df['Job::R'] == '40430/3')].copy()
airdeadCO2['Collection_Date'] = 2013.759
airdeadCO2['Concensus_fm'] = .002

bhdamb = df.loc[(df['Job::R'] == '40430/1')].copy()
bhdamb['Collection_Date'] = 2013.759
bhdamb['Concensus_fm'] = 1.0395

bhdspike = df.loc[(df['Job::R'] == '40430/2')].copy()
bhdspike['Collection_Date'] = 2013.759
bhdspike['Concensus_fm'] = 0.9352

bhdamb_flask = df.loc[(df['Job::R'] == '40430/1') & (df['preptype'] == 'FLASK')].copy()
bhdspike_flask = df.loc[(df['Job::R'] == '40430/2') & (df['preptype'] == 'FLASK')].copy()
bhdamb_flask['Collection_Date'] = 2013.759
bhdspike_flask['Collection_Date'] = 2013.759
bhdamb_flask['Concensus_fm'] = 1.0395
bhdspike_flask['Concensus_fm'] = 0.9352

carr_marb_carb = df.loc[(df['Job::R'] == '14047/1')].copy()
carr_marb_carb ['Collection_Date'] = 1950
carr_marb_carb ['Concensus_fm'] = .002

travertine_carb = df.loc[(df['Job::R'] == '14047/2')].copy()
travertine_carb['Collection_Date'] = 1950
travertine_carb['Concensus_fm'] = 0.4114

lac1carb = df.loc[(df['Job::R'] == '41347/2')].copy()
lac1carb['Collection_Date'] = 1991
lac1carb['Concensus_fm'] = 0.6662

laa1carb = df.loc[(df['Job::R'] == '41347/3')].copy()
laa1carb['Collection_Date'] = 1991
laa1carb['Concensus_fm'] = 0.5597

firi_l = df.loc[(df['Job::R'] == '26281/1')].copy()
firi_l['Collection_Date'] = 1991
firi_l['Concensus_fm'] = 0.2035

carr_marb_water = df.loc[(df['Job::R'] == '14047/11')].copy()
carr_marb_water['Collection_Date'] = 1950
carr_marb_water['Concensus_fm'] = .002

travertine_water = df.loc[(df['Job::R'] == '14047/12')].copy()
travertine_water['Collection_Date'] = 1950
travertine_water['Concensus_fm'] = 0.4114

lac1water = df.loc[(df['Job::R'] == '41347/12')].copy()
lac1water['Collection_Date'] = 1991
lac1water['Concensus_fm'] = 0.6662

laa1water = df.loc[(df['Job::R'] == '41347/13')].copy()
laa1water['Collection_Date'] = 1991
laa1water['Concensus_fm'] = 0.5597

# now the organics...
# kauri blanks
kauri_all = df.loc[((df['Job::R'] == '40142/1') | (df['Job::R'] == '40142/2'))].copy()
kauri_all['Collection_Date'] = 1950
kauri_all['Concensus_fm'] = .002

kauri_aaa = df.loc[(df['Job::R'] == '40142/2')].copy()
kauri_aaa['Collection_Date'] = 1950
kauri_aaa['Concensus_fm'] = .002

kauri_cell = df.loc[(df['Job::R'] == '40142/1')].copy()
kauri_cell['Collection_Date'] = 1950
kauri_cell['Concensus_fm'] = .002

kauri_aaa_ea = df.loc[((df['Job::R'] == '40142/2') & (df['EA_ST'] =='EA'))].copy()
kauri_aaa_st = df.loc[((df['Job::R'] == '40142/2') & (df['EA_ST'].isna()))].copy()
kauri_aaa_ea['Collection_Date'] = 1950
kauri_aaa_st['Collection_Date'] = 1950
kauri_aaa_ea['Concensus_fm'] = .002
kauri_aaa_st['Concensus_fm'] = .002

kauri_cell_ea = df.loc[((df['Job::R'] == '40142/1') & (df['EA_ST'] =='EA'))].copy()
kauri_cell_st = df.loc[((df['Job::R'] == '40142/1') & (df['EA_ST'].isna()))].copy()
kauri_cell_ea['Collection_Date'] = 1950
kauri_cell_st['Collection_Date'] = 1950
kauri_cell_ea['Concensus_fm'] = .002
kauri_cell_st['Concensus_fm'] = .002

# we're setting the FIRI-F R numbers to go into the FIRI D category too....
# will be simplest to first set all FIRI-F's to FIRI D...the line below accomplishes that
df.loc[(df['Job::R'] == '24889/6'),'Job::R'] = '24889/4'

firi_d_all = df.loc[(df['Job::R'] == '24889/4')].copy()
firi_d_all['Collection_Date'] = 1991
firi_d_all['Concensus_fm'] = 0.5688

firi_d_aaa_ea = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA')].copy()
firi_d_aaa_st = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna())].copy()
firi_d_cell_ea = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA')].copy()
firi_d_cell_st = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'].isna())].copy()
firi_d_cell = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose')].copy()
firi_d_aaa = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA')].copy()
firi_d_aaa_ea['Collection_Date'] = 1991
firi_d_aaa_st['Collection_Date'] = 1991
firi_d_cell_ea['Collection_Date'] = 1991
firi_d_cell_st['Collection_Date'] = 1991
firi_d_cell['Collection_Date'] = 1991
firi_d_aaa['Collection_Date'] = 1991
firi_d_aaa_ea['Concensus_fm'] = 0.5688
firi_d_aaa_st['Concensus_fm'] = 0.5688
firi_d_cell_ea['Concensus_fm'] = 0.5688
firi_d_cell_st['Concensus_fm'] = 0.5688
firi_d_cell['Concensus_fm'] = 0.5688
firi_d_aaa['Concensus_fm'] = 0.5688

firi_d_rpo = df.loc[(df['Job::R'] == '24889/14')].copy()
firi_d_rpo['Collection_Date'] = 1991
firi_d_rpo['Concensus_fm'] = 0.5688

firi_e_aaa_st = df.loc[(df['Job::R'] == '24889/5') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna())].copy()
firi_e_aaa_st['Collection_Date'] = 1991
firi_e_aaa_st['Concensus_fm'] = 0.2307

firi_g_all = df.loc[(df['Job::R'] == '24889/7')].copy()
firi_g_all['Collection_Date'] = 1991
firi_g_all['Concensus_fm'] = 0.8975

firi_g_aaa_ea = df.loc[(df['Job::R'] == '24889/7') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA')].copy()
firi_g_aaa_ea['Collection_Date'] = 1991
firi_g_aaa_ea['Concensus_fm'] = 0.8975

firi_g_aaa_st = df.loc[(df['Job::R'] == '24889/7') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna())].copy()
firi_g_aaa_st['Collection_Date'] = 1991
firi_g_aaa_st['Concensus_fm'] = 0.8975

firi_i_all = df.loc[(df['Job::R'] == '24889/9')].copy()
firi_i_all['Collection_Date'] = 1991
firi_i_all['Concensus_fm'] = 0.5722

firi_i_aaa_ea = df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA')].copy()
firi_i_aaa_ea['Collection_Date'] = 1991
firi_i_aaa_ea['Concensus_fm'] = 0.5722




firi_i_cell_ea = df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA')].copy()
firi_i_cell_ea['Collection_Date'] = 1991
firi_i_cell_ea['Concensus_fm'] = 0.5722

firi_i_aaa = df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='AAA')].copy()
firi_i_aaa['Collection_Date'] = 1991
firi_i_aaa['Concensus_fm'] = 0.5722

firi_i_cell = df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='Cellulose')].copy()
firi_i_cell['Collection_Date'] = 1991
firi_i_cell['Concensus_fm'] = 0.5722



"""
I'm going to see if it works and then add the FIRI's etc...
"""

datasets = [kapuni,airdeadCO2, bhdamb, bhdspike, bhdamb_flask, bhdspike_flask,
            carr_marb_carb, travertine_carb, lac1carb, laa1carb,
            carr_marb_water, travertine_water, lac1water, laa1water,
            firi_l,
            kauri_all,
            kauri_aaa, kauri_aaa_ea, kauri_aaa_st,
            kauri_cell, kauri_cell_ea, kauri_cell_st,
            firi_d_all, firi_d_aaa_ea, firi_d_aaa_st, firi_d_cell_ea, firi_d_cell_st, firi_d_cell, firi_d_aaa,
            firi_d_rpo,
            firi_e_aaa_st,
            firi_g_all, firi_g_aaa_ea, firi_g_aaa_st,
            firi_i_all, firi_i_aaa_ea, firi_i_cell_ea, firi_i_aaa, firi_i_cell]

names = ['KAPUNI','AIRDEADCO2','BHDAMB','BHDSPIKE','BHDAMB_FLASK','BHDSPIKE_FLASK',
         'CARR_MARB_CARB','TRAV_CARB','LAC1_CARB','LAA1_CARB',
         'CARR_MARB_WATER','TRAV_WATER','LAC1_WATER','LAA1_WATER',
         'FIRI_L',
         'KAURI_ALL',
         'KAURI_AAA','KAURI_AAA_EA','KAURI_AAA_ST',
         'KAURI_CELL','KAURI_CELL_EA','KAURI_CELL_ST',
         'FIRI_D_ALL', 'FIRI_D_AAA_EA','FIRI_D_AAA_ST','FIRI_D_CELL_EA','FIRI_D_CELL_ST', 'FIRI_D_CELL','FIRI_D_AAA',
         'FIRI_D_RPO',
         'FIRI_E_AAA_EA',
         'FIRI_G_ALL','FIRI_G_AAA_EA','FIRI_G_AAA_ST',
         'FIRI_I_ALL','FIRI_I_AAA_EA', 'FIRI_I_CELL_EA', 'FIRI_I_AAA','FIRI_I_CELL']


"""
lets loop through the R numbers and get means and stats assigned to each value in the database...
The loop will compare R numbers from the 'seconds.xlsx' with the R numbers from the dataframe
"""

# set output for plotly file later
outdir = r"C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/plotly_check"

# set inital value for wmean so i can calc residual later
df['wmean'] = -999

group_name = []
R_num = []
desc_arr = []
length = []
wmean_arr = []
straight_mean_arr = []
straight_mean_unc_arr = []
stdev_arr = []
sterr_arr = []
chi2_red_arr = []
sig_bw_straight = []
# sig_bw_calc = []
sig_tot_arr = []
wtw_err_arr =[]
sig_bw_backcalc = []
std_arr_2 = [] # manually using wmean
fm_arr = []
fm_err_arr = []
coll_date_arr = []
d14C_arr = []
d14C_err_arr = []

sig_bw_pm_arr = []
sig_ams_pm_arr = []
sig_total_pm_arr = []

for i in range(0, len(datasets)):

    # Create figure and 2 vertical subplots
    fig, axs = plt.subplots(2, 1, figsize=(6, 8), sharex=True)  # 3 rows, 1 column

    # holdover from previous version
    df2 = datasets[i]

    """
    Append the R number
    """
    this_r = df2['Job::R'].iloc[0]
    R_num.append(this_r)

    """
    Append the group "name"
    """

    desc_arr.append(names[i])


    """
    Append length
    """
    length.append(len(df2))


    """
    The weighted mean comes from Albert's original version of the paper. I've copied his formula here which comes from
    #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    CHANGING ALL TO RTS SPACE. This makes extraneous uncertaitny calculation work better, see below.
    """
    # renaming as holdover from previous version
    subset1 = df2

    wmean_num = np.sum(subset1['RTS_corrected']/subset1['RTS_corrected_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    wmean_dem = np.sum(1/subset1['RTS_corrected_error']**2)
    wmean = wmean_num / wmean_dem
    wmean_arr.append(wmean)


    # We've lost the capability to do this in this type of loop where we've disconnected ourselves from the main dataset and recreated smaller datasets using .loc
    # df.loc[df['Job::R'] == rs[i], 'wmean'] = wmean

    """
    Calculate residual
    """
    subset1['residual'] = ( subset1['RTS_corrected'] - wmean ) / subset1['RTS_corrected_error']
    # subset1 = subset1.loc[subset1['residual'].notna()]

    straight_mean_unc = np.nanmean(subset1['RTS_corrected_error'])
    straight_mean_unc_arr.append(straight_mean_unc)


    """
    Calculate and append the standard deviation
    """
    std1 = np.std(subset1['RTS_corrected'])
    stdev_arr.append(std1)


    # doing stdev manually
    a1 = np.sum((subset1['RTS_corrected'] - wmean)**2)
    a2 = a1/len(subset1)
    a3 = np.sqrt(a2)
    std_arr_2.append(a3)


    sterr_arr.append(np.sum(1/(subset1['RTS_corrected']**2))**-0.5)

    """
    Now we shift to thinking about the uncertainty budget.
    We're going to calculate the uncertainty budget in RTS space.
    The uncertainty comes from
    1. the RTS error
    2. the blank error
    3. extraneous error (wheel to wheel error (WTW) in RLIMS) or sigma_bw (uncertainty between wheels) in (Turnbull 2015)
    Turnbull, Jocelyn C., Albert Zondervan, Johannes Kaiser, Margaret Norris, Jenny Dahl, Troy Baisden, and Scott Lehman.
    "High-precision atmospheric 14CO2 measurement at the Rafter Radiocarbon Laboratory." Radiocarbon 57, no. 3 (2015): 377-388.

    In RLIMS, the term "RTS_corrected_error" contains the quadriture error of both the RTS error and blank error.
    See "I:\C14Data\Data Quality Paper\CBL_V3\DataQualityEqns_JCT_CBL.pdf"

    So what we need to deal with, is the extraneous error, WTW or sigma_bw (all mean the same thing...)
    In my dicussions with JCT today, we decided we're happy with the derivation and implementation of equatinos on the file in the directory above

    Here is the order of operations:
    method 1.
    a. calculate chi2 in RTS space for each R number of interest (DONE)
    b. compare that chi2 value to 1
    c. calculate sigma_bw "straight up" (use the eqn on bottom of page 1 of my scan)
    method 2.
    d. find uncertainty of long-term repeatability (std-deviation)
    e. assume this stddev is sigma_total, and solve for sigma_bw in last square root eqn on the document (sigma total equation).
    The two methods should be equivalent.
    f. Now take sigma_tot (from long-term repeatability or from calculated, we'll see) and calculate F_corrected_normed_error.

    Its November 11, 2025.
    I've had further conversations with JCT following our derivations of sigma_bw, and the two ways to do it.
    See, the two ways to do it yield slightly different output beacuse they end up with slightly different formulas.
    "I:\C14Data\Data Quality Paper\CBL_V3\Data_Quality_Eqns_CBL_JCT_part2.pdf" See here.
    So, after discussing this on Nov 11, 2025, at lunch, we've decided to simply use the eqn from Jocelyn's 2015 paper.

    After this, I've done some cleaning up below, only keeping the calculations that are essential, so that the final
    output is most similar to what will be published.


    """
    """
    Step 1, calculate chi2 reduced
    """
    # calc chi2
    chi2_red_num = np.sum((subset1['RTS_corrected']-wmean)**2/subset1['RTS_corrected_error']**2)
    chi2_red_denom = len(subset1)-1 # subtract number of groups in degrees of freedom calc.
    chi2_red = chi2_red_num/chi2_red_denom
    chi2_red_arr.append(chi2_red)

    """
    Step 2, calculate sigma_bw striaght up (This is the turnbull 2015 method) (if this doesn't work, its beacuse the sqrt function went negative because chi2 was less than 1)
    See Eqn at bottom of page 1 of scan file:///I:/C14Data/Data%20Quality%20Paper/CBL_V3/Data_Quality_Eqns_CBL_JCT.pdf
    """
    if chi2_red < 1:
        sigbw = 0
        print('I found a zero!')

    else:
        term2 = np.sqrt(chi2_red - 1)
        term1 = np.nanmean(subset1['RTS_corrected_error'])
        sigbw = term1*term2

    sig_bw_straight.append(sigbw)

    """
    Step 3, what is the total uncertainty using this new sigma_bw?
    """

    sig_tot1 = np.sqrt(term1**2 + sigbw**2)
    sig_tot_arr.append(sig_tot1)


    """
    What is the WTWerror if we calculate it using sigma_bw, and how does it compare with the wheel to wheel error that is in use?
    """

    wtw_err = sigbw/(wmean*0.01)
    wtw_err_arr.append(wtw_err)


    """
    Conversion to Fraction modern
    RLIMS EQN: If(IsEmpty(rts_stds_av) = False; (RTS_corrected / (Standard Specific Activity Constant * rts_stds_av)) *( ((1 + delta13C_stds_av/ 1000) / (1 + delta13C_In_Calculation / 1000)) ^Normalization_exp_factor )* Standard 13C Value Constant;"")
    # The last term is the 13C value constant, a go-between for conventions - its so confusing
    """

    F_corrected_normed = (wmean/0.95)*0.98780499 #wmean converted to FM
    F_corrected_normed_error = (np.sqrt(term1**2 + sigbw**2)/0.95)*0.98780499
    fm_arr.append(F_corrected_normed)
    fm_err_arr.append(F_corrected_normed_error)
    """
    IMPORTANT NOTE!
    Feb 19, 2025. 
    The points and error bars that appear on the plots are F_corrected_normed that was output from RLIMS!
    We re-calculate that metric and its uncertainty above because we want to re-calculate sigbw, which is wrapped up in 
    the F_corrected_normed_error equation. But at this point, the actual values and error bars on the plots represent the orignal RLIMS values, 
    only the summary data table will reflect the final updated sigbw!!!!!!
    """

    """
    Conversion to D14C
    """
    colldate1 = subset1['Collection_Date'].iloc[0]
    delta_14C =  1000*(F_corrected_normed*np.exp((1950-colldate1)/8267)-1)
    delta_14C_err = 1000*(F_corrected_normed_error*np.exp((1950-colldate1)/8267))
    d14C_arr.append(delta_14C)
    d14C_err_arr.append(delta_14C_err)

    """
    Above we have the AMS uncertainty, the sigma_bw,and the total uncertainty all in RTS space,
    I want them converted to per mille, to be more comparable to Turnbull et al., 2015's 1.3 per mil AMS uncertainty
    """

    sig_bw_pm_arr.append(rts_to_permille_for_errors(sigbw, colldate1))
    sig_ams_pm_arr.append(rts_to_permille_for_errors(term1, colldate1))
    sig_total_pm_arr.append(rts_to_permille_for_errors(sig_tot1, colldate1))


    """
    Draw a nice plot with residuals and FM's (we're not using D14C because the collection dates for FIRI are too difficult to pin down)...
    """

    # Residuals on the bottom
    axs[1].scatter(subset1['TP'], subset1['residual'], color='black', linestyle='')
    axs[1].axhline(y=0, color='black')

    # Second subplot
    subset1['F_corrected_normed'] = pd.to_numeric(df['F_corrected_normed'], errors="coerce")
    subset1['F_corrected_normed_error'] = pd.to_numeric(df['F_corrected_normed_error'], errors="coerce")
    subset1['TP'] = pd.to_numeric(df['TP'], errors="coerce")
    axs[0].axhline(y=F_corrected_normed, color='black') # see above, I convert wmean to FM space
    concval = subset1['Concensus_fm'].iloc[0]
    axs[0].axhline(y=concval, color='red', alpha=0.5)

    axs[0].errorbar(subset1['TP'], subset1['F_corrected_normed'], yerr=subset1['F_corrected_normed_error'], color='black', linestyle='', label = f'{names[i]}', marker='o')
    axs[0].legend()
    axs[1].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
    axs[0].set_ylabel('Fraction Modern')

    stats_text = (
        f"$n$ = {len(df2)}\n"
        f"$\\chi^2 red$ = {chi2_red:.2f}\n"
        f"wmean = {F_corrected_normed:.4f}"
    )

    axs[0].text(
        0.05, 0.95,                # position (relative axes coords)
        stats_text,
        transform=axs[0].transAxes,
        fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
    )

    plt.tight_layout()

    """
    IF YOU WANT TO HOVER OVER TO CHECK, USE BOX BELOW
    """
    # Connect the mplcursors library to the plot
    # mplcursors.cursor(hover=True)
    # plt.show()
    """
    """

    plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_paper_2_2026_output/mpl_output/{i}.png',
                dpi=300, bbox_inches="tight")
    plt.close()

"""
IN 12_MANUAL_PLOTLY DROP I went thorugh and flagged some data where it looks like there were clear outliers. 
Some of the data sets are just so scattered that its too chaotic to try to flag, but such was done for ALL R numbers 
in the data set. 

At this stage, I'll potentally add MORE TP's to that list, specifically for secondaries that we care about in this paper. 
Then I'll re-run both scripts until we're happy

Such TO's are: 
69556 (A BHD AMB THAT IS NEXT TO SOME OTHER TP's that were removed! 
78656 (another BHD AMB that is low) 
68328 BHDSPIKE too high
69558 BHDSPIKE too high
71016 (travertine carbonate has huge error bars) 
72524 Travertine water is super low
72918 FIRI D too low
62921 FIRI I is really low...

This will be reflected in Data_Quality_Paper1.py
"""


    # # use plotly created now for next manual filtering step (see later)
    # # set output for plotly file later
    # outdir = r"C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2026_output/plotly/"
    # fig = px.scatter(subset1, x="TP", y='residual', error_y='TP', hover_data=["TP"],title=f"R = {names[i]}")
    # outfile = os.path.join(outdir, f"{names[i]}.html")
    # # Save as interactive HTML
    # fig.write_html(outfile)


output1 = pd.DataFrame({'R_number': R_num,
                        'Description': desc_arr,
                        'Data Length (n)': length,
                        # 'RTS (wmean)': wmean_arr,
                        # 'RTS_err (mean)': straight_mean_unc_arr,
                        # 'sigma_AMS': sig_ams_pm_arr,
                        # 'Standard Deviation': stdev_arr,
                        # 'Standard Deviation w Weighted mean': std_arr_2,
                        # 'Standard Error': sterr_arr,
                        'Chi2 Reduced': chi2_red_arr,
                        # 'Sigma_bw, Straight': sig_bw_straight,
                        'sigma_bw_in_pm': sig_bw_pm_arr,
                        # 'Sigma_total using Sigma_bw straight':sig_tot_arr,
                        'Fraction Modern': fm_arr,
                        'Fraction Modern Err':fm_err_arr,
                        # 'Calcd Wheel to Wheel Error': wtw_err_arr,
                        # 'Collection Date': coll_date_arr,
                        'D14C': d14C_arr,
                        'D14C_err': d14C_err_arr,
                        # 'sigma_total_converted_to_pm': sig_total_pm_arr
                        })


# NOW RUN SOME T-TESTS BEFORE OUTPUTTING THE RESULTS!
results_lines = []

# EA versus ST shown via FIRI-D's
t1, p1 = stats.ttest_ind(firi_d_cell_ea['F_corrected_normed'], firi_d_cell_st['F_corrected_normed'])
results_lines.append(
    f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_D_CELL_EA and FIRI_D_CELL_ST. Results <0.05 shows there is no observable difference")

# EA versus ST shown via FIRI-G's
t1, p1 = stats.ttest_ind(firi_g_aaa_ea['F_corrected_normed'], firi_g_aaa_st['F_corrected_normed'])
results_lines.append(
    f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_G_CELL_EA and FIRI_G_CELL_ST. Results <0.05 shows there is no observable difference")

results_lines.append('#The results above show that there is no observable difference between EA and ST for organic pretreatments. Since thats settled, we can recombined all and do t-tests with the AAA and Cell main groupings'
)

# CELL vs AAA using FIRI D
t1, p1 = stats.ttest_ind(firi_d_cell['F_corrected_normed'], firi_d_aaa['F_corrected_normed'])
results_lines.append(
    f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_D_CELL and FIRI_D_AAA. Results <0.05 shows there is no observable difference")

# CELL vs AAA using FIRI I
t1, p1 = stats.ttest_ind(firi_i_aaa['F_corrected_normed'], firi_i_cell['F_corrected_normed'])
results_lines.append(
    f"The results are t={t1:.3f} and p={p1:.4f} for FIRI_I_CELL and FIRI_I_AAA. Results <0.05 shows there is no observable difference")


results_df = pd.DataFrame({"T-test Results": results_lines})

output_dir = (f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2026_output/statistics.xlsx')

# Write to Excel
with pd.ExcelWriter(output_dir, engine="openpyxl", mode="w") as writer:
    output1.to_excel(writer, sheet_name="Stats Table", index=False)
    results_df.to_excel(writer, sheet_name="T-test results", index=False)
