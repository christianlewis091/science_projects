import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Below is the data for wheels 3504, 3509, 3514, 3524, and 3532 (hence file name 1-5)
# This is read in seperately because Hayden originally plotted RCM 2-4 seperately from RCM5
# This means in previous code he grabbed 3509, 3514, and 3524 (RCM2,3,and4). 
# RCM5 is the only wheel where we have distinct comparison between slushes and TEC

"""
MAKE A PLOT OF THE GRAPHITE YIELD
"""

# df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\RCM1-5_graphite_yields.xlsx").dropna(subset='TP')
# df = df.loc[(df["TW"] == 3509) |(df["TW"] == 3514) |(df["TW"] == 3524)] # Legacy from RCM10 report. We want RCM2-4. 
# df = df.loc[(df["Job::Graphite Line"] == "RCM10")]

# df5 = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\RCM5_yields.xlsx")
# df5 = df5.loc[(df5["Graphite::Graphite Line"] == 10)]
# print(df5)

# df5_tec = df5.loc[df5["Graphite::Freezing By"] == 'TEC']
# df5_slush = df5.loc[df5["Graphite::Freezing By"] == 'Slushie']

# plt.axhline(y=100, color='black', alpha=0.25)
# plt.scatter(df['wtgraph'], df["Graphite::Graphite_Yield"]*100, label='TEC', alpha=0.7, s=45, color='0.2', edgecolor='white', linewidth=0.5)
# plt.scatter(df5_slush['wtgraph'], df5_slush["Graphite::Graphite_Yield"]*100, alpha=.8, color='#0072B2', marker='D', label=r'N$_{2(l)}$ slush', edgecolor='white',linewidth=0.5)
# plt.scatter(df5_tec['wtgraph'], df5_tec["Graphite::Graphite_Yield"]*100, alpha=0.7, s=45, color='0.2', edgecolor='white', linewidth=0.5) # ALSO TEC BUT NOT ADDING LABEL BECAUSE IT WOULD APPEAR TWICE
# plt.xlabel('Graphite mass (mg)')
# plt.ylabel('Graphite Yield (%)')
# plt.legend()

# plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_8_V6_output\GraphiteYield.png", dpi=300, bbox_inches="tight")
# plt.close()

"""
PLOT THE DATA! Just copying Hayden's code...see Wed 27/05/2026 email
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import chisquare

# trying to understand this naming convention...
# RCM3_4_data = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\RCM2-4.xlsx", sheet_name="RCM3 and 4").dropna(subset='TP')
# a = np.unique(RCM3_4)
# RCM2_4_data = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\RCM1-5_graphite_yields.xlsx").dropna(subset='TP')
# b = np/unique
# print(f'First dataset has TWs {a}, second has {b}, so we dont need the first sheet.')

# rewriting:

"""
below commented out so I can just make plot for table below
"""

# df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\RCM1-5_graphite_yields.xlsx").dropna(subset='TP')
# df = df.loc[df["Job::Graphite Line"] == "RCM10"]
# kap = df.loc[df['Samples::Sample ID'] == 'Kapuni CO2']
# kau = df.loc[df['Samples::Sample ID'] == 'Kauri 0157 - Wk17031']
# c1 = df.loc[df['Samples::Sample ID'] == 'IAEA-C1']


# fig, ax = plt.subplots(1, 3, figsize=(12, 6))

# main_color = '#333333'      # charcoal
# line_color = '0.7'          # light grey

# # -------------------
# # Kapuni
# # -------------------
# ax[0].errorbar(
#     kap["wtgraph"],
#     kap["Ratio to standard"],
#     yerr=kap["Ratio to standard error"],
#     fmt='o',
#     linestyle='',
#     color=main_color,
#     markersize=6,
#     markeredgecolor='white',
#     markeredgewidth=0.5,
#     capsize=2,
#     alpha=0.8
# )

# ax[0].axvline(0.2, color=line_color, ls='--', lw=1)
# ax[0].axhline(0.0013, color=line_color, ls='-', lw=1)
# ax[0].set_title('Kapuni')
# ax[0].set_xlabel('Mass (mg)')
# ax[0].set_ylabel('Ratio to Standard')
# ax[0].set_yscale('log')

# # -------------------
# # Kauri
# # -------------------
# ax[1].errorbar(
#     kau["wtgraph"],
#     kau["Ratio to standard"],
#     yerr=kau["Ratio to standard error"],
#     fmt='o',
#     linestyle='',
#     color=main_color,
#     markersize=6,
#     markeredgecolor='white',
#     markeredgewidth=0.5,
#     capsize=2,
#     alpha=0.8
# )

# ax[1].axvline(0.2, color=line_color, ls='--', lw=1)
# ax[1].axhline(0.0026, color=line_color, ls='-', lw=1)
# ax[1].set_title('Kauri')
# ax[1].set_xlabel('Mass (mg)')


# # -------------------
# # C1
# # -------------------
# ax[2].errorbar(
#     c1["wtgraph"],
#     c1["Ratio to standard"],
#     yerr=c1["Ratio to standard error"],
#     fmt='o',
#     linestyle='',
#     color=main_color,
#     markersize=6,
#     markeredgecolor='white',
#     markeredgewidth=0.5,
#     capsize=2,
#     alpha=0.8
# )

# ax[2].axvline(0.2, color=line_color, ls='--', lw=1)
# ax[2].axhline(0.0022, color=line_color, ls='-', lw=1)
# ax[2].set_title('C1')
# ax[2].set_xlabel('Mass (mg)')


# # Consistent styling
# for a in ax:
#     a.tick_params(direction='in')
#     a.grid(False)

# plt.tight_layout()

# plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_8_V6_output\result.png", dpi=300, bbox_inches="tight")

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(1, 3, marker='o')
plt.ylim(0, 1.3)
plt.xlim(0, 1.3)
plt.axvline(x=0.1, color='black',linestyle='-')
plt.axvline(x=0.2, color='black',linestyle='-')
plt.axvline(x=0.4, color='black',linestyle='-')
plt.axvline(x=0.8, color='black',linestyle='-')
ax.set_yticks([])  # Remove y-axis ticks
plt.xlabel('Graphite mass (mg)')
plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_8_V6_output\blankfortable.png", dpi=300, bbox_inches="tight")
