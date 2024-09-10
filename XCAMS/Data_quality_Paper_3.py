"""
Data Quality Paper 1 = adding descriptors and flagging
Data Quality Ppaer 2 = looking at blanks and making plots
This sheet (Data Quality Paper 3) calculate residuals of secondary standards and making plots

"""
import pandas as pd
import numpy as np
import warnings
from datetime import date
warnings.simplefilter(action='ignore')
import matplotlib.pyplot as plt
today = date.today()
import seaborn as sns
import matplotlib.gridspec as gridspec


def chi2red(subset):
    data_squared = (subset['F_corrected_normed'].astype(float) - (np.mean(subset['F_corrected_normed'].astype(float))))**2
    error_squared = subset['F_corrected_normed_error'].astype(float)**2
    numerator = np.sum(data_squared/error_squared)
    denominator = len(subset) - 1
    chi2_red = numerator/denominator
    return chi2_red

# read in the csv file that was created at the end of the last script
df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/12_second_manual_check.xlsx', sheet_name= 'Whole Dataframe')
df = df.loc[df['Keep_Remove'] == 'Keep']
df = df.rename(columns={'RTS_corrected': 'RTS', 'RTS_corrected_error': 'RTSerr','Samples::Sample Description':'sampleDESC'})
cols = ['F_corrected_normed', 'F_corrected_normed_error']
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)

# TODO need to break up blanks by EA and ST like I did with the secondaries...
firilist = ['40142/2','40142/1'] # here is the list of R numbers I want to check. I'm only checking FIRI D
firis = df.loc[(df['Job::R'].isin(firilist))]        # make a subset dataframe where these FIRIs are found
firis = firis[['EA Combustion::Run Numner','TP','TW','Job::R','Samples::Sample ID']]
firis.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/firis.xlsx')  # write it to excel
firis = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/firis_edited.xlsx', comment='#') # I edited it by checking RLIMS. Read it back in
firis = firis[['TP','EA_ST','AAA_CELL']]  # drop columns to prep for merge
df = df.merge(firis, on='TP', how='outer')  # merge

# edit the R numbers to be able to break up AAA ST and EA, and same for cellulose and prep for the mathematics below:
df.loc[(df['Job::R'] == '40142/2') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA'), 'Job::R'] = '40142/2_AAA_EA'
df.loc[(df['Job::R'] == '40142/2') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna()), 'Job::R'] = '40142/2_AAA_ST'
df.loc[(df['Job::R'] == '40142/1') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA'), 'Job::R'] = '40142/1_CELL_EA'
df.loc[(df['Job::R'] == '40142/1') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'].isna()), 'Job::R'] = '40142/1_CELL_ST'


"""
Print a report about what's in here for section 3.1
"""
print(f"The whole dataset has length {len(df)}, with {len(np.unique(df['TW']))}")

# grab only the keeps from now on
df = df.loc[df['Keep_Remove'] == 'Keep']

# get rid of pesky separators
df['Job::R'] = df['Job::R'].replace('/', '_', regex=True)#

# add a new column to filter on or change later
df['CBL_stat_flags'] = -999

# unique list to loop over later
knowns_Rs = np.unique(df['Job::R'].astype(str))

"""
ANALYZING THE BLANKS
"""
# unique list of BLANKS R numbers that I'll use for BLANK analysis
blank_r_list = [ '40142_2_AAA_EA','40142_2_AAA_ST','40142_1_CELL_EA','40142_1_CELL_ST','40430_3','14047_1','14047_11','40699_1']
names = ['Kauri AAA_EA','Kauri AAA_ST', 'Kauri Cellulose_EA','Kauri Cellulose_ST','Air Dead CO2','Carrera Marble Carbonate Line','Carrera Marble Water Line','Kapuni Comb-Graph']
colors = ['#A52A2A', '#228B22', '#A0522D', '#6A5ACD','#008080','#CD853F','#4682B4','#8B4513','#2E8B57']
# labels = ['Subset 1', 'Subset 2', 'Subset 4', 'Subset 5',
#           'Subset 6', 'Subset 7']
markers = ['o','D','^','o','s','D','o','s','D']
blank_Rs = df.loc[df['Job::R'].isin(blank_r_list)].reset_index(drop=True)

# DATA FOR THE GLOBAL MEAN
wmean = []
one_sigma = []
sterr = []
n = []
name = []
chi2_red = []
knownR = []
ams_cat = []
mean_wtgraph = []
mean_RTS = []
mean_RTS_sig = []

# DATA EMPTY ARRAYS FOR THE ROLLING DATA
roll_step = []

# SETUP THE PLOT
xlen =8
yylim = 0.012
grat = 1.618*xlen
fig = plt.figure(figsize=(16,8))
gs = gridspec.GridSpec(1, 9)
gs.update(wspace=0.15, hspace=0.35)

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 0:4])
plt.title('Fraction Modern over time')

for i in range(0, len(blank_r_list)):
    subset = blank_Rs.loc[blank_Rs['Job::R'] == blank_r_list[i]].reset_index(drop=True)

    wmean.append(np.mean(subset['F_corrected_normed'].astype(float)))  # calculate and append average FM
    # one_sigma.append(np.std(subset['F_corrected_normed'].astype(float))) # calc and append standard deviation
    one_sigma.append((np.mean(subset['F_corrected_normed'].astype(float)))*0.45) # See COMMENT IN MANUSCRIPT REGARDING 45% error

    mean_wtgraph.append((np.mean(subset['wtgraph'].astype(float)))) # adding graphitization mass average for XXU plot
    mean_RTS.append((np.mean(subset['RTS'].astype(float)))) # adding RTS average for XXU plot
    mean_RTS_sig.append((np.std(subset['RTS'].astype(float)))) # adding RTS std for XXU plot

    n.append(len(subset))
    name.append(names[i])
    chi2 = chi2red(subset)
    chi2_red.append(chi2)
    knownR.append(blank_r_list[i])
    # setting edge color to white beacuse it hurts my eyes to look at all those error bars
    plt.errorbar(subset['TP'], subset['F_corrected_normed'], yerr = subset['F_corrected_normed_error'], fmt=markers[i], color=f'{colors[i]}', ecolor='white', capsize=5, alpha=0.2)

    """
    I also want to plot the rolling average...
    """
    # the rolling average will break each R number's data up into ten increments.
    fm = subset['F_corrected_normed']
    tps = subset['TP']
    x = fm.rolling(2)
    inc = 50
    roll_fm = fm.rolling(inc, center=True).mean()
    roll_fm_std = fm.rolling(inc, center=True).std()
    roll_tps = tps.rolling(inc, center=True).mean()
    res_roll = pd.DataFrame({"FM": roll_fm, "FM_STD": roll_fm_std,"TP": roll_tps}).reset_index(drop=True)
    # res_roll = res_roll[::10]
    plt.plot(res_roll['TP'], res_roll['FM'], color=f'{colors[i]}', alpha=.8)
    #plot the last point as a scatter point
    res_roll = res_roll.dropna(subset='FM')
    res_roll = res_roll.iloc[-1]
    print(res_roll)
    plt.scatter(res_roll['TP'], res_roll['FM'], color=f'{colors[i]}', marker=markers[i], alpha=1, label=f'{blank_r_list[i]}_{names[i]}')
    print(f'For data of type {blank_r_list[i]}_{name}, there are {len(fm)} measurements. The reported average is that of every 50 measurements, from the center of the group.')
    print(f'The data have then been subsampled to grab every 10th item of the series')
    print()
    print()


plt.legend(loc='upper right')
plt.xlabel('TP: Chronological Lab Identifier')
plt.ylabel('Fraction Modern (FM)')
plt.xlim(60000, 90000)
plt.ylim(0, yylim)

# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/Blanks.png', dpi=300, bbox_inches="tight")
res = pd.DataFrame({"Name": name, "R": knownR,"Mean FM": wmean, "Mean FM 1sigma": one_sigma, "Chi2 Reduced": chi2_red, "n": n, "wtgraph_mean": mean_wtgraph, 'mean_RTS':mean_RTS, 'mean_RTS_SIG': mean_RTS_sig}).reset_index(drop=True)
res.to_csv('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/summary_table.csv')
# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 4:8])

for i in range(0, len(blank_r_list)):
    subset = res.loc[res['R'] == blank_r_list[i]].reset_index(drop=True)
    plt.errorbar(subset['Name'], subset['Mean FM'], yerr=subset['Mean FM 1sigma'], fmt=markers[i], color=f'{colors[i]}', ecolor=f'{colors[i]}', capsize=5)

plt.xticks(rotation=45, ha='right')
plt.title('Mean FM with 1σ Error')
plt.ylim(0, yylim)
plt.yticks([], [])
plt.legend()

# September 6, 2024
# add another subplot showing water blank before and after
xtr_subsplot = fig.add_subplot(gs[0:1, 8:9])

# from above for reference
# blank_Rs = df.loc[df['Job::R'].isin(blank_r_list)].reset_index(drop=True)
# we can filter before and after water blanks based on TP#
b4 = blank_Rs.loc[(blank_Rs['Job::R'] == '14047_11') & (blank_Rs['TP'] < 87423)]
aft = blank_Rs.loc[(blank_Rs['Job::R'] == '14047_11') & (blank_Rs['TP'] > 87422)]

b4_mean = np.mean(b4['F_corrected_normed'].astype(float))
b4_std = np.std(b4['F_corrected_normed'].astype(float))

aft_mean = np.mean(aft['F_corrected_normed'].astype(float))
aft_std = np.std(aft['F_corrected_normed'].astype(float))

plt.errorbar('Carrera Marble Water Line Historical', b4_mean, yerr=b4_std, fmt=markers[6], color=f'{colors[6]}', ecolor=f'{colors[6]}', capsize=5)
plt.errorbar('Carrera Marble Water Line Current', aft_mean, yerr=aft_std, fmt=markers[6], color=f'{colors[6]}', ecolor=f'{colors[6]}', capsize=5)
plt.ylim(0,yylim)
plt.yticks([], [])
plt.xticks(rotation=45, ha='right')
# plt.show()
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/Blanks.png', dpi=300, bbox_inches="tight")
plt.close()


"""
PLOTS THE BLANKS AGAIN BUT WITH XXU PLOT
"""
from matplotlib.ticker import ScalarFormatter

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Set the x and y scales to logarithmic
ax.set_xscale('log')
ax.set_yscale('log')

# Set the limits for x and y axes
ax.set_xlim(0.1, 10)
ax.set_ylim(0.0001, .1)

# Add labels to the axes
ax.set_xlabel('Sample Size (mg)')
ax.set_ylabel('Ratio to OX-1')
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.xaxis.get_major_formatter().set_scientific(False)
ax.yaxis.get_major_formatter().set_scientific(False)
# Add a grid for better readability
ax.grid(True, which="both", ls="--")

# add the diagonal lines
x = [0.001, 10]
# y1 = [0.2, .00002]
# y2 = [0.3, .00003]
# y3 = [0.4, .00004]
# y4 = [0.5, .00005]
# y5 = [0.6, .00006]
# y6 = [0.8, .00008]
y7 = [1, .0001]
y8 = [2, .0002]
y9 = [5, .0005]
# ys = [y1, y2, y3, y4, y5, y6, y7, y8, y9]
ys = [y7, y8, y9]
labels = ['0.2','0.3','0.4','0.5','0.6','0.8','1','2','5']
for i in range(0, len(ys)):
    plt.plot(x, ys[i], color='k')

for i in range(0, len(blank_r_list)):
    subset = res.loc[res['R'] == blank_r_list[i]].reset_index(drop=True)
    plt.errorbar(subset['wtgraph_mean'], subset['mean_RTS'], yerr=subset['mean_RTS_SIG'], fmt=markers[i], color=f'{colors[i]}', ecolor=f'{colors[i]}', capsize=5, label=f"{names[i]}" )
plt.errorbar(np.mean(aft['wtgraph']), np.mean(aft['RTS']), yerr=np.std(aft['RTS']), fmt=markers[6], color=f'{colors[6]}', ecolor=f'{colors[6]}', capsize=5, label="Water Line AFTER" )

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/Blanks_XXU.png', dpi=300, bbox_inches="tight")

plt.close()

















































































#
#
# # create some arrays in which to store data later
# wmean = []
# one_sigma = []
# sterr = []
# n = []
# name = []
# chi2_red = []
# knownR = []
# ams_cat = []
# df_resdiuals = pd.DataFrame()
#
#
# # lets loop through the subset of data that we've selected in the rows above
# for i in range(0, len(blank_r_list)):
#
#     # this line below actually grabs the subset based on the R number
#     subset = blank_Rs.loc[blank_Rs['Job::R'] == blank_Rs[i]].sort_values(by=['TP']).reset_index(drop=True)
#
#     # line below: we only want to do stats on R numbers where there's at least 3 data points. This also helps remove
#     # loads of one-off R numbers that would clutter the analysis
#     if len(subset) > 10:
#         wm = (np.mean(subset['F_corrected_normed'].astype(float)))
#         wmean.append(np.mean(subset['F_corrected_normed'].astype(float)))  # calculate and append average FM
#         one_sigma.append(np.std(subset['F_corrected_normed'].astype(float))) # calc and append standard deviation
#         n.append(len(subset))
#
#         chi2 = chi2red(subset)
#         chi2_red.append(chi2)
#
#         #prepare the plot
#         one_sig = np.std(subset['F_corrected_normed'].astype(float))
#         desc = subset['sampleDESC']
#         desc = desc.replace('-', '_', regex=True)#
#         desc = desc.replace(':', '_', regex=True)#
#         ddd = subset['Job::AMS Category']
#
#         # append a few more things
#         name.append(desc[0])
#         knownR.append(knowns_Rs[i])
#         ams_cat.append(ddd[0])
#
#         # find residual
#         subset['Residual'] = (subset['F_corrected_normed'].astype(float) - (np.mean(subset['F_corrected_normed'].astype(float)))) / (np.std(subset['F_corrected_normed'].astype(float)))
#
#         fig = plt.figure(figsize=(12, 8))
#         plt.scatter(subset['TP'], subset['Residual'], color='black', alpha=0.5)
#         plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
#         plt.fill_between(subset['TP'], -1, 1, alpha=.05, color='black')
#         plt.fill_between(subset['TP'], -2, 2, alpha=.05, color='black')
#         plt.title(f'{knowns_Rs[i]}, {desc[0]}, Chi2 Reduced = {"{:.1f}".format(chi2)}')
#         plt.ylabel(f'Residual (x-\u0078\u0305/1-\u03c3)')
#         plt.xlabel('TP, chronological lab identifier')
#         plt.ylim(-3,3)
#         # plt.show()
#         plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/{knowns_Rs[i]}_{desc[0]}.png', dpi=300, bbox_inches="tight")
#         plt.close()
#
#         # concatonate the residual data
#         df_resdiuals = pd.concat([df_resdiuals, subset])
#
# # save the arrays into a dataframe
# res = pd.DataFrame({"Name": name, "R": knownR, "AMScategID": ams_cat, "Mean RTS": wmean, "Mean RTS 1sigma": one_sigma, "Chi2 Reduced": chi2_red, "n": n}).sort_values(by=['Chi2 Reduced']).reset_index(drop=True)
# res.to_csv('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/summary_table.csv')
# #
# df_resdiuals.to_csv('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/df_with_residuals.csv')


#
# knowns = ['CBOr','GB','CBAi','CBIn','UNSt','GB','OX1','OX1_SM'] # although this script is meant for secondaries only, it doesn't huty to just run it for everything, cuz I"m going to filter on it later on to make specific plots of certain groups of secondaries
# sub_list = df.loc[df['AMScategID'].isin(knowns)]  # I'm keeping