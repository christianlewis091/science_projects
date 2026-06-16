import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import read_excel

"""
FIRI PLOT
"""

df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/Final_results_V6_edit2.xlsx")

d = df.loc[(df['Job::R']=='24889/4')] # all FIRI-F's were already set to /4 so no need to re-index them! 
e = df.loc[df['Job::R']=='24889/5']
ij = df.loc[df['Job::R']=='24889/9']
l = df.loc[df['Job::R']=='26281/1']
#
"""
Plot FIRI-D and others; FIRI-D will remain IN the paper, the rest will go to Supp Info
"""
# df inidicates which FIRI we're plotting
# WM is the weighted mean, from the results tables
# cv is concensus value also from the results tables 
def firi_plot(df, wm, cv, title, savetitle):
    fig, axs = plt.subplots(2, 1, figsize=(5.5, 7), sharex=True, gridspec_kw={'hspace': 0.075}
    )
    axs[0].errorbar(df['TP'], df['F_corrected_normed'], yerr=df['F_corrected_normed_error'], color='black', linestyle='', marker='o')

    axs[0].axhline(y=cv, linestyle='--', linewidth=1, color="#2c38a0", label='Concensus') # copied from the Tables.xlsx
    axs[0].axhline(y=wm, linestyle='-', linewidth=1, color="black", label='Weighted Mean FM')

    # bottom is the residual
    axs[1].scatter(df['TP'], df['residual'], color='black', linestyle='')
    axs[1].axhline(y=0, color='#333333')

    axs[0].set_title(f"{title}")
    axs[0].set_ylabel('F14C')
    axs[1].set_xlabel('TP (sample ID)')
    axs[1].set_ylabel('Residual')
    axs[0].legend()

    plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_3_V6_figures_output/{savetitle}.png", dpi=300, bbox_inches="tight")

# firi_plot(d, 0.568924504820682, 0.568830496, 'FIRI-D', 'firi_d')
# firi_plot(e, 0.229893607055364, 0.22953969, 'FIRI-E', 'firi_e')
# firi_plot(ij, 0.571817339656415, 0.572168402, 'FIRI-I', 'firi_i')
# firi_plot(l, 0.203183828615025, 0.203531748, 'TIRI-L', 'tiri_l')

"""
Air Materials Plot

If we want to compare Air Materials before and after using normalization to flask oxalics, we need to compare residuals that are NOT corrected by wtw error. 
Because of course the idea of the wtw error is to correct for the difference. 
"""

# Go back to the data that has the pretreatments added and labels added, but before it was indexed to only include flasks
df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/for_air_plot.xlsx")
air_r = ['40430/1','40430/2','40430/5']

bhdamb_b4  = df.loc[(df['Job::R'] == '40430/1') & (df['AMS Timetable From Results::Standard Prep Type'] != 'FLASK')].copy()
bhdamb_aft = df.loc[(df['Job::R'] == '40430/1') & (df['AMS Timetable From Results::Standard Prep Type'] == 'FLASK')].copy()

# here is the original way we calculate FM error (commented out)
# df['FM_err_new_sigbw'] = (np.sqrt(df['RTS_corrected_error']**2 + (df['sigmabw_rts_percent']*.01*df['RTS_corrected'])**2)/0.95)*0.98780499

# If the sigmabw_rts_percent is set to zero, that whole term drops out and we're left with this. 
bhdamb_b4['FM_err_new_sigbw'] = (np.sqrt(bhdamb_b4['RTS_corrected_error']**2)/0.95)*0.98780499
bhdamb_aft['FM_err_new_sigbw'] = (np.sqrt(bhdamb_aft['RTS_corrected_error']**2)/0.95)*0.98780499

plt.errorbar(bhdamb_b4['TP'],bhdamb_b4['F_corrected_normed'], yerr=bhdamb_b4['F_corrected_normed_error'], color='gray', marker='D', label='BHDamb2013', linestyle='')
plt.errorbar(bhdamb_aft['TP'],bhdamb_aft['F_corrected_normed'], yerr=bhdamb_aft['F_corrected_normed_error'], color='black', marker='o',  label='BHDamb2013 Flask OX', linestyle='')

plt.title('BHDamb before and after flask oxalic normalization')
plt.ylabel('F14C, without CV (or SigBW), added!')
plt.legend()
plt.xlabel('TP')

plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_3_V6_figures_output/AirFig.png", dpi=300, bbox_inches="tight")

# """
# We want an RCM10 Figure. We'll have to kind of build it from scratch...
# """


# # here's the big file from 0.py. Why not use a clearer one? We want to filter on oxalics that were run on RCM too, whihc 
# # won't appear if we use that filtered already by "secondaries"
# # df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\new_full_export_may25_2026.xlsx")
# # rcm10 = df.loc[df['Graphite Completed::Graphite Line'] == 10]
# # print(len(rcm10))
# rcm10 = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_3_V6_figures_output/rcm10file.xlsx")
# print(f'How many samples are in RCM10 TOTAL from main export? {len(rcm10)}')

# # print(np.unique(rcm10['Quality Flag']))
# # ['...' '.S.' '.T.' 'A..' 'M..' 'XT.']
# okflags = ['...', '.S.', '.T.']
# rcm10 = rcm10.loc[rcm10['Quality Flag'].isin(okflags)]
# print(f'After removing first column flags, how many are in RCM10 dataset? {len(rcm10)}')

# """
# Below is the list we've been indexing on for this work, but I"m going to add oxalics in this case. 
# """
# # seconds = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\seconds_April3_2026.xlsx", sheet_name='new', comment='#')
# # rs_of_secondaries_and_blanks = np.unique(seconds['Job::R'])
# # print(rs_of_secondaries_and_blanks)
# rs_of_interset = ['14047/1', '14047/11', '14047/12', '14047/2', '24889/14', '24889/4', '24889/5',
#  '24889/6', '24889/7', '24889/9', '26281/1', '40142/1', '40142/2', '40430/1',
#  '40430/2', '40430/3', '40430/5' ,'40430/6', '40699/1' ,'41347/12', '41347/13',
#  '41347/2' '41347/3','26294/1',
#  '40696/1',
#   '40696/2',
#    '40696/3',
#     '40696/4',
#      '40696/5',
#       '40696/6',
# ]
# rcm10 = rcm10.loc[rcm10['Job::R'].isin(rs_of_interset)]
# print(f'After selecting our Rs of interest? {len(rcm10)}')

# rcm10ox = rcm10 = rcm10.loc[rcm10['Job::R'] == '26294/1']
# print(f'How many oxalics? {len(rcm10ox)}')


























"""
OLD JUNK
"""





# # ax3_bot.set_ylabel('Residual')
# # ax1_bot.set_ylabel('Residual')
# # ax3_bot.set_xlabel('TP (sample ID)')

# # Outer 2x2 grid (4 panels)
# outer = fig.add_gridspec(2, 2, wspace=0.15, hspace=0.2)
#
# # ---- Panel 1 (top-left) ----
# gs00 = outer[0, 0].subgridspec(2, 1, height_ratios=[2, 1], hspace=0.125)
# ax1_top = fig.add_subplot(gs00[0])
# ax1_top.errorbar(d['TP'], d['F_corrected_normed'], yerr=d['F_corrected_normed_error'], color='black', linestyle='', marker='o')
#
# ax1_bot = fig.add_subplot(gs00[1], sharex=ax1_top)
# ax1_bot.scatter(d['TP'], d['residual'], color='black', linestyle='')
#
# # ---- Panel 2 (top-right) ----
# gs01 = outer[0, 1].subgridspec(2, 1, height_ratios=[2, 1], hspace=0.125)
# ax2_top = fig.add_subplot(gs01[0])
# ax2_top.errorbar(e['TP'], e['F_corrected_normed'], yerr=e['F_corrected_normed_error'], color='black', linestyle='', marker='o')
#
# ax2_bot = fig.add_subplot(gs01[1], sharex=ax2_top)
# ax2_bot.scatter(e['TP'], e['residual'], color='black', linestyle='')
#
# # ---- Panel 3 (bottom-left) ----
# gs10 = outer[1, 0].subgridspec(2, 1, height_ratios=[2, 1], hspace=0.125)
# ax3_top = fig.add_subplot(gs10[0])
# ax3_top.errorbar(ij['TP'],ij['F_corrected_normed'], yerr=ij['F_corrected_normed_error'], color='black', linestyle='', marker='o')
#
# ax3_bot = fig.add_subplot(gs10[1], sharex=ax3_top)
# ax3_bot.scatter(ij['TP'], ij['residual'], color='black', linestyle='')
#
# # ---- Panel 4 (bottom-right) ----
# gs11 = outer[1, 1].subgridspec(2, 1, height_ratios=[2, 1], hspace=0.125)
# ax4_top = fig.add_subplot(gs11[0])
# ax4_top.errorbar(l['TP'],l['F_corrected_normed'], yerr=l['F_corrected_normed_error'], color='black', linestyle='', marker='o')
#
# ax4_bot = fig.add_subplot(gs11[1], sharex=ax4_top)
# ax4_bot.scatter(l['TP'], l['residual'], color='black', linestyle='')
# # Optional: clean up top x-axis labels
# for ax in [ax1_top, ax2_top, ax3_top, ax4_top]:
#     ax.tick_params(labelbottom=False)
#
# # Example placeholders (replace with your data)
# ax1_top.set_title("FIRI-D")
# ax2_top.set_title("FIRI-E")
# ax3_top.set_title("FIRI-I")
# ax4_top.set_title("TIRI-L")
#
# ax1_top.axhline(y=0.56883, linestyle='--', linewidth=1, color='red', label='Concensus') #color='#7f7f7f'
# ax1_top.axhline(y=0.570532, linestyle=':', linewidth=1, color='#9467bd', label='AMS Concensus')
# ax1_top.axhline(y=0.5688979440688, linestyle='-', linewidth=1, color='#2ca02c', label='Weighted Mean FM')
# ax1_bot.axhline(y=0, color='#333333')
#
# ax2_top.axhline(y=0.23074296581363, linestyle='--', linewidth=1, color='red', label='Concensus') # copied from the Tables.xlsx
# ax2_top.axhline(y=0.229893607055364, linestyle='-', linewidth=1, color='#2ca02c', label='Weighted Mean FM')
# ax2_bot.axhline(y=0, color='#333333')
#
# ax3_top.axhline(y=0.57216840186830, linestyle='--', linewidth=1, color='red', label='Concensus') # copied from the Tables.xlsx
# ax3_top.axhline(y=0.571817339656415, linestyle='-', linewidth=1, color='#2ca02c', label='Weighted Mean FM')
# ax3_bot.axhline(y=0, color='#333333')
#
# ax4_top.axhline(y=0.20353174824426, linestyle='--', linewidth=1, color='red', label='Concensus') # copied from the Tables.xlsx
# ax4_top.axhline(y=0.203183828615025, linestyle='-', linewidth=1, color='#2ca02c', label='Weighted Mean FM')
# ax4_bot.axhline(y=0, color='#333333')
#
# # ax1_top.set_ylabel('Fraction modern')
# # ax3_top.set_ylabel('Fraction modern')
# # ax3_bot.set_ylabel('Residual')
# # ax1_bot.set_ylabel('Residual')
# # ax3_bot.set_xlabel('TP (sample ID)')
# # ax4_bot.set_xlabel('TP (sample ID)')
#
# plt.savefig(f"I:\C14Data\Data Quality Paper\CBL_V5\FIGURES/firi_fig.png",
#             dpi=300, bbox_inches="tight")

"""
Air mateirals plot 1 residuals: showcase before and after flasks oxalics 
"""

# def weighted_mean(rts_corrected, rts_corrected_error):
#     wmean_num = np.sum(rts_corrected/rts_corrected_error**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
#     wmean_dem = np.sum(1/rts_corrected_error**2)
#     wmean = wmean_num / wmean_dem
#     return wmean

# def residual(rts_corrected, wm, rts_corrected_error):
#     residual = (rts_corrected - wm) / rts_corrected_error
#     return residual

# # get finished data from preivous sheets, residual already calculated
# df = pd.read_excel(f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/Final_results.xlsx')
# bhdamb_after = df.loc[(df['Job::R'] =='40430/1') & (df['preptype'] == 'FLASK')].copy()
# bhdspike_after = df.loc[(df['Job::R'] =='40430/2') & (df['preptype'] == 'FLASK')].copy()

# df = read_excel('C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/data_checks_along_the_way/ox_prep_labels_added.xlsx') # grab data after prep type was addded in previuos sheet
# bhdamb_b4 = df.loc[(df['Job::R'] =='40430/1') & (df['preptype'] != 'FLASK')].copy()
# bhdspike_b4 = df.loc[(df['Job::R'] =='40430/2') & (df['preptype'] != 'FLASK')].copy()

# bhdamb_b4['wm'] = weighted_mean(bhdamb_b4['RTS_corrected'], bhdamb_b4['RTS_corrected_error'])
# bhdspike_b4['wm'] = weighted_mean(bhdspike_b4['RTS_corrected'], bhdspike_b4['RTS_corrected_error'])

# bhdamb_b4['residual'] = residual(bhdamb_b4['RTS_corrected'], bhdamb_b4['wm'], bhdamb_b4['RTS_corrected_error'])
# bhdspike_b4['residual'] = residual(bhdspike_b4['RTS_corrected'], bhdspike_b4['wm'], bhdspike_b4['RTS_corrected_error'])


# # Create figure and 2 vertical subplots
# fig, axes = plt.subplots(
#     nrows=2,
#     ncols=1,
#     figsize=(7.75, 5.5),   # width, height in inches
#     sharex=True)       # share x-axis if appropriate)

# # Unpack axes for clarity
# ax1, ax2 = axes

# # --- Top subplot ---
# ax1.plot([], [])  # replace with your data
# ax1.set_ylabel("Blank Corrected FM")
# ax1.errorbar(bhdamb_b4['TP'],bhdamb_b4['F_corrected_normed'], yerr=bhdamb_b4['F_corrected_normed_error'], color='gray', marker='D', label='BHDamb2013')
# ax1.errorbar(bhdamb_after['TP'],bhdamb_after['F_corrected_normed'], yerr=bhdamb_after['F_corrected_normed_error'], color='black', marker='o',  label='BHDamb2013 Flask OX')

# # --second--
# ax2.plot([], [])  # replace with your data
# ax2.set_ylabel("Blank Corrected FM")
# ax2.errorbar(bhdspike_b4['TP'],bhdspike_b4['F_corrected_normed'], yerr=bhdspike_b4['F_corrected_normed_error'], color='gray', marker='D', label='BHDspike2013')
# ax2.errorbar(bhdspike_after['TP'],bhdspike_after['F_corrected_normed'], yerr=bhdspike_after['F_corrected_normed_error'], color='black', marker='o',  label='BHDspike2013 Flask OX')
# # Adjust layout to prevent overlap
# plt.tight_layout()

# plt.savefig(f"I:\C14Data\Data Quality Paper\CBL_V5\FIGURES/OX_fig.png",
#             dpi=300, bbox_inches="tight")
# plt.close()

"""
FIGURE BELOW MAKES RESIDUAL PLOT
"""

# fig = plt.figure(figsize=(7.75, 5.5))
#
# plt.scatter(bhdamb_after['TP'], bhdamb_after['residual'], color='black', linestyle='', label='Normalized to flask-OX')
# plt.scatter(bhdamb_b4['TP'], bhdamb_b4['residual'], marker='D', facecolors='none', edgecolors='black', label='Normalized to sealed tube OX')
# plt.scatter(bhdspike_b4['TP'], bhdspike_b4['residual'], marker='D', facecolors='none', edgecolors='black')
# plt.axhline(y=0, color='#333333')
# plt.legend()
# plt.ylabel('Residual: (x$_i$ - mean) / \u03C3')
# plt.xlabel('TP (sample ID)')
# plt.savefig(f"I:\C14Data\Data Quality Paper\CBL_V5\FIGURES/OX_fig.png",
#             dpi=300, bbox_inches="tight")
# plt.close()
#
