import numpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from X_my_functions import plotfunc_line, plotfunc_scat, plotfunc_2line, plotfunc_error
import matplotlib.gridspec as gridspec

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/samples_with_references10000.xlsx')
ref2 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/harmonized_dataset.xlsx')
ref3 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/reference3.xlsx')

df = df.loc[df['Decimal_date'] > 1980].reset_index(drop=True)
ref2 = ref2.loc[ref2['Decimal_date'] > 1980].reset_index(drop=True)
ref3 = ref3.loc[ref3['Decimal_date'] > 1980].reset_index(drop=True)
# I need to drop the index column in order to drop some duplicates that made their way through
# df = df[['Ring code', 'R number', 'Site', 'F14C',
#          'F14Cerr', 'Decimal_date', 'D14C', 'D14Cerr', 'Lat', 'Lon', '#location',
#          'Sample', 'Lab', 'Analysis', 'Sample ', 'Sample.1', 'Average of Dates',
#          'd13C', 'Flag', 'D14C_1', 'weightedstderr_D14C_1', 'sampler_id',
#          'wheightedanalyticalstdev_D14C', 'D14C_ref2s_mean', 'D14C_ref2s_std',
#          'D14C_ref2t_mean', 'D14C_ref2t_std', 'D14C_ref3s_mean',
#          'D14C_ref3s_std', 'D14C_ref3t_mean', 'D14C_ref3t_std']]

""" 
Need to add lat and lon data to NEUMAYER and MCQ
Need to add a flag for the "Chile" versus "NZ" datasets
Also, all the Lon data are not systematically E or W...
This block of code cleans up all the messiness in the lats and lons, and gives us flags to index later based on country
"""
neumayer_lat = -70.6666
neumayer_lon = -8.2667  # E
mcq_lat = -54.6208
mcq_lon = 158.8556  # E

lat_array = []
lon_array = []
for i in range(0, len(df)):
    current_row = df.iloc[i]
    if current_row['Site'] == 'NMY':
        lat_array.append(neumayer_lat)
        lon_array.append(neumayer_lon)
    elif current_row['Site'] == 'MCQ':
        lat_array.append(mcq_lat)
        lon_array.append(mcq_lon)
    elif current_row['Site'] == '23 Nikau St, Eastbourne, NZ':
        lat_array.append(-41.2923)
        lon_array.append(174.8971)  # change Chilean Longitudes to degrees East.
    elif current_row['Site'] == '19 Nikau St, Eastbourne, NZ':
        lat_array.append(-41.2923)
        lon_array.append(174.8971)  # change Chilean Longitudes to degrees East.
    else:
        lat_array.append(current_row['Lat'])
        lon_array.append(current_row['Lon'])
df['NewLat'] = lat_array
df['NewLon'] = lon_array


df['Country'] = -999  # Chile = 0, NZ = 1, NMY = 2
country_array = []
for i in range(0, len(df)):
    current_row = df.iloc[i]
    if current_row['NewLon'] > 90:
        country_array.append(1)
    elif 50 < current_row['NewLon'] < 90:
        country_array.append(0)
    elif current_row['NewLon'] < 0:
        country_array.append(2)
    else:
        print(current_row)
df['Country'] = country_array


    # test = df.loc[df['#location'] == 'Macquarie_Isl.']  # MCQ looked sparse in the plot
# print(len(test))
# x_0 = len(df)
# some duplicates were able to slide through from initial dataset from Jocelyn, through cleaning process, to here
df = df.drop_duplicates().reset_index(drop=True)
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
# The difference between the CORRECTED samples, and REFERENCE 2, the harmonized reference (WEIGHTED RESIDUAL)
quaderr = np.sqrt(df['weightedstderr_D14C_1']**2 + df['D14C_ref2t_std']**2)

df['r2_diff_trend'] = df['D14C_1'] - df['D14C_ref2t_mean']
df['r2_diff_trend_errprop'] = np.sqrt(df['weightedstderr_D14C_1'] ** 2 + df['D14C_ref2t_std'] ** 2)


# The difference between the raw samples, and REFERENCE 3, BHD with CGO in the gaps (WEIGHTED RESIDUAL)
df['r3_diff_trend'] = df['D14C'] - df['D14C_ref3t_mean']
df['r3_diff_trend_errprop'] = np.sqrt(df['D14Cerr'] ** 2 + df['D14C_ref3t_std'] ** 2)

# And the difference between the two differences...
df['deltadelta'] = df['r2_diff_trend'] - df['r3_diff_trend']
df['deltadelta_err'] = np.sqrt(df['r2_diff_trend_errprop'] ** 2 + df['r3_diff_trend_errprop'] ** 2)
#
# df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/testing.xlsx')
#
df_2 = df  # renaming for import into second analytical file

"""
Break up the data by general latitude bands 
"""
# you can easily see the different latitude bands where the data falls in the 3D plot, see 3d3.png, or you can recreate
# it below and actually play around with moving the plot. I determined where to draw the bands based on this visual cue

b1 = df.loc[(df['NewLat'] > - 40) & (df['NewLat'] <= - 39)]
b2 = df.loc[(df['NewLat'] > - 42) & (df['NewLat'] < - 40)]
b3 = df.loc[(df['NewLat'] > - 44.25) & (df['NewLat'] < - 43)]
b4 = df.loc[(df['NewLat'] > - 47) & (df['NewLat'] < - 46)]
b5 = df.loc[(df['NewLat'] > - 48) & (df['NewLat'] < - 47)]
b6 = df.loc[(df['NewLat'] > - 53) & (df['NewLat'] < - 52)]
b7 = df.loc[(df['NewLat'] > - 54) & (df['NewLat'] < - 53)]
b8 = df.loc[(df['NewLat'] > - 55.5) & (df['NewLat'] < - 54)]
b9 = df.loc[(df['NewLat'] > - 60) & (df['NewLat'] < -55.5)]
b10 = df.loc[(df['NewLat'] > - 75) & (df['NewLat'] < -60)]

# See Plot 2 for the data based on the indexing above
# now we find the summary data based on each
# (This loop finds the mean and standard deviation of the b1-b9 above, and links it to a lat lon
datas = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10]
lats = [-40, -42, -44, -47, -48, -53, -54, -55, -60, -75] # The MAX LAT
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
    mean_array_ref2.append(mean1)
    mean_array_ref3.append(mean2)
    stdev1.append(stdevr1)
    stdev2.append(stdevr2)


"""
I want to answer the question: In how many cases are Reference 1 and reference 2 outside of each other's 1-sigma errors? 
"""




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
a1, a2, a3, a4, a5, a6 = '#253494', '#7fcdbb', '#2c7fb8', '#c7e9b4', '#41b6c4', '#ffffcc'
c1, c2, c3 = '#ece2f0', '#a6bddb', '#1c9099'
d1, d2 = '#ef8a62', '#67a9cf'
colors = [a1, a2, a3, a4, a5, a6, c1, c2, c3, d1, d2,a1, a2, a3, a4, a5, a6, c1, c2, c3, d1, d2,a1, a2, a3, a4, a5, a6, c1, c2, c3, d1, d2]
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D']
size1 = 10
ch1 = 'black'
ch2 = a3
alph = .9
# Look at ALL the data relative to Reference 2 and Reference 3
p1 = plotfunc_2line(ref2['Decimal_date'], ref2['D14C'], color_p1='black', size1=5, px2=ref3['Decimal_date'],
                    py2=ref3['D14C'], sx1=df['Decimal_date'], sy1=df['D14C_1'], name='firstlook')

p2 = plotfunc_error(df['Decimal_date'], df['deltadelta'], df['deltadelta_err'],
                    ylab='\u0394Reference2 - \u0394Reference3 - (\u2030) [NWT3]', name='Errorplot1')
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# plt.scatter(df['Decimal_date'], df['D14C_1'], cmap='viridis', linewidth=0.5)
#
# # plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/main1.png',
# #             dpi=300, bbox_inches="tight")
plt.show()
plt.close()
"""The below block of code was made redundant in edits"""
# """
# For the next plot, I want to plot by site, but I need to slightly adjust the site tab since
# some sites appear in different places than others
# """
# site_array = []
# for i in range(0, len(df)):
#     current_row = df.iloc[i]
#     if str(current_row['#location']) == 'nan':
#         site_array.append(current_row['Site'])
#     elif str(current_row['Site']) == 'nan':
#         site_array.append(current_row['#location'])
# df['SiteNew'] = site_array
# df = df.sort_values(by=['Decimal_date'], ascending=False).reset_index(drop=True)

locs = np.unique(df['Site'])


fig = plt.figure(4, figsize=(15, 10))
gs = gridspec.GridSpec(6, 3)
gs.update(wspace=.15, hspace=.35)


xtr_subsplot = fig.add_subplot(gs[0:3, 0:1])
plt.title('Background Reference')
plt.text(1980, 8, '[A]', fontsize=12)
# plt.errorbar(df['Decimal_date'], df['D14C'], yerr=df['D14Cerr'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
plt.plot(df['Decimal_date'], df['D14C_ref2t_mean'], color=a1, label='R2 (BHD+CGO, harmonized)')
plt.plot(df['Decimal_date'], df['D14C_ref3t_mean'], color=a2, label='R3 (BHD w CGO in gaps)')
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.ylim(0, 300)
plt.legend()

xtr_subsplot = fig.add_subplot(gs[0:3, 1:2])
for i in range(0, len(locs)):
    col = colors[i]
    mark = markers[i]
    slice = df.loc[df['Site'] == str(locs[i])]  # grab the first data to plot, based on location
    plt.scatter(slice['Decimal_date'], slice['D14C'], label='{}'.format(str(locs[i])), color=col, marker=mark, alpha = 0.5)
plt.title('Southern Hemisphere Tree Rings and Atmos. Samples')
plt.ylim(0, 300)
plt.text(1980, 8, '[B]', fontsize=12)
plt.yticks([])
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

xtr_subsplot = fig.add_subplot(gs[3:4, 0:3])
plt.text(1978.5, -20, '[C]', fontsize=12)
# plt.title('Samples Relative to Reference 2')
plt.errorbar(df['Decimal_date'], df['r2_diff_trend'], yerr=df['r2_diff_trend_errprop'], fmt='o', color='black',
             ecolor='black', elinewidth=1, capsize=2, alpha=0.5)
plt.xticks([])

xtr_subsplot = fig.add_subplot(gs[4:5, 0:3])
# plt.title('Samples Relative to Reference 3')
plt.errorbar(df['Decimal_date'], df['r3_diff_trend'], yerr=df['r3_diff_trend_errprop'], fmt='o', color='black',
             ecolor='black', elinewidth=1, capsize=2, alpha=0.5)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y a
plt.xticks([])
plt.text(1978.5, -20, '[D]', fontsize=12)

xtr_subsplot = fig.add_subplot(gs[5:6, 0:3])
# plt.title('Plot C - D')
plt.errorbar(df['Decimal_date'], df['deltadelta'], yerr=df['deltadelta_err'], fmt='o', color='black', ecolor='black',
             elinewidth=1, capsize=2, alpha=0.5)
plt.text(1978.5, -7.50, '[E]', fontsize=12)
plt.xlabel('Date', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot1.png',
            dpi=300, bbox_inches="tight")

plt.close()

# """3d PLOT"""
# fig = plt.figure()
# ax = plt.axes(projection='3d')
# ax.scatter(df['Decimal_date'], df['NewLat'], df['r2_diff_trend'], c=df['r2_diff_trend'], cmap='viridis', linewidth=0.5)
# ax.set_xlabel('Date')
# ax.set_ylabel('Lat')
# ax.set_zlabel('Sample - ref');
# # plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot_3d.png',
# #             dpi=300, bbox_inches="tight")
# # plt.close()
# plt.show()


fig = plt.figure(4, figsize=(10, 12.5))
gs = gridspec.GridSpec(10, 4)
gs.update(wspace=.15, hspace=.25)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.errorbar(b1['Decimal_date'], b1['r2_diff_trend'], yerr=b1['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1,
             elinewidth=1, capsize=2, alpha=alph, label='R2')
plt.errorbar(b1['Decimal_date'], b1['r3_diff_trend'], yerr=b1['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2,
             elinewidth=1, capsize=2, alpha=alph, label='R3')
plt.xticks([])
plt.xlim(1980, 2020)
plt.ylim(-10, 15)

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.errorbar(b2['Decimal_date'], b2['r2_diff_trend'], yerr=b2['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1,
             elinewidth=1, capsize=2, alpha=alph, label='R2')
plt.errorbar(b2['Decimal_date'], b2['r3_diff_trend'], yerr=b2['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2,
             elinewidth=1, capsize=2, alpha=alph, label='R3')
plt.legend()
plt.xticks([])
plt.xlim(1980, 2020)
plt.ylim(-10, 15)
plt.yticks([])
xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.errorbar(b3['Decimal_date'], b3['r2_diff_trend'], yerr=b3['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1,
             elinewidth=1, capsize=2, alpha=alph, label='R2')
plt.errorbar(b3['Decimal_date'], b3['r3_diff_trend'], yerr=b3['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2,
             elinewidth=1, capsize=2, alpha=alph, label='R3')
plt.xticks([])
plt.xlim(1980, 2020)
plt.ylim(-10, 15)
xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
plt.errorbar(b4['Decimal_date'], b4['r2_diff_trend'], yerr=b4['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1,
             elinewidth=1, capsize=2, alpha=alph, label='R2')
plt.errorbar(b4['Decimal_date'], b4['r3_diff_trend'], yerr=b4['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2,
             elinewidth=1, capsize=2, alpha=alph, label='R3')
plt.xticks([])
plt.xlim(1980, 2020)
plt.ylim(-10, 15)
plt.yticks([])
xtr_subsplot = fig.add_subplot(gs[4:6, 0:2])
plt.errorbar(b5['Decimal_date'], b5['r2_diff_trend'], yerr=b5['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1,
             elinewidth=1, capsize=2, alpha=alph, label='R2')
plt.errorbar(b5['Decimal_date'], b5['r3_diff_trend'], yerr=b5['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2,
             elinewidth=1, capsize=2, alpha=alph, label='R3')
plt.xticks([])
plt.xlim(1980, 2020)
plt.ylim(-10, 15)
xtr_subsplot = fig.add_subplot(gs[4:6, 2:4])
plt.errorbar(b6['Decimal_date'], b6['r2_diff_trend'], yerr=b6['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1,
             elinewidth=1, capsize=2, alpha=alph, label='R2')
plt.errorbar(b6['Decimal_date'], b6['r3_diff_trend'], yerr=b6['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2,
             elinewidth=1, capsize=2, alpha=alph, label='R3')
plt.xticks([])
plt.xlim(1980, 2020)
plt.ylim(-10, 15)
plt.yticks([])
xtr_subsplot = fig.add_subplot(gs[6:8, 0:2])
plt.errorbar(b7['Decimal_date'], b7['r2_diff_trend'], yerr=b7['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1,
             elinewidth=1, capsize=2, alpha=alph, label='R2')
plt.errorbar(b7['Decimal_date'], b7['r3_diff_trend'], yerr=b7['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2,
             elinewidth=1, capsize=2, alpha=alph, label='R3')
plt.xlim(1980, 2020)
plt.ylim(-10, 15)
plt.xticks([])

xtr_subsplot = fig.add_subplot(gs[6:8, 2:4])
plt.errorbar(b8['Decimal_date'], b8['r2_diff_trend'], yerr=b8['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1,
             elinewidth=1, capsize=2, alpha=alph, label='R2')
plt.errorbar(b8['Decimal_date'], b8['r3_diff_trend'], yerr=b8['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2,
             elinewidth=1, capsize=2, alpha=alph, label='R3')
plt.xlim(1980, 2020)
plt.ylim(-10, 15)
plt.yticks([])

xtr_subsplot = fig.add_subplot(gs[8:10, 0:2])
plt.errorbar(b9['Decimal_date'], b9['r2_diff_trend'], yerr=b9['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1,
             elinewidth=1, capsize=2, alpha=alph, label='R2')
plt.errorbar(b9['Decimal_date'], b9['r3_diff_trend'], yerr=b9['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2,
             elinewidth=1, capsize=2, alpha=alph, label='R3')
plt.xlim(1980, 2020)
plt.ylim(-20, 15)
plt.xlabel('Date', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[8:10, 2:4])
plt.errorbar(b10['Decimal_date'], b10['r2_diff_trend'], yerr=b10['r2_diff_trend_errprop'], fmt='o', color=ch1, ecolor=ch1,
             elinewidth=1, capsize=2, alpha=alph, label='R2')
plt.errorbar(b10['Decimal_date'], b10['r3_diff_trend'], yerr=b10['r3_diff_trend_errprop'], fmt='o', color=ch2, ecolor=ch2,
             elinewidth=1, capsize=2, alpha=alph, label='R3')
plt.xlim(1980, 2020)
plt.ylim(-20, 15)
plt.xlabel('Date', fontsize=14)  # label the y axis


# plt.ylabel('plot b - c', fontsize=14)  # label the y axis
plt.xlabel('Date', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/plot2.png',
            dpi=300, bbox_inches="tight")
plt.close()

fig = plt.figure()
plt.errorbar(lats, mean_array_ref2, stdevr1, fmt='o', color=ch1, ecolor=ch1, elinewidth=1, capsize=2, alpha=alph,
             label='R2')
plt.errorbar(lats, mean_array_ref3, stdevr2, fmt='o', color=ch2, ecolor=ch2, elinewidth=1, capsize=2, alpha=alph,
             label='R3')
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





