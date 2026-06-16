"""
We want to see the change in statistics from before and after RCM10 for carbonates and firi's...
I'll essentailly make a copy of the _2 script and run it for RG20s and RCM10's by indexing by graphite line.
"""
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

def weighted_mean(rts_corrected, rts_corrected_error):
    wmean_num = np.sum(rts_corrected/rts_corrected_error**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    wmean_dem = np.sum(1/rts_corrected_error**2)
    wmean = wmean_num / wmean_dem
    return wmean

def residual(rts_corrected, wm, rts_corrected_error):
    residual = (rts_corrected - wm) / rts_corrected_error
    return residual

def rts_to_permille_for_errors(rts, colldate):
    rts_to_FM  = (np.sqrt(rts**2)/0.95)*0.98780499
    FM_to_permille = 1000*(rts_to_FM*np.exp((1950-colldate)/8267))
    return FM_to_permille


"""
"""

# We're going to be using the data from _2 where I just grab the secondaries and blanks with R numbers that we care about
df = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/secondaries_subset.xlsx")

"""
THIS BLOCK COPIED FROM _2
We have to be doubly sure that the blanks are indeed getting 45% error. 
In the end, we'll be calculating standard error, but for now, lets set the F_corrected_normed_error for blanks to 45%
"""
df['err45'] = df['F_corrected_normed']*0.45
blank_rs = ['40430/6','40142/2','40142/1','14047/1','14047/11']
mask = df['Job::R'].isin(blank_rs)
df.loc[mask, 'F_corrected_normed_error'] = df.loc[mask, 'err45']
df['blank_error_check'] = df['F_corrected_normed_error']/df['F_corrected_normed'] # should be 0.45 for blanks...

df['wmean'] = df.groupby('Job::R')['RTS_corrected'].transform(lambda x: weighted_mean(df.loc[x.index, 'RTS_corrected'], df.loc[x.index, 'RTS_corrected_error']))
df['residual'] = residual(df['RTS_corrected'],df['wmean'],df['RTS_corrected_error'])


"""
DO THE KEEP FILTER, DON'T DO THE SIZE FILTER!
"""
df = df.loc[df['Keep_Remove'] == 'Keep']

seconds = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\seconds_April3_2026.xlsx", sheet_name='new', comment='#')

df = df.merge(seconds[['Job::R', 'Collection Date', 'Group','Merge Comment','Reference for Collection Date','Expected FM']], on='Job::R', how='left')

"""
WHAT R NUMBERS EVEN EXIST FOR RCM10 IN OUR SECONDARIES DATASET? 
"""

rcm10 = df.loc[df['Graphite Completed::Graphite Line'] == 10]
rg20 = df.loc[df['Graphite Completed::Graphite Line'] == 20]


rs_rcm10 = np.unique(rcm10['Job::R'])
print(rs_rcm10)
# rcm10.to_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_7_V6_output/test.xlsx")


"""
RCM10 contains: 
['14047/1' '14047/11' # Inorganic blank and water blank are both in there, but those are for next stage. 
'24889/14'            # FIRID RPO
'24889/4'             # FIRI-D standard
'40142/2'             # Kauri AAA blank
'40699/1'             # Kapuni Blank
'41347/12'            # LAC1 water
'41347/2'             # LAC1 inorganic
'41347/3'             # LAA1 inorganic

"""

"""
FROM HERE I'M GOING TO WRAP IT ALL IN A FUNCTION BECAUSE I'M GOING TO BE DOING THE SAME THING TWICE,
ONCE FOR RCO10
ONCE FOR RG20 DATA
"""
def analysis_7(df, df_name):

    # what sample groups are we interested in
    inor_r = ['41347/2','41347/3'] # keep as in _2
    water_r = ['41347/12']         # removed the other one, only keep the one in both datasets
    organic_r = ['24889/4']        # I'm not going to include RPO data in this section where the CVr is calculated through

    inorganic_materials = df.loc[(df['Job::R'].isin(inor_r))].copy()
    water_materials = df.loc[(df['Job::R'].isin(water_r))].copy()
    organic_materials = df.loc[(df['Job::R'].isin(organic_r))].copy()

    datasets = [inorganic_materials, water_materials, organic_materials]
    names = ['Inorganic', 'Water', 'Organic']
    k = [2,1,1]

    # SET SOME ARRAYS TO FILL WITH DATA!
    length = []
    desc_arr = []
    chi2_red_arr = []
    sigbw_arr = []
    sigbw_percent_arr = []
    sig_bw_pm_arr = []

    for i in range(0, len(datasets)):

        df2 = datasets[i]  # access first subset
        length.append(len(df2))  # append length of data
        desc_arr.append(names[i]) # append description of data

        """
        Calculate chi2 reduced
        """
        chi2_red_num = np.sum((df2['RTS_corrected']-df2['wmean'])**2/df2['RTS_corrected_error']**2)
        chi2_red_denom = len(df2)-k[i] # subtract number of groups in degrees of freedom calc.
        chi2_red = chi2_red_num/chi2_red_denom
        # print(chi2_red)
        chi2_red_arr.append(chi2_red)

        """
        calculate sigma_bw striaght up (This is the turnbull 2015 method) (if this doesn't work, its beacuse the sqrt function went negative because chi2 was less than 1)
        See Eqn at bottom of page 1 of scan file:///I:/C14Data/Data%20Quality%20Paper/CBL_V3/Data_Quality_Eqns_CBL_JCT.pdf
        """
        if chi2_red < 1:
            # according to the eqn, if chi2 is less than 1, you'd be taking sqrt of negative number which doesn't work. So if less than 1, set to 0.
            sigbw = 0
            # print('I found a zero!')

        else:
            term2 = np.sqrt(chi2_red - 1)
            # term1 = np.nanmean(df2['RTS_corrected_error'])/(df2['wmean'].iloc[0]); this is wrong, see notes right below!
            # There has been some confusion lately about the term above (in my own head)
            # here is where we are normalizing by RTS (in the manuscript this lands as Eqn 5.)
            # In earlier version, I had this listed as term1 = np.nanmean(df2['RTS_corrected_error'])/np.nanmean(df2['RTS_corrected']) 
            # Then, I thought it was wrong/thoght I caught a bug when I was updating the eqns in the manuscript. Why are we using the nanmean instead of the weighted mean???
            # So then, I switched to weighted mean (the RTSb bar)
            # BUT now I believe these are both wrong...
            # For a given df2 in the loop, there are a few values each with different set values (for instance for airs, there is BHDamb, BHDspike, BHDspike2025)
            # In reality, the first one was almost right but there shouldn't be the nanmean before the RTS_corrected. It shouid be nanmean of (RTS_err/RTS)
            term1 = np.nanmean(df2['RTS_corrected_error']/df2['RTS_corrected'])  

            sigbw = term1*term2
        sigbw_percent_arr.append(sigbw*100) # convert to percent, which is used in RLIMS, which we can use later for FM calc so its consistent with RLIMS
        sigbw_arr.append(sigbw)

        colldate1 = df2['Collection Date'].iloc[0]
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
        plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_7_V6_output/mpl_output/{df_name}_{i}.png",
                    dpi=300, bbox_inches="tight")
        plt.close()

    output_grouped = pd.DataFrame({
        'Group': desc_arr,
        'Data Length (n)': length,
        'Chi2 Reduced': chi2_red_arr,
        'sigmabw_rts': sigbw_arr,
        'sigmabw_rts_percent': sigbw_percent_arr,
        'sigmabw_pm': sig_bw_pm_arr,
    })

    df = df.merge(output_grouped[['sigmabw_rts','sigmabw_pm','sigmabw_rts_percent','Group']], on='Group', how='left')
    df['F_corrected_normed_error_NEW, with sigbw_RTS_percent'] = (np.sqrt(df['RTS_corrected_error']**2 + (df['sigmabw_rts_percent']*0.01*df['RTS_corrected'])**2)/0.95)*0.98780499



    """
    Entering the second main phase of the _2 script...
    """
    # some groups have sigmabw as 0 becuse chi2 were >1, see output from module above. Others have 0 beacuse they don't have WTW error applied. These include blanks, and things in "tuning" or "removed" categories
    df["sigmabw_rts"] = df["sigmabw_rts"].fillna(0) # dupliactes line later but I left that later one cuz it was added first and don't want to break the code
    
    """
    # STEP 2.2: INDEX BASED ON PRETREATMENTS
    - - Then, we've been asked to index/seperate a lot of the organics based on pre-treatment. This will be a chunk of messy code

    # I'm taking this from Data_Quality_Paper_2_2026_v1.py

    Remember here is the data we want for comparison for RCM10:
    ['14047/1' '14047/11' # Inorganic blank and water blank are both in there, but those are for next stage. 
    '24889/14'            # FIRID RPO
    '24889/4'             # FIRI-D standard
    '40142/2'             # Kauri AAA blank
    '40699/1'             # Kapuni Blank
    '41347/12'            # LAC1 water
    '41347/2'             # LAC1 inorganic
    '41347/3'             # LAA1 inorganic

    """

    kapuni = df.loc[(df['Job::R'] == '40699/1')].copy()
    carr_marb_carb = df.loc[(df['Job::R'] == '14047/1')].copy()
    carr_marb_water = df.loc[(df['Job::R'] == '14047/11')].copy()
    kauri_aaa = df.loc[(df['Job::R'] == '40142/2')].copy()

    firi_d_all = df.loc[(df['Job::R'] == '24889/4')].copy()
    firi_d_rpo = df.loc[(df['Job::R'] == '24889/14')].copy()

    lac1carb = df.loc[(df['Job::R'] == '41347/2')].copy()
    laa1carb = df.loc[(df['Job::R'] == '41347/3')].copy()

    lac1water = df.loc[(df['Job::R'] == '41347/12')].copy()


    datasets = [kapuni,
            carr_marb_carb, 
            carr_marb_water,
            kauri_aaa,
            firi_d_all,
            firi_d_rpo,
            lac1carb,
            laa1carb,
            lac1water]

    names = ['KAPUNI',
            'CARR_MARB_CARB',
            'CARR_MARB_WATER',
            'KAURI_AAA',
            'FIRI_D_ALL', 
            'FIRI_D_RPO',
            'LAC1_CARB',
            'LAA1_CARB',
            'LAC1_WATER']

    """

    RE_ADD LOOP, DELETED AFTER V6.1 edits, re-add from _2...

    """

    """
    lets loop through the R numbers and get means and stats assigned to each value in the database...
    The loop will compare R numbers from the 'seconds.xlsx' with the R numbers from the dataframe
    """

    # set output for plotly file later
    outdir = r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/plotly_check"

    # set inital value for wmean so i can calc residual later
    df['wmean_subsets'] = -999

    # dataset descriptors
    group_name = []
    R_num = []
    desc_arr = []
    length = []

    # calculated statistics
    wmean_arr = []

    # summary statistics for each individual group
    chi2_red_arr = []  # will contain: individual material chi2 result
    fm_arr = []        # will contain: weighted mean from RTS converted to FM; ### F_corrected_normed = (wmean/0.95)*0.98780499
    stderr_arr = []    # will contain: standard error of the FM' standard_err = np.std(subset1['F_corrected_normed'], ddof=1) / np.sqrt(len(subset1['F_corrected_normed']))
    stdev_arr=[]       # will contain: standard deviation; np.std(subset1['F_corrected_normed'])
    coll_date_arr = [] # will contain: collection date, transferred from manually filled in sheet with secondary standards information
    d14C_arr = []      # will contain: converted d14C
    d14C_err_arr = []  # will contain: conveted d14C error

    # stuff based on the pooled statistics
    CV_r_arr = []          # sigma_bw from above
    CV_percent_arr = []
    CV_permil_arr = []
    sigma_r_arr = []       # sigma_r corresponds to eqn 7 on the manuscript; the CVr (previously called sigma_bw) multiplied by the weighted mean
    sigma_r_permil_arr = []

    total_unc_min_arr = [] # these two will hold the data which answers: what is our repeatability that we can expect on an individual measuremnet? For that, we apply the total uncertaity calculatino using new sigma_bw
                    #    for all rows, and look at the max and min, which we'll report in the table. 
    total_unc_max_arr = []
    total_unc_min_permil_arr = []
    total_unc_max_permil_arr = []
    av_prec_arr = []

    for i in range(0, len(datasets)):

        # Create figure and 2 vertical subplots
        fig, axs = plt.subplots(2, 1, figsize=(6, 8), sharex=True)  # 3 rows, 1 column

        # holdover from previous version
        df2 = datasets[i]

        # print(f'Length of df {names[i]} is {len(df2)}')
        title_i = df2['Job::R'].iloc[0]
        R_num.append(df2['Job::R'].iloc[0]) # append R number, description, group name
        desc_arr.append(names[i])
        group_name.append(df2['Group'].iloc[0])
        length.append(len(df2))
        colldate1 = df2['Collection Date'].iloc[0]

        # map the max and min expected uncerainties for indiviudual measurements onto the final table. 
        total_unc_min = np.min(df2['F_corrected_normed_error_NEW, with sigbw_RTS_percent'])
        total_unc_max = np.max(df2['F_corrected_normed_error_NEW, with sigbw_RTS_percent'])
        # append to the arrays
        total_unc_min_arr.append(total_unc_min)
        total_unc_max_arr.append(total_unc_max)

        # what is the average precision? 
        avprec = np.nanmean(df2['F_corrected_normed_error_NEW, with sigbw_RTS_percent'])

        total_unc_min_per_mil = rts_to_permille_for_errors(total_unc_min, colldate1)
        total_unc_max_per_mil = rts_to_permille_for_errors(total_unc_max, colldate1)
        avprec_per_mil = rts_to_permille_for_errors(avprec, colldate1)

        total_unc_min_permil_arr.append(total_unc_min_per_mil)
        total_unc_max_permil_arr.append(total_unc_max_per_mil)
        av_prec_arr.append(avprec_per_mil)

        CV_r = df2['sigmabw_rts'].iloc[0]
        CV_r_arr.append(CV_r)

        CV_percent = df2['sigmabw_rts_percent'].iloc[0]
        CV_percent_arr.append(CV_percent)

        CV_permil = df2['sigmabw_pm'].iloc[0]
        CV_permil_arr.append(CV_permil)

        """
        The weighted mean comes from Albert's original version of the paper. I've copied his formula here which comes from
        #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
        We need to recalculate wmean since we're dealing with subsets now, especially for the many permutations or organic pretreatment subsets
        """
        # renaming as holdover from previous version
        subset1 = df2

        wmean_num = np.sum(subset1['RTS_corrected']/subset1['RTS_corrected_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
        wmean_dem = np.sum(1/subset1['RTS_corrected_error']**2)
        wmean = wmean_num / wmean_dem
        wmean_arr.append(wmean)
        print(f'{names[i]}, {wmean}')

        sigma_r = wmean*CV_r
        sigma_r_arr.append(sigma_r)

        sigma_r_permil_arr.append(rts_to_permille_for_errors(sigma_r, colldate1))

        """
        Calculate residual: again, while we've already done this in previous section, we're re-doing it relative to wmean of subset for pretreatment permutations
        """
        subset1['residual'] = ( subset1['RTS_corrected'] - wmean ) / subset1['RTS_corrected_error']

        """
        Calculate chi2 reduced for subset
        """
        # calc chi2
        chi2_red_num = np.sum((subset1['RTS_corrected']-wmean)**2/subset1['RTS_corrected_error']**2)
        chi2_red_denom = len(subset1)-1 # subtract number of groups in degrees of freedom calc.
        chi2_red = chi2_red_num/chi2_red_denom
        chi2_red_arr.append(chi2_red)

        """
        Conversion to Fraction modern
        RLIMS EQN: If(IsEmpty(rts_stds_av) = False; (RTS_corrected / (Standard Specific Activity Constant * rts_stds_av)) *( ((1 + delta13C_stds_av/ 1000) / (1 + delta13C_In_Calculation / 1000)) ^Normalization_exp_factor )* Standard 13C Value Constant;"")
        # The last term is the 13C value constant, a go-between for conventions - its so confusing
        """

        term1 = np.nanmean(subset1['RTS_corrected_error']) # why is it written like this? Legacy. From Data Qualiyt Paper_2 2026 v1.py

        subset1["sigmabw_rts_percent"] = subset1["sigmabw_rts_percent"].fillna(0) # This line is important. For blanks, and Kapuni (tuning), no WTW error is applied. But if there is no data there, the rest of the calcualtions won't run. So we just need to set it to 0.
        sigbw_rts_percent = (subset1['sigmabw_rts_percent'].iloc[0])

        F_corrected_normed = (wmean/0.95)*0.98780499 #wmean converted to FM
        fm_arr.append(F_corrected_normed)

        F_corrected_normed_error = (np.sqrt(term1**2 + (sigbw_rts_percent*0.01*wmean)**2)/0.95)*0.98780499
        
        """
        May 20, 2025, making an edit to the FM corrected values. 
        In the past I've calculated it as: 
        F_corrected_normed_error = (np.sqrt(term1**2 + (sigbw_rts_percent*0.01*wmean)**2)/0.95)*0.98780499
        This figuration incorporates the sigbw_rts_percent that we've worked so hard to calculate. 
        But actually JCT thinks we should be reporting the standard error.
        Perhaps I've been thinking about it slightly wrong; 
        I've been wanting to use sigma_bw in the final calculation of our uncertainty. However, 
        it's perhaps better thought of as a marker of how much uncertainty needs to be added to each 
        measurement in real life (as they're coming off of XCAMS); and the calculation as I've had it before
        isn't the best for summarized long-term data sets. 
        I've kept the original commented out below, and added in the numpy standard error calculation here: 
        standard error of the mean:sem = np.std(data, ddof=1) / np.sqrt(len(data))
        """


        stddev = np.std(subset1['F_corrected_normed'])
        stdev_arr.append(stddev)
        # we deicded to use STANDARD ERROR, but were keeping this in the output for now...

        standard_err = np.std(subset1['F_corrected_normed'], ddof=1) / np.sqrt(len(subset1['F_corrected_normed']))
        # F_corrected_normed_error = (np.sqrt(term1**2 + (sigbw_rts_percent*0.01*wmean)**2)/0.95)*0.98780499 

        stderr_arr.append(standard_err)
        

        """
        Conversion to D14C
        """
        colldate1 = subset1['Collection Date'].iloc[0]
        coll_date_arr.append(colldate1)
        delta_14C =  1000*(F_corrected_normed*np.exp((1950-colldate1)/8267)-1)
        delta_14C_err = 1000*(standard_err*np.exp((1950-colldate1)/8267))
        d14C_arr.append(delta_14C)
        d14C_err_arr.append(delta_14C_err)

        """
        Draw a nice plot with residuals and FM's (we're not using D14C because the collection dates for FIRI are too difficult to pin down)...
        """

        # Residuals on the bottom
        axs[1].scatter(subset1['TP'], subset1['residual'], color='black', linestyle='')
        axs[1].axhline(y=0, color='black')

        # Second subplot
        subset1['F_corrected_normed'] = pd.to_numeric(subset1['F_corrected_normed'], errors="coerce")
        subset1['F_corrected_normed_error'] = pd.to_numeric(subset1['F_corrected_normed_error'], errors="coerce")
        subset1['TP'] = pd.to_numeric(subset1['TP'], errors="coerce")
        axs[0].axhline(y=F_corrected_normed, color='black') # see above, I convert wmean to FM space
        concval = subset1['Expected FM'].iloc[0]
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
        axs[0].set_title(title_i)
        plt.tight_layout()


        plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output\mpl_output/{i}.png", dpi=300, bbox_inches="tight")
        plt.close()

        """
        Some quick plotly to faster identify outliers to remove
        """

    #     import plotly.graph_objects as go

    #     fig_plotly = go.Figure()

    #     fig_plotly.add_trace(go.Scatter(x=subset1['TP'],y=subset1['residual'],mode='markers', marker=dict(size=8), text=subset1['TP'], hovertemplate=
    #                 '<b>TP:</b> %{x}<br>' +
    #                 '<b>Residual:</b> %{y:.2f}<br>' +
    #                 '<extra></extra>')
    #     )
    #     # Zero line
    #     fig_plotly.add_hline(
    #         y=0,
    #         line_color='black'
    #     )
    #     fig_plotly.update_layout(
    #         title=title_i,
    #         xaxis_title='TP',
    #         yaxis_title='Residual',
    #         height=500,
    #         width=800
    #     )
    #     fig_plotly.show()


    output_R_specific = pd.DataFrame({
                            'Group': group_name,
                            'Job::R': R_num,
                            'Description': desc_arr,
                            'n': length,

                            'wmean': wmean_arr,

                            'chi2red': chi2_red_arr,
                            'Fraction Modern': fm_arr,
                            'Standard Error':stderr_arr,
                            'Standard Deviation (dont for main unc!)': stdev_arr,
                            'Collection Date': coll_date_arr,
                            'D14C': d14C_arr,
                            'D14C_err': d14C_err_arr,

                            'CV_r': CV_r_arr,
                            'CV_r_percent': CV_percent_arr,
                            'CV_permil': CV_permil_arr,
                            'sigma_r': sigma_r_arr,
                            'sigma_r_permil': sigma_r_permil_arr,
                            'total_unc_min': total_unc_min_arr,
                            'total_unc_min_permil': total_unc_min_permil_arr,
                            'tot_unc_max': total_unc_max_arr,
                            'total_unc_max_permil': total_unc_max_permil_arr,
                            'Average precision for ind cathode': av_prec_arr,
                            })

    print(av_prec_arr)


    output_dir = (rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_7_V6_output/RCM10_check_{df_name}.xlsx")

    df_columns_cleaned = df[[
        'RTS_corrected', 'RTS_corrected_error',
        'MCC',
        'F_corrected_normed', 'F_corrected_normed_error','F_corrected_normed_error_NEW, with sigbw_RTS_percent', 
        'DELTA14C',
        'DELTA14C_Error',
        'wtgraph',
        'TP', 'TW', 'Quality Flag',
        'Job::R', 'Samples::Sample Description',
        'Collection Date', 'Group', 'Merge Comment',
        'Reference for Collection Date', 'Expected FM', 'wmean', 'residual',
        'sigmabw_rts','sigmabw_pm','sigmabw_rts_percent','Group','Date Run']]

    # Write to Excel
    with pd.ExcelWriter(output_dir, engine="openpyxl", mode="w") as writer:
        df_columns_cleaned.to_excel(writer, sheet_name="Clean Dataset", index=False)
        output_grouped.to_excel(writer, sheet_name="Group Statistics", index=False)
        output_R_specific.to_excel(writer, sheet_name="Secondaries Statistics", index=False)


analysis_7(rcm10, 'RCM10')
analysis_7(rg20, 'RG20')

