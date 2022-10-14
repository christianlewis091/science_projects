import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from X_my_functions import plotfunc_line, plotfunc_scat, plotfunc_2line, plotfunc_error
import matplotlib.gridspec as gridspec

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/samples_with_references10000.xlsx')
ref2 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/harmonized_dataset.xlsx')
ref3 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/reference3.xlsx')

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
First, let's explore the samples wrt Reference 2 (Harmonized Dataset) 
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

plt.errorbar(df['Decimal_date'], df['D14C'], yerr=df['D14Cerr'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
plt.plot(ref2['Decimal_date'], ref2['D14C'], color=a1)
plt.plot(ref3['Decimal_date'], ref3['D14C'], color=a2)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[3:4, 0:1])
plt.errorbar(df['Decimal_date'], df['r2_diff_trend'], yerr=df['r2_diff_trend_errprop'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
plt.ylabel('S - R2', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[4:5, 0:1])
plt.errorbar(df['Decimal_date'], df['r3_diff_trend'], yerr=df['r3_diff_trend_errprop'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
plt.ylabel('S - R3', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[5:6, 0:1])
plt.errorbar(df['Decimal_date'], df['deltadelta'], yerr=df['deltadelta_err'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
plt.ylabel('R2 - R3', fontsize=14)  # label the y axis
plt.xlabel('Date', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot1.png',
            dpi=300, bbox_inches="tight")
plt.close()




fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(df['Decimal_date'], df['Lat'], df['r2_diff_trend'], c=df['r2_diff_trend'], cmap='viridis', linewidth=0.5)
ax.set_xlabel('Date')
ax.set_ylabel('Lat')
ax.set_zlabel('Sample - ref');
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot_3d.png',
            dpi=300, bbox_inches="tight")
plt.close()
#
#
