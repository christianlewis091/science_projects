"""
Follows on from Data Quality Paper 2_2025.py
"""
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

from xcams.OLD_MISC.chi2 import subset

df = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/df_out_from_DQ_2_2025.xlsx')

#
# """
# Define function for plotting comarpative plots
# """
#
# def this_plot(a_x,
#               a_fm, a_fm_err,
#               a_name,
#               b_x,
#               b_fm, b_fm_err,
#               b_name,
#               title):
#
#     # make sure all are numeric
#     a_x = pd.to_numeric(a_x, errors="coerce")
#     a_fm = pd.to_numeric(a_fm, errors="coerce")
#     a_fm_err = pd.to_numeric(a_fm_err, errors="coerce")
#     b_x = pd.to_numeric(b_x, errors="coerce")
#     b_fm = pd.to_numeric(b_fm, errors="coerce")
#     b_fm_err = pd.to_numeric(b_fm_err, errors="coerce")
#
#     fig, axs = plt.subplots(2, 1, figsize=(6, 8), sharex=True)  # 3 rows, 1 column
#
#     a_res = (a['RTS_corrected'] - a['wmean'] ) / a['RTS_corrected_error']
#     b_res = (b['RTS_corrected'] - b['wmean'] ) / b['RTS_corrected_error']
#
#     axs[1].scatter(a_x, a_res, color='black', linestyle='', label=a_name)
#     axs[1].scatter(b_x, b_res, color='gray', linestyle='', label=a_name)
#     axs[1].axhline(y=0, color='black')
#
#     axs[0].errorbar(a_x, a_fm, yerr=a_fm_err, color='black', linestyle='', label = f'{a_name}', marker='o')
#     axs[0].errorbar(b_x, b_fm, yerr=b_fm_err, color='gray', linestyle='', label = f'{b_name}', marker='o')
#     axs[0].legend()
#     axs[1].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
#     axs[0].set_ylabel('Fraction Modern')
#     plt.tight_layout()
#     plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_paper_3_2025_output/treatment_comparisons/{title}.png',
#                 dpi=300, bbox_inches="tight")
#     plt.close()
#
#
#
# """
# The first thing I need to do is run some statistics.
# Albert and JCT have interest in understanding if there are discrepancies between AAA and Cellulose pretreatments
# We can analyze this with some organic secondaries and blank.
# The summary data from the table tells us somethings, but not the whole story. We need to run some t-tests on the sub-dataframes
# """
#
# a = df.loc[df['Job::R'] == '24889/4_CELL_EA']
# a1 = a['F_corrected_normed']
# b = df.loc[df['Job::R'] == '24889/4_CELL_ST']
# b1 = b['F_corrected_normed']
#
# print('')
# print('For FIRI Ds with Cellulose treatment, is there a difference between EA or ST combustion?')
# x,y= stats.ttest_ind(a1,b1)
# if y <= 0.05:
#     print(f"P-valuve is {y:.2f}, datasets can be described as different")
# else:
#     print(f"P-valuve is {y:.2f}, datasets can NOT be described as different")
#
# a = this_plot(a['TP'],
#               a1, a['F_corrected_normed_error'],
#               '24889/4_CELL_EA',
#               b['TP'],
#               b1, b['F_corrected_normed_error'],
#               '24889/4_CELL_ST',
#               'FIRI_D_EA_v_ST')
#
# """
# """
#
# a = df.loc[df['Job::R'] == '24889/7_AAA_EA']
# a1 = a['F_corrected_normed']
# b = df.loc[df['Job::R'] == '24889/7_AAA_ST']
# b1 = b['F_corrected_normed']
#
# print('')
# print('For FIRI Gs with AAA treatment, is there a difference between EA or ST combustion?')
# x,y= stats.ttest_ind(a1,b1)
# if y <= 0.05:
#     print(f"P-valuve is {y:.2f}, datasets can be described as different")
# else:
#     print(f"P-valuve is {y:.2f}, datasets can NOT be described as different")
#
# a = this_plot(a['TP'],
#               a1, a['F_corrected_normed_error'],
#               '24889/7_AAA_EA',
#               b['TP'],
#               b1, b['F_corrected_normed_error'],
#               '24889/7_AAA_ST',
#               'FIRI_G_EA_v_ST')
#
#
# """
# """
#
# a = df.loc[df['Job::R'] == '24889/4_AAA_EA']
# a1 = a['F_corrected_normed']
# b = df.loc[(df['Job::R'] == '24889/4_CELL_EA')]
# b1 = b['F_corrected_normed']
#
# print('')
# print('For FIRI Ds both through EA, do we see a differnece between AAA and Cellulose?')
# x,y= stats.ttest_ind(a1,b1)
# if y <= 0.05:
#     print(f"P-valuve is {y:.2f}, datasets can be described as different")
# else:
#     print(f"P-valuve is {y:.2f}, datasets can NOT be described as different")
#
#
# a = this_plot(a['TP'],
#               a1, a['F_corrected_normed_error'],
#               '24889/4_AAA_EA',
#               b['TP'],
#               b1, b['F_corrected_normed_error'],
#               '24889/4_CELL_EA',
#               'FIRI_D_AAA_v_CELL')
#
# """
#
# """
#
# a = df.loc[df['Job::R'] == '24889/9_CELL_EA']
# a1 = a['F_corrected_normed']
# b = df.loc[df['Job::R'] == '24889/9_AAA_EA']
# b1 = b['F_corrected_normed']
#
# print('')
# print('For FIRI Is with EAs, do we see difference beween AAA and Cellulose pretreatment? ?')
# x,y= stats.ttest_ind(a1,b1)
# if y <= 0.05:
#     print(f"P-valuve is {y:.2f}, datasets can be described as different")
# else:
#     print(f"P-valuve is {y:.2f}, datasets can NOT be described as different")
#
# a = this_plot(a['TP'],
#               a1, a['F_corrected_normed_error'],
#               '24889/9_CELL_EA',
#               b['TP'],
#               b1, b['F_corrected_normed_error'],
#               '24889/9_AAA_EA',
#               'FIRI_I_AAA_v_CELL')
#


"""
I want to make a RTS v 1/m plot to display the blanks 
"""

blanks = ['40699/1','40430/3','14047/1','14047/11','40142/2_AAA_EA','40142/2_AAA_ST','40142/1_CELL_EA','40142/1_CELL_ST']
name = ['Kapuni Comb-Graph','Air Dead CO2','Carrera Marble Carbonate Line','Carrera Marble Water Line','Kauri AAA_EA','Kauri AAA_ST','Kauri Cellulose_EA','Kauri Cellulose_ST']

for i in range(0, len(blanks)):
    subset2 = df.loc[df['Job::R'] == blanks[i]]

    fig, axs = plt.subplots(2, 1, figsize=(6, 8))  # 3 rows, 1 column

    axs[0].errorbar(subset2['TP'],subset2['RTS_corrected'] , yerr=subset2['RTS_corrected_error'], color='black', linestyle='', label = f'{name[i]}', marker='o')
    axs[0].legend()

    axs[1].scatter(1/(subset2['wtgraph']), subset2['RTS_corrected'], c=subset2['TP'], cmap='binary', linestyle='')
    axs[1].set_ylim(0,0.02)
    axs[0].set_xlim(50000,90000)
    plt.tight_layout()
    plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_paper_3_2025_output/blanks/{name[i]}.png',
                dpi=300, bbox_inches="tight")
    plt.close()



import matplotlib.pyplot as plt
from cmcrameri import cm  # colorblind-friendly colormaps

fig, axs = plt.subplots(2, 1, figsize=(12, 8))
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D']

# choose a color map with enough colors for your number of blanks
colors = getattr(cm, 'lipari')(np.linspace(.8, .2, len(blanks)))

for i in range(len(blanks)):
    subset2 = df.loc[df['Job::R'] == blanks[i]]

    axs[0].errorbar(subset2['TP'],subset2['RTS_corrected'], yerr=subset2['RTS_corrected_error'],linestyle='',marker=markers[i] ,label=f'{name[i]}',color=colors[i])
    axs[1].scatter(1 / subset2['wtgraph'],subset2['RTS_corrected'], color=colors[i])

    # Put legend *outside* right side of plot
    axs[0].legend(bbox_to_anchor=(1.05, 1),loc='upper left',borderaxespad=0.)


plt.tight_layout()
plt.savefig(
    r'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_3_2025_output/blanks/all_blanks.png',dpi=300, bbox_inches="tight")
plt.close()




"""
Kapuni blank only
"""
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/df_out_from_DQ_2_2025.xlsx')


name = 'Kapuni - Machine Blank'

subset2 = df.loc[df['Job::R'] == '40699/1']

wmean_num = np.sum(subset2['F_corrected_normed']/subset2['F_corrected_normed_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
wmean_dem = np.sum(1/subset2['F_corrected_normed_error']**2)
wmean = wmean_num / wmean_dem
print(wmean)


fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # 3 rows, 1 column

axs[0].errorbar(subset2['TP'],subset2['F_corrected_normed'] , yerr=subset2['F_corrected_normed_error'], color='black', linestyle='', label = f'{name}', marker='o')
axs[0].legend()

axs[1].scatter(1/(subset2['wtgraph']), subset2['F_corrected_normed'], c=subset2['TP'], cmap='binary', linestyle='')


axs[0].set_ylabel('Fraction Modern')
axs[1].set_ylabel('Fraction Modern')

axs[0].set_xlabel('TP')
axs[1].set_xlabel('1/mg')

axs[0].set_ylim(0,0.0045)
axs[1].set_ylim(0,0.0045)
axs[1].tick_params(axis='y', which='both', left=False, labelleft=False)

axs[0].axhline(wmean, color='black')
axs[1].axhline(wmean, color='black')

plt.tight_layout()
plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_paper_3_2025_output/blanks/Kapuni_special_plot.png',
            dpi=300, bbox_inches="tight")






import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/df_out_from_DQ_2_2025.xlsx')

name = 'Carrera Marble Water Line'

plt.figure(figsize=(8, 6))

subset = df.loc[(df['Job::R'] == '14047/11')]
wmean_num = np.sum(subset['F_corrected_normed']/subset['F_corrected_normed_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
wmean_dem = np.sum(1/subset['F_corrected_normed_error']**2)
wmean = wmean_num / wmean_dem

#before blank fix
subset2 = df.loc[(df['Job::R'] == '14047/11') & (df['TW'] < 3488)]
wmean_num = np.sum(subset2['F_corrected_normed']/subset2['F_corrected_normed_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
wmean_dem = np.sum(1/subset2['F_corrected_normed_error']**2)
wmean2 = wmean_num / wmean_dem

# afterblank fix
subset3 = df.loc[(df['Job::R'] == '14047/11') & (df['TW'] >= 3488)]
wmean_num = np.sum(subset3['F_corrected_normed']/subset3['F_corrected_normed_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
wmean_dem = np.sum(1/subset3['F_corrected_normed_error']**2)
wmean3 = wmean_num / wmean_dem
print()
print('std3')
print(np.std(subset3['F_corrected_normed']))
print()

xmax = np.max(df['TP'])
xmin = np.max(df['TP'])
# TP 87300 is after the 87272 control on the water test wheel
plt.hlines(wmean2, xmin=np.min(subset2['TP']), xmax=87300, colors='black')
plt.hlines(wmean3, xmin=87300, xmax=np.max(subset3['TP']), colors='red', zorder=10)

plt.axvline(87300, color='black', linestyle='--', alpha=0.5)

plt.errorbar(subset2['TP'],subset2['F_corrected_normed'] , yerr=subset2['F_corrected_normed_error'], color='black', linestyle='', marker='o')
plt.errorbar(subset3['TP'],subset3['F_corrected_normed'] , yerr=subset3['F_corrected_normed_error'], color='black', linestyle='', label = f'{name}', marker='o')
plt.legend()

plt.ylabel('Fraction Modern')
plt.xlabel('TP')

plt.tight_layout()
plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_paper_3_2025_output/blanks/waters_special_plot.png',
            dpi=300, bbox_inches="tight")
print(wmean)
print(wmean2)
print(wmean3)
print('Differences between the wmean (for all waters blanks) and those found in the table at the 6th decimal point (should I eye roll at myself?) are beacuse im taking the wmean of rts and then converting to FM for table, while taking wmean of FM here')




















#
# """
# REPEAT THE ABOVE FOR THE ORGANICS PLOT!
# """
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# # SPLIT AXES DOCUMENTATION
# # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/broken_axis.html
#
# carb1 = df.loc[df['Job::R'] == '14047/12'] # IAEA-C2: Freshwater Travertine waterline
# carb2 = df.loc[df['Job::R'] == '14047/2'] # IAEA-C2: Freshwater Travertine carbonate
#
# carb3 = df.loc[df['Job::R'] == '41347/12'] # LAC1 coral water
# carb4 = df.loc[df['Job::R'] == '41347/2'] # LAC1 coral carbonate
#
# carb5 = df.loc[df['Job::R'] == '41347/13'] # LAA1 coral water
# carb6 = df.loc[df['Job::R'] == '41347/3'] # LAC1 coral carbonate
#
# # Create figure and 3 vertical subplots
# fig, axs = plt.subplots(4, 1, figsize=(6, 8), sharex=True)  # 3 rows, 1 column
#
# # First subplot
# axs[0].scatter(carb1['TP'], carb1['residual'], color='black', linestyle='', label = 'IAEA-C2: Water line')
# axs[0].scatter(carb2['TP'], carb2['residual'], color='gray', linestyle='', label = 'IAEA-C2: Carbonate Line')
#
# axs[0].scatter(carb3['TP'], carb3['residual'], color='red', linestyle='', label = 'LAC1 coral water')
# axs[0].scatter(carb4['TP'], carb4['residual'], color='green', linestyle='', label = 'LAC1 coral carbonate')
#
# axs[0].scatter(carb5['TP'], carb5['residual'], color='yellow', linestyle='', label = 'LAA1 coral water')
# axs[0].scatter(carb6['TP'], carb6['residual'], color='orange', linestyle='', label = 'LAC1 coral carbonate')
#
# axs[0].axhline(y=0, color='black')
#
#
# # Second subplot
# axs[3].errorbar(carb1['TP'], carb1['delta_14C_new'], yerr=carb1['delta_14C_err_new'], color='black', linestyle='', label = 'IAEA-C2: Waterline', marker='o')
# axs[3].errorbar(carb2['TP'], carb2['delta_14C_new'],  yerr=carb2['delta_14C_err_new'], color='gray', linestyle='', label = 'IAEA-C2: Carbonate Line', marker='o')
#
# # Second subplot
# axs[1].errorbar(carb3['TP'], carb3['delta_14C_new'], yerr=carb3['delta_14C_err_new'], color='red', linestyle='', label = 'LAC1 coral water', marker='o')
# axs[1].errorbar(carb4['TP'], carb4['delta_14C_new'],  yerr=carb4['delta_14C_err_new'], color='green', linestyle='', label = 'LAC1 coral carbonate', marker='o')
#
# # Second subplot
# axs[2].errorbar(carb5['TP'], carb5['delta_14C_new'], yerr=carb5['delta_14C_err_new'], color='yellow', linestyle='', label = 'LAA1 coral water', marker='o')
# axs[2].errorbar(carb6['TP'], carb6['delta_14C_new'],  yerr=carb6['delta_14C_err_new'], color='orange', linestyle='', label = 'LAC1 coral carbonate', marker='o')
#
#
# axs[1].spines.bottom.set_visible(False)  # removes spine on bottom of 1
# axs[2].spines.bottom.set_visible(False)  # removes spine on bottom of 2
# axs[2].spines.top.set_visible(False)  # removes spine on top of 2
# axs[3].spines.top.set_visible(False)  # removes spine on top of 3
# axs[1].tick_params(axis='x', which='both', bottom=False, labelbottom=False)
# axs[2].tick_params(axis='x', which='both', bottom=False, labelbottom=False)
# axs[3].tick_params(axis='x', which='both', top=False, labeltop=False)
# axs[1].legend()
# axs[2].legend()
# axs[3].legend()
#
#
# # axs[1].tick_params(labeltop=False)  # don't put tick labels at the top
# # # axs[2].tick_params(labelbottom=False)  # don't put tick labels at the top
#
# d = .5  # proportion of vertical to horizontal extent of the slanted line
# kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
#               linestyle="none", color='k', mec='k', mew=1, clip_on=False)
# axs[1].plot([0, 1], [0, 0], transform=axs[1].transAxes, **kwargs)
# axs[2].plot([0, 1], [1, 1], transform=axs[2].transAxes, **kwargs)
# axs[2].plot([0, 1], [0, 0], transform=axs[2].transAxes, **kwargs)
# axs[3].plot([0, 1], [1, 1], transform=axs[3].transAxes, **kwargs)
#
#
# axs[0].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
# axs[1].set_ylabel('\u0394$^1$$^4$C (\u2030)')
# axs[2].set_ylabel('\u0394$^1$$^4$C (\u2030)')
# axs[3].set_ylabel('\u0394$^1$$^4$C (\u2030)')
# # Adjust layout so titles and labels don't overlap
# plt.tight_layout()
#
# plt.savefig(
#     r'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output/Fig1_inorganic.png',
#     dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# ORGANICS
# """
#
# # SPLIT AXES DOCUMENTATION
# # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/broken_axis.html
#
# o1 = df.loc[df['Job::R'] == '24889/14']
# o2 = df.loc[df['Job::R'] == '24889/4_AAA_EA']
# o3 = df.loc[df['Job::R'] == '24889/4_AAA_ST']
# o4 = df.loc[df['Job::R'] == '24889/4_CELL_EA']
# o5 = df.loc[df['Job::R'] == '24889/4_CELL_ST']
#
# # Create figure and 3 vertical subplots
# fig, axs = plt.subplots(2, 1, figsize=(6, 8), sharex=True)  # 3 rows, 1 column
#
# # First subplot
# axs[0].scatter(o1['TP'], o1['residual'], color='black', linestyle='', label = 'RPO')
# axs[0].scatter(o2['TP'], o2['residual'], color='gray', linestyle='', label = 'AAA EA')
# axs[0].scatter(o3['TP'], o3['residual'], color='blue', linestyle='', label = 'AAA ST')
# axs[0].scatter(o4['TP'], o4['residual'], color='red', linestyle='', label = 'CELL EA')
# axs[0].scatter(o5['TP'], o5['residual'], color='yellow', linestyle='', label = 'CELL ST')
# axs[0].axhline(y=0, color='black')
# axs[0].legend()
#
# # Second subplot
# axs[1].errorbar(o1['TP'], o1['delta_14C_new'], yerr=o1['delta_14C_err_new'], color='black', linestyle='', label = 'BHDamb', marker='o')
# axs[1].errorbar(o2['TP'], o2['delta_14C_new'],  yerr=o2['delta_14C_err_new'], color='gray', linestyle='', label = 'BHDspike', marker='o')
# axs[1].errorbar(o3['TP'], o3['delta_14C_new'], yerr=o3['delta_14C_err_new'], color='blue', linestyle='', label = 'BHDamb', marker='o')
# axs[1].errorbar(o4['TP'], o4['delta_14C_new'],  yerr=o4['delta_14C_err_new'], color='yellow', linestyle='', label = 'BHDspike', marker='o')
# axs[1].errorbar(o5['TP'], o5['delta_14C_new'], yerr=o5['delta_14C_err_new'], color='red', linestyle='', label = 'BHDamb', marker='o')
#
# #
# # axs[1].set_ylim(25, 37)
# # axs[2].set_ylim(-77, -66)
#
#
# axs[0].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
# axs[1].set_ylabel('\u0394$^1$$^4$C (\u2030)')
#
# # Adjust layout so titles and labels don't overlap
# plt.tight_layout()
# plt.show()
# plt.savefig(
#     r'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output/Fig1_organics.png',
#     dpi=300, bbox_inches="tight")
# plt.close()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # """
# # Calculate the weighted mean (again) to calculate the residuals to make a residual plot
# # """
# # wmean_num = np.sum(df['delta_14C_new']/df['delta_14C_err_new']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
# # wmean_dem = np.sum(1/df['delta_14C_err_new']**2)
# # df['wmean'] = wmean_num / wmean_dem
# # """
# # Calculate residual
# # """
# # df['residual'] = ( df['delta_14C_new'] - df['wmean'] ) / df['delta_14C_err_new']
# #
# # df.to_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output\subset_for_plotting.xlsx")
#
#
#
#
#
#
#
# #
# #
# #
# #
# #
# #
# #
# # """
# # Now I'll make the figures
# # Now we have FM, Detla 14C ready to go
# # """
# #
# # df = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output\subset_for_plotting.xlsx")
# #
# # """
# # Calculate the weighted mean (again) to calculate the residuals to make a residual plot
# # """
# # wmean_num = np.sum(df['delta_14C_new']/df['delta_14C_err_new']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
# # wmean_dem = np.sum(1/df['delta_14C_err_new']**2)
# # df['wmean'] = wmean_num / wmean_dem
# # """
# # Calculate residual
# # """
# # df['residual'] = ( df['delta_14C_new'] - df['wmean'] ) / df['delta_14C_err_new']
# #
# #
# #
# # # # I only want to have a look at the secondary standards with R number we care about, from this sheet.
# # df2 = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_2_2025_output\seconds.xlsx", comment='#')
# # df2 = df2.sort_values(by='Expected FM')
# # rs = pd.unique(df2['R_number'])
# # plt.close()
# # for i in range(0, len(rs)):
# #     subset1 = df.loc[df['Job::R'] == rs[i]]
# #     plt.scatter(subset1['TP'], subset1['residual'])
# #     plt.show()
# #
#
#
#
#
#
#
#
#
