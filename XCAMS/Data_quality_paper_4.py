"""
Recreate albert's figure from poster and see how he calcultes RES
"""
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore')
import matplotlib.pyplot as plt
import plotly.express as px

"""
July 1, 2024:
I discussed the idea of sigma_res with JCT today. Essentially, sigma_res is an added error term in the chi2 equation
Paper is updated now with the right equation

BELOW, I tried to recreate some data from Albert's 2022 Radiocarbon Poster, but it was folly. I cant reproduce his sigma_res.
I'm going to try to do that his "simplified_RLIMS_dataset by recreating the data in his "Tables.xlsx" that came with his data and v1 of paper
"""

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/12_second_manual_check.xlsx', sheet_name= 'Whole Dataframe')
df = df.loc[df['Keep_Remove'] == 'Keep']
df = df.rename(columns={'RTS_corrected': 'RTS', 'RTS_corrected_error': 'RTSerr','Samples::Sample Description':'sampleDESC'})

cols = ['F_corrected_normed', 'F_corrected_normed_error']
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)
df['MCCerr'] = 0.45*df['MCC']

# data with the secondaries to filter on
df2 = pd.read_excel('H:/Science/Papers/In Prep Work/2023_Zondervan_DataQuality/seconds.xlsx', comment='#')

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
firilist = ['24889/4','24889/5','24889/9','26281/1'] # here is the list of R numbers I want to check
firis = df.loc[(df['Job::R'].isin(firilist))]        # make a subset dataframe where these FIRIs are found
# firis.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_4_output/firis.xlsx')  # write it to excel
firis = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_4_output/firis_edited.xlsx', comment='#') # I edited it by checking RLIMS. Read it back in
firis = firis[['TP','EA_ST','AAA_CELL']]  # drop columns to prep for merge
df = df.merge(firis, on='TP', how='outer')  # merge
# df.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_4_output/mergecheck.xlsx') # output to recheck

# edit the R numbers to fit that of "seconds.xlsx" and prep for the mathematics below:
df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/4_AAA_EA'
df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna()), 'Job::R'] = '24889/4_AAA_ST'
df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/4_CELL_EA'
df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'].isna()), 'Job::R'] = '24889/4_CELL_ST'

value_counts = df['Job::R'].value_counts()
pd.set_option('display.max_rows', None)
print(value_counts)

# groups to filter on
rs = np.unique(df2['R_number'])

"""
# lets loop through the R numbers and get means and stats assigned to each value in the database...
"""

group_name = []
R_num = []
length = []
wmean_arr = []
stdev_arr = []
sterr_arr = []
chi2_red_arr = []
sig_res_arr = []
opt_chi = []
mcc_err_arr = []
FracMODerr_arr = []

for i in range(0, len(rs)):
    subset1 = df.loc[df['Job::R'] == rs[i]]
    R_num.append(rs[i])

    group = df2.loc[df2['R_number'] == rs[i]]
    group_name.append(np.unique(group['Group']).astype(str))

    length.append(len(subset1))

    wmean_num = np.sum(subset1['F_corrected_normed']/subset1['F_corrected_normed_error']**2)
    wmean_dem = np.sum(1/subset1['F_corrected_normed_error']**2)
    wmean = wmean_num / wmean_dem
    wmean_arr.append(wmean)
    straight_mean = np.nanmean(subset1['F_corrected_normed'])

    stdev_arr.append(np.std(subset1['F_corrected_normed']))
    sterr_arr.append(np.sum(1/(subset1['F_corrected_normed_error']**2))**-0.5)

    # calc chi2
    chi2_red_num = np.sum((subset1['F_corrected_normed']-wmean)**2/subset1['F_corrected_normed_error']**2)
    chi2_red_denom = len(subset1)-1 # subtract number of groups in degrees of freedom calc.
    chi2_red = chi2_red_num/chi2_red_denom
    chi2_red_arr.append(chi2_red)

    mcc_err_arr.append(np.nanmean(subset1['MCCerr']))
    FracMODerr_arr.append(np.nanmean(subset1['F_corrected_normed_error']))

    """
    Optomize Chi2 to find sigma_residual
    """
    sig_res = np.linspace(0.00001, 0.010, 100)

    # Variables to store the best result
    best_sig_res = None
    closest_chi2_red = float('inf')
    target_chi2_red = 1.0

    for i in range(len(sig_res)):
        # Calculate chi2_red for the current sig_res
        chi2_red_num = np.sum((subset1['F_corrected_normed'] - wmean)**2 / (subset1['F_corrected_normed_error']**2 + sig_res[i]**2))
        chi2_red_denom = len(subset1)-1
        chi2_red = chi2_red_num / chi2_red_denom

        # Check if this chi2_red is closer to 1
        if abs(chi2_red - target_chi2_red) < abs(closest_chi2_red - target_chi2_red):
            closest_chi2_red = chi2_red
            best_sig_res = sig_res[i]

    sig_res_arr.append(best_sig_res)
    opt_chi.append(closest_chi2_red)

output1 = pd.DataFrame({'R_number': R_num,
                        'Group':group_name,
                        'Data Length (n)': length,
                        'FM (wmean)': wmean_arr,
                        'Standard Deviation': stdev_arr,
                        'Standard Error': sterr_arr,
                        'Chi2 Reduced': chi2_red_arr,
                        'Optd Chi2': opt_chi,
                        'Sigma Residual': sig_res_arr,
                        'Sigma_FM': FracMODerr_arr,
                        'Sigma_blank': mcc_err_arr,
 })

output1['sigma_total_FM'] = np.sqrt(output1['Sigma_FM']**2 + output1['Sigma_blank']**2 + output1['Sigma Residual']**2)
output1['sigma_total_CRA'] = 8033 * (output1['Sigma_FM']/output1['FM (wmean)'])
output1['CRA (from FM wmean)'] = -8033 * np.log(output1['FM (wmean)'])

# add some of the metadata from the secondary sheet.
df2 = df2[['Name','Collection Date','R_number','Expected FM','Expected Age (CRA)','Expected Age Delta14C']]
output1 = output1.merge(df2, on='R_number')

# do this in excel beacuse of errors from those without collection dates.
# output1['Delta14C'] = ((output1['FM (wmean)']*np.exp(1950/output1['Collection Date']))-1)*1000


output1.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_4_output/statistics.xlsx')


# PLOT THE DATA
def calc_residuals(subset1):
    wmean_num = np.sum(subset1['F_corrected_normed']/subset1['F_corrected_normed_error']**2)
    wmean_dem = np.sum(1/subset1['F_corrected_normed_error']**2)
    wmean = wmean_num / wmean_dem
    residuals = ((subset1['F_corrected_normed']-wmean)/subset1['F_corrected_normed_error'])  # SAME AS CHI2 RED NUM without the summation before!
    return residuals

# Create figure and subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
x = np.linspace(0, 100000, 100)

aa = 0.2
ab = .1
c1 = 'gray'
c2 = 'gray'
x1 = 60000
x2 = 90000


# First subplot: AIRS
# need to get the subset again:
BHDamb = df.loc[df['Job::R'] == '40430/1']
BHDspike = df.loc[df['Job::R'] == '40430/2']

BHDamb['Res'] = calc_residuals(BHDamb)
BHDspike['Res'] = calc_residuals(BHDspike)

ax1.scatter(BHDamb['TP'], BHDamb['Res'], label=f'BHDamb')
ax1.scatter(BHDspike['TP'], BHDspike['Res'], label=f'BHDspike')

ax1.fill_between(x, -1, 1, color=c1, alpha=aa)
ax1.fill_between(x, -2, 2, color=c2, alpha=ab)
ax1.set_title('Air')
ax1.set_ylabel('Residual')
ax1.set_xlim(x1, x2)
ax1.set_ylim(-3, 3)
ax1.legend()


# Second subplot: Organics
FIRID_aaa_ea = df.loc[df['Job::R'] == '24889/4_AAA_EA']
FIRID_aaa_st = df.loc[df['Job::R'] == '24889/4_AAA_ST']
FIRID_cell_ea = df.loc[df['Job::R'] == '24889/4_CELL_EA']
FIRID_cell_st = df.loc[df['Job::R'] == '24889/4_CELL_ST']

FIRID_aaa_ea['Res'] = calc_residuals(FIRID_aaa_ea)
FIRID_aaa_st['Res'] = calc_residuals(FIRID_aaa_st)
FIRID_cell_ea['Res'] = calc_residuals(FIRID_cell_ea)
FIRID_cell_st['Res'] = calc_residuals(FIRID_cell_st)

ax2.scatter(FIRID_aaa_ea['TP'], FIRID_aaa_ea['Res'], label=f'FIRI-D (AAA-EA)')
ax2.scatter(FIRID_aaa_st['TP'], FIRID_aaa_st['Res'], label=f'FIRI-D (AAA-ST)')
ax2.scatter(FIRID_cell_ea['TP'], FIRID_cell_ea['Res'], label=f'FIRI-D (Cellulose-EA)')
ax2.scatter(FIRID_cell_st['TP'], FIRID_cell_st['Res'], label=f'FIRI-D (Cellulose-ST)')

ax2.fill_between(x, -1, 1, color=c1, alpha=aa)
ax2.fill_between(x, -2, 2, color=c2, alpha=ab)
ax2.set_title('Organic (Cellulose and AAA)')
ax2.set_ylabel('Residual')
ax2.set_xlim(x1, x2)
ax2.set_ylim(-3, 3)
ax2.legend()

# Third subplot Inorganics
trav_wat = df.loc[df['Job::R'] == '14047/12']
lac_wat = df.loc[df['Job::R'] == '41347/12']
laa_wat = df.loc[df['Job::R'] == '41347/13']

trav_carb = df.loc[df['Job::R'] == '14047/2']
lac_carb = df.loc[df['Job::R'] == '41347/2']
laa_carb = df.loc[df['Job::R'] == '41347/3']

trav_wat['Res'] = calc_residuals(trav_wat)
lac_wat['Res'] = calc_residuals(lac_wat)
laa_wat['Res'] = calc_residuals(laa_wat)

trav_carb['Res'] = calc_residuals(trav_carb)
lac_carb['Res'] = calc_residuals(lac_carb)
laa_carb['Res'] = calc_residuals(laa_carb)

ax3.scatter(trav_wat['TP'], trav_wat['Res'], label=f'Travertine (DIC)')
ax3.scatter(lac_wat['TP'], lac_wat['Res'], label=f'LAC1-coral (DIC)')
ax3.scatter(laa_wat['TP'], laa_wat['Res'], label=f'LAA-coral (DIC)')

ax3.scatter(trav_carb['TP'], trav_carb['Res'], label=f'Travertine (Solid)')
ax3.scatter(lac_carb['TP'], lac_carb['Res'], label=f'LAC1-coral (Solid)')
ax3.scatter(laa_carb['TP'], laa_carb['Res'], label=f'LAA-coral (Solid)')

ax3.fill_between(x, -1, 1, color=c1, alpha=aa)
ax3.fill_between(x, -2, 2, color=c2, alpha=ab)
ax3.set_title('Inorganic (DIC and Carbonate)')
ax3.set_xlabel('TP Number (Lab Identifier)')
ax3.set_ylabel('Residual')
ax3.set_xlim(x1, x2)
ax3.set_ylim(-3, 3)
ax3.legend()

# Adjust layout
plt.tight_layout()

# Show plot
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_4_output/secondaries.png', dpi=300, bbox_inches="tight")
