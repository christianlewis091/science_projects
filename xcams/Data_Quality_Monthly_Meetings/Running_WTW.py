def weighted_mean(rts_corrected, rts_corrected_error):
    wmean_num = np.sum(rts_corrected/rts_corrected_error**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    wmean_dem = np.sum(1/rts_corrected_error**2)
    wmean = wmean_num / wmean_dem
    return wmean

def residual(rts_corrected, wm, rts_corrected_error):
    residual = (rts_corrected - wm) / rts_corrected_error
    return residual

# convert ratio to standard to per mil, for instance for sigma_bw calculation
def rts_to_permille_for_errors(rts, colldate):
    rts_to_FM  = (np.sqrt(rts**2)/0.95)*0.98780499
    FM_to_permille = 1000*(rts_to_FM*np.exp((1950-colldate)/8267))
    return FM_to_permille

def tp_not_in_second(df1, df2):
    """
    Return TP values that are in df1['TP'] but not in df2['TP'].
    """
    return sorted(set(df1["TP"]) - set(df2["TP"]))

"""
Toward the end of the Data Quality Paper, we decided it would be good to summarize the changes to our data quality calculations monthly
This way we can assess where there may be problems before they pop up in the long term
We can re-calculate the CVr over time, and look at which secondaries have new data. 

Most of the code will be stripped straight from the Data_Quality V6 scripts, and I'll indicate which are from there and which are new
I'll also play around with putting the implementation into a function so that it's easier to implement. 

SCRIPT 0
# script 0 is where the new export was read in and filtered to be secondaries only
# It then counted how much data was added between V5 and V6, so we don't need to do any of that here. 

# How much of previous scripts have I incorporated? 
SCRIPTS 0_AIR and 0_FIRI
# Scripts 0_air and 0_firi can be dealt with by just exporting the right columns for us to filter on for their pretreatment information
# Why didn't we do this for the paper? 1) we were originally dealing with Albert's dataset and building off it 2) after a while there was enough inertia in one direction it didn't make sense to restart the coding. 

SCRIPT 1
# script 1 is where did the flagging and commenting of the original dataset and the dataset as it grew
# It doesn't make sense to keep all this code in; but what we can do is keep all the flags on the secondaries that we've added and append them to the output from RLIMS, so we have all the information at 
# hand for our monthly data checks

# TO DO: MAKE EXPORT SCRIPT
Here is a list of the columns we need to export: 
RTS_corrected
RTS_corrected_error
rts_bl_av
Ratio to standard
Ratio to standard error
MCC
F_corrected_normed
F_corrected_normed_error
DELTA14C
DELTA14C_Error
delta13C_AMS
delta13C_AMS_Error
delta13C_IRMS
delta13C_IRMS_Source
Blank rts assigned
Blank rts err assigned
Category In Calculation
Job::Job notes
wtgraph
EA Combustion::Run Number
Date Run
TP
TW
Quality Flag
Job::R
Samples::Sample ID
Samples::Sample Description
Job::AMS Category
Graphite Completed::Graphite Line
AMS Timetable From Results::Standard Prep Type  # for Air Materials pretreatment
AAA Processes::End Operator                     # for AAA vs Cellulose comparisons
Cellulose Extraction Completed::Start Operator  # for AAA vs Cellulose comparisons

TO DO:
Add next phase of analyzing each secondary! Not just group. 

"""
# IMPROT STATEMENT
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns


def monthly_CV(df, export_date, comment1): # put export date as "2026-07-01"

    """
    SOME DEBUGGING NOTES: 
    In RLIMS, we had a wheel where Mode 5 AND Mode 1 were imported, and we ended up with these weird decimal wheels. 
    Now, the data comes up of course its different if it was analyzed in Mode 1
    We need to remove that wheel (see below).
    This wasn't removed in the DQ paper though! Why wasn't it? 
    Actually for the DQ paper there was a double-glitch where these data didn't have "FLASK" added as a pretreatment type due to TW virtual wheel over-writing,
    so the double mistake led to it being left out.

    Now, 91053 and 91203 are included in the analysis because they've had flask added, and I've removed 3537.5 AND 3537 from the analysis. Data matches DQ paper. 
    Previously, we may have included the 3537 (not 3537.5), but it didn't have flask label, so we missed it. but clearly the data throws off Air materials stats, and it was a bad wheel, so we would have removed it anyway
    """
    bugs = [3537.5, 3537]
    df = df.loc[~df['TW'].isin(bugs)]
    # bugs = [89255, 89266]
    # df = df.loc[~df['TP'].isin(bugs)]

    # read in list of secondaries of interest 
    seconds = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\seconds_April3_2026.xlsx", sheet_name='new', comment='#')

    # whats the max TW?
    maxtw = np.max(df['TW'])

    # check the dataset only contains data in our excel sheet list
    rs_of_secondaries_and_blanks = np.unique(seconds['Job::R'])
    df = df.loc[df['Job::R'].isin(rs_of_secondaries_and_blanks)]

    # add metadata to secondary standards, like collection date, group for pooled CVr, and more...
    print(f"Length before merge 1 is {len(df)}")
    df = df.merge(seconds[['Job::R', 'Collection Date', 'Group','Merge Comment','Reference for Collection Date','Expected FM']], on='Job::R', how='left')
    print(f"Length after merge 1 is {len(df)}")
    print()
    # READ IN THE FILE OUTPUT FROM _1 WHERE WE HAVE FLAGGED CERTAIN DATA, 
    prev_flags = pd.read_excel(rf"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\13_manual_drop.xlsx")
    prev_flags = prev_flags[['TP','Keep_Remove','Comment','JCT','Manual Check Comment','Should a new flag be added? ']]

    print(f"Length before merge 2 is {len(df)}")
    df = df.merge(prev_flags, on='TP', how='left')
    print(f"Length after merge 2 is {len(df)}")
    print()
    df.to_excel(rf'I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\script_testing/Line98.xlsx')

    # Below will remove data previously set for removal. New data won't have a label so we tell it to keep the '' data as well.
    keeps = ['Keep','']
    print(f"Length before Keep_Remove is {len(df)}")
    df = df.loc[df['Keep_Remove'].isin(keeps)]
    print(f"Length after Keep_Remove is {len(df)}")
    print()

    # remove data <0.2 because in the past we couldn't run it. Will decide as a team how to tackle this moving forward for monthly checks
    print(f"Length before size filter is {len(df)}")
    df = df.loc[df['wtgraph'] > 0.2]
    print(f"Length after size filter is {len(df)}")
    print()

    # Quick housekeeping/troubleshooting check before any math is done
    # Try converting to numeric and see if anything fails
    pd.to_numeric(df['RTS_corrected_error'], errors='raise')
    pd.to_numeric(df['RTS_corrected'], errors='raise')
    pd.to_numeric(df['Collection Date'], errors='raise')

    # calculate weighted mean for every R
    # also calculate resiual using function at the top
    df['wmean'] = df.groupby('Job::R')['RTS_corrected'].transform(lambda x: weighted_mean(df.loc[x.index, 'RTS_corrected'], df.loc[x.index, 'RTS_corrected_error']))
    df['residual'] = residual(df['RTS_corrected'],df['wmean'],df['RTS_corrected_error'])

    # create new datasets for each GROUP for calculating pooled CVr
    # Set list of R numbers for each group, then create new dataframes for each group
    air_r = ['40430/1','40430/2','40430/5']
    inor_r = ['41347/2','41347/3']
    water_r = ['41347/12','41347/13']
    organic_r = ['24889/4','24889/5','24889/7','24889/9']
    rpo_r = ['24889/14']
    bone_r = ['26281/1']

    air_materials = df.loc[(df['Job::R'].isin(air_r)) & (df['AMS Timetable From Results::Standard Prep Type'] == 'FLASK')].copy()
    inorganic_materials = df.loc[(df['Job::R'].isin(inor_r))].copy()
    water_materials = df.loc[(df['Job::R'].isin(water_r))].copy()
    organic_materials = df.loc[(df['Job::R'].isin(organic_r))].copy()
    rpo_materials = df.loc[(df['Job::R'].isin(rpo_r))].copy()
    bone_materials = df.loc[(df['Job::R'].isin(bone_r))].copy()

    # IF YOU ADD A NEW MATERIAL, MAKE SURE TO CHANGE THE K!!! 
    datasets = [air_materials, inorganic_materials, water_materials, organic_materials, rpo_materials, bone_materials]
    names = ['Air', 'Inorganic', 'Water', 'Organic','RPO', 'Bone']
    k = [3,2,2,4,1,1]

    # SET SOME ARRAYS TO FILL WITH DATA!
    length = []
    desc_arr = []
    chi2_red_arr = []
    sigbw_arr = []
    sigbw_percent_arr = []
    sig_bw_pm_arr = []
    date_arr = []
    comment = []
    max_TW = []

    for i in range(0, len(datasets)):

        df2 = datasets[i]  # access first subset
        length.append(len(df2))  # append length of data
        desc_arr.append(names[i]) # append description of data
        k_i = k[i] # edit denominator of chi2 to be n-k, where k is the number of materials. 
        max_TW.append(maxtw)

        export_date1 = pd.Timestamp(export_date)
        date_arr.append(export_date1)
        """
        Calculate chi2 reduced
        """
        chi2_red_num = np.sum((df2['RTS_corrected']-df2['wmean'])**2/df2['RTS_corrected_error']**2)
        chi2_red_denom = len(df2)-k_i # subtract number of groups in degrees of freedom calc.
        chi2_red = chi2_red_num/chi2_red_denom
        # print(chi2_red)
        chi2_red_arr.append(chi2_red)

        """
        calculate sigma_bw striaght up (This is the turnbull 2015 method) (if this doesn't work, its beacuse the sqrt function went negative because chi2 was less than 1)
        See Eqn at bottom of page 1 of scan file:///I:/C14Data/Data%20Quality%20Paper/CBL_V3/Data_Quality_Eqns_CBL_JCT.pdf
        """
        if chi2_red < 1:
            sigbw = 0

        else:
            term2 = np.sqrt(chi2_red - 1)
            term1 = np.nanmean(df2['RTS_corrected_error']/df2['RTS_corrected']) 

            sigbw = term1*term2

        sigbw_arr.append(sigbw) 

        sigbw_percent_arr.append(sigbw*100) # convert to percent, which is used in RLIMS, which we can use later for FM calc so its consistent with RLIMS

        colldate1 = df2['Collection Date'].iloc[0]
        sig_bw_pm_arr.append(rts_to_permille_for_errors(sigbw, colldate1))

        comment.append(f'{comment1}')

    output_grouped = pd.DataFrame({
        'Date': date_arr,
        'Max_TW': max_TW,
        'Group': desc_arr,
        'Data Length (n)': length,
        'Chi2 Reduced': chi2_red_arr,
        'sigmabw_rts': sigbw_arr,
        'sigmabw_rts_percent': sigbw_percent_arr,
        'sigmabw_pm': sig_bw_pm_arr,
        'comment': comment
    })

    print(output_grouped)

    files = pd.read_excel(
        rf"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\output\Monthly_CVr_Tracker.xlsx"
    )

    # Append new rows
    files = pd.concat([files, output_grouped], ignore_index=True)

    files.to_excel(rf"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\output\Monthly_CVr_Tracker.xlsx")


    files["Date"] = pd.to_datetime(files["Date"])

    groups = files["Group"].unique()

    fig, axs = plt.subplots(1, 3, figsize=(12, 5.5))

    for i, group in enumerate(groups):
        subdf = files.loc[files["Group"] == group].sort_values("Date")
        
        axs[0].plot(subdf["Date"],subdf["Data Length (n)"],marker="o",linestyle="-",label=group)
        axs[1].plot(subdf["Date"],subdf["Chi2 Reduced"],marker="o",linestyle="-")
        axs[2].plot(subdf["Date"],subdf["sigmabw_pm"],marker="o",linestyle="-")

    for ax in axs:
        ax.set_xlim(pd.Timestamp("2026-05-01"), pd.Timestamp("2026-12-01"))
        ax.tick_params(axis="x", rotation=45)

    axs[0].set_title("Sample Count (n))")
    axs[1].set_title("Chi² reduced")
    axs[2].set_title("σbw (pm)")

    axs[0].set_ylabel("n")
    axs[1].set_ylabel("Chi² reduced")
    axs[2].set_ylabel("σbw (pm)")

    axs[0].legend()

    plt.tight_layout()
    plt.savefig(f"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\output\{export_date}.png",
               dpi=300, bbox_inches="tight")


"""
Using the Function Above
1. Comment out previous iterations. 
2. Fix the arguments
3. Run
4. Check output
"""
# Testing Phase, using data from July 2, 2026
df = pd.read_excel(rf"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\Monthly_Export_From_RLIMS\Monthly_Export_02072026.xlsx")
monthly_CV(df, "2026-07-02", "Testing")

# # Testing first time with real new data, exported today (July 14, 2026)
df = pd.read_excel(rf"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\Monthly_Export_From_RLIMS\Monthly_Export_14072026.xlsx")
monthly_CV(df, "2026-07-14", "Second test")



