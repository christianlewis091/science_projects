import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandas import read_excel

"""
FIRI PLOT
"""

# df = pd.read_excel(f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/Final_results.xlsx')
#
# d = df.loc[df['Job::R']=='24889/4']
# e = df.loc[df['Job::R']=='24889/5']
# ij = df.loc[df['Job::R']=='24889/9']
# l = df.loc[df['Job::R']=='26281/1']
#
#
# fig = plt.figure(figsize=(7.75, 5.5))
#
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

def weighted_mean(rts_corrected, rts_corrected_error):
    wmean_num = np.sum(rts_corrected/rts_corrected_error**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
    wmean_dem = np.sum(1/rts_corrected_error**2)
    wmean = wmean_num / wmean_dem
    return wmean

def residual(rts_corrected, wm, rts_corrected_error):
    residual = (rts_corrected - wm) / rts_corrected_error
    return residual

# get finished data from preivous sheets, residual already calculated
df = pd.read_excel(f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/Final_results.xlsx')
bhdamb_after = df.loc[(df['Job::R'] =='40430/1') & (df['preptype'] == 'FLASK')].copy()
bhdspike_after = df.loc[(df['Job::R'] =='40430/2') & (df['preptype'] == 'FLASK')].copy()

df = read_excel('C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/data_checks_along_the_way/ox_prep_labels_added.xlsx') # grab data after prep type was addded in previuos sheet
bhdamb_b4 = df.loc[(df['Job::R'] =='40430/1') & (df['preptype'] != 'FLASK')].copy()
bhdspike_b4 = df.loc[(df['Job::R'] =='40430/2') & (df['preptype'] != 'FLASK')].copy()

bhdamb_b4['wm'] = weighted_mean(bhdamb_b4['RTS_corrected'], bhdamb_b4['RTS_corrected_error'])
bhdspike_b4['wm'] = weighted_mean(bhdspike_b4['RTS_corrected'], bhdspike_b4['RTS_corrected_error'])

bhdamb_b4['residual'] = residual(bhdamb_b4['RTS_corrected'], bhdamb_b4['wm'], bhdamb_b4['RTS_corrected_error'])
bhdspike_b4['residual'] = residual(bhdspike_b4['RTS_corrected'], bhdspike_b4['wm'], bhdspike_b4['RTS_corrected_error'])


# Create figure and 2 vertical subplots
fig, axes = plt.subplots(
    nrows=2,
    ncols=1,
    figsize=(7.75, 5.5),   # width, height in inches
    sharex=True)       # share x-axis if appropriate)

# Unpack axes for clarity
ax1, ax2 = axes

# --- Top subplot ---
ax1.plot([], [])  # replace with your data
ax1.set_ylabel("Blank Corrected FM")
ax1.errorbar(bhdamb_b4['TP'],bhdamb_b4['F_corrected_normed'], yerr=bhdamb_b4['F_corrected_normed_error'], color='gray', marker='D', label='BHDamb2013')
ax1.errorbar(bhdamb_after['TP'],bhdamb_after['F_corrected_normed'], yerr=bhdamb_after['F_corrected_normed_error'], color='black', marker='o',  label='BHDamb2013 Flask OX')

# --second--
ax2.plot([], [])  # replace with your data
ax2.set_ylabel("Blank Corrected FM")
ax2.errorbar(bhdspike_b4['TP'],bhdspike_b4['F_corrected_normed'], yerr=bhdspike_b4['F_corrected_normed_error'], color='gray', marker='D', label='BHDspike2013')
ax2.errorbar(bhdspike_after['TP'],bhdspike_after['F_corrected_normed'], yerr=bhdspike_after['F_corrected_normed_error'], color='black', marker='o',  label='BHDspike2013 Flask OX')
# Adjust layout to prevent overlap
plt.tight_layout()

plt.savefig(f"I:\C14Data\Data Quality Paper\CBL_V5\FIGURES/OX_fig.png",
            dpi=300, bbox_inches="tight")
plt.close()

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
