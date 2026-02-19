"""
WHAT IS THIS FILE:
An edited version of "Data_quality_paper_2_2025.py but to get data without the FIRI's and such separated by pretreatment.

"""
from re import error

"""
IMPORT STATEMENT
"""
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import os

def calc_delta_14C(FM, FM_err, colldate):
    # delta_14C = ((FM*np.exp((1950-colldate)/8267))-1)*1000 # my written version
    delta_14C =  1000*(FM*np.exp((1950-colldate)/8267)-1)
    delta_14C_err = 1000*(FM_err*np.exp((1950-colldate)/8267))
    return delta_14C, delta_14C_err

def rts_to_permille_for_errors(rts, colldate):
    rts_to_FM  = (np.sqrt(rts**2)/0.95)*0.98780499
    FM_to_permille = 1000*(rts_to_FM*np.exp((1950-1950)/8267))
    return FM_to_permille


df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/12_manual_plotly_drop.xlsx', sheet_name= 'Whole Dataframe')
print(f"Dataframe length at t0 for this script: {len(df)}")
df = df.loc[df['Keep_Remove'] == 'Keep']
df.to_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_quality_paper_2_2025_FIRIsTogether/check1.xlsx') # wanted to check that TP 67815 was removed...
print(f"Dataframe length at t1, after selecting only !Keeps!: {len(df)}")

"""
Please find the scanned derivation of these formulas in place TBD by CBL
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
df.to_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_quality_paper_2_2025_FIRIsTogether/ox_prep_labels_added.xlsx')
print(f"Dataframe length at t2, after adding prep types: {len(df)}")

"""
I need to parse between the different types of FIRI pretreatments from albert's TABLES.xlsx and see if I can find the same difference
after getting rid of flagged data.
FIRI-D is cellulose pretreated.
FIRI-E is AAA
FIRI-I is AAA
TIRL-L only has 2 measurements in RLIMS so lets forget about this.
I'm going to EDIT the R numbers for those names which may have EA and ST to look at these differences. This will be shown below. "EA Combustion::Run Numner"
After spending a bunch of July 4, 2024 on this: I just have to manually go through and check the pre-treatments for all FIRIs that were in Alberts sheet
"""
firilist = ['24889/4','24889/5','24889/9','26281/1','24889/7'] # here is the list of R numbers I want to check
firis = df.loc[(df['Job::R'].isin(firilist))]        # make a subset dataframe where these FIRIs are found
firis.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_quality_paper_2_2025_FIRIsTogether/firis.xlsx')  # write it to excel
firis = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/firis_edited.xlsx', comment='#') # I edited it by checking RLIMS. Read it back in
firis = firis[['TP','EA_ST','AAA_CELL']]  # drop columns to prep for merge
firis = firis.drop_duplicates(subset='TP', keep='first') # get rid of duplicates on the prep type output from RLIMS
df = df.merge(firis, on='TP', how='left')  # merge
df.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_quality_paper_2_2025_FIRIsTogether/mergecheck.xlsx') # output to recheck
print(f"Dataframe length at t3, after checking FIRI prep types and mergeing: {len(df)}")

# # edit the R numbers to fit that of "seconds.xlsx" and prep for the mathematics below:
# df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/4_AAA_EA'
# df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna()), 'Job::R'] = '24889/4_AAA_ST'
# df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/4_CELL_EA'
# df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'].isna()), 'Job::R'] = '24889/4_CELL_ST'
#
# df.loc[(df['Job::R'] == '24889/5') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/5_AAA_EA'
# df.loc[(df['Job::R'] == '24889/5') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna()), 'Job::R'] = '24889/5_AAA_ST'
# df.loc[(df['Job::R'] == '24889/5') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/5_CELL_EA'
# df.loc[(df['Job::R'] == '24889/5') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'].isna()), 'Job::R'] = '24889/5_CELL_ST'
#
# df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/9_AAA_EA'
# df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna()), 'Job::R'] = '24889/9_AAA_ST'
# df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/9_CELL_EA'
# df.loc[(df['Job::R'] == '24889/9') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'].isna()), 'Job::R'] = '24889/9_CELL_ST'
#
# df.loc[(df['Job::R'] == '26281/1') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA'), 'Job::R'] = '26281/1_AAA_EA'
# df.loc[(df['Job::R'] == '26281/1') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna()), 'Job::R'] = '26281/1_AAA_ST'
# df.loc[(df['Job::R'] == '26281/1') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA'), 'Job::R'] = '26281/1_CELL_EA'
# df.loc[(df['Job::R'] == '26281/1') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'].isna()), 'Job::R'] = '26281/1_CELL_ST'
#
# df.loc[(df['Job::R'] == '24889/7') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/7_AAA_EA'
# df.loc[(df['Job::R'] == '24889/7') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna()), 'Job::R'] = '24889/7_AAA_ST'
# df.loc[(df['Job::R'] == '24889/7') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/7_CELL_EA'
# df.loc[(df['Job::R'] == '24889/7') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'].isna()), 'Job::R'] = '24889/7_CELL_ST'
#
# # edit similarly for some blank materials
# df.loc[(df['Job::R'] == '40142/2') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA'), 'Job::R'] = '40142/2_AAA_EA'
# df.loc[(df['Job::R'] == '40142/2') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna()), 'Job::R'] = '40142/2_AAA_ST'
# df.loc[(df['Job::R'] == '40142/1') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA'), 'Job::R'] = '40142/1_CELL_EA'
# df.loc[(df['Job::R'] == '40142/1') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'].isna()), 'Job::R'] = '40142/1_CELL_ST'

#make distinction between pre and post flask ox according to JCT comments September 11, 2024
# df.loc[(df['Job::R'] == '40430/2') & (df['preptype'] == 'FLASK') & (df['TW'] >= 3211) & (df['TW'] <= 3533), 'Job::R'] = '40430/2_flask'
# df.loc[(df['Job::R'] == '40430/1') & (df['preptype'] == 'FLASK') & (df['TW'] >= 3211) & (df['TW'] <= 3533), 'Job::R'] = '40430/1_flask'
# #
"""
add collection dates for secondaries where its listed: 
Two notes here: 
Collection date are extremely poorly documented so we're going to move forward with plottingin FM. 
Secondly, citations for my investigation into collectin dates is found in a column here  
r"C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_paper_2_2025_output\seconds.xlsx"
"""
# "C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_2_2025_output\seconds.xlsx"
# df['Collection_Date'] = -999
# df.loc[(df['Job::R'] == '40430/2_flask'),'Collection_Date'] = 2013
# df.loc[(df['Job::R'] == '40430/1_flask'),'Collection_Date'] = 2013
# df.loc[(df['Job::R'] == '14047/2'),'Collection_Date'] = 1950
# df.loc[(df['Job::R'] == '14047/12'),'Collection_Date'] = 1950
#
# df.loc[(df['Job::R'] == '24889/4_AAA_EA'),'Collection_Date'] = 1950
# df.loc[(df['Job::R'] == '24889/4_AAA_ST'),'Collection_Date'] = 1950
# df.loc[(df['Job::R'] == '24889/4_CELL_EA'),'Collection_Date'] = 1950
# df.loc[(df['Job::R'] == '24889/4_CELL_ST'),'Collection_Date'] = 1950
# df.loc[(df['Job::R'] == '24889/14'),'Collection_Date'] = 1950
#
# df.loc[(df['Job::R'] == '24889/14'),'Collection_Date'] = 1991
# df.loc[(df['Job::R'] == '24889/4_AAA_EA'),'Collection_Date'] = 1991
# df.loc[(df['Job::R'] == '24889/4_AAA_ST'),'Collection_Date'] = 1991
# df.loc[(df['Job::R'] == '24889/4_CELL_EA'),'Collection_Date'] = 1991
# df.loc[(df['Job::R'] == '24889/4_CELL_ST'),'Collection_Date'] = 1991
#
# df.loc[(df['Job::R'] == '41347/12'),'Collection_Date'] = 1991
# df.loc[(df['Job::R'] == '41347/13'),'Collection_Date'] = 1991
# df.loc[(df['Job::R'] == '41347/2'),'Collection_Date'] = 1991
# df.loc[(df['Job::R'] == '41347/3'),'Collection_Date'] = 1991

"""
Below I read this file in which tells me which R numbers I care about. 
"""
# # data with the secondaries to filter on: THIS LINE IMPORTS THE CONCENSUS VALUES
# need to read the new excel file with the FIRI's not adjusted for seperation by pretreatment
df2 = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_quality_paper_2_2025_FIRIsTogether\seconds.xlsx", comment='#')
rs = np.unique(df2['R_number'])

"""
lets loop through the R numbers and get means and stats assigned to each value in the database...
The loop will compare R numbers from the 'seconds.xlsx' with the R numbers from the dataframe
"""

# set output for plotly file later
outdir = r"C:/Users/clewis/IdeaProjects/GNS/xcams/Data_quality_paper_2_2025_FIRIsTogether/plotly_check"

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

for i in range(0, len(rs)):

    # Create figure and 3 vertical subplots
    fig, axs = plt.subplots(2, 1, figsize=(6, 8), sharex=True)  # 3 rows, 1 column

    """
    Append the R number 
    """
    subset1 = df.loc[df['Job::R'] == rs[i]]
    this_r = rs[i]
    R_num.append(rs[i])

    """
    Append the group "name"
    """
    # I later learn that this isn't the way to do this! Use iloc, as shown below!!!!
    group = df2.loc[df2['R_number'] == rs[i]].reset_index(drop=True)
    name = group['Name']
    name = name[0]
    group_name.append(np.unique(group['Group']).astype(str))


    desc1 = group['Name'].iloc[0]
    desc_arr.append(desc1)

    colldate1 = group['Collection Date'].iloc[0]
    coll_date_arr.append(colldate1)

    """
    Append D14C data
    """
    # colldate = group['Collection Date'].astype(str)
    # colldate = colldate[0]
    # if colldate != 'No collection date':
    #     del14C.append(np.nanmean(subset1['DELTA 14C']))
    #     del14Cstd.append(np.nanstd(subset1['DELTA 14C']))
    # else:
    #     del14C.append(-999)
    #     del14Cstd.append(-999)

    """
    Append length
    """
    length.append(len(subset1))

    """
    The weighted mean comes from Albert's original version of the paper. I've copied his formula here which comes from 
    #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    CHANGING ALL TO RTS SPACE. This makes extraneous uncertaitny calculation work better, see below. 
    """
    wmean_num = np.sum(subset1['RTS_corrected']/subset1['RTS_corrected_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    wmean_dem = np.sum(1/subset1['RTS_corrected_error']**2)
    wmean = wmean_num / wmean_dem
    wmean_arr.append(wmean)

    df.loc[df['Job::R'] == rs[i], 'wmean'] = wmean

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
    Step 3, what is the sigma_bw if we back calculate it using eqn sigma_tot = sqrt(sigma_ams^2 + sigma_bw^2), 
    Assumnig that sugma_tot = stdev
    # REMOVED SEE NOVEMBER 11 NOTE ABOVE
    """

    # sig_bw_backcalc1 = np.sqrt(a3**2 - term1**2)
    # sig_bw_backcalc.append(sig_bw_backcalc1)

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

    F_corrected_normed = (wmean/0.95)*0.98780499
    F_corrected_normed_error = (np.sqrt(term1**2 + sigbw**2)/0.95)*0.98780499
    fm_arr.append(F_corrected_normed)
    fm_err_arr.append(F_corrected_normed_error)

    """
    Conversion to D14C
    """

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

    axs[0].errorbar(subset1['TP'], subset1['F_corrected_normed'], yerr=subset1['F_corrected_normed_error'], color='black', linestyle='', label = f'{rs[i]}', marker='o')
    axs[0].legend()
    axs[1].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
    axs[0].set_ylabel('Fraction Modern')
    plt.tight_layout()

    plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS/xcams\Data_quality_paper_2_2025_FIRIsTogether/mpl_output/{i}.png',
                dpi=300, bbox_inches="tight")
    plt.close()


output1 = pd.DataFrame({'R_number': R_num,
                        'Group':group_name,
                        'Description': desc_arr,
                        'Data Length (n)': length,
                        'RTS (wmean)': wmean_arr,
                        'RTS_err (mean)': straight_mean_unc_arr,
                        'sigma_AMS': sig_ams_pm_arr,
                        'Standard Deviation': stdev_arr,
                        'Standard Deviation w Weighted mean': std_arr_2,
                        'Standard Error': sterr_arr,
                        'Chi2 Reduced': chi2_red_arr,
                        'Sigma_bw, Straight': sig_bw_straight,
                        'sigma_bw_in_pm': sig_bw_pm_arr,
                        'Sigma_total using Sigma_bw straight':sig_tot_arr,
                        'Fraction Modern': fm_arr,
                        'Fraction Modern Err':fm_err_arr,
                        'Calcd Wheel to Wheel Error': wtw_err_arr,
                        'Collection Date': coll_date_arr,
                        'D14C': d14C_arr,
                        'D14C_err': d14C_err_arr,
                        'sigma_total_converted_to_pm': sig_total_pm_arr

                        # 'Sigma Between Wheels, Calc': sig_bw_calc
                        # 'Optd Chi2': opt_chi,
                        # 'Sigma Residual': sig_res_arr,
                        # 'Sigma_FM': FracMODerr_arr,
                        # 'Sigma_blank': mcc_err_arr,
                        # 'Delta 14C': del14C,
                        # 'Delta 14C std': del14Cstd
                        })

df.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_quality_paper_2_2025_FIRIsTogether/df_out_from_DQ_2_2025.xlsx')

# # output1['sigma_total_FM'] = np.sqrt(output1['Sigma_FM']**2 + output1['Sigma_blank']**2 + (output1['Sigma Residual']**2)*(output1['FM (wmean)']**2))
# # october 14 2024 sigma_blank removed from totla uncertainty budget
# output1['sigma_total_FM'] = np.sqrt(output1['Sigma_FM']**2 + (output1['Sigma Residual']**2)*(output1['FM (wmean)']**2))
# output1['sigma_total_CRA'] = 8033 * (output1['Sigma_FM']/output1['FM (wmean)'])
# output1['CRA (from FM wmean)'] = -8033 * np.log(output1['FM (wmean)'])
#
# # add some of the metadata from the secondary sheet.
# df2 = df2[['Name','Collection Date','R_number','Expected FM','Expected Age (CRA)','Expected Age Delta14C']]
# output1 = output1.merge(df2, on='R_number')

# do this in excel beacuse of errors from those without collection dates.
# output1['Delta14C'] = ((output1['FM (wmean)']*np.exp(1950/output1['Collection Date']))-1)*1000

output1.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_quality_paper_2_2025_FIRIsTogether/statistics.xlsx')
# TODO make some plots like JCT's 2015 paper and then we can carry on writing!!!




# OLD CLODE
#
#
# """
# Please find the scanned derivation of these formulas in place TBD by CBL
# """
# #  Strongest check: try converting to numeric and see if anything fails
# pd.to_numeric(df['RTS_corrected_error'], errors='raise')
# pd.to_numeric(df['RTS_corrected'], errors='raise')
#
# # No weird stuff found in the data
# # TODO adapt work from "C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Paper_OLD\Data_quality_Paper_4.py"
# # TODO to recalculate sigma_res to get rid of WTW error
# """
# Step 3, calculate sigma_bw from sigma_total equation
# """
# num1 = np.sqrt(std1**2 - term1**2)
# den1 = straight_mean*0.01 # """ Not sure if I should be using weighted mean or straight mean for denominator..."""
# sig_bw_calc.append(num1/den1)

# mcc_err_arr.append(np.nanmean(subset1['MCCerr']))
# FracMODerr_arr.append(np.nanmean(subset1['F_corrected_normed_error']))
#
# # just want to see them each plotted over time to make sure nothing totally crazy is in there...
# # plt.errorbar(subset1['TP'], subset1['F_corrected_normed'], yerr=subset1['F_corrected_normed_error'], linestyle='', marker='o')
# # plt.axhline(y=wmean, color='black', linestyle='--')
# # plt.title(f'{rs[i]}_{name}')
# # plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_4_output/{i}.png', dpi=300, bbox_inches="tight")
# # plt.close()
# fig = px.scatter(subset1, x="TP", y="F_corrected_normed", error_y='F_corrected_normed_error', title=f'{name}')
# fig.write_html(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_4_output/{name}.html')
