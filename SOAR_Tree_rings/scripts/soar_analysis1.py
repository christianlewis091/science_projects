import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from X_my_functions import plotfunc_line, plotfunc_scat, plotfunc_2line, plotfunc_error
import matplotlib.gridspec as gridspec

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/samples_with_references10000.xlsx')
ref2 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/harmonized_dataset.xlsx')
ref3 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/reference3.xlsx')

df = df.loc[df['Decimal_date'] > 1987]
ref2 = ref2.loc[ref2['Decimal_date'] > 1987]
ref3 = ref3.loc[ref3['Decimal_date'] > 1987]
# I need to drop the index column in order to drop some duplicates that made their way through
df = df[['Ring code', 'R number', 'Site', 'F14C',
         'F14Cerr', 'Decimal_date', 'D14C', 'D14Cerr', 'Lat', 'Lon', '#location',
         'Sample', 'Lab', 'Analysis', 'Sample ', 'Sample.1', 'Average of Dates',
         'd13C', 'Flag', 'D14C_1', 'weightedstderr_D14C_1', 'sampler_id',
         'wheightedanalyticalstdev_D14C', 'D14C_ref2s_mean', 'D14C_ref2s_std',
         'D14C_ref2t_mean', 'D14C_ref2t_std', 'D14C_ref3s_mean',
         'D14C_ref3s_std', 'D14C_ref3t_mean', 'D14C_ref3t_std']]

# x_0 = len(df)
# some duplicates were able to slide through from initial dataset from Jocelyn, through cleaning process, to here
df = df.drop_duplicates()
# x_1 = len(df)
# dx = x_0-x_1
# print(x_0)
# print(x_1)
# print(dx) # shows the amount of duplicates that were dropped

"""
Currently, the data has two types of "sample D14C values". There is the 1) Original D14C values, and "corrected" D14C values
which are called D14C_1. These corrected values only exist for NEU and MCQ datasets, and will be used in reference to 
the harmonized dataset, where the reference also has a correction applied. However, in the dataframe, the SOAR data cells
wrt D14C_1 are completely empty (because no corrected data exists), and this may complicate the otherwise simple script. 
Therefore, I'm going to tell python, wherever D14C_1 is NaN, put in the data from D14C. 
"""

mtarray = []
mtarray2 = []
for i in range(0, len(df)):
    df_row = df.iloc[i]

    if pd.isna(df_row['D14C_1']) is True:
        mtarray.append(df_row['D14C'])
        mtarray2.append(df_row['D14Cerr'])
    else:
        mtarray.append(df_row['D14C_1'])
        mtarray2.append(df_row['weightedstderr_D14C_1'])

df['D14C_1'] = mtarray
df['weightedstderr_D14C_1'] = mtarray2
# df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/test.xlsx')
# Checked, it works!


"""
How is the data when viewed relative to reference 2 and reference 3? 
"""
# The difference between the CORRECTED samples, and REFERENCE 2, the harmonized reference
df['r2_diff_trend'] = df['D14C_1'] - df['D14C_ref2t_mean']
df['r2_diff_trend_errprop'] = np.sqrt(df['weightedstderr_D14C_1']**2 + df['D14C_ref2t_std']**2)

# The difference between the raw samples, and REFERENCE 3, BHD with CGO in the gaps
df['r3_diff_trend'] = df['D14C'] - df['D14C_ref3t_mean']
df['r3_diff_trend_errprop'] = np.sqrt(df['D14Cerr']**2 + df['D14C_ref3t_std']**2)

# And the difference between the two differences...
df['deltadelta'] = df['r2_diff_trend'] - df['r3_diff_trend']
df['deltadelta_err'] = np.sqrt(df['r2_diff_trend_errprop']**2 + df['r3_diff_trend_errprop']**2)
#
# df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/testing.xlsx')
#


"""
Break up the data by general latitude bands 
"""
# you can easily see the different latitude bands where the data falls in the 3D plot, see 3d3.png, or you can recreate
# it below and actually play around with moving the plot. I determined where to draw the bands based on this visual cue

b1 = df.loc[(df['Lat'] > - 40) & (df['Lat'] < - 39)]
b2 = df.loc[(df['Lat'] > - 42) & (df['Lat'] < - 40)]
b3 = df.loc[(df['Lat'] > - 44.25) & (df['Lat'] < - 43)]
b4 = df.loc[(df['Lat'] > - 47) & (df['Lat'] < - 46)]
b5 = df.loc[(df['Lat'] > - 48) & (df['Lat'] < - 47)]
b6 = df.loc[(df['Lat'] > - 53) & (df['Lat'] < - 52)]
b7 = df.loc[(df['Lat'] > - 54) & (df['Lat'] < - 53)]
b8 = df.loc[(df['Lat'] > - 55.5) & (df['Lat'] < - 54)]

# See Plot 2 for the data based on the indexing above
# now we find the summary data based on each

datas = [b1, b2, b3, b4, b5, b6, b7, b8]
lats = [-39, -41, -43, -46, -47, -52, -53, -54]
mean_array_ref2 = []
std_error_array_ref2 = []
mean_array_ref3 = []
std_error_array_ref3 = []
stdev1 = []
stdev2 = []
for i in range(0, len(datas)):
    data = datas[i]  # grab first dataset
    mean1 = np.mean(data['r2_diff_trend'])
    mean2 = np.mean(data['r3_diff_trend'])
    stdevr1 = (np.std(data['r2_diff_trend']))
    stdevr2 = (np.std(data['r3_diff_trend']))
    std_err2 = (np.std(data['r2_diff_trend'])) / len(data)
    std_err3 = (np.std(data['r3_diff_trend'])) / len(data)

    mean_array_ref2.append(mean1)
    mean_array_ref3.append(mean2)
    stdev1.append(stdevr1)
    stdev2.append(stdevr2)
    std_error_array_ref2.append(std_err2)
    std_error_array_ref3.append(std_err3)


"""
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
PLOTTING FUNCTIONS
"""
# https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3
# Skyblue to distant mountain green
a1, a2, a3, a4, a5, a6 = '#253494','#7fcdbb','#2c7fb8','#c7e9b4','#41b6c4','#ffffcc'
c1, c2, c3 = '#ece2f0', '#a6bddb', '#1c9099'
d1, d2 = '#ef8a62', '#67a9cf'
size1 = 10
ch1 = 'black'
ch2 = a3
alph = .9
# Look at ALL the data relative to Reference 2 and Reference 3
p1 = plotfunc_2line(ref2['Decimal_date'], ref2['D14C'], color_p1='black', size1=5, px2=ref3['Decimal_date'], py2=ref3['D14C'], sx1=df['Decimal_date'], sy1=df['D14C_1'], name='firstlook')

p2 = plotfunc_error(df['Decimal_date'], df['deltadelta'], df['deltadelta_err'], ylab='\u0394Reference2 - \u0394Reference3 - (\u2030) [NWT3]', name='Errorplot1')


# fig = plt.figure()
# ax = plt.axes(projection='3d')
# plt.scatter(df['Decimal_date'], df['D14C_1'], cmap='viridis', linewidth=0.5)
#
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/main1.png',
#             dpi=300, bbox_inches="tight")


fig = plt.figure(4, figsize=(10, 12.5))
gs = gridspec.GridSpec(6, 1)
gs.update(wspace=.35, hspace=.25)

xtr_subsplot = fig.add_subplot(gs[0:3, 0:1])

# plt.errorbar(df['Decimal_date'], df['D14C'], yerr=df['D14Cerr'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
plt.plot(df['Decimal_date'],df['D14C_ref2t_mean'], color=a1, label='R2 (BHD+CGO, harmonized')
plt.plot(df['Decimal_date'], df['D14C_ref3t_mean'], color=a2, label='R3 (BHD w CGO in gaps')
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.legend()

xtr_subsplot = fig.add_subplot(gs[3:4, 0:1])
plt.errorbar(df['Decimal_date'], df['r2_diff_trend'], yerr=df['r2_diff_trend_errprop'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
plt.ylabel('S - R2', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[4:5, 0:1])
plt.errorbar(df['Decimal_date'], df['r3_diff_trend'], yerr=df['r3_diff_trend_errprop'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
plt.ylabel('S - R3', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[5:6, 0:1])
plt.errorbar(df['Decimal_date'], df['deltadelta'], yerr=df['deltadelta_err'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
plt.ylabel('plot b - c', fontsize=14)  # label the y axis
plt.xlabel('Date', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot1.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""3d PLOT"""
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.scatter(df['Decimal_date'], df['Lat'], df['r2_diff_trend'], c=df['r2_diff_trend'], cmap='viridis', linewidth=0.5)
# ax.set_xlabel('Date')
# ax.set_ylabel('Lat')
# ax.set_zlabel('Sample - ref');
# # plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot_3d.png',
# #             dpi=300, bbox_inches="tight")
# # plt.close()
# plt.show()


fig = plt.figure(4, figsize=(10, 12.5))
gs = gridspec.GridSpec(8, 4)
gs.update(wspace=.15, hspace=.25)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.errorbar(b1['Decimal_date'], b1['r2_diff_trend'], yerr=b1['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha = alph, label='R2')
plt.errorbar(b1['Decimal_date'], b1['r3_diff_trend'], yerr=b1['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha = alph, label='R3')
plt.xticks([])
plt.xlim(1987, 2020)
plt.ylim(-10, 15)

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.errorbar(b2['Decimal_date'], b2['r2_diff_trend'], yerr=b2['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha = alph, label='R2')
plt.errorbar(b2['Decimal_date'], b2['r3_diff_trend'], yerr=b2['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha = alph, label='R3')
plt.legend()
plt.xticks([])
plt.xlim(1987, 2020)
plt.ylim(-10, 15)
plt.yticks([])
xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.errorbar(b3['Decimal_date'], b3['r2_diff_trend'], yerr=b3['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha = alph, label='R2')
plt.errorbar(b3['Decimal_date'], b3['r3_diff_trend'], yerr=b3['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha = alph, label='R3')
plt.xticks([])
plt.xlim(1987, 2020)
plt.ylim(-10, 15)
xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
plt.errorbar(b4['Decimal_date'], b4['r2_diff_trend'], yerr=b4['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha = alph, label='R2')
plt.errorbar(b4['Decimal_date'], b4['r3_diff_trend'], yerr=b4['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha = alph, label='R3')
plt.xticks([])
plt.xlim(1987, 2020)
plt.ylim(-10, 15)
plt.yticks([])
xtr_subsplot = fig.add_subplot(gs[4:6, 0:2])
plt.errorbar(b5['Decimal_date'], b5['r2_diff_trend'], yerr=b5['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha = alph, label = 'R2')
plt.errorbar(b5['Decimal_date'], b5['r3_diff_trend'], yerr=b5['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha = alph, label='R3')
plt.xticks([])
plt.xlim(1987, 2020)
plt.ylim(-10, 15)
xtr_subsplot = fig.add_subplot(gs[4:6, 2:4])
plt.errorbar(b6['Decimal_date'], b6['r2_diff_trend'], yerr=b6['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha = alph, label='R2')
plt.errorbar(b6['Decimal_date'], b6['r3_diff_trend'], yerr=b6['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha = alph, label='R3')
plt.xticks([])
plt.xlim(1987, 2020)
plt.ylim(-10, 15)
plt.yticks([])
xtr_subsplot = fig.add_subplot(gs[6:8, 0:2])
plt.errorbar(b7['Decimal_date'], b7['r2_diff_trend'], yerr=b7['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha = alph, label='R2')
plt.errorbar(b7['Decimal_date'], b7['r3_diff_trend'], yerr=b7['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha = alph, label='R3')
plt.xlim(1987, 2020)
plt.ylim(-10, 15)
plt.xlabel('Date', fontsize=14)  # label the y axis
xtr_subsplot = fig.add_subplot(gs[6:8, 2:4])
plt.errorbar(b8['Decimal_date'], b8['r2_diff_trend'], yerr=b8['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha = alph, label='R2')
plt.errorbar(b8['Decimal_date'], b8['r3_diff_trend'], yerr=b8['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha = alph, label='R3')
plt.xlim(1987, 2020)
plt.ylim(-10, 15)
plt.yticks([])

# plt.ylabel('plot b - c', fontsize=14)  # label the y axis
plt.xlabel('Date', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot2.png',
            dpi=300, bbox_inches="tight")
plt.close()



fig = plt.figure(4, figsize=(10, 12.5))
gs = gridspec.GridSpec(2, 2)
gs.update(wspace=.15, hspace=0)

xtr_subsplot = fig.add_subplot(gs[0:1, 0:2])
plt.errorbar(lats, mean_array_ref2, std_error_array_ref2, fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha = alph, label='R2')
plt.errorbar(lats, mean_array_ref3, std_error_array_ref3, fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha = alph, label='R3')
plt.xticks([])
plt.ylabel('Average Difference from Reference', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[1:2, 0:2])
plt.errorbar(lats, mean_array_ref2, stdevr1, fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha = alph, label='R2')
plt.errorbar(lats, mean_array_ref3, stdevr2, fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha = alph, label='R3')
plt.xlabel('Latitude', fontsize=14)  # label the y axis
plt.ylabel('Average Difference from Reference', fontsize=14)  # label the y axis

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot3.png',
            dpi=300, bbox_inches="tight")
plt.close()


#
# mean_array_ref2.append(mean1)
# mean_array_ref3.append(mean2)
# std_error_array_ref2.append(std_err2)
# std_error_array_ref3.append(std_err3)