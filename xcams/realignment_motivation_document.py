# August 21 2025

import pandas as pd
import matplotlib.pyplot as plt

# two excel sheets derived by KS for initial draft of motivation document
df = pd.read_excel(r"I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Preparation\oxalic chi2 red records_1.xlsx", sheet_name="4python")
df2 = pd.read_excel(r"I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Preparation\historic oxalic I.xlsx", sheet_name='oxalic')

# Create figure and axis
fig, ax = plt.subplots()

# Plot line
ax.scatter(df['TW'], df['Chi2_calibration'], marker="o")

# Add horizontal line at y=5
ax.axhline(y=2, color="r", linestyle="-", label="Acceptable Chi2 Value", alpha=0.2)
ax.axvline(x=3546, color="b", linestyle="--", label="Failed Measurement", alpha=0.2)
# Labels and title
ax.set_xlabel("TW (measurement number)")
ax.set_ylabel("Calibration Chi2")
ax.set_title("")

# Show legend
ax.legend()

# Show plot
plt.savefig(r"I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Preparation\chi2_oxalics_python", dpi=300, bbox_inches="tight")
plt.close()


# Make figure wider, 10 inches wide x 6 inches tall
fig, (ax1, ax2) = plt.subplots(2, 1)

df2 = df2.loc[df2['TW'] >= 3500]
df2 = df2.dropna(subset='TW')
# Top plot
ax1.scatter(df2['TP'], df2['Ratio to standard'], marker="o", alpha=0.4)
ax1.set_ylabel("Ratio to Standard")
ax1.axvline(x=89585, color="b", linestyle="--", label="Failed Measurement", alpha=0.2)
ax1.set_xlim(87000, 91000)

# Bottom plot
ax2.scatter(df2['TP'], df2['F_corrected_normed'], marker="o", alpha=0.4)
ax2.set_xlabel("TP Number")
ax2.set_ylabel("Fraction Modern")
ax2.legend()
ax2.axvline(x=89585, color="b", linestyle="--", label="Failed Measurement", alpha=0.2)
ax2.set_xlim(87000, 91000)
plt.savefig(r"I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Preparation\RTS_FM_oxalics_python", dpi=300, bbox_inches="tight")
plt.close()





# Create figure and axis
fig, ax = plt.subplots()
df2 = pd.read_excel(r"I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Preparation\historic oxalic I.xlsx", sheet_name='oxalic')

###########

# Make sure the data is sorted if order matters
df2 = df2.sort_values("TW")

# Compute rolling standard deviation with window=3
rolling_std = df2['C12C13 ratio'].rolling(window=50).std()

# Primary axis (left)
fig, ax = plt.subplots()

ax.scatter(df2['TW'], df2['C12C13 ratio'], marker="o", alpha=0.4, label="C12/C13")
ax.axvline(x=3546, color="b", linestyle="--", label="Failed Measurement", alpha=0.1)
ax.set_xlabel("TW Number")
ax.set_ylabel("C13/C12")
ax.set_xlim(2750, 3600)

# Secondary axis (right)
ax2 = ax.twinx()
ax2.plot(df2['TW'], rolling_std, color="red", label="Rolling Std (window=50)", alpha=0.3)

ax2.set_ylabel("Rolling Std Dev")

# Handle legends from both axes
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, loc="upper right")

plt.tight_layout()

# Show legend
ax.legend()
# Show plot
plt.savefig(r"I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Preparation\1312_oxalics_python", dpi=300, bbox_inches="tight")
plt.close()


"""
Analysis of 13/12 decreasing over time and relationship to cathode current
We will analyze 3532, 3546, 3537, 3571)
"""

import pandas as pd
import matplotlib.pyplot as plt
from cmcrameri import cm

# read file
df = pd.read_excel(r"I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Preparation\old_data_analysis_CBL.xlsx")

# calculate ratio
df['_1213'] = df['12Ccurr'].astype(float) / df['13Ccurr'].astype(float)

# save updated dataframe
df.to_excel(r"I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Preparation\test.xlsx")

airposition=[0,5,10,15,20,25,35]
normalposition = [0,7,14,21,35]

# grab wheels
# TODO test if oxalic positions are actually correct...
tw3517 = df.loc[(df['TW'] == 'TW3517')& (df['position'].isin(normalposition))] # good wheel
tw3518 = df.loc[(df['TW'] == 'TW3518')& (df['position'].isin(normalposition))]  # good wheel
tw3532 = df.loc[(df['TW'] == 'TW3532')& (df['position'].isin([0,5,20,30]))]  # bad wheel
tw3537 = df.loc[(df['TW'] == 'TW3537') & (df['position'].isin(airposition))]# bad wheel, extractor
tw3546 = df.loc[(df['TW'] == 'TW3546') & (df['position'].isin(airposition))] # Jocelyn's failed wheel
tw3571 = df.loc[(df['TW'] == 'TW3571')& (df['position'].isin(normalposition))]  # bad wheel
tw3000 = df.loc[(df['TW'] == 'TW3000')& (df['position'].isin([0,4,8,12,16,20]))]  # old wheel to have a look
tw3258 = df.loc[(df['TW'] == 'TW3258')& (df['position'].isin(normalposition))]  # old wheel to have a look

# plot
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(10, 12))
axes = axes.flatten()  # flatten to 1D list

axes[0].scatter(tw3517['12CLEcurr'], tw3517['_1213'], marker="o", label='TW3517 (good)')
axes[1].scatter(tw3518['12CLEcurr'], tw3518['_1213'], marker="o", label='TW3518 (good)')
axes[2].scatter(tw3532['12CLEcurr'], tw3532['_1213'], marker="o", label='TW3532 (bad)')
axes[3].scatter(tw3537['12CLEcurr'], tw3537['_1213'], marker="o", label='TW3537 (extractor problem)')
axes[4].scatter(tw3546['12CLEcurr'], tw3546['_1213'], marker="o", label='TW3546 (failed)')
axes[5].scatter(tw3571['12CLEcurr'], tw3571['_1213'], marker="o", label='TW3571 (bad)')
axes[6].scatter(tw3000['12CLEcurr'], tw3000['_1213'], marker="o", label='TW3000 (old to have a look)')
axes[7].scatter(tw3258['12CLEcurr'], tw3258['_1213'], marker="o", label='TW3258 (old to have a look)')

# add labels + legends to each subplot
for ax in axes:
    ax.set_xlabel("LE C12- Current")
    ax.set_ylabel("C12/C13 Current")
    ax.set_ylim(88, 92)  # fix y-axis scale for all plots
    ax.set_xlim(0, 120)  # fix y-axis scale for all plots
    ax.legend()


plt.tight_layout()
plt.show()
# save FIRST, then show
plt.savefig(r"I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Preparation\1312analysis.png",
            dpi=300, bbox_inches="tight")

plt.close()













